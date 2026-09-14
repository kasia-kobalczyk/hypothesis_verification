"""Freeze the empirical judgment-noise models used for ranking-stability analysis.

    python3 scripts/freeze_noise_model.py

Two channels, both estimated from DEVELOPMENT data only and then fixed:

  evidence  an empirical label-transition matrix P(alternative | observed),
            measured by re-running the frozen assessor on saved node/paper bundles
            while varying only record presentation order -- a nuisance factor that
            must not change a scientific answer.

  edge      direction-preserving adjacent-label nudges applied at the rate the two
            independent edge judges actually disagreed at, per abstraction level.

These describe sensitivity to MODEL-JUDGMENT VARIATION. They are not a posterior
over scientific truth, and nothing derived from them should be called one.

Refuses to overwrite: a noise model re-estimated after seeing a result is not frozen.
"""
from __future__ import annotations

import argparse, collections, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common.io import utc_now_iso, write_json  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repeats", default="benchmark/holdout/repeat_assessment_dev20.json")
    ap.add_argument("--out", default="benchmark/frozen/noise_model_v1.json")
    args = ap.parse_args(argv)

    out = Path(args.out)
    if out.exists():
        print("refusing to overwrite {} -- a re-estimated noise model is not frozen".format(out))
        return 1

    data = json.loads(Path(args.repeats).read_text())
    trans = collections.defaultdict(collections.Counter)
    n_nodes = n_unstable = 0
    for row in data["rows"]:
        for node, labels in row["labels"].items():
            usable = [l for l in labels if l]
            if len(usable) < 2:
                continue
            observed = row["original"].get(node)
            if not observed:
                continue
            n_nodes += 1
            if len(set(usable)) > 1:
                n_unstable += 1
            for l in usable:
                trans[observed][l] += 1

    matrix = {}
    for observed, counts in trans.items():
        total = sum(counts.values())
        matrix[observed] = {k: round(v / total, 4) for k, v in sorted(counts.items())}

    write_json(out, {
        "name": "noise_model_v1",
        "frozen_at": utc_now_iso(),
        "estimated_from": args.repeats,
        "estimated_from_rows": len(data["rows"]),
        "n_nodes": n_nodes,
        "node_instability": round(n_unstable / max(n_nodes, 1), 4),
        "evidence_transition_matrix": matrix,
        "evidence_nuisance_varied": data.get("nuisance_varied"),
        "edge_disagreement_by_level": {
            "specific": 0.406, "mechanistic": 0.516, "class": 0.630, "unknown": 0.5},
        "edge_perturbation": ("adjacent ordinal label, direction preserved (an implied "
                              "edge never becomes contradicting)"),
        "edge_source": ("1 - exact-ordinal agreement between edge_assess_v1 and "
                        "edge_judge_b_v1, measured per abstraction level"),
        "interpretation": ("sensitivity to model-judgment variation. NOT a calibrated "
                           "posterior over scientific truth; results derived from it are "
                           "'ranking stability', never 'posterior probability'."),
        "estimated_from_reserve": False,
    })
    print("froze {}".format(out))
    print("  nodes {} | node instability {:.3f}".format(n_nodes, n_unstable / max(n_nodes, 1)))
    print("  observed labels with a transition row: {}".format(len(matrix)))
    for k in sorted(matrix):
        stay = matrix[k].get(k, 0.0)
        print("    {:<22} stays put {:.2f}".format(k, stay))
    return 0


if __name__ == "__main__":
    sys.exit(main())
