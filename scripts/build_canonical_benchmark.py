"""Build the canonicalized style-controlled evaluation benchmark.

    python scripts/build_canonical_benchmark.py --target 100

Implements `docs/CANONICAL_PROTOCOL.md`, which was frozen before this ran.

Gates, in order: inherited scientific validity (reused verbatim from the v2
screening decisions) -> symmetric canonicalisation -> semantic preservation ->
pair comparability re-applied to the canonical texts. There is no length gate.

Resumable: every row's decisions are appended to a progress file and reused.
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

from src.benchmark.canonical import (  # noqa: E402
    CANONICALISE_PROMPT,
    MAX_CLAIM_WORDS,
    PAIR_PROMPT,
    PRESERVATION_PROMPT,
    CanonicalCandidate,
    build_pair,
    canonicalise_row,
)
from src.benchmark.temporal import resolve_source_dates  # noqa: E402
from src.benchmark.v2_slice import count_tokens, screening_order  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import (  # noqa: E402
    append_jsonl, ensure_dir, read_jsonl, resolve_path, utc_now_iso, write_json, write_jsonl,
)
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.literature.crossref import CrossrefClient  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.build_canonical")

OUT_DIR = "benchmark/canonical"
V2_PROGRESS = "benchmark/v2/v2_progress.jsonl"


def _review_verdict(doi, *, policy):
    """Classify a source DOI from its cached Crossref record, or None if absent.

    A missing record is not a verdict: the row is kept and the gap shows up in
    `n_dois_without_cached_metadata` in the flag report, exactly as an API failure
    is never read as an answer elsewhere in this codebase.
    """
    from src.benchmark.review_sources import classify_source, venue_and_title_from_crossref

    path = Path("data/cache/crossref") / "{}.json".format(doi.replace("/", "_"))
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (ValueError, OSError):
        return None
    message = payload.get("message") or payload
    fields = venue_and_title_from_crossref(message)
    return classify_source(venue=fields["venue"], title=fields["title"],
                           venue_patterns=policy.venue_patterns,
                           title_patterns=policy.title_patterns)


def load_inherited_screens(path: Path) -> Dict[int, Dict[str, Any]]:
    """Row-level R1/R3/R5/R6 + R4 decisions already made for v2."""
    out: Dict[int, Dict[str, Any]] = {}
    if path.exists():
        for entry in read_jsonl(path):
            out[int(entry["screen_rank"])] = entry
    return out


def screen_canonical_pair(question, gold_claim, negative_claim, *, llm, prompts) -> Dict[str, Any]:
    """R2, applied to the canonical texts a verifier will actually see."""
    template = prompts.get(PAIR_PROMPT)
    messages = [{"role": "user", "content": template.render(
        question=question, gold=gold_claim, alternative=negative_claim)}]

    def validate(parsed: Dict[str, Any]) -> None:
        for key in ("same_target", "disagrees_substantively"):
            if not isinstance(parsed.get(key), bool):
                raise ValueError("{!r} must be a boolean".format(key))

    try:
        response = llm.complete_json(messages, purpose="canonical.pair_comparability",
                                     prompt_version=PAIR_PROMPT, validator=validate)
    except (LLMParseError, LLMError) as exc:
        return {"decision": "ERROR", "error": "{}: {}".format(type(exc).__name__, exc)}
    parsed = response.parsed or {}
    detail = {k: bool(parsed.get(k)) for k in ("same_target", "disagrees_substantively")}
    detail["decision"] = "PASS" if all(detail.values()) else "FAIL"
    detail["rationale"] = parsed.get("rationale")
    return detail


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build the canonicalized benchmark.")
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--dataset", default="benchmark/ranking.jsonl")
    parser.add_argument("--out-dir", default=OUT_DIR)
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--max-words", type=int, default=MAX_CLAIM_WORDS)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    config = load_config(args.config)
    out_dir = ensure_dir(resolve_path(args.out_dir))
    order = screening_order(resolve_path(args.dataset))
    inherited = load_inherited_screens(resolve_path(V2_PROGRESS))
    LOGGER.info("inherited %d row screening decision(s) from the v2 build", len(inherited))

    progress_path = out_dir / "canonical_progress.jsonl"
    done: Dict[int, Dict[str, Any]] = {}
    if progress_path.exists():
        for entry in read_jsonl(progress_path):
            done[int(entry["screen_rank"])] = entry
        LOGGER.info("resuming: %d row(s) already canonicalised", len(done))

    event_log = EventLog(out_dir / "canonical_build_events.jsonl")
    llm = build_llm_client(config.llm, event_log=event_log)
    prompts = PromptLibrary(config.prompts.dir)
    crossref = CrossrefClient(config.crossref, event_log=event_log)

    pairs: List[Any] = []
    rejected = Counter()
    rows_processed = 0
    preservation_counts = Counter()
    review_policy = config.dataset.review_sources
    review_excluded: List[Dict[str, Any]] = []

    for screen_rank, doi, row in order:
        if len(pairs) >= args.target:
            LOGGER.info("target of %d pairs reached at screen rank %d", args.target, screen_rank)
            break
        if args.max_rows is not None and rows_processed >= args.max_rows:
            break

        screen = inherited.get(screen_rank)
        if screen is None:
            rejected["not_screened_for_validity"] += 1
            continue
        if (screen.get("row_screen") or {}).get("decision") != "PASS":
            rejected["row_screen"] += 1
            continue
        cutoff = screen.get("cutoff_date")
        if not cutoff:
            rejected["cutoff"] += 1
            continue
        # Task validity: a review's gold hypothesis summarises work already
        # published, so the answer is in the pre-cutoff literature by
        # construction. Cheap, deterministic, and before any model call.
        if review_policy.enabled and review_policy.action == "exclude":
            verdict = _review_verdict(doi, policy=review_policy)
            if verdict is not None and verdict.is_review:
                rejected["review_source"] += 1
                review_excluded.append({"doi": doi, "screen_rank": screen_rank,
                                        **verdict.record()})
                continue

        cached = done.get(screen_rank)
        if cached:
            candidates = [CanonicalCandidate(**c) for c in cached["candidates"]]
            verdicts = cached.get("pairs") or {}
        else:
            rows_processed += 1
            candidates = canonicalise_row(row, llm=llm, prompts=prompts, max_words=args.max_words)
            gold = candidates[0]
            verdicts = {}
            if gold.usable:
                for candidate in candidates[1:]:
                    if not candidate.usable:
                        continue
                    verdicts[str(candidate.source_index)] = screen_canonical_pair(
                        row.get("research_question") or "", gold.claim, candidate.claim,
                        llm=llm, prompts=prompts)
            entry = {
                "screen_rank": screen_rank, "doi": doi, "cutoff_date": cutoff,
                "candidates": [c.model_dump(mode="json") for c in candidates],
                "pairs": verdicts,
            }
            append_jsonl(progress_path, entry)
            done[screen_rank] = entry

        for candidate in candidates:
            preservation_counts["preserved" if candidate.preserved else
                                ("error" if candidate.error else "not_preserved")] += 1

        gold = candidates[0]
        if not gold.usable:
            rejected["gold_not_preserved"] += 1
            continue

        kept_here = 0
        for candidate in candidates[1:]:
            if not candidate.usable:
                continue
            verdict = verdicts.get(str(candidate.source_index)) or {}
            if verdict.get("decision") != "PASS":
                continue
            pairs.append(build_pair(
                row=row, screen_rank=screen_rank, gold=gold, negative=candidate,
                comparable=True, rationale=verdict.get("rationale"), cutoff_date=cutoff))
            kept_here += 1
        if kept_here == 0:
            rejected["no_comparable_canonical_pair"] += 1
        else:
            LOGGER.info("rank %d (%s): %d canonical pair(s)  [running total %d]",
                        screen_rank, doi, kept_here, len(pairs))

    write_jsonl(out_dir / "researchbench_canonical_pairs.jsonl",
                [p.model_dump(mode="json") for p in pairs])

    ratios = [p.length_ratio for p in pairs]
    gold_tokens = [p.gold_token_count for p in pairs]
    negative_tokens = [p.negative_token_count for p in pairs]
    manifest = {
        "name": "ResearchBench-derived canonicalized evaluation benchmark",
        "version": "canonical-v1",
        "status": "EVALUATION CANDIDATE — usable only if the frozen diagnostics pass",
        "derived": (
            "This is a DERIVED benchmark. Every candidate was rewritten by a model. "
            "It is not untouched ResearchBench and must not be described as such."
        ),
        "protocol": "docs/CANONICAL_PROTOCOL.md (frozen before this build ran)",
        "frozen_at": utc_now_iso(),
        "source_dataset": str(resolve_path(args.dataset)),
        "screening_order": "SHA256(DOI) ascending after DOI deduplication (v1 order)",
        "gates": [
            "inherited R1/R3/R5/R6 row screen + R4 cutoff (reused verbatim from the v2 build)",
            "symmetric canonicalisation, blind to candidate role",
            "semantic preservation check on every canonical claim",
            "R2 pair comparability re-applied to the CANONICAL texts",
            "review-article source excluded (task validity; see src/benchmark/review_sources.py)",
        ],
        "review_source_exclusion": {
            "policy": review_policy.model_dump(mode="json"),
            "n_excluded": len(review_excluded),
            "excluded": review_excluded,
            "limitation": (
                "venue/title matching on cached Crossref metadata. Crossref types "
                "review articles as journal-article, so a review in a "
                "general-purpose journal is not caught."
            ),
        },
        "no_length_gate": (
            "Length is measured and reported, never filtered. If a length cue survives "
            "canonicalisation that is a finding about the transformation."
        ),
        "prompts": {
            "canonicalise": prompts.get(CANONICALISE_PROMPT).record(),
            "preservation": prompts.get(PRESERVATION_PROMPT).record(),
            "pair_comparability": prompts.get(PAIR_PROMPT).record(),
        },
        "max_claim_words": args.max_words,
        "llm": {"provider": config.llm.provider, "deployment": getattr(llm, "deployment", None),
                "temperature": config.llm.temperature},
        "not_used_in_construction": [
            "literature retrieval", "Direct-RAG output", "consequence-graph output",
            "any verifier score", "any artifact-diagnostic result",
            "knowledge of which candidate is the gold, at any transformation step",
        ],
        "target_pairs": args.target,
        "target_reached": len(pairs) >= args.target,
        "n_pairs": len(pairs),
        "n_source_rows": len({p.doi for p in pairs}),
        "n_rows_canonicalised": rows_processed,
        "rejected": dict(rejected),
        "preservation": dict(preservation_counts),
        "length_profile": {
            "gold_tokens_median": statistics.median(gold_tokens) if gold_tokens else None,
            "negative_tokens_median": statistics.median(negative_tokens) if negative_tokens else None,
            "ratio_median": round(statistics.median(ratios), 3) if ratios else None,
            "ratio_min": round(min(ratios), 3) if ratios else None,
            "ratio_max": round(max(ratios), 3) if ratios else None,
            "share_gold_shorter": round(
                sum(1 for p in pairs if p.gold_token_count < p.negative_token_count) / len(pairs), 4
            ) if pairs else None,
        },
        "llm_usage": dict(getattr(llm, "usage_totals", {})),
    }
    write_json(out_dir / "canonical_manifest.json", manifest)

    print("\ncanonical pairs: {} across {} source row(s) (target {} {})".format(
        len(pairs), manifest["n_source_rows"], args.target,
        "reached" if manifest["target_reached"] else "NOT reached"))
    print("rejected: {}".format(dict(rejected)))
    print("preservation: {}".format(dict(preservation_counts)))
    print("length: gold median {} tok, negative median {} tok, gold shorter in {}".format(
        manifest["length_profile"]["gold_tokens_median"],
        manifest["length_profile"]["negative_tokens_median"],
        manifest["length_profile"]["share_gold_shorter"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
