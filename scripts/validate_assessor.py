"""Validate the assessor construct without domain experts.

    python3 scripts/validate_assessor.py --judges a b

What this CAN establish: that `INDIRECT` is operationally coherent, reproducible
across independent blinded assessors, grounded in the supplied text, and not
manufacturing signal from topical adjacency.

What it CANNOT establish: that `INDIRECT` matches the judgment a domain expert
would make. No expert labels exist. Passing makes the assessor **provisionally
validated**, never settled, and the agreement statistics are *reproducibility*, not
validity.

Four conditions per case, each judged independently by two assessors that share no
prompt and never see each other's output or the current assessor's:

| condition | what it is | what should happen |
| --- | --- | --- |
| `real` | the proposition with its own retrieved record | the baseline |
| `mismatched` | the proposition with an unrelated record from another case | collapse to NO_EVIDENCE |
| `swapped` | the proposition with a record that is genuinely informative *for a different proposition* | collapse to NO_EVIDENCE (harder negative) |
| `negated` | the proposition logically negated, own record | DIRECTION flips; informativeness should not simply persist unchanged |

A fifth condition, `span_removed`, is generated in a second pass from the positives
of the first: the sentence carrying the supporting span is deleted from the abstract
and the case re-judged. An indirect judgment that survives its own evidence being
removed was not using it.

Grounding is checked mechanically: `supporting_span` must appear verbatim in the
abstract that was supplied. A judgment whose span cannot be found is not counted as
evidence, whatever it claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.validate_assessor")

JUDGE_PROMPTS = {
    # The original three-way task, which FAILED criterion 3 (DECISIONS #28).
    "broad": {"a": "assessor_judge_a_v1", "b": "assessor_judge_b_v1"},
    # The narrow task after the architectural correction (DECISIONS #29): the
    # evidence assessor judges only direct bearing on the proposition node, and
    # every inferential bridge moves to the graph edges.
    "narrow": {"a": "assessor_narrow_judge_a_v1", "b": "assessor_narrow_judge_b_v1"},
}


# --------------------------------------------------------------------------- #
# Normalising two deliberately different judge schemas onto one construct
# --------------------------------------------------------------------------- #
def normalise_narrow(judge: str, parsed: Dict[str, Any]) -> Dict[str, Any]:
    """The narrow task has two categories: DIRECT or NO_EVIDENCE. No INDIRECT.

    Judge B is again never shown the category names; its step answers are mapped
    here. A quote that states the claim but in a different system does not count as
    direct -- that is a graph edge, not evidence.
    """
    if judge == "a":
        category = ("DIRECT" if str(parsed.get("category", "")).strip().upper()
                    == "DIRECT_EVIDENCE" else "NO_EVIDENCE")
        direction = str(parsed.get("direction", "none")).strip().lower()
        return {
            "category": category,
            "direction": direction if category == "DIRECT" else "none",
            "span": parsed.get("supporting_span"),
            "intermediate_fact": None,
            "needs_outside_fact": bool(parsed.get("requires_external_bridge")),
            "merely_related": bool(parsed.get("would_need_inference")),
            "unassessable": bool(parsed.get("proposition_unassessable")),
            "chain": None,
        }
    verdict = str(parsed.get("verdict", "neither")).strip().lower()
    direction = {"more_likely": "supports", "less_likely": "contradicts"}.get(verdict, "none")
    states = bool(parsed.get("a_quote_states_the_claim_or_its_opposite"))
    same_system = bool(parsed.get("same_system_as_the_claim"))
    needs_outside = bool(parsed.get("needs_outside_fact"))
    if states and same_system and not needs_outside and direction != "none":
        category = "DIRECT"
    else:
        category, direction = "NO_EVIDENCE", "none"
    return {
        "category": category,
        "direction": direction,
        "span": parsed.get("evidence_span"),
        "intermediate_fact": None,
        "needs_outside_fact": needs_outside,
        "merely_related": bool(parsed.get("same_subject_but_would_need_reasoning")),
        "unassessable": bool(parsed.get("claim_is_uncheckable_as_written")),
        "chain": None,
    }


def normalise(judge: str, parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Judge B never names the categories, so it cannot anchor on the vocabulary."""
    if judge == "a":
        category = str(parsed.get("category", "")).strip().upper() or "NO_EVIDENCE"
        direction = str(parsed.get("direction", "none")).strip().lower()
        return {
            "category": category,
            "direction": direction if category != "NO_EVIDENCE" else "none",
            "span": parsed.get("supporting_span"),
            "intermediate_fact": parsed.get("intermediate_fact"),
            "needs_outside_fact": bool(parsed.get("requires_unsupported_facts")),
            "merely_related": bool(parsed.get("merely_related")),
            "unassessable": bool(parsed.get("proposition_unassessable")),
            "chain": parsed.get("chain"),
        }
    verdict = str(parsed.get("verdict", "neither")).strip().lower()
    direction = {"more_likely": "supports", "less_likely": "contradicts"}.get(verdict, "none")
    needs_outside = bool(parsed.get("needs_outside_fact"))
    has_link = bool((parsed.get("connection") or "").strip())
    if parsed.get("tests_proposition_itself") and direction != "none":
        category = "DIRECT"
    elif has_link and not needs_outside and direction != "none":
        category = "INDIRECT"
    else:
        category = "NO_EVIDENCE"
        direction = "none"
    return {
        "category": category,
        "direction": direction,
        "span": parsed.get("evidence_span"),
        "intermediate_fact": parsed.get("connection"),
        "needs_outside_fact": needs_outside,
        "merely_related": bool(parsed.get("same_subject_but_no_link")),
        "unassessable": bool(parsed.get("proposition_is_uncheckable_as_written")),
        "chain": None,
    }


def _norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip().lower()


def span_is_grounded(span: Optional[str], abstract: str) -> bool:
    """Verbatim check, tolerant only of whitespace and case.

    Deliberately strict on content: the point is that the judge copied a real span
    rather than reconstructing one that sounds right.
    """
    if not span or not str(span).strip():
        return False
    return _norm_ws(str(span)) in _norm_ws(abstract)


def boundary_pairs(rows_a: Dict[str, str], rows_b: Dict[str, str]) -> List[Tuple[str, str]]:
    """Drop cases both judges called DIRECT: they are easy and inflate agreement."""
    shared = sorted(set(rows_a) & set(rows_b))
    return [(rows_a[c], rows_b[c]) for c in shared
            if not (rows_a[c] == "DIRECT" and rows_b[c] == "DIRECT")]


def render_record(paper: Dict[str, Any]) -> str:
    return "id: {}\ntitle: {}\nyear: {}\nvenue: {}\nabstract: {}".format(
        paper.get("id"), paper.get("title"), paper.get("year"),
        paper.get("venue"), paper.get("abstract"))


def primary_record(case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """The top-ranked retrieved record that actually carries an abstract."""
    for paper in case.get("papers", []):
        if (paper.get("abstract") or "").strip():
            return paper
    return None


def negate(proposition: str) -> str:
    """Crude but logically exact, and model-free.

    Control generation must not depend on the thing under test, so this is a prefix
    negation rather than a learned rewrite. It is clumsy prose; it is unambiguous
    about truth conditions, which is what the direction-flip check needs.
    """
    return "It is NOT the case that: {}".format(proposition.rstrip("."))


def drop_span_sentence(abstract: str, span: str) -> str:
    """Remove the sentence carrying the span, so the evidence is gone, not hidden."""
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    needle = _norm_ws(span)
    kept = [s for s in sentences if needle not in _norm_ws(s)]
    if len(kept) == len(sentences):          # span crosses sentences; fall back
        return _norm_ws(abstract).replace(needle, " ")
    return " ".join(kept)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--labelset", default="benchmark/assessor/labelset_candidates.jsonl")
    parser.add_argument("--judges", nargs="+", default=["a", "b"])
    parser.add_argument("--task", choices=["broad", "narrow"], default="broad",
                        help="broad = the original three-way task (failed, DECISIONS #28); "
                             "narrow = direct bearing on the proposition node only")
    parser.add_argument("--conditions", nargs="+",
                        default=["real", "mismatched", "swapped", "negated"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--all-records", action="store_true",
                        help="judge EVERY record with an abstract, not just the top-ranked "
                             "one. Same rubric, same prompts, same gate -- purely a "
                             "measurement-power change, because criterion 3 is a rate over "
                             "evidential judgments and one record per case yields too few.")
    parser.add_argument("--out", default=None,
                        help="default: benchmark/assessor/validation_<task>.json")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing output file. Without it the run "
                             "refuses rather than destroying a previous result.")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    out_path = Path(args.out or "benchmark/assessor/validation_{}.json".format(args.task))
    # A validation result is expensive and not reproducible call-for-call. Refuse to
    # clobber one: a two-case smoke test once overwrote a 350-judgment run, which was
    # only recoverable because the event log is append-only.
    if out_path.exists() and not args.force:
        print("refusing to overwrite {} -- pass --out or --force".format(out_path))
        return 1

    config = load_config(args.config)
    prompts = PromptLibrary(config.prompts.dir)
    event_log = EventLog(Path("benchmark/assessor/validation_events.jsonl"))
    llm = build_llm_client(config.llm, event_log=event_log)
    freeze = json.loads(Path("benchmark/assessor/rubric_freeze.json").read_text())
    gate = json.loads(Path("benchmark/assessor/acceptance_gate.json").read_text())

    raw = [json.loads(line) for line in Path(args.labelset).read_text().splitlines()
           if line.strip()]
    raw = [c for c in raw if primary_record(c)]
    if args.limit:
        raw = raw[: args.limit]

    if args.all_records:
        # One unit of judgment per (proposition, record) pair. The construct is
        # per-record already -- the grounding check needs a single abstract as the
        # whole input -- so this changes only how many units there are.
        cases = []
        for case in raw:
            for paper in case["papers"]:
                if not (paper.get("abstract") or "").strip():
                    continue
                unit = dict(case)
                unit["papers"] = [paper]
                unit["case_id"] = "{}#{}".format(case["case_id"], paper.get("id"))
                unit["source_case_id"] = case["case_id"]
                cases.append(unit)
    else:
        cases = raw
    LOGGER.info("%d judgment unit(s) from %d case(s)", len(cases), len(raw))

    # Deterministic pairings for the negative controls. The offset is large and
    # coprime-ish with the list length so a case is never paired with its neighbour
    # from the same instance.
    n = len(cases)
    mismatch_of = {c["case_id"]: cases[(i + n // 2 + 1) % n] for i, c in enumerate(cases)}
    swap_of = {c["case_id"]: cases[(i + 1) % n] for i, c in enumerate(cases)}

    def build(condition: str, case: Dict[str, Any]):
        own = primary_record(case)
        if condition == "real":
            return case["proposition"], own
        if condition == "mismatched":
            return case["proposition"], primary_record(mismatch_of[case["case_id"]])
        if condition == "swapped":
            return case["proposition"], primary_record(swap_of[case["case_id"]])
        if condition == "negated":
            return negate(case["proposition"]), own
        raise ValueError(condition)

    results: List[Dict[str, Any]] = []

    def ask(judge: str, proposition: str, record: Dict[str, Any],
            condition: str, case_id: str) -> Optional[Dict[str, Any]]:
        template = prompts.get(JUDGE_PROMPTS[args.task][judge])
        messages = [{"role": "user", "content": template.render(
            proposition=proposition, record=render_record(record))}]

        def validate(parsed: Dict[str, Any]) -> None:
            if judge == "a" and not str(parsed.get("category", "")).strip():
                raise ValueError("missing category")
            if judge == "b" and not str(parsed.get("verdict", "")).strip():
                raise ValueError("missing verdict")

        try:
            response = llm.complete_json(
                messages, purpose="assessor.validate.{}.{}".format(args.task, condition),
                prompt_version=JUDGE_PROMPTS[args.task][judge], validator=validate)
        except (LLMParseError, LLMError) as exc:
            LOGGER.error("%s/%s/%s: %s", case_id, condition, judge, exc)
            return None
        mapper = normalise_narrow if args.task == "narrow" else normalise
        row = mapper(judge, response.parsed or {})
        row.update({
            "case_id": case_id, "condition": condition, "judge": judge,
            "record_id": record.get("id"),
            "grounded": span_is_grounded(row["span"], record.get("abstract") or ""),
        })
        return row

    for condition in args.conditions:
        LOGGER.info("--- condition: %s ---", condition)
        for index, case in enumerate(cases, start=1):
            proposition, record = build(condition, case)
            if record is None:
                continue
            for judge in args.judges:
                row = ask(judge, proposition, record, condition, case["case_id"])
                if row:
                    results.append(row)
            if index % 10 == 0:
                LOGGER.info("  %s: %d/%d", condition, index, len(cases))

    # --- second pass: remove the evidence and see if the judgment survives ----- #
    if "real" in args.conditions:
        positives = [r for r in results
                     if r["condition"] == "real" and r["category"] != "NO_EVIDENCE"
                     and r["grounded"]]
        LOGGER.info("--- condition: span_removed (%d grounded positive(s)) ---", len(positives))
        by_case = {c["case_id"]: c for c in cases}
        for row in positives:
            case = by_case[row["case_id"]]
            record = dict(primary_record(case))
            record["abstract"] = drop_span_sentence(record.get("abstract") or "", row["span"])
            if not record["abstract"].strip():
                continue
            new = ask(row["judge"], case["proposition"], record, "span_removed", row["case_id"])
            if new:
                new["was"] = row["category"]
                results.append(new)

    write_json(out_path, {
        "generated_at": utc_now_iso(),
        "rubric_freeze": freeze,
        "gate": gate,
        "task": args.task,
        "judges": {j: JUDGE_PROMPTS[args.task][j] for j in args.judges},
        "model": config.llm.deployment,
        "same_model_caveat": (
            "Both judges run on one deployment; they differ in prompt and reasoning "
            "scaffold only. Same-model agreement has correlated errors and is weaker "
            "evidence than cross-model agreement."
        ),
        "n_cases": len(cases),
        "conditions": args.conditions + ["span_removed"],
        "rows": results,
    })
    print("\n{} judgment(s) -> {}".format(len(results), out_path))
    print("Run scripts/assessor_validation_report.py to evaluate the gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
