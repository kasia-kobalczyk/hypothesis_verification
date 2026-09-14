"""Extract real assessment cases into a file a human can adjudicate.

    python3 scripts/build_assessor_labelset.py --n-per-stratum 4

Pulls (proposition, retrieved papers, current label, current rationale) from saved
consequence-graph runs and writes `benchmark/assessor/labelset_candidates.jsonl`,
one case per line, with the abstracts included so the judgment can be made without
re-running retrieval.

This exists because `no_evidence` currently means something narrower than the
method needs. Measured over 528 assessments from the debug runs: of 343
`no_evidence` verdicts, **99% invoke directness** and **82% explicitly concede that
related work was retrieved before declining it**. So the label is reporting "no
retrieved paper *directly investigates* this proposition", not "the retrieved
literature does not bear on this proposition" -- and a consequence graph is built
on exactly the second notion.

No LLM calls, no network. Selection is deterministic (sorted, then strided) so the
same command yields the same cases.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CONCEDES = re.compile(r"while (some|several|the|one|a few)|although|however", re.I)
DIRECTNESS = re.compile(r"directly|direct ", re.I)


def collect(run_glob: str) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for instance_dir in sorted(glob.glob(run_glob)):
        base = Path(instance_dir)
        try:
            evidence = json.loads((base / "evidence.json").read_text())["by_node"]
            retrieval = json.loads((base / "retrieval.json").read_text())["by_node"]
        except (OSError, ValueError, KeyError):
            continue
        for node_id, record in evidence.items():
            assessment = record.get("assessment") or {}
            papers = (retrieval.get(node_id) or {}).get("papers_shown", [])
            rationale = assessment.get("rationale") or ""
            cases.append({
                # The run id has to be in the key: the same instance and node appear
                # in more than one run (e.g. the v1-prompt and v2-prompt A/B runs),
                # and a colliding case_id silently drops cases when answers are keyed
                # by it.
                "case_id": "{}::{}::{}".format(
                    base.parent.parent.name.split("_")[-1], base.name, node_id),
                "run": base.parent.parent.name,
                "instance": base.name,
                "node": node_id,
                "proposition": record.get("text", ""),
                "current_label": assessment.get("evidence_label"),
                "current_rationale": rationale,
                "rationale_invokes_directness": bool(DIRECTNESS.search(rationale)),
                "rationale_concedes_related_work": bool(CONCEDES.search(rationale)),
                "papers": [
                    {
                        "id": p.get("paper_id"),
                        "title": p.get("title"),
                        "abstract": p.get("abstract"),
                        "year": p.get("year"),
                        "venue": p.get("venue"),
                    }
                    for p in papers
                ],
                "n_papers": len(papers),
                "n_with_abstract": sum(
                    1 for p in papers if p.get("abstract") and str(p["abstract"]).strip()),
            })
    return cases


def stratify(cases: List[Dict[str, Any]], *, per_stratum: int) -> List[Dict[str, Any]]:
    """Deterministic stratified pick: the strata are the judgments we most doubt.

    Over-samples the `no_evidence`-with-conceded-related-work stratum, because that
    is where the construct question lives -- those are the cases where the assessor
    saw relevant work and declined it.
    """
    strata: "defaultdict[str, List[Dict[str, Any]]]" = defaultdict(list)
    for case in cases:
        if not case["n_with_abstract"]:
            continue  # nothing to adjudicate from
        label = case["current_label"] or "?"
        if label == "no_evidence":
            key = ("no_evidence/concedes_related"
                   if case["rationale_concedes_related_work"] else "no_evidence/clean")
        else:
            key = label
        strata[key].append(case)

    picked: List[Dict[str, Any]] = []
    for key in sorted(strata):
        group = sorted(strata[key], key=lambda c: c["case_id"])
        # Over-sample the stratum the construct question lives in.
        want = per_stratum * 3 if key == "no_evidence/concedes_related" else per_stratum
        if len(group) <= want:
            chosen = group
        else:
            stride = len(group) / float(want)
            chosen = [group[int(i * stride)] for i in range(want)]
        for case in chosen:
            case = dict(case)
            case["stratum"] = key
            picked.append(case)
    return picked


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", default="runs/consequence_graph_*/instances/*/")
    parser.add_argument("--n-per-stratum", type=int, default=4)
    parser.add_argument("--out", default="benchmark/assessor/labelset_candidates.jsonl")
    parser.add_argument("--include", nargs="*", default=[],
                        help="case_id suffixes (instance::node) to force into the set")
    parser.add_argument("--reshuffle", action="store_true",
                        help="discard the existing selection and re-sample from scratch. "
                             "Refuses if any case already carries a label.")
    args = parser.parse_args(argv)

    cases = collect(args.runs)
    by_id = {c["case_id"]: c for c in cases}

    # The selection must be STABLE once adjudication starts: adding a run changes
    # the pool, and re-striding it would swap cases out from under judges who have
    # already worked on them. So an existing file is preserved by default.
    out_path = Path(args.out)
    existing: List[Dict[str, Any]] = []
    if out_path.exists() and not args.reshuffle:
        existing = [json.loads(line) for line in out_path.read_text().splitlines()
                    if line.strip()]
    elif out_path.exists() and args.reshuffle:
        prior = [json.loads(line) for line in out_path.read_text().splitlines()
                 if line.strip()]
        laboured = [c for c in prior if c.get("gold_label")]
        if laboured:
            print("refusing to reshuffle: {} case(s) already carry labels. "
                  "Move the file aside first if you really mean it.".format(len(laboured)))
            return 1

    picked = stratify(cases, per_stratum=args.n_per_stratum)

    forced = []
    for suffix in args.include:
        matches = [c for c in cases if c["case_id"].endswith("::" + suffix)
                   or c["case_id"] == suffix]
        if not matches:
            print("warning: --include {} matched nothing".format(suffix))
            continue
        forced.append(sorted(matches, key=lambda c: c["case_id"])[0])

    # Existing selection wins; new picks only top it up.
    selected: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for case in existing:
        merged = dict(by_id.get(case["case_id"], {}))
        merged.update(case)  # keep any labels already recorded
        selected[case["case_id"]] = merged
    for case in forced + picked:
        if case["case_id"] not in selected:
            case = dict(case)
            case.setdefault("stratum", "forced" if case in forced else case.get("stratum"))
            selected[case["case_id"]] = case
    picked = list(selected.values())

    out = out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for case in picked:
            case.setdefault("gold_label", None)        # filled in by a human
            case.setdefault("gold_directness", None)   # direct | indirect | null
            case.setdefault("gold_link", None)         # one sentence naming the paper
            case.setdefault("labelled_by", None)
            handle.write(json.dumps(case, sort_keys=True) + "\n")

    by_stratum: "defaultdict[str, int]" = defaultdict(int)
    for case in picked:
        by_stratum[case["stratum"]] += 1
    print("{} assessed nodes available; {} selected for labelling".format(
        len(cases), len(picked)))
    for key in sorted(by_stratum):
        print("  {:<34} {}".format(key, by_stratum[key]))
    n_ne = sum(1 for c in cases if c["current_label"] == "no_evidence")
    if n_ne:
        print("\nacross ALL {} assessments:".format(len(cases)))
        print("  no_evidence verdicts:                {}".format(n_ne))
        print("  ... invoking directness:             {} ({:.0%})".format(
            sum(1 for c in cases if c["current_label"] == "no_evidence"
                and c["rationale_invokes_directness"]),
            sum(1 for c in cases if c["current_label"] == "no_evidence"
                and c["rationale_invokes_directness"]) / n_ne))
        print("  ... conceding related work was found: {} ({:.0%})".format(
            sum(1 for c in cases if c["current_label"] == "no_evidence"
                and c["rationale_concedes_related_work"]),
            sum(1 for c in cases if c["current_label"] == "no_evidence"
                and c["rationale_concedes_related_work"]) / n_ne))
    print("\nwrote {}".format(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
