"""Bayesian propagation over the consequence graph (IMPLEMENTATION_SPEC.md §22).

The model of the paper:

    P(H, X, D | G) = P(H) * prod_v P(X_v | X_pa(v), H) * prod_v P(D_v | X_v)

and the score of a hypothesis is its posterior after marginalising the
unobserved propositions.

**What is exact here.** For a single observed node `v`, with
`p = P(X_v = 1 | H = i)` and evidence likelihood ratio
`L_v = P(D_v | X_v=1) / P(D_v | X_v=0)`:

    P(D_v | H=i) = p * P(D_v|X_v=1) + (1-p) * P(D_v|X_v=0)
                 = P(D_v|X_v=0) * [p * L_v + (1 - p)]

The factor `P(D_v|X_v=0)` is the same for every hypothesis and cancels in the
posterior, so node `v` contributes exactly `log(p*L_v + 1 - p)` to hypothesis
`i`. That marginalisation is exact.

**What is approximated, and why it is flagged.** Observed nodes are combined as
if conditionally independent given `H`. When two observed nodes share a latent
parent, that is an approximation — the spec permits it provided it is explicit
(§21). `explain()` reports how many observed nodes share a parent, so the size
of the approximation is visible per instance rather than assumed away.

Three properties fall out, and each is tested:

* `lambda = 0` (no_evidence) gives `L = 1`, so the contribution is exactly
  `log(1) = 0`. Missing evidence moves nothing (§20, §35.5).
* A node with the same `p` under every hypothesis contributes the same amount to
  every hypothesis, so it cannot change the ranking however strong its evidence.
  Non-discriminative evidence is inert (§2, "Prioritise discriminative evidence").
* Distance attenuates only through the edge probabilities: a long chain of strong
  implications preserves `p`, a short weak one does not. Depth is never counted
  (§35.2).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from src.common.errors import ConfigError
from src.common.logging_utils import get_logger
from src.graph.schema import ConsequenceGraph, is_hypothesis
from src.inference.parameters import OrdinalMappings, normalise_edge_label

LOGGER = get_logger("inference.bayes")

MULTI_PARENT_RULES = ("noisy_or", "max", "mean")


@dataclass
class NodeContribution:
    """What one observed proposition did to one hypothesis."""

    node_id: str
    hypothesis_id: str
    p_true_given_h: float
    evidence_label: str
    log_likelihood_ratio: float
    contribution: float

    def record(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "hypothesis_id": self.hypothesis_id,
            "p_true_given_h": round(self.p_true_given_h, 4),
            "evidence_label": self.evidence_label,
            "log_likelihood_ratio": round(self.log_likelihood_ratio, 4),
            "contribution": round(self.contribution, 6),
        }


@dataclass
class PropagationResult:
    scores: Dict[str, float] = field(default_factory=dict)          # posterior
    log_scores: Dict[str, float] = field(default_factory=dict)      # unnormalised
    p_matrix: Dict[str, Dict[str, float]] = field(default_factory=dict)  # node -> H -> p
    contributions: List[NodeContribution] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def record(self) -> Dict[str, Any]:
        return {
            "scores": {k: round(v, 6) for k, v in self.scores.items()},
            "log_scores": {k: round(v, 6) for k, v in self.log_scores.items()},
            "p_matrix": {n: {h: round(p, 4) for h, p in row.items()}
                         for n, row in self.p_matrix.items()},
            "contributions": [c.record() for c in self.contributions],
            "notes": list(self.notes),
        }


def _combine(values: Sequence[float], rule: str) -> float:
    if not values:
        raise ValueError("no parent estimates to combine")
    if rule == "max":
        return max(values)
    if rule == "mean":
        return sum(values) / len(values)
    if rule == "noisy_or":
        product = 1.0
        for value in values:
            product *= (1.0 - value)
        return 1.0 - product
    raise ConfigError("unknown inference.multi_parent_rule {!r}; expected one of {}".format(
        rule, MULTI_PARENT_RULES))


def propagate(
    graph: ConsequenceGraph,
    *,
    mappings: OrdinalMappings,
    multi_parent_rule: str = "noisy_or",
    parent_false_baseline: float = 0.5,
) -> Dict[str, Dict[str, float]]:
    """`node -> hypothesis -> P(X_node = 1 | H = hypothesis)`.

    Routes are followed in topological order. For hypothesis `i`:

    * a root edge `H_i -> v` contributes `f_theta(r)` directly;
    * a root edge from a *different* hypothesis is ignored — it says nothing
      about what `H_i` predicts;
    * a chain edge `X_u -> v` contributes
      `f_theta(r) * p_u + baseline * (1 - p_u)`, so an uncertain parent
      attenuates the route;
    * a node with no route from `H_i` sits at `baseline`, i.e. `H_i` makes no
      prediction about it.
    """
    p_matrix: Dict[str, Dict[str, float]] = {}
    for node_id in graph.topological_order():
        parents = graph.parents(node_id)
        row: Dict[str, float] = {}
        for hypothesis_id in graph.hypothesis_ids:
            estimates: List[float] = []
            for edge in parents:
                label = normalise_edge_label(edge.ordinal_strength)
                if label is None:
                    continue  # unjudged edge carries no information
                q = mappings.edge_value(label)
                if is_hypothesis(edge.source):
                    if edge.source == hypothesis_id:
                        estimates.append(q)
                    continue
                parent_p = p_matrix.get(edge.source, {}).get(hypothesis_id)
                if parent_p is None:
                    continue
                estimates.append(q * parent_p + parent_false_baseline * (1.0 - parent_p))
            row[hypothesis_id] = (
                _combine(estimates, multi_parent_rule) if estimates else parent_false_baseline
            )
        p_matrix[node_id] = row
    return p_matrix


def score_hypotheses(
    graph: ConsequenceGraph,
    evidence: Dict[str, str],
    *,
    mappings: OrdinalMappings,
    prior: Optional[Dict[str, float]] = None,
    multi_parent_rule: str = "noisy_or",
    parent_false_baseline: float = 0.5,
    aggregation: str = "independent",
) -> PropagationResult:
    """Posterior over hypotheses given ordinal evidence labels per node.

    `evidence` maps node id -> ordinal evidence label. Nodes absent from it are
    unobserved and marginalise out exactly, contributing nothing.
    """
    result = PropagationResult()
    hypotheses = list(graph.hypothesis_ids)
    if not hypotheses:
        result.notes.append("no hypotheses to score")
        return result

    if prior is None:
        prior = {h: 1.0 / len(hypotheses) for h in hypotheses}
    missing = [h for h in hypotheses if h not in prior]
    if missing:
        raise ConfigError("prior is missing hypotheses: {}".format(missing))

    result.p_matrix = propagate(
        graph, mappings=mappings, multi_parent_rule=multi_parent_rule,
        parent_false_baseline=parent_false_baseline,
    )

    log_scores = {h: math.log(prior[h]) if prior[h] > 0 else -math.inf for h in hypotheses}

    if aggregation == "family":
        families = consequence_families(graph)
        observed_nodes = {n for n in evidence if n in graph.nodes}
        for root, members in sorted(families.items()):
            if not observed_nodes.intersection(members):
                continue  # nothing observed in this family: contributes exactly 0
            for hypothesis_id in hypotheses:
                contribution = _family_log_likelihood(
                    graph, members, root, hypothesis_id=hypothesis_id,
                    evidence=evidence, mappings=mappings, p_matrix=result.p_matrix,
                    parent_false_baseline=parent_false_baseline,
                    multi_parent_rule=multi_parent_rule)
                baseline = _family_log_likelihood(
                    graph, members, root, hypothesis_id=hypothesis_id,
                    evidence={}, mappings=mappings, p_matrix=result.p_matrix,
                    parent_false_baseline=parent_false_baseline,
                    multi_parent_rule=multi_parent_rule)
                # Subtract the no-evidence value so a family with no informative
                # evidence contributes exactly 0, matching the independent path.
                delta = contribution - baseline
                log_scores[hypothesis_id] += delta
                result.contributions.append(NodeContribution(
                    node_id="family:{}".format(root), hypothesis_id=hypothesis_id,
                    p_true_given_h=result.p_matrix.get(root, {}).get(
                        hypothesis_id, parent_false_baseline),
                    evidence_label="+".join(
                        "{}={}".format(m, evidence[m]) for m in members if m in evidence),
                    log_likelihood_ratio=delta, contribution=delta,
                ))
        result.notes.append(
            "aggregation=family: {} family/families, {} with observed evidence; "
            "within-family dependence marginalised exactly, families combined under "
            "conditional independence".format(
                len(families),
                sum(1 for m in families.values() if observed_nodes.intersection(m))))
        return _finalise(result, log_scores, hypotheses, graph, evidence, mappings,
                         aggregation)

    for node_id, label in sorted(evidence.items()):
        if node_id not in graph.nodes:
            result.notes.append("evidence for unknown node {} ignored".format(node_id))
            continue
        lam = mappings.evidence_value(label)
        likelihood_ratio = math.exp(lam)
        for hypothesis_id in hypotheses:
            p = result.p_matrix.get(node_id, {}).get(hypothesis_id, parent_false_baseline)
            contribution = math.log(p * likelihood_ratio + (1.0 - p))
            log_scores[hypothesis_id] += contribution
            result.contributions.append(NodeContribution(
                node_id=node_id, hypothesis_id=hypothesis_id, p_true_given_h=p,
                evidence_label=label, log_likelihood_ratio=lam, contribution=contribution,
            ))

    return _finalise(result, log_scores, hypotheses, graph, evidence, mappings,
                     aggregation)


def _finalise(result, log_scores, hypotheses, graph, evidence, mappings, aggregation):
    """Normalise log scores and record the notes, shared by both aggregation paths."""
    result.log_scores = log_scores
    largest = max(log_scores.values())
    weights = {h: math.exp(v - largest) for h, v in log_scores.items()}
    total = sum(weights.values())
    result.scores = {h: w / total for h, w in weights.items()} if total else {
        h: 1.0 / len(hypotheses) for h in hypotheses
    }

    observed = [n for n in evidence if n in graph.nodes]
    informative = [n for n in observed if abs(mappings.evidence_value(evidence[n])) > 1e-9]
    result.notes.append(
        "{} observed node(s), {} informative; {} unobserved node(s) marginalised out".format(
            len(observed), len(informative), len(graph.nodes) - len(observed))
    )
    shared = _shared_parent_pairs(graph, observed)
    if shared and aggregation == "independent":
        result.notes.append(
            "APPROXIMATION: {} pair(s) of observed nodes share a parent and are treated as "
            "conditionally independent given H (spec §21)".format(shared)
        )
    return result


def _shared_parent_pairs(graph: ConsequenceGraph, observed: Sequence[str]) -> int:
    parents = {
        node_id: {e.source for e in graph.parents(node_id) if not is_hypothesis(e.source)}
        for node_id in observed
    }
    count = 0
    for i, a in enumerate(observed):
        for b in list(observed)[i + 1:]:
            if parents.get(a) and parents.get(a) & parents.get(b, set()):
                count += 1
    return count


def discriminativeness(p_matrix: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Spread of `P(X_v|H)` across hypotheses, per node.

    A node whose spread is 0 predicts the same thing under every hypothesis and
    cannot change the ranking however well established it is.
    """
    out: Dict[str, float] = {}
    for node_id, row in p_matrix.items():
        values = list(row.values())
        out[node_id] = round(max(values) - min(values), 4) if values else 0.0
    return out


def consequence_families(graph: ConsequenceGraph) -> Dict[str, List[str]]:
    """`root node id -> [root, *chain descendants]`.

    A family is one depth-1 proposition together with everything reachable from it
    by chain edges. These are the nodes whose truth values are dependent given H:
    a mechanistic restatement of a specific claim is not a second independent
    observation of it.

    A node with no chain relationships forms a singleton family, so
    `aggregation: family` reduces exactly to `independent` on a graph with no chain
    edges. That is the intended degenerate case, not a special case in the code.
    """
    children: Dict[str, List[str]] = {}
    has_chain_parent = set()
    for edge in graph.edges:
        if edge.kind != "chain":
            continue
        children.setdefault(edge.source, []).append(edge.target)
        has_chain_parent.add(edge.target)

    families: Dict[str, List[str]] = {}
    for node_id in graph.topological_order():
        if node_id in has_chain_parent:
            continue  # belongs to an ancestor's family
        members = [node_id]
        queue = list(children.get(node_id, []))
        seen = {node_id}
        while queue:
            nxt = queue.pop(0)
            if nxt in seen:
                continue
            seen.add(nxt)
            members.append(nxt)
            queue.extend(children.get(nxt, []))
        families[node_id] = members
    return families


def _family_log_likelihood(
    graph: ConsequenceGraph,
    members: Sequence[str],
    root: str,
    *,
    hypothesis_id: str,
    evidence: Dict[str, str],
    mappings: OrdinalMappings,
    p_matrix: Dict[str, Dict[str, float]],
    parent_false_baseline: float,
    multi_parent_rule: str = "noisy_or",
) -> float:
    """log P(D_family | H_i), summing over the family's latent X values.

    Exact for a tree: condition on the root proposition being true or false, and
    each child contributes its own inner sum given that. An unobserved node has
    likelihood 1 either way and drops out, so it marginalises out exactly -- the
    same invariant as the independent path (spec 35.5).

    The difference from the independent path is that a child's probability is taken
    GIVEN the root's assumed value, instead of each node being scored against its
    own marginal. That is what stops a mechanistic restatement of a specific claim
    counting as a second independent observation.
    """
    def lr(node_id: str) -> float:
        label = evidence.get(node_id)
        if label is None:
            return 1.0
        return math.exp(mappings.evidence_value(label))

    # A family member usually has TWO parents: the chain edge from its ancestor AND
    # a root edge from the hypothesis itself (cross-evaluation assesses every node
    # against every candidate). Dropping the root edge would discard exactly the
    # information cross-evaluation exists to produce, so both are kept and combined
    # with the same rule the independent path uses.
    chain_q: Dict[str, float] = {}
    root_q: Dict[str, float] = {}
    for edge in graph.edges:
        if edge.target not in members:
            continue
        label = normalise_edge_label(edge.ordinal_strength)
        if label is None:
            continue
        if edge.kind == "chain":
            chain_q[edge.target] = mappings.edge_value(label)
        elif is_hypothesis(edge.source) and edge.source == hypothesis_id:
            root_q[edge.target] = mappings.edge_value(label)

    p_root = p_matrix.get(root, {}).get(hypothesis_id, parent_false_baseline)
    total = 0.0
    for root_true in (True, False):
        weight = p_root if root_true else (1.0 - p_root)
        if weight <= 0.0:
            continue
        term = weight * (lr(root) if root_true else 1.0)
        for member in members:
            if member == root:
                continue
            # P(child | root value): the chain strength when the root holds, the
            # configured baseline when it does not.
            estimates: List[float] = []
            q = chain_q.get(member)
            if q is not None:
                # the chain route, attenuated exactly by the assumed root value
                estimates.append(q if root_true else parent_false_baseline)
            if member in root_q:
                estimates.append(root_q[member])
            p_child = (_combine(estimates, multi_parent_rule) if estimates
                       else parent_false_baseline)
            child_lr = lr(member)
            term *= p_child * child_lr + (1.0 - p_child)
        total += term
    return math.log(total) if total > 0 else -math.inf


def _finalise(result, log_scores, hypotheses, graph, evidence, mappings, aggregation):
    """Shared tail: normalise the posterior and record what was observed."""
    result.log_scores = log_scores
    largest = max(log_scores.values())
    weights = {h: math.exp(v - largest) for h, v in log_scores.items()}
    total = sum(weights.values())
    result.scores = {h: w / total for h, w in weights.items()} if total else {
        h: 1.0 / len(hypotheses) for h in hypotheses
    }
    observed = [n for n in evidence if n in graph.nodes]
    informative = [n for n in observed if abs(mappings.evidence_value(evidence[n])) > 1e-9]
    result.notes.append(
        "{} observed node(s), {} informative; {} unobserved node(s) marginalised out".format(
            len(observed), len(informative), len(graph.nodes) - len(observed)))
    if aggregation != "family":
        shared = _shared_parent_pairs(graph, observed)
        if shared:
            result.notes.append(
                "APPROXIMATION: {} pair(s) of observed nodes share a parent and are "
                "treated as conditionally independent given H (spec 21)".format(shared))
    return result
