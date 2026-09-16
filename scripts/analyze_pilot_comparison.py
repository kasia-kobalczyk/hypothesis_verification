"""Hypothesis comparison for BENCH-GRAPH-PILOT-001 (Step 7C).

Answers: given only pre-cutoff evidence, what did the system actually conclude,
and how does that sit beside the hidden later resolution?

Two things this script deliberately does NOT do.

**It invents no decision threshold.** Picking a margin now, after seeing these
eight results, and calling anything above it "favored" would be choosing the
criterion to fit the data. The scores are reported with their margins and the
reader may judge; the only verdict this script issues on its own is
`insufficient_evidence`, and that one is structural -- it holds when no node
carried informative evidence, in which case the posterior is just the prior and
the ranking is an artifact of tie-breaking, not a finding.

**It computes no accuracy.** Four of the resolution types the benchmark permits
(`mixed`, `regime_dependent`, `component_wise`, `unresolved`) have no single
correct hypothesis, so "did it get it right" is not defined for them. Forcing
them into a binary would be exactly the thing the directive forbids. Agreement is
reported case by case, in words, and only where it means something.

Usage:
    python scripts/analyze_pilot_comparison.py --run runs/pilot_explanatory_001
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config
from src.common.io import resolve_path, write_json
from src.common.logging_utils import get_logger

LOGGER = get_logger("pilot.comparison")

HIDDEN_PATH = Path("benchmark/explanatory/cases_hidden.json")

INFORMATIVE_LABELS = {
    "strong_support", "support", "weak_support",
    "weak_contradiction", "contradiction", "strong_contradiction",
}

# Resolution types for which "which hypothesis won" is a well-formed question.
BINARY_RESOLUTIONS = {"favored", "disfavored"}


def system_conclusion(
    scores: Dict[str, Any], evidence: Dict[str, Any], recovery_case: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """What the run concluded, described rather than graded."""
    score_map = scores.get("scores") or {}
    ranking = scores.get("ranking") or []

    informative = []
    for node_id, entry in (evidence.get("by_node") or {}).items():
        label = ((entry or {}).get("assessment") or {}).get("evidence_label")
        if label in INFORMATIVE_LABELS:
            informative.append({"node_id": node_id, "label": label})

    # Which of those informative nodes were also ones the Step-6 auditor judged
    # to discriminate between the hypotheses? That intersection is what a
    # conclusion would have to rest on to be worth anything.
    discriminative_and_informative = []
    if recovery_case:
        judged = {
            row["node_id"]: (row.get("judge") or {})
            for row in recovery_case.get("propositions", [])
        }
        for item in informative:
            verdict = judged.get(item["node_id"]) or {}
            if verdict.get("is_discriminative"):
                discriminative_and_informative.append({
                    "node_id": item["node_id"],
                    "evidence_label": item["label"],
                    "category": verdict.get("category"),
                })

    ordered = sorted(score_map.items(), key=lambda kv: kv[1], reverse=True)
    margin = (ordered[0][1] - ordered[1][1]) if len(ordered) > 1 else None

    if not informative:
        verdict = "insufficient_evidence"
        verdict_basis = (
            "no node received an informative evidence label, so every posterior "
            "equals its prior and the ranking carries no information")
    else:
        verdict = "ranking_produced"
        verdict_basis = (
            "{} node(s) carried informative evidence; {} of those were also judged "
            "discriminative. No decision threshold is applied here.".format(
                len(informative), len(discriminative_and_informative)))

    return {
        "scores": score_map,
        "ranking": ranking,
        "top_ranked": ordered[0][0] if ordered else None,
        "margin_top_two": margin,
        "n_informative_assessments": len(informative),
        "informative_nodes": informative,
        "n_discriminative_and_informative": len(discriminative_and_informative),
        "discriminative_and_informative_nodes": discriminative_and_informative,
        "verdict": verdict,
        "verdict_basis": verdict_basis,
        "uncalibrated_note": (
            "Ordinal->numeric mappings are placeholders (configs/ordinal_mappings.yaml, "
            "v0-placeholder). The absolute posteriors are meaningless; only the "
            "ordering carries information, and only when informative evidence exists."
        ),
    }


def compare_to_resolution(
    conclusion: Dict[str, Any], resolution: Dict[str, Any], id_to_text: Dict[str, str]
) -> Dict[str, Any]:
    """Set the run's conclusion beside the hidden resolution, without scoring it."""
    kind = (resolution or {}).get("type")
    summary = (resolution or {}).get("summary")

    if conclusion["verdict"] == "insufficient_evidence":
        return {
            "resolution_type": kind,
            "resolution_summary": summary,
            "agreement": "not_applicable",
            "agreement_reason": (
                "the system reached no evidence-backed conclusion, so there is "
                "nothing to agree or disagree with"),
        }

    if kind not in BINARY_RESOLUTIONS:
        return {
            "resolution_type": kind,
            "resolution_summary": summary,
            "system_top_ranked": conclusion["top_ranked"],
            "agreement": "not_defined_for_this_resolution_type",
            "agreement_reason": (
                "the case resolved as {!r}: there is no single correct hypothesis, "
                "so a winner-matching comparison would be a category error. Read "
                "the system's ranking against the resolution summary by hand."
                .format(kind)),
        }

    return {
        "resolution_type": kind,
        "resolution_summary": summary,
        "system_top_ranked": conclusion["top_ranked"],
        "system_top_ranked_text": id_to_text.get(conclusion["top_ranked"]),
        "agreement": "reportable",
        "agreement_reason": (
            "this case has a directional resolution, so the system's top-ranked "
            "hypothesis can be set beside it -- descriptively, as one of eight, "
            "and not as an accuracy figure"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    parser.add_argument("--config", default="configs/pilot_explanatory.yaml")
    parser.add_argument("--out", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    run_dir = resolve_path(args.run)
    if not (run_dir / "summary.json").exists():
        LOGGER.error("%s is not a frozen run (no summary.json)", run_dir)
        return 2
    out_path = Path(args.out) if args.out else run_dir / "hypothesis_comparison.json"
    if out_path.exists() and not args.force:
        LOGGER.error("%s exists; pass --force to overwrite", out_path)
        return 2

    hidden = json.loads(resolve_path(HIDDEN_PATH).read_text(encoding="utf-8"))["cases"]
    config = load_config(args.config)
    visible = {}
    for line in resolve_path(config.dataset.case_path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            visible[row["case_id"]] = row

    recovery_by_case: Dict[str, Any] = {}
    recovery_path = run_dir / "recovery.json"
    if recovery_path.exists():
        for case in json.loads(recovery_path.read_text(encoding="utf-8"))["cases"]:
            recovery_by_case[case["case_id"]] = case

    cases: List[Dict[str, Any]] = []
    for instance_dir in sorted((run_dir / "instances").iterdir()):
        if not instance_dir.is_dir() or not (instance_dir / "scores.json").exists():
            continue
        case_id = instance_dir.name
        scores = json.loads((instance_dir / "scores.json").read_text(encoding="utf-8"))
        evidence = json.loads((instance_dir / "evidence.json").read_text(encoding="utf-8"))
        id_to_text = {h["hypothesis_id"]: h["text"] for h in visible[case_id]["hypotheses"]}

        conclusion = system_conclusion(scores, evidence, recovery_by_case.get(case_id))
        comparison = compare_to_resolution(
            conclusion, hidden[case_id].get("resolution") or {}, id_to_text)
        cases.append({
            "case_id": case_id,
            "cutoff": visible[case_id]["cutoff"],
            "hypotheses": id_to_text,
            "system_conclusion": conclusion,
            "comparison_to_hidden_resolution": comparison,
        })
        LOGGER.info("%s: %s | resolution=%s | agreement=%s", case_id,
                    conclusion["verdict"], comparison["resolution_type"],
                    comparison["agreement"])

    by_verdict: Dict[str, int] = {}
    by_agreement: Dict[str, int] = {}
    for case in cases:
        v = case["system_conclusion"]["verdict"]
        a = case["comparison_to_hidden_resolution"]["agreement"]
        by_verdict[v] = by_verdict.get(v, 0) + 1
        by_agreement[a] = by_agreement.get(a, 0) + 1

    payload = {
        "run_dir": str(run_dir),
        "analysis": "BENCH-GRAPH-PILOT-001 Step 7C hypothesis comparison",
        "cases": cases,
        "summary": {
            "n_cases": len(cases),
            "verdicts": by_verdict,
            "agreement_reportability": by_agreement,
            "interpretation": (
                "No accuracy figure is computed. Cases resolving as mixed / "
                "regime_dependent / component_wise have no single correct "
                "hypothesis; cases where the system reached no evidence-backed "
                "conclusion have nothing to compare. Both are reported as such "
                "rather than scored."
            ),
        },
    }
    write_json(out_path, payload)
    LOGGER.info("wrote %s", out_path)
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
