"""What actually drove each pilot ranking (BENCH-GRAPH-PILOT-001, Step 8 q5).

Decomposes each case's score exactly. With a uniform prior the log-odds between the
two hypotheses is the sum of per-node contributions in `scores.json`, so grouping
nodes by what the Step-6 audit found about them partitions the ranking with no
residual and no model call.

Groups (mutually exclusive, first match wins):
  genuine_discriminator     auditor: the hypotheses make different, non-silent predictions
  manufactured_opposition   one hypothesis silent, verifier gave opposite-signed edges
  silence_read_one_way      one hypothesis silent, given a directional edge, same sign
  one_sided_neutral_ok      one hypothesis silent, correctly labelled `neutral`
  both_predict_same         neither silent, same predicted status

Also tests which hypothesis manufactured opposition favours. The expectation being
checked -- not assumed -- is that it favours the hypothesis that generated the
proposition, because the literature mostly returns support.

Requires recovery.json produced (or re-summarised) with the current reconcile().

Usage:
    python scripts/analyze_pilot_attribution.py --run runs/pilot_explanatory_001
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import resolve_path, write_json


def node_group(row: Dict[str, Any]) -> str:
    rec = row["reconciliation"]
    if row["judge"]["is_discriminative"]:
        return "genuine_discriminator"
    if rec["manufactured_opposition"]:
        return "manufactured_opposition"
    if rec["silence_inflation"]:
        return "silence_read_one_way"
    if rec["one_sided_proposition"]:
        return "one_sided_neutral_ok"
    return "both_predict_same"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    run_dir = resolve_path(args.run)

    recovery = json.loads((run_dir / "recovery.json").read_text(encoding="utf-8"))
    sample_row = recovery["cases"][0]["propositions"][0]["reconciliation"]
    if "manufactured_opposition" not in sample_row:
        print("recovery.json predates the revised reconcile(); run "
              "analyze_pilot_recovery.py --resummarise first")
        return 2

    out: Dict[str, Any] = {}
    mech = {"n_manufactured": 0, "n_moving": 0, "n_toward_origin": 0, "n_toward_other": 0,
            "logodds_toward_origin": 0.0, "logodds_toward_other": 0.0,
            "evidence_labels": collections.Counter()}

    for case in recovery["cases"]:
        case_id = case["case_id"]
        scores = json.loads((run_dir / "instances" / case_id / "scores.json").read_text(encoding="utf-8"))
        top = scores["ranking"][0]
        groups = {row["node_id"]: node_group(row) for row in case["propositions"]}

        by_group: Dict[str, float] = collections.defaultdict(float)
        per_node: Dict[str, Dict[str, Dict[str, Any]]] = collections.defaultdict(dict)
        for item in scores["contributions"]:
            sign = 1.0 if item["hypothesis_id"] == top else -1.0
            by_group[groups[item["node_id"]]] += sign * item["contribution"]
            per_node[item["node_id"]][item["hypothesis_id"]] = item

        out[case_id] = {
            "top": top,
            "total_logodds_toward_top": sum(by_group.values()),
            "by_group": dict(by_group),
            "n_nodes_by_group": dict(collections.Counter(groups.values())),
        }

        for row in case["propositions"]:
            if groups[row["node_id"]] != "manufactured_opposition":
                continue
            mech["n_manufactured"] += 1
            origin = row["generation_origin_hypothesis"]
            entries = per_node[row["node_id"]]
            other = next(h for h in entries if h != origin)
            mech["evidence_labels"][entries[origin]["evidence_label"]] += 1
            delta = entries[origin]["contribution"] - entries[other]["contribution"]
            if delta > 0:
                mech["n_moving"] += 1
                mech["n_toward_origin"] += 1
                mech["logodds_toward_origin"] += delta
            elif delta < 0:
                mech["n_moving"] += 1
                mech["n_toward_other"] += 1
                mech["logodds_toward_other"] += -delta

    mech["evidence_labels"] = dict(mech["evidence_labels"])
    out["_manufactured_mechanism"] = mech
    write_json(run_dir / "ranking_attribution.json", out)
    print(json.dumps(mech, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
