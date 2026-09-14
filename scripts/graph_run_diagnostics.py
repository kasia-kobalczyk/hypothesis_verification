"""Aggregate consequence-graph debug runs into a single diagnostics table.

    python3 scripts/graph_run_diagnostics.py runs/consequence_graph_*/

Reads only saved artifacts -- no API calls, no LLM calls -- so it can be re-run
on any historical run directory. Reports, per instance and pooled:

  * graph shape (nodes, edges, depth, merges)
  * assessment yield (how many propositions produced informative evidence)
  * retrieval substrate (papers shown, how many carried an abstract)
  * the evidence-label distribution

Assessment yield is the number that matters for Milestone 2: a proposition whose
evidence is `no_evidence` contributes exactly zero to every candidate, so yield
bounds how much of the graph can influence the ranking at all.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import math
import re
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _load(base: Path, name: str) -> Optional[dict]:
    path = base / name
    if not path.exists():
        return None
    with path.open() as handle:
        return json.load(handle)


def node_rows(instance_dir: Path) -> List[Dict[str, object]]:
    graph = _load(instance_dir, "graph.json")
    evidence = _load(instance_dir, "evidence.json")
    retrieval = _load(instance_dir, "retrieval.json")
    if not graph or not evidence:
        return []
    depth = {n["id"]: n.get("depth") for n in graph.get("nodes", [])}
    by_node = evidence.get("by_node", {})
    shown = (retrieval or {}).get("by_node", {})
    rows = []
    for node_id, record in by_node.items():
        papers = shown.get(node_id, {}).get("papers_shown", [])
        with_abstract = sum(
            1 for p in papers if p.get("abstract") and str(p["abstract"]).strip()
        )
        row = {
            "instance": instance_dir.name,
            "node": node_id,
            "depth": depth.get(node_id),
            "n_shown": len(papers),
            "n_with_abstract": with_abstract,
            "label": record.get("assessment", {}).get("evidence_label"),
        }
        row.update(atomicity(str(record.get("text", ""))))
        rows.append(row)
    return rows


CONJUNCTION_MARKERS = (
    " and ", " as well as ", " together with ", " while also ", " while ",
    " whereas ", " but not ", " in addition to ", "; ",
)


def atomicity(text: str) -> Dict[str, int]:
    """Crude, deterministic proxies for how conjunctive a proposition is.

    Not linguistics -- just a stable count that can be compared between two
    generation prompts on the same instances. `n_tokens` uses the v2 slice
    tokenizer so proposition length is measured the same way candidate length is.
    """
    lowered = " " + text.lower() + " "
    return {
        "n_tokens": len(re.findall(r"\w+|[^\w\s]", text)),
        "n_clause_markers": sum(lowered.count(m) for m in CONJUNCTION_MARKERS),
        "n_commas": text.count(","),
    }


def cross_hypothesis_similarity(nodes_by_origin: Dict[str, List[str]]) -> Dict[str, float]:
    """Max/p95/median lexical similarity between propositions of DIFFERENT origins.

    This is the number that decides whether node merging could ever fire. It is
    computed with the same `text_similarity` the merger uses, so a threshold can be
    compared against it directly.
    """
    from src.graph.merge import text_similarity

    origins = sorted(nodes_by_origin)
    scores: List[float] = []
    for i, left in enumerate(origins):
        for right in origins[i + 1:]:
            for a in nodes_by_origin[left]:
                for b in nodes_by_origin[right]:
                    scores.append(text_similarity(a, b))
    if not scores:
        return {}
    scores.sort()
    return {
        "n_pairs": len(scores),
        "max": round(scores[-1], 3),
        "p95": round(scores[int(0.95 * (len(scores) - 1))], 3),
        "median": round(scores[len(scores) // 2], 3),
    }


def posterior_concentration(instance_dir: Path) -> Dict[str, object]:
    """How peaked the posterior is, and where gold sits in it.

    A graph whose propositions all came back `no_evidence` produces a flat
    posterior, so `spread` and `entropy_ratio` say directly how much the evidence
    moved anything. `entropy_ratio` is 1.0 for a uniform posterior over k
    candidates and falls towards 0 as it concentrates.
    """
    scores_file = _load(instance_dir, "scores.json")
    if not scores_file:
        return {}
    scores = scores_file.get("scores") or {}
    if not scores:
        return {}
    values = sorted(scores.values(), reverse=True)
    total = sum(values) or 1.0
    probs = [v / total for v in values]
    entropy = -sum(p * math.log(p) for p in probs if p > 0)
    k = len(values)
    ranking = scores_file.get("ranking") or []
    gold = scores_file.get("gold_id")
    return {
        "k": k,
        "top_score": round(values[0], 4),
        "spread": round(values[0] - values[-1], 4),
        "top1_minus_top2": round(values[0] - values[1], 4) if k > 1 else None,
        "entropy_ratio": round(entropy / math.log(k), 4) if k > 1 else None,
        "gold_rank": (ranking.index(gold) + 1) if gold in ranking else None,
    }


def summarise(rows: List[Dict[str, object]]) -> Dict[str, object]:
    if not rows:
        return {"n_nodes": 0}
    informative = [r for r in rows if r["label"] not in (None, "no_evidence")]
    return {
        "n_nodes": len(rows),
        "n_informative": len(informative),
        "informative_rate": round(len(informative) / len(rows), 3),
        "median_proposition_tokens": statistics.median(r["n_tokens"] for r in rows),
        "mean_clause_markers": round(statistics.mean(r["n_clause_markers"] for r in rows), 2),
        "mean_commas": round(statistics.mean(r["n_commas"] for r in rows), 2),
        "mean_papers_shown": round(statistics.mean(r["n_shown"] for r in rows), 1),
        "mean_with_abstract": round(statistics.mean(r["n_with_abstract"] for r in rows), 1),
        "abstract_coverage": round(
            sum(r["n_with_abstract"] for r in rows) / max(sum(r["n_shown"] for r in rows), 1), 3
        ),
        "labels": dict(collections.Counter(r["label"] for r in rows)),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", help="run directories (globs are expanded)")
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args(argv)

    run_dirs: List[Path] = []
    for pattern in args.runs:
        run_dirs.extend(Path(p) for p in sorted(glob.glob(pattern)))
    all_rows: List[Dict[str, object]] = []
    per_instance = []

    print("%-10s %-16s %3s %5s %5s %6s %6s %6s %6s %7s %6s" % (
        "run", "instance", "k", "nodes", "inf%", "tok", "clause", "merge", "xsim",
        "entropy", "gold"))
    for run_dir in run_dirs:
        for instance_dir in sorted((run_dir / "instances").glob("*")):
            if not instance_dir.is_dir():
                continue
            rows = node_rows(instance_dir)
            if not rows:
                continue
            graph = _load(instance_dir, "graph.json") or {}
            k = len(graph.get("hypothesis_ids", []))
            stats = graph.get("stats", {})
            by_origin: Dict[str, List[str]] = {}
            for node in graph.get("nodes", []):
                origin = node.get("generation_origin_hypothesis") or "?"
                by_origin.setdefault(origin, []).append(str(node.get("text", "")))
            summary = summarise(rows)
            similarity = cross_hypothesis_similarity(by_origin)
            concentration = posterior_concentration(instance_dir)
            summary.update({
                "run": run_dir.name,
                "instance": instance_dir.name,
                "n_candidates": k,
                "generate_prompt": ((_load(instance_dir, "edge_judgments.json") or {})
                                    .get("prompt_versions", {}).get("generate", {}).get("name")),
                "n_merges": (((_load(instance_dir, "edge_judgments.json") or {})
                              .get("merge") or {}).get("n_merges")),
                "graph_stats": stats,
                "n_merged": stats.get("n_merged"),
                "n_shared": stats.get("n_shared"),
                "cross_hypothesis_similarity": similarity,
                "posterior": concentration,
            })
            per_instance.append(summary)
            all_rows.extend(rows)
            print("%-10s %-16s %3d %5d %4.0f%% %6.0f %6.2f %6s %6s %7s %6s" % (
                run_dir.name[-8:], instance_dir.name, k, summary["n_nodes"],
                100 * summary["informative_rate"],
                summary["median_proposition_tokens"], summary["mean_clause_markers"],
                summary.get("n_merges", stats.get("n_merged", "-")), similarity.get("max", "-"),
                concentration.get("entropy_ratio", "-"), concentration.get("gold_rank", "-")))

    pooled = summarise(all_rows)
    print("\npooled: %s" % json.dumps(pooled, sort_keys=True))

    # The two cuts that actually separated the debug runs.
    def cut(name, predicate):
        subset = [r for r in all_rows if predicate(r)]
        if not subset:
            return
        s = summarise(subset)
        print("  %-24s n=%-4d informative=%.0f%%  abstracts=%.1f/10" % (
            name, s["n_nodes"], 100 * s["informative_rate"], s["mean_with_abstract"]))

    # The A/B that matters: same instances, same node budget, different
    # generation prompt. Grouped by prompt so one command answers it.
    prompt_of = {}
    for summary in per_instance:
        prompt_of[(summary["run"], summary["instance"])] = summary.get("generate_prompt")
    prompts_seen = sorted({v for v in prompt_of.values() if v})
    if len(prompts_seen) > 1:
        print("\nby generation prompt:")
        for name in prompts_seen:
            subset = [s for s in per_instance if s.get("generate_prompt") == name]
            nodes = sum(s["n_nodes"] for s in subset)
            inf = sum(s["n_informative"] for s in subset)
            merged = sum(s.get("n_merges") or s.get("n_merged") or 0 for s in subset)
            xsims = [s["cross_hypothesis_similarity"].get("max")
                     for s in subset if s.get("cross_hypothesis_similarity")]
            entropies = [s["posterior"].get("entropy_ratio")
                         for s in subset if (s.get("posterior") or {}).get("entropy_ratio")]
            toks = [s["median_proposition_tokens"] for s in subset]
            clauses = [s["mean_clause_markers"] for s in subset]
            print("  %-26s instances=%-2d nodes=%-4d informative=%4.0f%%  "
                  "median_tok=%4.0f  clause_markers=%.2f  merges=%d  "
                  "max_xsim=%s  mean_entropy=%s" % (
                      name, len(subset), nodes, 100 * inf / max(nodes, 1),
                      statistics.median(toks), statistics.mean(clauses), merged,
                      ("%.3f" % max(xsims)) if xsims else "-",
                      ("%.3f" % statistics.mean(entropies)) if entropies else "-"))

    k_by_instance = {s["instance"]: s["n_candidates"] for s in per_instance}
    print("\nby candidate count:")
    for k in sorted({v for v in k_by_instance.values()}):
        cut("k=%d" % k, lambda r, k=k: k_by_instance.get(r["instance"]) == k)
    print("by depth:")
    for d in sorted({r["depth"] for r in all_rows if r["depth"] is not None}):
        cut("depth=%d" % d, lambda r, d=d: r["depth"] == d)
    print("by abstract availability:")
    cut(">=8 of 10 abstracts", lambda r: r["n_with_abstract"] >= 8)
    cut("<=4 of 10 abstracts", lambda r: r["n_with_abstract"] <= 4)

    if args.json_out:
        payload = {"pooled": pooled, "per_instance": per_instance, "nodes": all_rows}
        Path(args.json_out).write_text(json.dumps(payload, indent=2, sort_keys=True))
        print("\nwrote %s" % args.json_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
