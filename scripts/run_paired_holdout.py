"""Row-paired held-out comparison: both arms on each row, back to back, order randomised.

    python3 scripts/run_paired_holdout.py --split benchmark/holdout/split.json

Why not simply run arm A over all rows and then arm B: Semantic Scholar's throughput
varies over the course of a long job — rate limiting worsened from 5 to 20 minutes
per instance within a single run earlier today. An arm-sequential design lets that
drift load onto the arm comparison, so a retrieval difference becomes indistinguishable
from a method difference.

So: for each test row, both arms run adjacent in time, and **which arm goes first is
randomised per row** from a recorded seed, so any residual first/second-position
effect is balanced across arms rather than aligned with one.

Every query, returned paper set, rate-limit event and timestamp is already written to
each run's `events.jsonl` and `retrieval.json`; this script additionally records the
per-row arm order and wall-clock boundaries so the pairing can be audited afterwards.
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import stable_hash, utc_now_iso, write_json  # noqa: E402

ARMS = {
    "narrow": "evidence_assess_v2",
    "broad": "evidence_assess_v1",
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", default="benchmark/holdout/split.json")
    parser.add_argument("--which", default="test", choices=["test", "calibration"])
    parser.add_argument("--seed", type=int, default=20260912)
    parser.add_argument("--max-nodes", type=int, default=20)
    parser.add_argument("--out", default="benchmark/holdout/paired_run_log.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    split = json.loads(Path(args.split).read_text())
    ids = split["{}_ids".format(args.which)]
    out_path = Path(args.out)
    log: Dict[str, Any] = {
        "started_at": utc_now_iso(), "split": args.split, "which": args.which,
        "seed": args.seed, "arms": ARMS, "rows": [],
        "design": ("both arms adjacent in time per row; arm order randomised per row "
                   "from the seed, so retrieval drift cannot align with one arm"),
    }
    if out_path.exists() and not args.dry_run:
        print("refusing to overwrite {}".format(out_path))
        return 1

    for index, pair_id in enumerate(ids, start=1):
        rng = random.Random(int(stable_hash("{}:{}".format(args.seed, pair_id)), 16))
        order = list(ARMS)
        rng.shuffle(order)
        row: Dict[str, Any] = {"pair_id": pair_id, "arm_order": order, "runs": {}}
        print("[{}/{}] {}  order={}".format(index, len(ids), pair_id, " -> ".join(order)))
        for arm in order:
            cmd = [
                sys.executable, "-m", "src.experiments.run",
                "--method", "consequence_graph", "--pairs",
                "--instances", pair_id,
                "--set", "graph.max_nodes={}".format(args.max_nodes),
                "--set", "evidence.assess_prompt={}".format(ARMS[arm]),
                "--label", "HELD-OUT {} row-paired, arm={}".format(args.which, arm),
            ]
            if args.dry_run:
                print("    would run:", " ".join(cmd[-6:]))
                continue
            started = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True)
            elapsed = time.time() - started
            run_id = None
            for line in (result.stderr or "").splitlines() + (result.stdout or "").splitlines():
                if "run consequence_graph_" in line:
                    run_id = line.split("run ", 1)[1].split(":")[0].strip()
                    break
            row["runs"][arm] = {
                "run_id": run_id, "returncode": result.returncode,
                "seconds": round(elapsed, 1), "finished_at": utc_now_iso(),
                "rate_limit_events": (result.stderr or "").count("429"),
            }
            print("    {:<7} {:>6.0f}s  429s={}  rc={}".format(
                arm, elapsed, row["runs"][arm]["rate_limit_events"], result.returncode))
        log["rows"].append(row)
        if not args.dry_run:
            log["updated_at"] = utc_now_iso()
            write_json(out_path, log)

    log["finished_at"] = utc_now_iso()
    if not args.dry_run:
        write_json(out_path, log)
    print("\nwrote {}".format(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
