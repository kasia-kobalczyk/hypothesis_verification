"""Build the length-controlled v2 pair slice.

    python scripts/build_v2_slice.py --dry-run     # free: length statistics only
    python scripts/build_v2_slice.py               # full build (model calls)

Rules, in the order they are applied (cheapest gate first — the gates are
conjunctive, so the order does not change which pairs survive):

  1. LENGTH (free, deterministic)  0.75 <= tokens(negative)/tokens(gold) <= 1.33
  2. R1/R3/R5/R6 row screen        prompt `row_screen_v1`, one call per row
  3. R4 temporal cutoff            Crossref must yield a cutoff date
  4. R2 semantic comparability     prompt `pair_comparability_v1` (frozen in v1)

Rows with no length-passing negative are skipped before any model call: they
cannot contribute a pair whatever the other gates say.

Nothing is rewritten to fit a threshold, no negative is preferred over another,
and no literature retrieval or verifier output is consulted. Resumable: every
decision is appended to a progress file and reused on a re-run.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.temporal import resolve_source_dates  # noqa: E402
from src.benchmark.v2_slice import (  # noqa: E402
    LENGTH_RATIO_MAX,
    LENGTH_RATIO_MIN,
    TOKENIZER_NAME,
    TOKENIZER_PATTERN,
    RowOutcome,
    V2Pair,
    build_pair,
    count_tokens,
    length_candidates,
    length_ratio,
    screening_order,
)
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import (  # noqa: E402
    append_jsonl,
    ensure_dir,
    read_jsonl,
    resolve_path,
    utc_now_iso,
    write_json,
    write_jsonl,
)
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.literature.crossref import CrossrefClient  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.build_v2_slice")

OUT_DIR = "benchmark/v2"
ROW_PROMPT = "row_screen_v1"
PAIR_PROMPT = "pair_comparability_v1"
TARGET_PAIRS = 100


def json_validator(keys):
    def validate(parsed: Dict[str, Any]) -> None:
        for key in keys:
            if not isinstance(parsed.get(key), bool):
                raise ValueError("{!r} must be a boolean".format(key))
    return validate


def screen_row(row, prompts, llm) -> Dict[str, Any]:
    """R1/R3/R5/R6. The verdict is derived from the criteria, not from the model's
    own summary field, so it cannot contradict its own answers."""
    template = prompts.get(ROW_PROMPT)
    messages = [{"role": "user", "content": template.render(
        question=row.get("research_question") or "", gold=row.get("gold_hypothesis") or "")}]
    keys = ("R1_empirical_or_mechanistic_proposition", "R3_presented_as_supported",
            "R5_no_row_level_artifact", "R6_empirical_science_scope")
    try:
        response = llm.complete_json(messages, purpose="v2.row_screen",
                                     prompt_version=ROW_PROMPT, validator=json_validator(keys))
    except (LLMParseError, LLMError) as exc:
        return {"decision": "ERROR", "error": "{}: {}".format(type(exc).__name__, exc)}
    parsed = response.parsed or {}
    out = {key: bool(parsed.get(key)) for key in keys}
    out["decision"] = "PASS" if all(out.values()) else "FAIL"
    out["rationale"] = parsed.get("rationale")
    return out


def screen_pair(row, negative, prompts, llm) -> Dict[str, Any]:
    """R2, using the prompt frozen during the v1 pair audit."""
    template = prompts.get(PAIR_PROMPT)
    messages = [{"role": "user", "content": template.render(
        question=row.get("research_question") or "",
        gold=row.get("gold_hypothesis") or "",
        alternative=negative)}]
    keys = ("same_target", "disagrees_substantively")
    try:
        response = llm.complete_json(messages, purpose="v2.pair_comparability",
                                     prompt_version=PAIR_PROMPT, validator=json_validator(keys))
    except (LLMParseError, LLMError) as exc:
        return {"decision": "ERROR", "error": "{}: {}".format(type(exc).__name__, exc)}
    parsed = response.parsed or {}
    out = {key: bool(parsed.get(key)) for key in keys}
    out["decision"] = "PASS" if all(out.values()) else "FAIL"
    out["rationale"] = parsed.get("rationale")
    return out


def length_statistics(order) -> Dict[str, Any]:
    ratios, per_row = [], []
    for _, _, row in order:
        gold = row.get("gold_hypothesis") or ""
        passing = 0
        for negative in row.get("model_negative_hypotheses") or []:
            ratio = length_ratio(gold, negative)
            if ratio is None:
                continue
            ratios.append(ratio)
            passing += int(LENGTH_RATIO_MIN <= ratio <= LENGTH_RATIO_MAX)
        per_row.append(passing)
    return {
        "n_rows": len(order),
        "n_pairs": len(ratios),
        "ratio_median": round(statistics.median(ratios), 3) if ratios else None,
        "ratio_mean": round(statistics.mean(ratios), 3) if ratios else None,
        "share_negative_shorter": round(sum(1 for r in ratios if r < LENGTH_RATIO_MIN) / len(ratios), 4),
        "share_in_band": round(sum(1 for r in ratios if LENGTH_RATIO_MIN <= r <= LENGTH_RATIO_MAX) / len(ratios), 4),
        "share_negative_longer": round(sum(1 for r in ratios if r > LENGTH_RATIO_MAX) / len(ratios), 4),
        "n_length_passing_pairs": sum(per_row),
        "n_rows_with_length_passing_pair": sum(1 for p in per_row if p),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build the v2 length-controlled pair slice.")
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--dataset", default="benchmark/ranking.jsonl")
    parser.add_argument("--out-dir", default=OUT_DIR)
    parser.add_argument("--target", type=int, default=TARGET_PAIRS)
    parser.add_argument("--max-rows", type=int, default=None, help="stop after N screened rows")
    parser.add_argument("--ratio-min", type=float, default=None, help="override the frozen band")
    parser.add_argument("--ratio-max", type=float, default=None)
    parser.add_argument("--dry-run", action="store_true", help="length statistics only, no model calls")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    if args.ratio_min is not None or args.ratio_max is not None:
        import src.benchmark.v2_slice as v2_module
        v2_module.LENGTH_RATIO_MIN = args.ratio_min if args.ratio_min is not None else v2_module.LENGTH_RATIO_MIN
        v2_module.LENGTH_RATIO_MAX = args.ratio_max if args.ratio_max is not None else v2_module.LENGTH_RATIO_MAX
        globals()["LENGTH_RATIO_MIN"] = v2_module.LENGTH_RATIO_MIN
        globals()["LENGTH_RATIO_MAX"] = v2_module.LENGTH_RATIO_MAX
        LOGGER.warning("band overridden to [%s, %s]", v2_module.LENGTH_RATIO_MIN, v2_module.LENGTH_RATIO_MAX)

    config = load_config(args.config)
    out_dir = ensure_dir(resolve_path(args.out_dir))
    order = screening_order(resolve_path(args.dataset))
    stats = length_statistics(order)

    print("\nlength rule {} <= tokens(neg)/tokens(gold) <= {}  [tokenizer {}]".format(
        LENGTH_RATIO_MIN, LENGTH_RATIO_MAX, TOKENIZER_NAME))
    for key in ("n_rows", "n_pairs", "ratio_median", "share_in_band",
                "n_length_passing_pairs", "n_rows_with_length_passing_pair"):
        print("  {:<34} {}".format(key, stats[key]))
    if args.dry_run:
        print("\ndry run: no model calls made.\n")
        return 0

    progress_path = out_dir / "v2_progress.jsonl"
    done: Dict[int, Dict[str, Any]] = {}
    if progress_path.exists():
        for entry in read_jsonl(progress_path):
            done[int(entry["screen_rank"])] = entry
        LOGGER.info("resuming: %d row(s) already screened", len(done))

    event_log = EventLog(out_dir / "v2_build_events.jsonl")
    llm = build_llm_client(config.llm, event_log=event_log)
    prompts = PromptLibrary(config.prompts.dir)
    crossref = CrossrefClient(config.crossref, event_log=event_log)

    pairs: List[V2Pair] = []
    outcomes: List[RowOutcome] = []
    screened_rows = 0

    for screen_rank, doi, row in order:
        if len(pairs) >= args.target:
            LOGGER.info("target of %d pairs reached at screen rank %d", args.target, screen_rank)
            break
        if args.max_rows is not None and screened_rows >= args.max_rows:
            break

        outcome = RowOutcome(
            screen_rank=screen_rank, doi=doi, sample_id=row.get("sample_id") or "",
            discipline=row.get("discipline"),
            n_negatives=len(row.get("model_negative_hypotheses") or []),
        )
        candidates = length_candidates(row)
        outcome.n_length_pass = len(candidates)
        if not candidates:
            # Cannot contribute a pair whatever the other gates say: skip before
            # spending a model call.
            outcome.rejected_at = "length"
            outcomes.append(outcome)
            continue

        cached = done.get(screen_rank)
        if cached:
            entry = cached
        else:
            screened_rows += 1
            entry: Dict[str, Any] = {"screen_rank": screen_rank, "doi": doi,
                                     "n_length_pass": len(candidates)}
            entry["row_screen"] = screen_row(row, prompts, llm)
            if entry["row_screen"]["decision"] == "PASS":
                try:
                    record = resolve_source_dates(
                        doi, crossref=crossref, temporal=config.temporal,
                        crossref_config=config.crossref)
                    entry["cutoff_date"] = record.cutoff_date.isoformat() if record.cutoff_date else None
                except Exception as exc:  # a provider failure is not "no cutoff"
                    entry["cutoff_date"] = None
                    entry["cutoff_error"] = str(exc)
                if entry["cutoff_date"]:
                    entry["pairs"] = {
                        str(index): screen_pair(row, negative, prompts, llm)
                        for index, negative, _ in candidates
                    }
            append_jsonl(progress_path, entry)
            done[screen_rank] = entry

        outcome.row_screen = entry.get("row_screen")
        outcome.cutoff_date = entry.get("cutoff_date")
        if (entry.get("row_screen") or {}).get("decision") != "PASS":
            outcome.rejected_at = "row_screen"
            outcome.note = (entry.get("row_screen") or {}).get("rationale")
            outcomes.append(outcome)
            continue
        if not entry.get("cutoff_date"):
            outcome.rejected_at = "cutoff"
            outcome.note = entry.get("cutoff_error") or "no cutoff date resolvable"
            outcomes.append(outcome)
            continue

        judged = entry.get("pairs") or {}
        for index, negative, ratio in candidates:
            verdict = judged.get(str(index)) or {}
            if verdict.get("decision") != "PASS":
                continue
            outcome.n_comparable += 1
            pairs.append(build_pair(
                row=row, screen_rank=screen_rank, negative_index=index, negative=negative,
                ratio=ratio, comparable=True, rationale=verdict.get("rationale"),
                comparability_prompt_version=PAIR_PROMPT, row_screen_prompt_version=ROW_PROMPT,
                cutoff_date=entry.get("cutoff_date"),
            ))
        outcome.n_retained = outcome.n_comparable
        if outcome.n_retained == 0:
            outcome.rejected_at = "comparability"
        outcomes.append(outcome)
        LOGGER.info("rank %d (%s): %d length-pass -> %d retained  [running total %d]",
                    screen_rank, doi, len(candidates), outcome.n_retained, len(pairs))

    # ---------------- outputs ---------------- #
    write_jsonl(out_dir / "researchbench_v2_pairs.jsonl",
                [p.model_dump(mode="json") for p in pairs])

    considered = [o for o in outcomes if o.n_length_pass]
    reached = len(pairs) >= args.target
    manifest = {
        "name": "ResearchBench-derived length-controlled pair slice",
        "version": "v2",
        "status": "DEVELOPMENT / DEBUGGING SET",
        "status_note": (
            "For method development and debugging only. Aggregate accuracy on this slice "
            "must NOT be reported as evidence for the method: a question-hidden judge "
            "recovers most pair labels from the candidate texts alone. The evaluation "
            "benchmark will be built separately by symmetric candidate canonicalisation."
        ),
        "frozen_at": utc_now_iso(),
        "motivation": (
            "v1 artifact diagnostics: ranking candidates by shortest text alone scored "
            "1.000 on the frozen v1 pair subset. Across the full ranking set the median "
            "negative is 3x the gold's length. v2 controls that confound by construction."
        ),
        "source_dataset": str(resolve_path(args.dataset)),
        "screening_order": "SHA256(DOI) ascending after deterministic DOI deduplication (v1 order, reproduced: all 20 v1 screen_rank values match)",
        "inherited_from_v1": [
            "the R1-R6 scientific-validity rubric text (benchmark/dev/README-3.md)",
            "the deterministic DOI screening order",
            "verbatim hypothesis text; nothing is rewritten",
        ],
        "new_rule_in_v2": {
            "length_ratio": "tokens(negative)/tokens(gold) in [{}, {}]".format(
                LENGTH_RATIO_MIN, LENGTH_RATIO_MAX),
            "band_history": (
                "specified [0.75, 1.33]; widened to [0.67, 1.50] before screening; reverted "
                "to [0.75, 1.33] after diagnostics. Widened slice kept at "
                "benchmark/v2_widened_diagnostic/ as a characterisation artifact."
            ),
            "applied": "per gold-negative pair; all passing pairs retained",
        },
        "tokenizer": {"name": TOKENIZER_NAME, "pattern": TOKENIZER_PATTERN,
                      "note": "tiktoken is unavailable offline; this tokenizer needs no download"},
        "prompts": {
            "row_screen_R1_R3_R5_R6": prompts.get(ROW_PROMPT).record(),
            "pair_comparability_R2": prompts.get(PAIR_PROMPT).record(),
        },
        "provenance_caveat": (
            "v1's R1-R6 rubric TEXT is frozen and quoted verbatim in row_screen_v1, but v1's "
            "screening PROMPT was not preserved in this repository. R1/R3/R5/R6 are therefore "
            "re-implemented, not replayed; R2 uses the prompt frozen during the v1 pair audit."
        ),
        "not_used_in_selection": [
            "literature retrieval", "Direct-RAG output", "consequence-graph output",
            "any verifier score", "any artifact-diagnostic result",
        ],
        "llm": {"provider": config.llm.provider, "deployment": getattr(llm, "deployment", None)},
        "length_statistics_full_dataset": stats,
        "target_pairs": args.target,
        "target_reached": reached,
        "n_pairs_retained": len(pairs),
        "n_source_rows_represented": len({p.doi for p in pairs}),
        "n_rows_in_order": len(order),
        "n_rows_considered_after_length_gate": len(considered),
        "n_rows_screened_with_model": screened_rows,
        "rejected_at": dict(Counter(o.rejected_at for o in outcomes if o.rejected_at)),
        "llm_usage": dict(getattr(llm, "usage_totals", {})),
    }
    write_json(out_dir / "v2_manifest.json", manifest)
    write_jsonl(out_dir / "v2_row_outcomes.jsonl", [o.record() for o in outcomes])

    print("\nretained {} pair(s) across {} source row(s)".format(
        len(pairs), manifest["n_source_rows_represented"]))
    print("rows: {} in order, {} had a length-passing pair, {} screened with a model".format(
        len(order), len(considered), screened_rows))
    print("rejected at: {}".format(manifest["rejected_at"]))
    if not reached:
        print("\nTARGET NOT REACHED: {} of {} pairs. The threshold was NOT adjusted.".format(
            len(pairs), args.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
