"""Freeze a held-out pool and split it into calibration and test, before any run.

    python3 scripts/build_holdout_split.py --n 40

"Held out" here means: **no pair from this source row has ever been run end-to-end,
and no artifact from it fed the assessor work.** Row-level, not pair-level, because
two pairs from one row share a gold hypothesis and a literature neighbourhood.

The split is written once and refuses to be rewritten. Calibration fits the ordinal
mappings; test is reported. Nothing reported may come from the calibration half.

**This does not make the slice a valid benchmark.** v2 remains a development set on
which a question-hidden judge scores 0.910 from candidate text alone. Holding cases
out fixes "tuned on those five instances"; it does not fix the style artifact. Only
relative comparisons between arms, and method-scaling quantities, are interpretable
here.
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import stable_hash, utc_now_iso, write_json  # noqa: E402


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", default="benchmark/v2/researchbench_v2_pairs.jsonl")
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--calibration-share", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=20260912)
    parser.add_argument("--out", default="benchmark/holdout/split.json")
    args = parser.parse_args(argv)

    out = Path(args.out)
    if out.exists():
        print("refusing to overwrite {} -- the split is frozen".format(out))
        return 1

    touched = {Path(d).name for d in glob.glob("runs/consequence_graph_*/instances/*/")}
    pairs = [json.loads(line) for line in Path(args.pairs).read_text().splitlines()
             if line.strip()]
    contaminated_rows = {p["doi"] for p in pairs if p["pair_id"] in touched}
    clean = [p for p in pairs if p["doi"] not in contaminated_rows]

    # One pair per source row, so the split has no within-row duplication, then a
    # deterministic seeded order.
    by_row = {}
    for pair in sorted(clean, key=lambda p: p["pair_id"]):
        by_row.setdefault(p_doi := pair["doi"], pair)
    candidates = sorted(by_row.values(), key=lambda p: stable_hash(
        "{}:{}".format(args.seed, p["pair_id"])))
    chosen = candidates[: args.n]
    if len(chosen) < args.n:
        print("only {} clean row(s) available; taking all of them".format(len(chosen)))

    n_cal = int(round(len(chosen) * args.calibration_share))
    calibration = [p["pair_id"] for p in chosen[:n_cal]]
    test = [p["pair_id"] for p in chosen[n_cal:]]

    write_json(out, {
        "frozen_at": utc_now_iso(),
        "seed": args.seed,
        "source": args.pairs,
        "definition_of_held_out": (
            "no pair from this source row has been run end-to-end, and no artifact from "
            "it fed the assessor validation work"
        ),
        "n_pairs_in_slice": len(pairs),
        "n_rows_contaminated": len(contaminated_rows),
        "n_clean_rows": len(by_row),
        "one_pair_per_row": True,
        "calibration_ids": calibration,
        "test_ids": test,
        "n_calibration": len(calibration),
        "n_test": len(test),
        "rules": [
            "the ordinal mappings are fitted on `calibration_ids` only",
            "every reported number comes from `test_ids` only",
            "neither list may be re-drawn after a run; this file refuses to be rewritten",
        ],
        "benchmark_caveat": (
            "v2 is a DEVELOPMENT set: a question-hidden judge recovers 0.910 of pair "
            "labels from candidate text alone. Holding rows out removes the "
            "tuned-on-these-cases problem, not the style artifact. Absolute pair accuracy "
            "here is not evidence of verification ability; arm-to-arm differences and "
            "method-scaling quantities are."
        ),
    })
    print("froze {} calibration + {} test pair(s) -> {}".format(
        len(calibration), len(test), out))
    print("  calibration:", " ".join(calibration[:6]), "...")
    print("  test       :", " ".join(test[:6]), "...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
