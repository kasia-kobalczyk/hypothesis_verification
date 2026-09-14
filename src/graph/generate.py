"""Consequence-graph construction (IMPLEMENTATION_SPEC.md §13).

    build_graph(question, hypotheses, config) -> ConsequenceGraph

Pipeline, in order:

  1. expand each candidate hypothesis into propositions it predicts;
  2. recursively expand selected propositions to `graph.max_depth`;
  3. pool everything from every hypothesis into ONE graph;
  4. merge semantically equivalent propositions;
  5. cross-evaluate every surviving proposition against EVERY hypothesis, which
     is what makes shared and non-discriminative nodes visible;
  6. judge the proposition-to-proposition edges;
  7. freeze.

Outcome-blindness (§13, §35.6): nothing here consults the literature. Which
nodes get expanded is decided by generation order and budget alone, never by
whether retrieval later turns out to be favourable. The graph is frozen before
`src.evidence` is allowed to run, and `ConsequenceGraph.freeze()` enforces that
structurally.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, List, Optional, Sequence, Tuple

from src.benchmark.presentation import Presentation
from src.common.config import AppConfig
from src.common.errors import GraphBudgetError, LLMError, LLMParseError
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.graph.merge import merge_propositions
from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode
from src.inference.parameters import EDGE_LABELS, normalise_edge_label
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

LOGGER = get_logger("graph.generate")

ROOT_EDGE_PROMPT = "edge_assess_v1"
CHAIN_EDGE_PROMPT = "edge_assess_chain_v1"


def _round_robin_by_origin(nodes: Sequence[PropositionNode]) -> List[PropositionNode]:
    """Interleave nodes by origin hypothesis, preserving order within each origin.

    Deeper levels are expanded until the total node cap is hit, so the order the
    frontier is walked in decides who gets truncated. Walking pool order gives
    every depth-2 slot to the first candidate's propositions; interleaving spreads
    the truncation evenly across candidates. Deterministic either way.
    """
    groups: "OrderedDict[Optional[str], List[PropositionNode]]" = OrderedDict()
    for node in nodes:
        groups.setdefault(node.generation_origin_hypothesis, []).append(node)
    ordered: List[PropositionNode] = []
    while any(groups.values()):
        for bucket in groups.values():
            if bucket:
                ordered.append(bucket.pop(0))
    return ordered


def _render_candidates(presentation: Presentation, *, exclude_label: Optional[str] = None) -> str:
    blocks = []
    for item in presentation.items:
        if exclude_label is not None and item.label == exclude_label:
            continue
        blocks.append("Candidate {}:\n{}".format(item.label, item.text))
    return "\n\n".join(blocks)


def _generate_children(
    *,
    question: str,
    focal: str,
    presentation: Presentation,
    exclude_label: Optional[str],
    max_children: int,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    prompt_version: str,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    template = prompts.get(prompt_version)
    # Pass only what the template declares. A generation prompt that does not
    # declare `$alternatives` is therefore never shown the competing candidates,
    # which is what makes non-contrastive generation structural rather than a
    # matter of the prompt's wording.
    values: Dict[str, Any] = {
        "question": question,
        "focal": focal,
        "max_children": max_children,
    }
    if "alternatives" in template.placeholders:
        values["alternatives"] = _render_candidates(presentation, exclude_label=exclude_label)
    messages = [{"role": "user", "content": template.render(**values)}]

    def validate(parsed: Dict[str, Any]) -> None:
        items = parsed.get("propositions")
        if not isinstance(items, list) or not items:
            raise ValueError("missing 'propositions' list")
        for item in items:
            if not isinstance(item, dict) or not str(item.get("text", "")).strip():
                raise ValueError("each proposition needs non-empty text")

    response = llm.complete_json(
        messages, purpose="graph.generate", prompt_version=prompt_version, validator=validate)
    items = (response.parsed or {}).get("propositions", [])[:max_children]
    return items, response.record(include_messages=messages)


def build_graph(
    *,
    instance_id: str,
    question: str,
    presentation: Presentation,
    config: AppConfig,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    event_log: Optional[EventLog] = None,
) -> Tuple[ConsequenceGraph, Dict[str, Any]]:
    """Build and freeze the consequence graph. Returns the graph and its artifacts."""
    log = event_log or NULL_EVENT_LOG
    graph_config = config.graph
    hypothesis_ids = [item.hypothesis_id for item in presentation.items]

    # Refuse a budget that cannot expand every candidate, before spending a
    # single call. The alternative -- truncating depth 1 -- leaves some
    # candidates with no propositions of their own, so they are ranked only
    # through other candidates' consequences. That is a silently deformed graph,
    # and it is not a failure mode worth having a config default for.
    root_budget = len(presentation.items) * graph_config.max_root_consequences_per_hypothesis
    if root_budget > graph_config.max_nodes:
        raise GraphBudgetError(
            "graph.max_nodes={} cannot hold depth 1: {} candidates x "
            "max_root_consequences_per_hypothesis={} needs {} nodes. Raise max_nodes "
            "to at least {}, or lower max_root_consequences_per_hypothesis.".format(
                graph_config.max_nodes, len(presentation.items),
                graph_config.max_root_consequences_per_hypothesis, root_budget, root_budget))
    graph = ConsequenceGraph(instance_id=instance_id, hypothesis_ids=hypothesis_ids)
    artifacts: Dict[str, Any] = {
        "prompt_versions": {
            "generate": prompts.get(graph_config.generate_prompt).record(),
            "root_edge": prompts.get(ROOT_EDGE_PROMPT).record(),
            "chain_edge": prompts.get(CHAIN_EDGE_PROMPT).record(),
        },
        "config": graph_config.model_dump(mode="json"),
        "generation_calls": [],
        "errors": [],
    }

    pooled: List[PropositionNode] = []
    counter = 0

    def next_id() -> str:
        nonlocal counter
        counter += 1
        return "X{}".format(counter)

    # -- 1. depth 1: one expansion per candidate hypothesis --------------- #
    for item in presentation.items:
        try:
            children, call = _generate_children(
                question=question, focal=item.text, presentation=presentation,
                exclude_label=item.label,
                max_children=graph_config.max_root_consequences_per_hypothesis,
                llm=llm, prompts=prompts, prompt_version=graph_config.generate_prompt)
        except (LLMParseError, LLMError) as exc:
            artifacts["errors"].append({"where": "generate.depth1", "hypothesis": item.hypothesis_id,
                                        "error": str(exc)})
            LOGGER.warning("%s: generation failed for %s: %s", instance_id, item.hypothesis_id, exc)
            continue
        artifacts["generation_calls"].append({"focal": item.hypothesis_id, "depth": 1, "call": call})
        for child in children[:graph_config.max_root_consequences_per_hypothesis]:
            pooled.append(PropositionNode(
                id=next_id(), text=str(child["text"]).strip(),
                empirically_assessable=bool(child.get("empirically_assessable", True)),
                generation_parent=item.hypothesis_id,
                generation_origin_hypothesis=item.hypothesis_id,
                depth=1,
                metadata={
                    "why_discriminative": child.get("why_discriminative"),
                    # v3 only: the abstraction level and the stated implication link.
                    # `why_implied` is what stops abstraction becoming an unsupported
                    # leap moved into the graph -- it is required above 'specific'.
                    "abstraction_level": child.get("abstraction_level"),
                    "why_implied": child.get("why_implied"),
                },
            ))

    # -- 2. deeper levels, expanded in deterministic generation order ------ #
    for depth in range(2, graph_config.max_depth + 1):
        frontier = _round_robin_by_origin([n for n in pooled if n.depth == depth - 1])
        for parent in frontier:
            if len(pooled) >= graph_config.max_nodes:
                graph.generation_notes.append(
                    "node budget {} reached at depth {}".format(graph_config.max_nodes, depth))
                break
            origin_label = presentation.id_to_label.get(parent.generation_origin_hypothesis or "")
            try:
                children, call = _generate_children(
                    question=question, focal=parent.text, presentation=presentation,
                    exclude_label=origin_label, max_children=graph_config.max_children_per_node,
                    llm=llm, prompts=prompts, prompt_version=graph_config.generate_prompt)
            except (LLMParseError, LLMError) as exc:
                artifacts["errors"].append({"where": "generate.depth{}".format(depth),
                                            "parent": parent.id, "error": str(exc)})
                continue
            artifacts["generation_calls"].append({"focal": parent.id, "depth": depth, "call": call})
            for child in children:
                if len(pooled) >= graph_config.max_nodes:
                    break
                pooled.append(PropositionNode(
                    id=next_id(), text=str(child["text"]).strip(),
                    empirically_assessable=bool(child.get("empirically_assessable", True)),
                    generation_parent=parent.id,
                    generation_origin_hypothesis=parent.generation_origin_hypothesis,
                    depth=depth,
                    metadata={
                        "why_discriminative": child.get("why_discriminative"),
                        "abstraction_level": child.get("abstraction_level"),
                        "why_implied": child.get("why_implied"),
                    },
                ))

    # -- 3/4. pool and merge ---------------------------------------------- #
    merged = merge_propositions(
        pooled, mode=graph_config.semantic_merge_mode, threshold=graph_config.merge_threshold,
        event_log=log)
    artifacts["merge"] = merged.record()
    for node in merged.nodes:
        graph.add_node(node)
    # Generation parents may have been merged away; follow them to the survivor.
    for node in graph.nodes.values():
        if node.generation_parent in merged.remap:
            node.generation_parent = merged.remap[node.generation_parent]

    # -- 5. cross-evaluate every node against EVERY hypothesis ------------- #
    root_template = prompts.get(ROOT_EDGE_PROMPT)
    labels = [item.label for item in presentation.items]
    artifacts["root_edge_calls"] = []
    for node in list(graph.nodes.values()):
        messages = [{"role": "user", "content": root_template.render(
            proposition=node.text,
            candidates=_render_candidates(presentation),
            labels=", ".join(EDGE_LABELS),
            ids=", ".join(labels),
        )}]

        def validate(parsed: Dict[str, Any]) -> None:
            entries = parsed.get("judgments")
            if not isinstance(entries, list) or not entries:
                raise ValueError("missing 'judgments'")
            for entry in entries:
                if normalise_edge_label(entry.get("strength")) is None:
                    raise ValueError("unknown strength {!r}".format(entry.get("strength")))

        try:
            response = llm.complete_json(
                messages, purpose="graph.root_edge", prompt_version=ROOT_EDGE_PROMPT,
                validator=validate)
        except (LLMParseError, LLMError) as exc:
            artifacts["errors"].append({"where": "root_edge", "node": node.id, "error": str(exc)})
            continue
        artifacts["root_edge_calls"].append({"node": node.id, "call": response.record()})
        for entry in (response.parsed or {}).get("judgments", []):
            hypothesis_id = presentation.resolve(entry.get("id"))
            label = normalise_edge_label(entry.get("strength"))
            if hypothesis_id is None or label is None:
                continue
            graph.add_edge(GraphEdge(source=hypothesis_id, target=node.id, kind="root",
                                     ordinal_strength=label, rationale=entry.get("rationale")))

    # -- 6. proposition-to-proposition edges ------------------------------- #
    chain_template = prompts.get(CHAIN_EDGE_PROMPT)
    artifacts["chain_edge_calls"] = []
    for node in list(graph.nodes.values()):
        parent_id = node.generation_parent
        if not parent_id or parent_id not in graph.nodes or parent_id == node.id:
            continue
        messages = [{"role": "user", "content": chain_template.render(
            parent=graph.nodes[parent_id].text, child=node.text, labels=", ".join(EDGE_LABELS))}]

        def validate_chain(parsed: Dict[str, Any]) -> None:
            if normalise_edge_label(parsed.get("strength")) is None:
                raise ValueError("unknown strength {!r}".format(parsed.get("strength")))

        try:
            response = llm.complete_json(
                messages, purpose="graph.chain_edge", prompt_version=CHAIN_EDGE_PROMPT,
                validator=validate_chain)
        except (LLMParseError, LLMError) as exc:
            artifacts["errors"].append({"where": "chain_edge", "node": node.id, "error": str(exc)})
            continue
        artifacts["chain_edge_calls"].append({"edge": [parent_id, node.id], "call": response.record()})
        parsed = response.parsed or {}
        graph.add_edge(GraphEdge(
            source=parent_id, target=node.id, kind="chain",
            ordinal_strength=normalise_edge_label(parsed.get("strength")),
            rationale=parsed.get("rationale")))

    # -- 7. freeze --------------------------------------------------------- #
    graph.freeze()
    problems = graph.validate()
    if problems:
        LOGGER.warning("%s: graph problems: %s", instance_id, problems[:3])
    artifacts["graph"] = graph.record()
    log.emit("graph_frozen", instance_id=instance_id, **graph.stats())
    return graph, artifacts
