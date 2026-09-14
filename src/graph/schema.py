"""Consequence-graph representation (IMPLEMENTATION_SPEC.md §12).

One categorical root variable `H in {1..k}`, one value per candidate hypothesis.
Every non-hypothesis node carries a binary proposition variable `X_v`; retrieved
literature for that node is `D_v`. There is deliberately **no separate `C`
variable or node type** (§35.4) — "consequence" is a role a proposition plays,
not a class of object, and any node may be empirically assessable at any depth
(§35.3).

Edges are uncertain scientific implications, not logical rules. A hypothesis root
may be an edge source, so `H_i -> X_v` and `X_u -> X_v` are the same kind of
object with the same ordinal scale.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from pydantic import BaseModel, ConfigDict, Field

HYPOTHESIS_PREFIX = "H"
PROPOSITION_PREFIX = "X"


def is_hypothesis(node_id: str) -> bool:
    """`H0`, `H3` are hypothesis roots; `X7` is a proposition."""
    return bool(node_id) and node_id[0] == HYPOTHESIS_PREFIX and node_id[1:].isdigit()


class PropositionNode(BaseModel):
    """One scientific proposition `X_v`."""

    model_config = ConfigDict(extra="forbid")

    id: str
    text: str
    empirically_assessable: bool = True
    generation_parent: Optional[str] = None
    generation_origin_hypothesis: Optional[str] = None
    depth: int = 1
    # Ids merged into this node by `src.graph.merge`, with their origins.
    merged_from: List[str] = Field(default_factory=list)
    merged_origin_hypotheses: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """An uncertain implication `source -> target`.

    `source` may be a hypothesis root or another proposition. `ordinal_strength`
    is filled by the edge assessor and is `None` until then.
    """

    model_config = ConfigDict(extra="forbid")

    source: str
    target: str
    ordinal_strength: Optional[str] = None
    rationale: Optional[str] = None
    # root : judged against a hypothesis (cross-evaluation, §13.5)
    # chain: judged between two propositions
    kind: str = "chain"

    @property
    def key(self) -> Tuple[str, str]:
        return (self.source, self.target)


class ConsequenceGraph(BaseModel):
    """A graph frozen before any literature outcome is observed (§13, §35.6)."""

    model_config = ConfigDict(extra="forbid")

    instance_id: str
    hypothesis_ids: List[str]
    nodes: Dict[str, PropositionNode] = Field(default_factory=dict)
    edges: List[GraphEdge] = Field(default_factory=list)
    frozen: bool = False
    generation_notes: List[str] = Field(default_factory=list)

    # -- construction ---------------------------------------------------- #
    def add_node(self, node: PropositionNode) -> PropositionNode:
        if self.frozen:
            raise RuntimeError("the graph is frozen; nodes cannot be added after freezing")
        self.nodes[node.id] = node
        return node

    def add_edge(self, edge: GraphEdge) -> Optional[GraphEdge]:
        if self.frozen:
            raise RuntimeError("the graph is frozen; edges cannot be added after freezing")
        if edge.source == edge.target:
            return None
        for existing in self.edges:
            if existing.key == edge.key:
                return existing
        self.edges.append(edge)
        return edge

    def freeze(self) -> "ConsequenceGraph":
        """Close the graph. Everything after this point only observes it."""
        self.frozen = True
        return self

    # -- queries ---------------------------------------------------------- #
    def parents(self, node_id: str) -> List[GraphEdge]:
        return [e for e in self.edges if e.target == node_id]

    def children(self, node_id: str) -> List[GraphEdge]:
        return [e for e in self.edges if e.source == node_id]

    def assessable_nodes(self) -> List[PropositionNode]:
        """Any node may be assessable — there is no terminal node type (§35.3)."""
        return [n for n in self.nodes.values() if n.empirically_assessable]

    def shared_nodes(self) -> List[PropositionNode]:
        """Nodes reachable from more than one hypothesis (§35.9)."""
        return [n for n in self.nodes.values() if len(self.origin_hypotheses(n.id)) > 1]

    def origin_hypotheses(self, node_id: str) -> List[str]:
        node = self.nodes.get(node_id)
        if node is None:
            return []
        origins = set(node.merged_origin_hypotheses)
        if node.generation_origin_hypothesis:
            origins.add(node.generation_origin_hypothesis)
        return sorted(origins)

    def topological_order(self) -> List[str]:
        """Propositions ordered so every parent precedes its children.

        Cycles cannot arise from generation, but a merge can create one; any
        node left over is appended and reported rather than silently dropped.
        """
        incoming: Dict[str, Set[str]] = {
            node_id: {e.source for e in self.parents(node_id) if not is_hypothesis(e.source)}
            for node_id in self.nodes
        }
        ordered: List[str] = []
        remaining = dict(incoming)
        while remaining:
            ready = sorted(n for n, deps in remaining.items() if not (deps & set(remaining)))
            if not ready:
                ordered.extend(sorted(remaining))  # cycle: reported by validate()
                break
            ordered.extend(ready)
            for node_id in ready:
                remaining.pop(node_id)
        return ordered

    def validate(self) -> List[str]:
        """Structural problems, as a list of human-readable strings."""
        problems: List[str] = []
        for edge in self.edges:
            if not is_hypothesis(edge.source) and edge.source not in self.nodes:
                problems.append("edge from unknown node {}".format(edge.source))
            if is_hypothesis(edge.source) and edge.source not in self.hypothesis_ids:
                problems.append("edge from unknown hypothesis {}".format(edge.source))
            if edge.target not in self.nodes:
                problems.append("edge to unknown node {}".format(edge.target))
            if is_hypothesis(edge.target):
                problems.append("hypothesis {} used as an edge target".format(edge.target))
        order = self.topological_order()
        if len(order) != len(self.nodes):
            problems.append("topological order covers {} of {} nodes".format(len(order), len(self.nodes)))
        for node_id in self.nodes:
            if not self.parents(node_id):
                problems.append("node {} has no parent".format(node_id))
        return problems

    def stats(self) -> Dict[str, Any]:
        return {
            "n_nodes": len(self.nodes),
            "n_edges": len(self.edges),
            "n_root_edges": sum(1 for e in self.edges if e.kind == "root"),
            "n_chain_edges": sum(1 for e in self.edges if e.kind == "chain"),
            "n_assessable": len(self.assessable_nodes()),
            "n_shared": len(self.shared_nodes()),
            "n_merged": sum(1 for n in self.nodes.values() if n.merged_from),
            "max_depth": max([n.depth for n in self.nodes.values()] or [0]),
            "frozen": self.frozen,
        }

    def record(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "hypothesis_ids": list(self.hypothesis_ids),
            "stats": self.stats(),
            "nodes": [n.model_dump(mode="json") for n in self.nodes.values()],
            "edges": [e.model_dump(mode="json") for e in self.edges],
            "generation_notes": list(self.generation_notes),
            "problems": self.validate(),
        }
