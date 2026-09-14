"""Re-assess saved graph nodes with a different evidence prompt, then re-propagate.

    python3 scripts/reassess_nodes.py --run runs/consequence_graph_..._be139301 \
        --assess-prompt evidence_assess_v2

The controlled version of "does the narrow assessor still support ranking": the
graph, the nodes, the edges and the retrieved papers are all taken from a completed
run and held fixed. Only the evidence prompt changes, so the comparison is not
confounded by generation or retrieval varying between arms.

Retrieval is NOT re-run and the network is not touched for literature: the records
shown to the assessor are exactly the ones the original run showed, replayed from
`retrieval.json`. Temporal eligibility was enforced when they were first retrieved.

Outputs a side-by-side of node-level yield, posterior separation and pair ranking.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode  # noqa: E402
from src.experiments.metrics import ranking_from_scores  # noqa: E402
from src.inference.bayes import discriminativeness, score_hypotheses  # noqa: E402
from src.inference.parameters import EVIDENCE_LABELS, load_ordinal_mappings  # noqa: E402
from src.inference.parameters import normalise_evidence_label  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.reassess")


def rebuild_graph(saved: Dict[str, Any]) -> ConsequenceGraph:
    graph = ConsequenceGraph(instance_id=saved["instance_id"],
                             hypothesis_ids=list(saved["hypothesis_ids"]))
    node_fields = set(PropositionNode.model_fields)
    edge_fields = set(GraphEdge.model_fields)
    for node in saved["nodes"]:
        graph.add_node(PropositionNode(**{k: v for k, v in node.items() if k in node_fields}))
    for edge in saved["edges"]:
        graph.add_edge(GraphEdge(**{k: v for k, v in edge.items() if k in edge_fields}))
    return graph.freeze()


def render_literature(papers: List[Dict[str, Any]], max_papers: int) -> str:
    blocks = []
    for paper in papers[:max_papers]:
        if not (paper.get("abstract") or "").strip():
            continue
        blocks.append("id: {}\ntitle: {}\nyear: {}\nvenue: {}\nabstract: {}".format(
            paper.get("paper_id") or paper.get("id"), paper.get("title"),
            paper.get("year"), paper.get("venue"), paper.get("abstract")))
    return "\n\n".join(blocks)


def separation(scores: Dict[str, float]) -> Dict[str, Any]:
    values = sorted(scores.values(), reverse=True)
    if len(values) < 2:
        return {}
    total = sum(values) or 1.0
    import math
    probs = [v / total for v in values]
    entropy = -sum(p * math.log(p) for p in probs if p > 0)
    return {"top1_minus_top2": round(values[0] - values[1], 5),
            "spread": round(values[0] - values[-1], 5),
            "entropy_ratio": round(entropy / math.log(len(values)), 4)}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--run", required=True)
    parser.add_argument("--assess-prompt", default="evidence_assess_v2")
    parser.add_argument("--out", default=None)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    config = load_config(args.config)
    prompts = PromptLibrary(config.prompts.dir)
    template = prompts.get(args.assess_prompt)
    run_dir = Path(args.run)
    out_path = Path(args.out or (run_dir / "reassessed_{}.json".format(args.assess_prompt)))
    llm = build_llm_client(config.llm, event_log=EventLog(
        run_dir / "reassess_events.jsonl"))
    mappings = load_ordinal_mappings(config.ordinal_mappings_path)
    max_papers = config.baselines.direct_rag.max_papers_in_prompt

    instances: List[Dict[str, Any]] = []
    for instance_dir in sorted((run_dir / "instances").glob("*")):
        if not instance_dir.is_dir():
            continue
        try:
            saved_graph = json.loads((instance_dir / "graph.json").read_text())
            retrieval = json.loads((instance_dir / "retrieval.json").read_text())["by_node"]
            old_scores = json.loads((instance_dir / "scores.json").read_text())
            old_evidence = json.loads((instance_dir / "evidence.json").read_text())["by_node"]
        except (OSError, ValueError, KeyError):
            continue
        graph = rebuild_graph(saved_graph)
        LOGGER.info("%s: %d node(s)", instance_dir.name, len(graph.nodes))

        new_labels: Dict[str, str] = {}
        details: Dict[str, Any] = {}
        refused_bridges = unassessable = 0
        for node_id, node in graph.nodes.items():
            papers = (retrieval.get(node_id) or {}).get("papers_shown", [])
            literature = render_literature(papers, max_papers)
            if not literature:
                new_labels[node_id] = "no_evidence"
                continue
            messages = [{"role": "user", "content": template.render(
                proposition=node.text, literature=literature,
                labels=", ".join(EVIDENCE_LABELS))}]

            def validate(parsed: Dict[str, Any]) -> None:
                if normalise_evidence_label(parsed.get("evidence_label")) is None:
                    raise ValueError("unknown evidence_label")

            try:
                response = llm.complete_json(
                    messages, purpose="reassess.evidence",
                    prompt_version=args.assess_prompt, validator=validate)
            except (LLMParseError, LLMError) as exc:
                LOGGER.error("%s/%s: %s", instance_dir.name, node_id, exc)
                continue
            parsed = response.parsed or {}
            label = normalise_evidence_label(parsed.get("evidence_label")) or "no_evidence"
            new_labels[node_id] = label
            refused_bridges += bool(parsed.get("requires_external_bridge"))
            unassessable += bool(parsed.get("proposition_unassessable"))
            details[node_id] = {
                "text": node.text, "label": label,
                "spans": parsed.get("supporting_spans"),
                "requires_external_bridge": parsed.get("requires_external_bridge"),
                "rationale": parsed.get("rationale"),
                "old_label": (old_evidence.get(node_id) or {}).get(
                    "assessment", {}).get("evidence_label"),
            }

        result = score_hypotheses(graph, new_labels, mappings=mappings)
        gold = old_scores["gold_id"]
        # Rank with the same deterministic tie-break the runner uses, so a tie does
        # not silently favour either arm.
        ranking = ranking_from_scores(result.scores, order=list(graph.hypothesis_ids))
        old_ranking = old_scores["ranking"]
        old_labels = {k: (v.get("assessment") or {}).get("evidence_label")
                      for k, v in old_evidence.items()}

        def informative(labels):
            return sum(1 for v in labels.values() if v and v != "no_evidence")

        instances.append({
            "instance": instance_dir.name,
            "n_nodes": len(graph.nodes),
            "old": {"informative": informative(old_labels),
                    "labels": dict(Counter(v for v in old_labels.values() if v)),
                    "gold_rank": old_ranking.index(gold) + 1 if gold in old_ranking else None,
                    "separation": separation(old_scores["scores"])},
            "new": {"informative": informative(new_labels),
                    "labels": dict(Counter(new_labels.values())),
                    "gold_rank": ranking.index(gold) + 1 if gold in ranking else None,
                    "separation": separation(result.scores)},
            "refused_bridges": refused_bridges,
            "unassessable": unassessable,
            "k": len(graph.hypothesis_ids),
            "nodes": details,
        })

    write_json(out_path, {
        "generated_at": utc_now_iso(), "run": str(run_dir),
        "assess_prompt": args.assess_prompt,
        "held_fixed": ["graph", "nodes", "edges", "retrieved papers", "ordinal mappings"],
        "instances": instances,
    })

    print("\n%-16s %6s | %-22s | %-22s" % ("instance", "nodes", "OLD (broad assessor)",
                                           "NEW ({})".format(args.assess_prompt)))
    tot_old = tot_new = tot_nodes = 0
    for row in instances:
        tot_nodes += row["n_nodes"]; tot_old += row["old"]["informative"]
        tot_new += row["new"]["informative"]
        print("%-16s %6d | %2d inf  rank %-2s sep %-7s | %2d inf  rank %-2s sep %-7s  bridges refused %d" % (
            row["instance"], row["n_nodes"],
            row["old"]["informative"], row["old"]["gold_rank"],
            row["old"]["separation"].get("top1_minus_top2"),
            row["new"]["informative"], row["new"]["gold_rank"],
            row["new"]["separation"].get("top1_minus_top2"), row["refused_bridges"]))
    print("%-16s %6d | %2d inf (%.0f%%)%14s | %2d inf (%.0f%%)" % (
        "TOTAL", tot_nodes, tot_old, 100 * tot_old / max(tot_nodes, 1), "",
        tot_new, 100 * tot_new / max(tot_nodes, 1)))
    print("\nwrote {}".format(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
