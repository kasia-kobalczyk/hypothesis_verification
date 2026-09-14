"""Inter-judge agreement on the adjudicated assessor cases.

    python3 scripts/adjudication_agreement.py --judges A B

The headline is NOT raw agreement. It is `boundary_agreement`: agreement restricted
to cases where at least one judge said `indirect` or `no_evidence`. `direct` cases
are easy and inflate a raw number, and they are not where the construct is at risk.

The question this answers, from `docs/ASSESSOR_RUBRIC.md`:

> Can two people reliably tell *indirect but evidential* from *merely related*?

If they cannot, the `indirect` category is too subjective to calibrate safely, and
no assessor prompt can rescue it. That is criterion 1 of the pre-registered
acceptance gate, and if it fails the other two are not evaluated.

Also emits the resolved labels — cases where the judges agree — as the adjudicated
set a prompt is later scored against. Disagreements are listed for a third pass and
are NOT auto-resolved.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import utc_now_iso, write_json  # noqa: E402


def cohen_kappa(pairs: List[Tuple[Any, Any]]) -> Optional[float]:
    """Chance-corrected agreement. None when it is undefined (one category only)."""
    if not pairs:
        return None
    n = len(pairs)
    observed = sum(1 for a, b in pairs if a == b) / n
    left = Counter(a for a, _ in pairs)
    right = Counter(b for _, b in pairs)
    expected = sum((left[c] / n) * (right[c] / n) for c in set(left) | set(right))
    if expected >= 1.0:
        return None
    return (observed - expected) / (1 - expected)


def judgment_class(row: Dict[str, Any]) -> Optional[str]:
    """Collapse a judgment to the three-way construct: direct / indirect / none."""
    if row.get("direction") is None and row.get("directness") is None:
        return None
    if row.get("direction") == "none":
        return "no_evidence"
    return row.get("directness") or "no_evidence"


def load(path: Path) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["case_id"]] = row
    return out


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--judges", nargs="+", default=["A", "B"])
    parser.add_argument("--dir", default="benchmark/assessor/adjudication")
    parser.add_argument("--out", default="benchmark/assessor/adjudication/agreement.json")
    args = parser.parse_args(argv)

    base = Path(args.dir)
    answers = {j: load(base / "answers_judge_{}.jsonl".format(j)) for j in args.judges}
    completed = {j: {c: r for c, r in rows.items() if judgment_class(r) is not None}
                 for j, rows in answers.items()}

    for judge, rows in completed.items():
        print("judge {}: {} of {} case(s) judged".format(
            judge, len(rows), len(answers[judge])))
    if sum(len(r) for r in completed.values()) == 0:
        print("\nNo judgments recorded yet. Worksheets are in {}.".format(base))
        print("This script measures the adjudication; it does not perform it.")
        return 1

    report: Dict[str, Any] = {"generated_at": utc_now_iso(), "judges": args.judges,
                              "pairs": {}}
    resolved: Dict[str, Dict[str, Any]] = {}
    disagreements: List[Dict[str, Any]] = []

    for left, right in combinations(args.judges, 2):
        shared = sorted(set(completed[left]) & set(completed[right]))
        if not shared:
            continue
        three_way = [(judgment_class(completed[left][c]), judgment_class(completed[right][c]))
                     for c in shared]
        direction = [(completed[left][c].get("direction"), completed[right][c].get("direction"))
                     for c in shared]
        # The boundary: drop cases both judges called `direct`.
        boundary_cases = [c for c in shared
                          if not (judgment_class(completed[left][c]) == "direct"
                                  and judgment_class(completed[right][c]) == "direct")]
        boundary = [(judgment_class(completed[left][c]), judgment_class(completed[right][c]))
                    for c in boundary_cases]
        merely = [(completed[left][c].get("merely_related"),
                   completed[right][c].get("merely_related")) for c in shared]

        entry = {
            "n_shared": len(shared),
            "three_way_agreement": sum(1 for a, b in three_way if a == b) / len(three_way),
            "three_way_kappa": cohen_kappa(three_way),
            "direction_agreement": sum(1 for a, b in direction if a == b) / len(direction),
            "direction_kappa": cohen_kappa(direction),
            "n_boundary_cases": len(boundary),
            "boundary_agreement": (sum(1 for a, b in boundary if a == b) / len(boundary)
                                   if boundary else None),
            "boundary_kappa": cohen_kappa(boundary),
            "merely_related_agreement": (sum(1 for a, b in merely if a == b) / len(merely)
                                         if merely else None),
        }
        report["pairs"]["{}-{}".format(left, right)] = entry

        print("\n{} vs {} — {} shared case(s)".format(left, right, len(shared)))
        print("  three-way agreement      {:.3f}   kappa {}".format(
            entry["three_way_agreement"],
            "{:.3f}".format(entry["three_way_kappa"]) if entry["three_way_kappa"] is not None else "n/a"))
        print("  direction agreement      {:.3f}   kappa {}".format(
            entry["direction_agreement"],
            "{:.3f}".format(entry["direction_kappa"]) if entry["direction_kappa"] is not None else "n/a"))
        print("  * BOUNDARY agreement     {}   kappa {}   (n={})".format(
            "{:.3f}".format(entry["boundary_agreement"]) if entry["boundary_agreement"] is not None else "n/a",
            "{:.3f}".format(entry["boundary_kappa"]) if entry["boundary_kappa"] is not None else "n/a",
            entry["n_boundary_cases"]))
        print("    ^ indirect-vs-merely-related is the construct at risk; this is criterion 1")
        print("  merely_related agreement {}".format(
            "{:.3f}".format(entry["merely_related_agreement"])
            if entry["merely_related_agreement"] is not None else "n/a"))

        for case in shared:
            a, b = completed[left][case], completed[right][case]
            if judgment_class(a) == judgment_class(b) and a.get("direction") == b.get("direction"):
                resolved[case] = {
                    "case_id": case,
                    "direction": a.get("direction"),
                    "directness": a.get("directness"),
                    "strength": a.get("strength") or b.get("strength"),
                    "intermediate_fact": a.get("intermediate_fact") or b.get("intermediate_fact"),
                    "merely_related": bool(a.get("merely_related")),
                    "proposition_unassessable": bool(a.get("proposition_unassessable")
                                                     or b.get("proposition_unassessable")),
                    "resolved_by": "unanimous",
                }
            else:
                disagreements.append({
                    "case_id": case,
                    left: {k: a.get(k) for k in ("direction", "directness", "merely_related")},
                    right: {k: b.get(k) for k in ("direction", "directness", "merely_related")},
                })

    report["n_resolved_unanimous"] = len(resolved)
    report["n_disagreements"] = len(disagreements)
    report["disagreements"] = disagreements
    report["note"] = ("Disagreements are NOT auto-resolved. They go to a third pass against "
                      "docs/ASSESSOR_RUBRIC.md.")
    write_json(args.out, report)

    if resolved:
        out = Path(base) / "adjudicated.jsonl"
        with out.open("w", encoding="utf-8") as handle:
            for case in sorted(resolved):
                handle.write(json.dumps(resolved[case], sort_keys=True) + "\n")
        print("\n{} case(s) resolved unanimously -> {}".format(len(resolved), out))
    if disagreements:
        print("{} disagreement(s) need a third pass:".format(len(disagreements)))
        for row in disagreements[:10]:
            print("  {}".format(row["case_id"]))
    print("\nwrote {}".format(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
