"""Reproducibility report for the graph-edge judgments.

    python3 scripts/edge_validation_report.py

After DECISIONS #29 the edges carry all the scientific reasoning, so this is the
component that now most needs validating. Reports:

* **direction reproducibility** — implies / neutral / contradicts. This is the
  distinction that moves a ranking; an ordinal step between `implied` and
  `strongly_implied` does not.
* exact ordinal agreement, and agreement within one step on the scale.
* agreement of each judge with the **production** label already stored in the graph.
* the `mismatched` control: a proposition paired with a hypothesis from a different
  instance should be judged `neutral`. An edge judge that finds implications between
  unrelated claims is inventing the structure the method rests on.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.inference.parameters import EDGE_LABELS  # noqa: E402

ORDER = {label: i for i, label in enumerate(
    ["strongly_implied", "implied", "weakly_implied", "neutral",
     "unlikely", "strongly_contradicted"])}


def kappa(pairs):
    if not pairs:
        return None
    n = len(pairs)
    observed = sum(1 for a, b in pairs if a == b) / n
    left, right = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    expected = sum((left[c] / n) * (right[c] / n) for c in set(left) | set(right))
    return None if expected >= 1.0 else (observed - expected) / (1 - expected)


def _f(v, fmt="{:.3f}"):
    return fmt.format(v) if isinstance(v, (int, float)) else "n/a"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", default="benchmark/assessor/edge_validation.json")
    parser.add_argument("--out", default="benchmark/assessor/edge_validation_report.json")
    parser.add_argument("--md-out", default="benchmark/assessor/edge_validation_report.md")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.validation).read_text())
    rows = data["rows"]
    real = [r for r in rows if r["condition"] == "real"]
    mismatched = [r for r in rows if r["condition"] == "mismatched"]

    lines = ["# Edge-judgment validation", "",
             "The consequence graph's edges carry `P(X_v | H_i)` — the scientific "
             "implication. After DECISIONS #29 they carry *all* of it, so this is the "
             "component most in need of validation.", "",
             "Judge A is the production prompt; judge B is never shown the ordinal "
             "labels and is mapped onto them afterwards. Same single deployment, so the "
             "same-model caveat applies.", ""]
    report: Dict[str, Any] = {"generated_at": utc_now_iso(), "n_real": len(real),
                              "n_mismatched": len(mismatched)}

    if real:
        direction = [(r["a_direction"], r["b_direction"]) for r in real]
        exact = [(r["a_label"], r["b_label"]) for r in real]
        within1 = sum(1 for a, b in exact
                      if a in ORDER and b in ORDER and abs(ORDER[a] - ORDER[b]) <= 1)
        prod_a = [(r["production_label"], r["a_label"]) for r in real if r["production_label"]]
        prod_b = [(r["production_label"], r["b_label"]) for r in real if r["production_label"]]
        stats = {
            "direction_reproducibility": sum(1 for a, b in direction if a == b) / len(direction),
            "direction_kappa": kappa(direction),
            "exact_ordinal_agreement": sum(1 for a, b in exact if a == b) / len(exact),
            "within_one_step": within1 / len(exact),
            "judge_a_vs_production": (sum(1 for a, b in prod_a if a == b) / len(prod_a)
                                      if prod_a else None),
            "judge_b_vs_production": (sum(1 for a, b in prod_b if a == b) / len(prod_b)
                                      if prod_b else None),
        }
        report["real"] = stats
        lines += ["## Reproducibility on real edges (n={})".format(len(real)), "",
                  "| statistic | value |", "| --- | --- |",
                  "| **direction reproducibility** (implies/neutral/contradicts) | **{}** |".format(
                      _f(stats["direction_reproducibility"])),
                  "| direction kappa | {} |".format(_f(stats["direction_kappa"])),
                  "| exact ordinal agreement | {} |".format(_f(stats["exact_ordinal_agreement"])),
                  "| agreement within one ordinal step | {} |".format(_f(stats["within_one_step"])),
                  "| judge A vs the stored production label | {} |".format(
                      _f(stats["judge_a_vs_production"])),
                  "| judge B vs the stored production label | {} |".format(
                      _f(stats["judge_b_vs_production"])), "",
                  "Direction is the number that matters: an ordinal step between "
                  "`implied` and `strongly_implied` barely moves a ranking, whereas "
                  "`implies` against `neutral` does.", ""]

        dist = Counter(r["a_label"] for r in real)
        lines += ["Distribution of judge A's labels on real edges: " + ", ".join(
            "`{}` {}".format(k, v) for k, v in dist.most_common()), ""]

    # Stratified by abstraction level: v3 moves the scientific bridge into edges
    # from mechanistic and class-level nodes, so those edges are the ones that must
    # reproduce. Pooling would hide a problem confined to the abstracted half.
    levels = sorted({r.get("abstraction_level") for r in real if r.get("abstraction_level")})
    if levels:
        lines += ["## Reproducibility by abstraction level of the node", "",
                  "| level | edges | direction reproducibility | exact ordinal | neutral rate |",
                  "| --- | --- | --- | --- | --- |"]
        report["by_abstraction_level"] = {}
        for level in levels:
            sub = [r for r in real if r.get("abstraction_level") == level]
            dr = sum(1 for r in sub if r["a_direction"] == r["b_direction"]) / len(sub)
            ex = sum(1 for r in sub if r["a_label"] == r["b_label"]) / len(sub)
            nt = sum(1 for r in sub if r["a_direction"] == "neutral") / len(sub)
            lines.append("| `{}` | {} | {} | {} | {} |".format(
                level, len(sub), _f(dr), _f(ex), _f(nt)))
            report["by_abstraction_level"][level] = {
                "n": len(sub), "direction_reproducibility": dr,
                "exact_ordinal": ex, "neutral_rate": nt}
        lines += ["",
                  "A *higher* neutral rate at the abstracted levels would be the warning "
                  "sign: it would mean the abstraction went so far that the hypothesis no "
                  "longer implies the proposition, i.e. the node carries evidence but no "
                  "connection back to the claim. Lower direction reproducibility there "
                  "would mean the bridge is not one two readers agree on.", ""]

    if mismatched:
        neutral_a = sum(1 for r in mismatched if r["a_direction"] == "neutral")
        neutral_b = sum(1 for r in mismatched if r["b_direction"] == "neutral")
        report["mismatched"] = {
            "n": len(mismatched),
            "judge_a_neutral_rate": neutral_a / len(mismatched),
            "judge_b_neutral_rate": neutral_b / len(mismatched),
        }
        lines += ["## Control: a proposition paired with a hypothesis from another instance",
                  "", "These are unrelated claims. Both judges should answer `neutral`.", "",
                  "| judge | neutral rate |", "| --- | --- |",
                  "| A (production prompt) | **{}** |".format(_f(neutral_a / len(mismatched))),
                  "| B | **{}** |".format(_f(neutral_b / len(mismatched))), "",
                  "A low neutral rate here means the edge judge is inventing implications "
                  "between unrelated claims — and since the edges now carry all the "
                  "scientific reasoning, that failure would not show up anywhere in the "
                  "evidence numbers.", ""]

    Path(args.md_out).write_text("\n".join(lines) + "\n")
    write_json(args.out, report)
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
