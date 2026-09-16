"""Historical evidence discovery for BENCH-GRAPH-PILOT-001 (Step 7B).

Deliberately a separate script from the consequence-recovery analysis, because
the two answer different questions and must be readable apart. A system can
generate the right discriminator and fail to find evidence for it; a system can
also find abundant evidence for propositions that decide nothing. Merging the two
into one score would hide both.

Structural facts are taken from the run and never guessed:

* an assessment ERROR is an error. It is reported as `evidence_assessor_error`
  and is never folded into `no_evidence` -- a failed API call says nothing about
  the literature, and treating it as absence of evidence would silently penalise
  a proposition for a network problem;
* zero eligible papers is a retrieval outcome, recorded as such;
* the assessor's own label is carried through verbatim.

Only the genuinely ambiguous branch is put to a judge: retrieval returned
something, the assessor reached a verdict, and the question is whether the
literature really failed to speak to the proposition or whether the process did.

Usage:
    python scripts/analyze_pilot_evidence.py --run runs/pilot_explanatory_001
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config
from src.common.io import resolve_path, write_json
from src.common.logging_utils import EventLog, get_logger
from src.llm.client import build_llm_client
from src.llm.prompts import PromptLibrary

# Post-hoc audit prompts live OUTSIDE the verifier's prompt directory. They are
# allowed to state the cutoff date and to show hidden annotations, both of which
# are forbidden in verifier prompts -- see src/llm/prompts_audit/README.md. The
# separation is a directory, not a flag, so a verifier run cannot reach them.
AUDIT_PROMPTS = Path(__file__).resolve().parents[1] / "src" / "llm" / "prompts_audit"

LOGGER = get_logger("pilot.evidence")

ATTRIBUTIONS = [
    "informative_evidence_found",
    "no_relevant_historical_evidence_exists",
    "retrieval_failure",
    "evidence_assessor_failure",
    "generic_compatibility_only",
    "construct_mismatch",
]

# Labels that carry information about the proposition. `no_evidence` and `mixed`
# both map to a log-LR of 0.0 in configs/ordinal_mappings.yaml, but they are not
# the same event and are counted separately here.
INFORMATIVE_LABELS = {
    "strong_support", "support", "weak_support",
    "weak_contradiction", "contradiction", "strong_contradiction",
}


def _validator(payload: Dict[str, Any]) -> None:
    if payload.get("attribution") not in ATTRIBUTIONS:
        raise ValueError("unknown attribution {!r}".format(payload.get("attribution")))


def structural_facts(
    node_id: str, retrieval: Dict[str, Any], evidence: Dict[str, Any]
) -> Dict[str, Any]:
    """What the run itself records, with no interpretation applied."""
    ret = (retrieval.get("by_node") or {}).get(node_id) or {}
    ev = (evidence.get("by_node") or {}).get(node_id) or {}
    assessment = ev.get("assessment") or {}

    queries = ret.get("queries") or []
    n_eligible = int(ret.get("n_unique_eligible") or 0)
    n_shown = int(assessment.get("n_papers_shown") or 0)
    label = assessment.get("evidence_label")

    # An error is an error. This is the standing constraint that API failure must
    # never be read as `no_evidence`.
    had_error = bool(ev.get("error") or assessment.get("error"))

    return {
        "n_queries": len(queries),
        "n_unique_eligible_papers": n_eligible,
        "n_papers_shown_to_assessor": n_shown,
        "evidence_label": label,
        "model_evidence_label": assessment.get("model_evidence_label"),
        "label_enforced_by_harness": bool(assessment.get("label_enforced_by_harness")),
        "proposition_unassessable": bool(assessment.get("proposition_unassessable")),
        "requires_external_bridge": bool(assessment.get("requires_external_bridge")),
        "n_supporting_spans": len(assessment.get("supporting_spans") or []),
        "assessor_errored": had_error,
        "retrieved_nothing": n_eligible == 0,
        "label_is_informative": label in INFORMATIVE_LABELS,
    }


def _papers_block(retrieval_node: Dict[str, Any], limit: int = 10) -> str:
    seen, lines = set(), []
    for query in retrieval_node.get("queries") or []:
        for paper in query.get("eligible") or []:
            key = paper.get("doi") or paper.get("paper_id")
            if key in seen:
                continue
            seen.add(key)
            lines.append("- {} ({}). {}".format(
                paper.get("title") or "<untitled>",
                paper.get("publication_date") or paper.get("year") or "undated",
                (paper.get("abstract") or "")[:300]))
            if len(lines) >= limit:
                return "\n".join(lines)
    return "\n".join(lines) or "(no papers were retrieved)"


def attribute(
    llm, library: PromptLibrary, *, proposition: str, cutoff: str,
    retrieval_node: Dict[str, Any], assessment: Dict[str, Any], n_shown: int,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    queries = []
    for query in retrieval_node.get("queries") or []:
        attempts = query.get("attempts") or []
        n_results = attempts[-1].get("n_results") if attempts else "?"
        queries.append("- {!r} -> {} raw result(s), {} eligible after cutoff filter".format(
            query.get("query"), n_results, query.get("n_eligible")))
    prompt = library.render(
        "evidence_attribution_v1",
        proposition=proposition,
        cutoff=cutoff,
        queries="\n".join(queries) or "(none)",
        papers=_papers_block(retrieval_node),
        n_papers=n_shown,
        evidence_label=assessment.get("evidence_label"),
        rationale=(assessment.get("rationale") or "")[:1500],
    )
    try:
        response = llm.complete_json(
            [{"role": "user", "content": prompt}],
            purpose="pilot.evidence_attribution",
            prompt_version="evidence_attribution_v1",
            validator=_validator,
        )
    except Exception as exc:  # noqa: BLE001
        return None, "{}: {}".format(type(exc).__name__, exc)
    return response.parsed, None


def analyse_case(
    llm, library: PromptLibrary, *, instance_dir: Path, cutoff: str,
    discriminator_nodes: Dict[str, str], workers: int = 1,
) -> Dict[str, Any]:
    graph = json.loads((instance_dir / "graph.json").read_text(encoding="utf-8"))
    retrieval = json.loads((instance_dir / "retrieval.json").read_text(encoding="utf-8"))
    evidence = json.loads((instance_dir / "evidence.json").read_text(encoding="utf-8"))

    def one(node: Dict[str, Any]) -> Dict[str, Any]:
        node_id = node["id"]
        facts = structural_facts(node_id, retrieval, evidence)
        ret_node = (retrieval.get("by_node") or {}).get(node_id) or {}
        assessment = (((evidence.get("by_node") or {}).get(node_id)) or {}).get(
            "assessment") or {}

        judged, error = None, None
        if facts["assessor_errored"]:
            # Recorded, never judged and never converted into an evidence claim.
            attribution = "evidence_assessor_error"
        else:
            judged, error = attribute(
                llm, library, proposition=node["text"], cutoff=cutoff,
                retrieval_node=ret_node, assessment=assessment,
                n_shown=facts["n_papers_shown_to_assessor"])
            attribution = (judged or {}).get("attribution")

        LOGGER.info("%s %s -> %s", instance_dir.name, node_id, attribution)
        return {
            "node_id": node_id,
            "text": node["text"],
            # Carried from the Step-6 analysis so 7B can be read for the
            # discriminators alone, which is what the directive asks about.
            "recovery_category": discriminator_nodes.get(node_id),
            "structural": facts,
            "attribution": attribution,
            "judge": judged,
            "judge_error": error,
        }

    # Independent calls; `map` preserves graph order.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows: List[Dict[str, Any]] = list(pool.map(one, graph.get("nodes") or []))

    return {"case_id": instance_dir.name, "cutoff": cutoff, "nodes": rows}


DISCRIMINATOR_CATEGORIES = {
    "reference_discriminator_recovered", "novel_plausible_discriminator"}


def summarise(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    def tally(rows):
        out: Dict[str, int] = {}
        for row in rows:
            key = row.get("attribution") or "judge_error"
            out[key] = out.get(key, 0) + 1
        return out

    all_rows = [row for case in cases for row in case["nodes"]]
    disc_rows = [r for r in all_rows
                 if r.get("recovery_category") in DISCRIMINATOR_CATEGORIES]

    return {
        "n_nodes": len(all_rows),
        "attribution_all_nodes": tally(all_rows),
        # The directive's actual question: "for USEFUL discriminators, did the
        # system find genuinely relevant pre-cutoff evidence?"
        "n_discriminative_nodes": len(disc_rows),
        "attribution_discriminative_nodes": tally(disc_rows),
        "evidence_labels_all_nodes": _label_tally(all_rows),
        "evidence_labels_discriminative_nodes": _label_tally(disc_rows),
        "n_assessor_errors": sum(
            1 for r in all_rows if r["structural"]["assessor_errored"]),
        "n_retrieved_nothing": sum(
            1 for r in all_rows if r["structural"]["retrieved_nothing"]),
        "per_case": [
            {"case_id": case["case_id"],
             "n_nodes": len(case["nodes"]),
             "attribution": tally(case["nodes"])}
            for case in cases
        ],
        "interpretation": (
            "Descriptive. `no_relevant_historical_evidence_exists` is a fact about "
            "the pre-cutoff literature, not a failure of the method and not "
            "evidence against the proposition."
        ),
    }


def _label_tally(rows) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for row in rows:
        key = row["structural"].get("evidence_label") or "none"
        out[key] = out.get(key, 0) + 1
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    parser.add_argument("--config", default="configs/pilot_explanatory.yaml")
    parser.add_argument("--out", default=None)
    parser.add_argument("--cases", nargs="*", default=None)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    run_dir = resolve_path(args.run)
    if not (run_dir / "summary.json").exists():
        LOGGER.error("%s is not a frozen run (no summary.json)", run_dir)
        return 2
    out_path = Path(args.out) if args.out else run_dir / "evidence_discovery.json"
    if out_path.exists() and not args.force:
        LOGGER.error("%s exists; pass --force to overwrite", out_path)
        return 2

    # Step 6 must already have run: 7B reports on the discriminators it identified.
    recovery_path = run_dir / "recovery.json"
    discriminator_nodes: Dict[str, Dict[str, str]] = {}
    if recovery_path.exists():
        recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
        for case in recovery["cases"]:
            discriminator_nodes[case["case_id"]] = {
                row["node_id"]: (row.get("judge") or {}).get("category")
                for row in case["propositions"]
            }
    else:
        LOGGER.warning(
            "no recovery.json: running 7B without the Step-6 categories, so the "
            "discriminator-only summary will be empty")

    config = load_config(args.config)
    cutoffs = {}
    for line in resolve_path(config.dataset.case_path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            cutoffs[row["case_id"]] = row["cutoff"]

    llm = build_llm_client(config.llm)
    llm.event_log = EventLog(run_dir / "evidence_analysis_events.jsonl")
    library = PromptLibrary(AUDIT_PROMPTS)

    wanted = set(args.cases) if args.cases else None
    cases = []
    for instance_dir in sorted((run_dir / "instances").iterdir()):
        if not instance_dir.is_dir() or (wanted and instance_dir.name not in wanted):
            continue
        if not (instance_dir / "graph.json").exists():
            LOGGER.warning("%s: no graph.json; skipped", instance_dir.name)
            continue
        cases.append(analyse_case(
            llm, library, instance_dir=instance_dir,
            cutoff=cutoffs[instance_dir.name],
            discriminator_nodes=discriminator_nodes.get(instance_dir.name, {}),
            workers=args.workers))

    payload = {
        "run_dir": str(run_dir),
        "analysis": "BENCH-GRAPH-PILOT-001 Step 7B historical evidence discovery",
        "judge_prompt": "evidence_attribution_v1",
        "judge_model": getattr(llm, "deployment", None),
        "cases": cases,
        "summary": summarise(cases),
    }
    write_json(out_path, payload)
    LOGGER.info("wrote %s", out_path)
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
