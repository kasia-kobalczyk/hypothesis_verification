"""Reproducibility of the graph-edge judgments — the hard scientific reasoning.

    python3 scripts/validate_edges.py --limit 150

After DECISIONS #29 the evidence assessor no longer bridges between claims: every
inferential step lives in an edge, as `P(X_v | H_i)`. That makes the edges the
component carrying the scientific reasoning, and therefore the component that now
needs its own validation. Until this exists, the edges are the unvalidated part of
the pipeline and should be described that way.

Method mirrors the evidence validation. Edges are sampled from saved graphs, and two
judges rate each one independently:

* **A** is the production prompt `edge_assess_v1`, which rates every candidate for a
  proposition on the ordinal scale.
* **B** is `edge_judge_b_v1`, which is never shown the ordinal labels. It is walked
  through the implication one candidate at a time and its answers are mapped onto the
  scale afterwards.

Plus one adversarial control: `mismatched`, pairing a proposition with a hypothesis
from a different instance. Those should land on `neutral`. An edge judge that finds
implications between unrelated claims is inventing structure, and since the edges are
now where all the scientific reasoning sits, that failure would be invisible in the
evidence numbers.

No retrieval, no evidence: edges are literature-free by construction.
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.inference.parameters import EDGE_LABELS  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.validate_edges")

# Judge B's step answers -> the ordinal scale. Deliberately coarse: B is not being
# asked to reproduce a seven-point scale it has never seen.
MAP_B = {
    ("follows", "surprised"): "strongly_implied",
    ("follows", "mildly_surprised"): "implied",
    ("follows", "not_surprised"): "implied",
    ("more_likely", "surprised"): "implied",
    ("more_likely", "mildly_surprised"): "weakly_implied",
    ("more_likely", "not_surprised"): "weakly_implied",
    ("unaffected", "surprised"): "neutral",
    ("unaffected", "mildly_surprised"): "neutral",
    ("unaffected", "not_surprised"): "neutral",
    ("less_likely", "surprised"): "strongly_contradicted",
    ("less_likely", "mildly_surprised"): "unlikely",
    ("less_likely", "not_surprised"): "unlikely",
}

# Direction collapses the scale to the distinction that moves a ranking.
DIRECTION = {
    "strongly_implied": "implies", "implied": "implies", "weakly_implied": "implies",
    "neutral": "neutral",
    "unlikely": "contradicts", "strongly_contradicted": "contradicts",
}


def collect_edges(pattern: str) -> List[Dict[str, Any]]:
    """Every (hypothesis, proposition) root edge in the saved graphs, with its label."""
    out: List[Dict[str, Any]] = []
    for instance_dir in sorted(glob.glob(pattern)):
        base = Path(instance_dir)
        try:
            graph = json.loads((base / "graph.json").read_text())
            # presentation.json carries ids and display labels only; the verbatim
            # hypothesis text lives in input.json.
            supplied = json.loads((base / "input.json").read_text())
        except (OSError, ValueError):
            continue
        texts = {h["id"]: h.get("text", "") for h in supplied.get("hypotheses", [])}
        nodes = {n["id"]: n for n in graph.get("nodes", [])}
        for edge in graph.get("edges", []):
            if edge.get("kind") != "root":
                continue
            hypothesis, node = edge.get("source"), edge.get("target")
            if hypothesis not in texts or node not in nodes:
                continue
            meta = nodes[node].get("metadata") or {}
            out.append({
                # v3 records the abstraction level; edges from abstracted nodes are
                # where the scientific bridge now sits, so reproducibility has to be
                # reported stratified by level, not pooled.
                "abstraction_level": meta.get("abstraction_level"),
                "why_implied": (meta.get("why_implied") or "").strip() or None,
                "edge_id": "{}::{}->{}".format(base.name, hypothesis, node),
                "instance": base.name,
                "hypothesis_id": hypothesis,
                "hypothesis_text": texts[hypothesis],
                "node_id": node,
                "proposition": nodes[node].get("text", ""),
                "production_label": edge.get("ordinal_strength"),
            })
    return out


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--runs", default="runs/consequence_graph_*/instances/*/")
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--conditions", nargs="+", default=["real", "mismatched"])
    parser.add_argument("--out", default="benchmark/assessor/edge_validation.json")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    out_path = Path(args.out)
    if out_path.exists() and not args.force:
        print("refusing to overwrite {} -- pass --out or --force".format(out_path))
        return 1

    config = load_config(args.config)
    prompts = PromptLibrary(config.prompts.dir)
    llm = build_llm_client(config.llm, event_log=EventLog(
        Path("benchmark/assessor/edge_validation_events.jsonl")))

    edges = collect_edges(args.runs)
    LOGGER.info("%d root edge(s) available", len(edges))
    if not edges:
        print("no edges found")
        return 1
    # Deterministic spread across instances rather than the first N of one graph.
    edges.sort(key=lambda e: e["edge_id"])
    stride = max(1, len(edges) // args.limit)
    sample = edges[::stride][: args.limit]
    LOGGER.info("sampled %d edge(s), stride %d", len(sample), stride)

    n = len(sample)
    mismatch_of = {e["edge_id"]: sample[(i + n // 2 + 1) % n] for i, e in enumerate(sample)}

    template_b = prompts.get("edge_judge_b_v1")
    template_a = prompts.get("edge_assess_v1")
    results: List[Dict[str, Any]] = []

    def judge_a(hypothesis: str, proposition: str) -> Optional[str]:
        messages = [{"role": "user", "content": template_a.render(
            proposition=proposition,
            candidates="Candidate A:\n{}".format(hypothesis),
            ids="A",
            labels=", ".join(EDGE_LABELS))}]

        def validate(parsed: Dict[str, Any]) -> None:
            if not parsed.get("judgements") and not parsed.get("judgments"):
                raise ValueError("missing judgements")

        try:
            response = llm.complete_json(messages, purpose="edge.validate.a",
                                         prompt_version="edge_assess_v1", validator=validate)
        except (LLMParseError, LLMError) as exc:
            LOGGER.error("judge a: %s", exc)
            return None
        parsed = response.parsed or {}
        items = parsed.get("judgements") or parsed.get("judgments") or []
        if not items:
            return None
        return str(items[0].get("ordinal_strength") or items[0].get("strength") or "").strip()

    def judge_b(hypothesis: str, proposition: str) -> Optional[Dict[str, Any]]:
        messages = [{"role": "user", "content": template_b.render(
            hypothesis=hypothesis, proposition=proposition)}]

        def validate(parsed: Dict[str, Any]) -> None:
            if not str(parsed.get("if_claim_true_then_prediction", "")).strip():
                raise ValueError("missing implication")

        try:
            response = llm.complete_json(messages, purpose="edge.validate.b",
                                         prompt_version="edge_judge_b_v1", validator=validate)
        except (LLMParseError, LLMError) as exc:
            LOGGER.error("judge b: %s", exc)
            return None
        parsed = response.parsed or {}
        key = (str(parsed.get("if_claim_true_then_prediction", "")).strip().lower(),
               str(parsed.get("surprise_if_prediction_false", "")).strip().lower())
        return {"label": MAP_B.get(key, "neutral"), "raw": key,
                "caveat": parsed.get("reading_where_it_does_not_follow")}

    for condition in args.conditions:
        LOGGER.info("--- condition: %s ---", condition)
        for index, edge in enumerate(sample, start=1):
            hypothesis = (edge["hypothesis_text"] if condition == "real"
                          else mismatch_of[edge["edge_id"]]["hypothesis_text"])
            a = judge_a(hypothesis, edge["proposition"])
            b = judge_b(hypothesis, edge["proposition"])
            if a is None or b is None:
                continue
            results.append({
                "edge_id": edge["edge_id"], "condition": condition,
                "abstraction_level": edge.get("abstraction_level"),
                "has_why_implied": bool(edge.get("why_implied")),
                "instance": edge["instance"],
                "production_label": edge["production_label"],
                "a_label": a, "b_label": b["label"], "b_raw": b["raw"],
                "b_caveat": b["caveat"],
                "a_direction": DIRECTION.get(a, "?"),
                "b_direction": DIRECTION.get(b["label"], "?"),
            })
            if index % 20 == 0:
                LOGGER.info("  %s: %d/%d", condition, index, len(sample))

    write_json(out_path, {
        "generated_at": utc_now_iso(),
        "judges": {"a": "edge_assess_v1 (production)", "b": "edge_judge_b_v1"},
        "model": "one deployment; same-model caveat applies as in the evidence validation",
        "n_edges_available": len(edges), "n_sampled": len(sample),
        "conditions": args.conditions,
        "b_mapping": {"|".join(k): v for k, v in MAP_B.items()},
        "rows": results,
    })
    print("\n{} edge judgment(s) -> {}".format(len(results), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
