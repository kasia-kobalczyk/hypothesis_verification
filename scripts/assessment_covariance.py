"""Is node-level evidence judgment correlated WITHIN a row?

    python3 scripts/assessment_covariance.py --repeats benchmark/holdout/repeat_assessment_dev20.json

Tests the one hypothesis left standing after the family ablation ruled out
proposition-structure dependence and driving-paper overlap was measured at 12-19%.

Each node has repeated labels under nuisance variation (record order only). Labels
are mapped to their ordinal log-likelihood-ratio so "more supportive" is a number,
and each node's deviation from its own mean is taken per repeat. If the assessor
drifts coherently across a row -- more supportive on X1 in the same repeat it is
more supportive on X2 -- then within-row pair covariance exceeds cross-row.

Cross-row pairs are the null: repeats are indexed identically across rows, so a
global "this repeat was generous" effect would raise BOTH, and only the excess is
evidence of row-specific dependence.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common.config import load_config  # noqa: E402
from src.inference.parameters import load_ordinal_mappings  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", required=True)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--max-cross-pairs", type=int, default=20000)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    maps = load_ordinal_mappings(load_config(args.config).ordinal_mappings_path)
    data = json.loads(Path(args.repeats).read_text())
    R = data["repeats"]

    # node -> deviation vector across repeats
    rows = {}
    unstable = total = 0
    for row in data["rows"]:
        vecs = {}
        for node, labels in row["labels"].items():
            # Keep nodes with >= 2 usable repeats rather than requiring all R. A
            # parse failure is likelier on nodes where the assessor is least
            # decisive, so dropping them entirely would bias the sample toward
            # stable nodes and understate instability. Deviations are computed over
            # whatever repeats exist, and pair covariance below uses only the repeat
            # indices two nodes share.
            usable = {i: l for i, l in enumerate(labels) if l is not None}
            if len(usable) < 2:
                continue
            total += 1
            if len(set(usable.values())) > 1:
                unstable += 1
            vals = {i: maps.evidence_value(l) for i, l in usable.items()}
            m = statistics.mean(vals.values())
            vecs[node] = {i: v - m for i, v in vals.items()}
        if len(vecs) >= 2:
            rows[row["instance"]] = vecs

    def cov(a, b):
        shared = sorted(set(a) & set(b))
        if len(shared) < 2:
            return None
        return sum(a[i] * b[i] for i in shared) / len(shared)

    within = [c for v in rows.values()
              for a, b in itertools.combinations(sorted(v), 2)
              if (c := cov(v[a], v[b])) is not None]
    flat = [(inst, n, vec) for inst, v in rows.items() for n, vec in v.items()]
    rng = random.Random(0)
    cross = []
    for _ in range(min(args.max_cross_pairs, len(flat) * 4)):
        x, y = rng.sample(flat, 2)
        if x[0] != y[0]:
            c = cov(x[2], y[2])
            if c is not None:
                cross.append(c)

    print("nodes with >=2 usable repeats: %d (of %d repeats requested)" % (total, R))
    print("node instability  P(labels differ across repeats) = %.3f (%d/%d)"
          % (unstable / max(total, 1), unstable, total))
    print()
    print("covariance of supportiveness deviations:")
    print("  WITHIN-row pairs  n=%-6d mean %+.4f  median %+.4f"
          % (len(within), statistics.mean(within) if within else 0,
             statistics.median(within) if within else 0))
    print("  CROSS-row pairs   n=%-6d mean %+.4f  median %+.4f   [the null]"
          % (len(cross), statistics.mean(cross) if cross else 0,
             statistics.median(cross) if cross else 0))
    if within and cross:
        excess = statistics.mean(within) - statistics.mean(cross)
        var = statistics.mean([c for _, _, v in flat if (c := cov(v, v)) is not None])
        print()
        print("  excess within-row covariance %+.4f  (per-node variance %.4f)" % (excess, var))
        print("  => intraclass-style ratio %.3f" % (excess / var if var else 0))
        print()
        if excess > 0.1 * var:
            print("  Within-row judgments CO-MOVE: direct evidence for evidence-channel")
            print("  dependence, which the family ablation could not have fixed.")
        else:
            print("  No material within-row co-movement. Assessor correlation is NOT")
            print("  demonstrated either; the fragility source remains unidentified.")
    if args.out:
        json.dump({"instability": unstable / max(total, 1),
                   "within_mean": statistics.mean(within) if within else None,
                   "cross_mean": statistics.mean(cross) if cross else None,
                   "n_within": len(within), "n_cross": len(cross)},
                  open(args.out, "w"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
