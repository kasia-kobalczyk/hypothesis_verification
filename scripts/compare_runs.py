"""Compare methods over a common set of instances.

    python scripts/compare_runs.py                          # every run, latest per method
    python scripts/compare_runs.py --instances RBV-01 RBV-02
    python scripts/compare_runs.py --runs runs/direct_rag_2026... runs/direct_judge_2026...

Metrics are recomputed from the per-instance rows in `metrics.json`, restricted
to the instances every selected run has in common — comparing a 5-instance run
against a 20-instance run on their headline numbers would be meaningless.

The primary metric is pair accuracy over the frozen R2 subset; listwise numbers
are shown as secondary. Runs are labelled with their config so a style baseline
is never mistaken for a method.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml  # noqa: E402

from src.common.io import read_json, repo_root  # noqa: E402


def load_run(path: Path) -> Optional[Dict[str, Any]]:
    summary_path, metrics_path = path / "summary.json", path / "metrics.json"
    if not summary_path.exists() or not metrics_path.exists():
        return None
    summary = read_json(summary_path)
    rows = {r["instance_id"]: r for r in read_json(metrics_path)["instances"]}
    name = summary.get("method", "?")
    config_path = path / "config.yaml"
    if name == "style_artifact" and config_path.exists():
        with config_path.open("r", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh)
        name = "style_artifact ({} first)".format(cfg["baselines"]["style_artifact"]["prefer"])
    return {
        "run_id": summary.get("run_id"),
        "path": path,
        "method": summary.get("method"),
        "name": name,
        "label": summary.get("label"),
        "finished_at": summary.get("finished_at"),
        "cost": (summary.get("cost") or {}).get("cost_usd"),
        "rows": rows,
    }


def restrict(run: Dict[str, Any], instances: List[str]) -> Dict[str, Any]:
    """Recompute the aggregate over exactly `instances`."""
    rows = [run["rows"][i] for i in instances if i in run["rows"]]
    scored = [r for r in rows if r.get("scored")]
    pairs = [r for r in scored if r.get("pair_accuracy") is not None]
    n_pairs = sum(int(r.get("n_pairs_scored") or 0) for r in pairs)
    credit = sum(float(r.get("pair_credit") or 0.0) for r in pairs)
    mean = lambda key: (
        sum(float(r[key]) for r in scored if r.get(key) is not None)
        / max(1, len([r for r in scored if r.get(key) is not None]))
        if scored else None
    )
    return {
        "pair_accuracy": (credit / n_pairs) if n_pairs else None,
        "n_pairs": n_pairs,
        "n_scored": len(scored),
        "n_instances": len(rows),
        "top1": mean("top1_strict"),
        "mrr": mean("reciprocal_rank"),
        "gold_rank": mean("gold_rank"),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Compare methods on a common instance set.")
    parser.add_argument("--runs", nargs="*", default=None, help="explicit run directories")
    parser.add_argument("--instances", nargs="*", default=None, help="restrict to these instances")
    parser.add_argument("--root", default="runs")
    args = parser.parse_args(argv)

    root = repo_root() / args.root
    paths = [Path(p) for p in args.runs] if args.runs else sorted(root.glob("*/"))
    runs = [r for r in (load_run(p) for p in paths) if r]
    if not runs:
        print("no runs found under {}".format(root))
        return 1

    # Latest run per method name, unless the caller named runs explicitly.
    if not args.runs:
        latest: Dict[str, Dict[str, Any]] = {}
        for run in sorted(runs, key=lambda r: r["finished_at"] or ""):
            latest[run["name"]] = run
        runs = list(latest.values())

    common = set.intersection(*[set(r["rows"]) for r in runs]) if runs else set()
    instances = sorted(set(args.instances) & common) if args.instances else sorted(common)
    if not instances:
        print("no instances in common across the selected runs")
        return 1

    print("\ncommon instances ({}): {}".format(len(instances), ", ".join(instances)))
    print("primary = pair accuracy over the frozen R2 subset; ties score 0.5\n")
    header = "{:<30} {:>9} {:>7} {:>7} {:>7} {:>8} {:>9}"
    print(header.format("method", "pair_acc", "pairs", "top1", "mrr", "goldrank", "cost"))
    print("-" * 82)
    for run in sorted(runs, key=lambda r: -(restrict(r, instances)["pair_accuracy"] or -1)):
        m = restrict(run, instances)
        fmt = lambda v, d=3: "-" if v is None else "{:.{}f}".format(v, d)
        print(header.format(
            run["name"][:30], fmt(m["pair_accuracy"]), m["n_pairs"],
            fmt(m["top1"], 2), fmt(m["mrr"], 2), fmt(m["gold_rank"], 1),
            "-" if run["cost"] is None else "${:.2f}".format(run["cost"]),
        ))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
