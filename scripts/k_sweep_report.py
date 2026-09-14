"""Report how verification quality and cost scale with the candidate-set size k.

    python3 scripts/k_sweep_report.py runs/consequence_graph_2026*_2e09d5ed runs/...

Reads saved artifacts only -- no API calls. Produces the two tables the protocol
asks for (`docs/EVALUATION_PROTOCOL.md`):

1. **Ranking, stratified by k**, each row beside its own chance baseline. Top-1, MRR
   and mean gold rank are NOT comparable across k; normalised gold rank and the
   pairwise win rate are, and are marked as such.
2. **Method scaling by k**: propositions, graph size, informative-evidence rate,
   retrieval yield, merges, cost. This is where k stops being a difficulty knob and
   becomes a property of the method.

When the runs come from the nested k-slices, rows present at every k are reported
separately as a *balanced panel*: within those rows nothing changes but the size of
the candidate set, so a difference there is attributable to k rather than to which
instances happened to be available.
"""

from __future__ import annotations

import argparse
import glob
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import write_json  # noqa: E402


def _load(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    with path.open() as handle:
        return json.load(handle)


def collect(run_dirs: List[Path]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for run_dir in run_dirs:
        per_instance = {}
        for record in (_load(run_dir / "metrics.json") or {}).get("instances", []):
            per_instance[record.get("instance_id")] = record
        # Per-instance cost from the run's own ledger, so it needs no repricing.
        cost_by_instance: Dict[str, float] = defaultdict(float)
        ledger = run_dir / "cost_ledger.jsonl"
        if ledger.exists():
            for line in ledger.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    call = json.loads(line)
                except ValueError:
                    continue
                key = call.get("instance_id")
                if key:
                    cost_by_instance[key] += float(call.get("cost_usd") or 0.0)
        for instance_dir in sorted((run_dir / "instances").glob("*")):
            if not instance_dir.is_dir():
                continue
            result = _load(instance_dir / "result.json")
            scores = _load(instance_dir / "scores.json")
            graph = _load(instance_dir / "graph.json")
            evidence = _load(instance_dir / "evidence.json")
            if not (result and scores and graph):
                continue
            diagnostics = result.get("diagnostics") or {}
            k = len(graph.get("hypothesis_ids") or [])
            row_id = (_load(instance_dir / "input.json") or {}).get(
                "researchbench_sample_id") or instance_dir.name.rsplit("-K", 1)[0]
            texts = [str(n.get("text", "")) for n in graph.get("nodes", [])]
            usage = result.get("usage") or {}
            instance_cost = cost_by_instance.get(instance_dir.name) or usage.get("cost_usd")
            rows.append({
                "run": run_dir.name,
                "instance": instance_dir.name,
                "row_id": row_id,
                "k": k,
                "metrics": per_instance.get(instance_dir.name, {}),
                "n_nodes": diagnostics.get("n_graph_nodes"),
                "n_edges": diagnostics.get("n_graph_edges"),
                "n_merged": diagnostics.get("n_merged_nodes"),
                "n_shared": diagnostics.get("n_shared_nodes"),
                "n_informative": diagnostics.get(
                    "n_informative_assessments", diagnostics.get("n_informative")),
                "n_queries": diagnostics.get("n_queries"),
                "n_eligible_papers": diagnostics.get("n_eligible_papers"),
                "median_proposition_tokens": (
                    statistics.median(len(t.split()) for t in texts) if texts else None),
                "cost_usd": instance_cost,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "gold_rank": (scores.get("ranking") or []).index(scores["gold_id"]) + 1
                if scores.get("gold_id") in (scores.get("ranking") or []) else None,
            })
    return rows


def _mean(values):
    kept = [v for v in values if v is not None]
    return sum(kept) / len(kept) if kept else None


def _f(value, fmt="%.3f"):
    return (fmt % value) if isinstance(value, (int, float)) else "-"


def tables(rows: List[Dict[str, Any]], *, restrict_rows=None) -> Dict[int, Dict[str, Any]]:
    by_k: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if restrict_rows is not None and row["row_id"] not in restrict_rows:
            continue
        by_k[row["k"]].append(row)

    out: Dict[int, Dict[str, Any]] = {}
    for k, group in sorted(by_k.items()):
        metrics = [g["metrics"] for g in group if g.get("metrics")]
        nodes = sum(g["n_nodes"] or 0 for g in group)
        informative = sum(g["n_informative"] or 0 for g in group)
        out[k] = {
            "n_instances": len(group),
            "chance_top1": 1.0 / k,
            "top1_tie_aware": _mean(m.get("top1_tie_aware") for m in metrics),
            "mrr": _mean(m.get("reciprocal_rank") for m in metrics),
            "mean_gold_rank": _mean(g["gold_rank"] for g in group),
            "gold_rank_normalised": _mean(m.get("gold_rank_normalised") for m in metrics),
            "pairwise_win_rate": _mean(
                m.get("pairwise_accuracy_all_negatives") for m in metrics),
            "pair_accuracy": _mean(m.get("pair_accuracy") for m in metrics),
            "mean_nodes": _mean(g["n_nodes"] for g in group),
            "mean_edges": _mean(g["n_edges"] for g in group),
            "informative_rate": (informative / nodes) if nodes else None,
            "mean_queries": _mean(g["n_queries"] for g in group),
            "mean_eligible_papers": _mean(g["n_eligible_papers"] for g in group),
            "mean_merges": _mean(g["n_merged"] for g in group),
            "total_shared": sum(g["n_shared"] or 0 for g in group),
            "median_proposition_words": _mean(g["median_proposition_tokens"] for g in group),
            "mean_cost_usd": _mean(g["cost_usd"] for g in group),
            "instances": [g["instance"] for g in group],
        }
    return out


def render(title: str, table: Dict[int, Dict[str, Any]]) -> List[str]:
    lines = ["### {}".format(title), ""]
    if not table:
        return lines + ["(no runs)", ""]
    lines += [
        "**Ranking** — top-1, MRR and mean gold rank are not comparable across k.",
        "",
        "| k | sets | chance top-1 | top-1 | MRR | mean gold rank | "
        "normalised gold rank † | pairwise win rate † |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for k, entry in sorted(table.items()):
        lines.append("| {} | {} | {} | {} | {} | {} | **{}** | **{}** |".format(
            k, entry["n_instances"], _f(entry["chance_top1"]), _f(entry["top1_tie_aware"]),
            _f(entry["mrr"]), _f(entry["mean_gold_rank"], "%.2f"),
            _f(entry["gold_rank_normalised"]), _f(entry["pairwise_win_rate"])))
    lines += [
        "",
        "† chance 0.5 for every k, so these are the two that may be pooled.",
        "",
        "**Method scaling** — how the verifier itself changes with k.",
        "",
        "| k | nodes | edges | median proposition words | informative evidence | "
        "queries | eligible papers | merges | shared | cost |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for k, entry in sorted(table.items()):
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            k, _f(entry["mean_nodes"], "%.0f"), _f(entry["mean_edges"], "%.0f"),
            _f(entry["median_proposition_words"], "%.0f"),
            _f(entry["informative_rate"]) if entry["informative_rate"] is None
            else "{:.0%}".format(entry["informative_rate"]),
            _f(entry["mean_queries"], "%.0f"), _f(entry["mean_eligible_papers"], "%.0f"),
            _f(entry["mean_merges"], "%.1f"), entry["total_shared"],
            "$" + _f(entry["mean_cost_usd"], "%.2f")))
    lines.append("")
    return lines


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+")
    parser.add_argument("--out", default="runs/k_sweep_report.md")
    parser.add_argument("--json-out", default="runs/k_sweep.json")
    args = parser.parse_args(argv)

    run_dirs: List[Path] = []
    for pattern in args.runs:
        run_dirs.extend(Path(p) for p in sorted(glob.glob(pattern)))
    rows = collect(run_dirs)
    if not rows:
        print("no instances found")
        return 1

    ks = sorted({r["k"] for r in rows})
    rows_by_k = defaultdict(set)
    for row in rows:
        rows_by_k[row["k"]].add(row["row_id"])
    balanced = set.intersection(*(rows_by_k[k] for k in ks)) if len(ks) > 1 else set()

    full = tables(rows)
    panel = tables(rows, restrict_rows=balanced) if balanced else {}

    lines = ["# k sweep — verification quality and cost against candidate-set size", ""]
    lines += ["Generated from saved artifacts; no API calls. k values: {}.".format(
        ", ".join(str(k) for k in ks)), ""]
    lines += render("All runs", full)
    if panel:
        lines += [
            "### Balanced panel — {} row(s) present at every k".format(len(balanced)), "",
            "Within these rows the candidates are nested, so nothing changes but the size "
            "of the candidate set. Differences here are attributable to k; differences in "
            "the table above may also reflect which instances were available at each k.",
            "",
        ]
        lines += render("Balanced panel", panel)[1:]
    Path(args.out).write_text("\n".join(lines) + "\n")
    write_json(args.json_out, {"k_values": ks, "all_runs": full, "balanced_panel": panel,
                               "balanced_panel_rows": sorted(balanced), "instances": rows})
    print("\n".join(lines))
    print("wrote {} and {}".format(args.out, args.json_out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
