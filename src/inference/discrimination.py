"""v4 discrimination gate: prediction states, comparative eligibility, gated scoring.

Deterministic. The LLM judgments this module consumes (prediction states, construct
match) are produced elsewhere; everything here is a rule applied to them.

Why v4 exists (BENCH-GRAPH-V4-DEV-001). In v3 every (hypothesis, proposition) pair got
an ordinal implication label mapped straight to P(X|H), with `neutral` = 0.50 and a
missing label also 0.50. Human review of the frozen pilot (D045/D046) found that:

* a hypothesis silent about a proposition was often labelled `unlikely`
  (categorical silence error);
* even a correct `neutral` let literature support move relative scores, because a
  determinate label was set against a pseudo-likelihood of 0.50;
* generic component facts gained comparative weight from such labels;
* evidence about a related construct was scored as if it addressed the proposition.

v4 therefore separates prediction STATE from prediction STRENGTH, and lets a
proposition move relative scores only when hypotheses make determinate, different
predictions about it and the evidence directly addresses its construct. An
`indeterminate` hypothesis is never converted into a number.

Scoring reuses the verifier's own `score_hypotheses` and the frozen ordinal mappings;
no new numeric parameter is introduced.
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, List, Mapping, Optional, Sequence

from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode
from src.inference.bayes import score_hypotheses

STATES = ("positive_or_present", "negative_or_absent", "substantive_null", "indeterminate")
DETERMINATE = frozenset(STATES[:3])
STRENGTHS = ("strong", "moderate", "weak")

# Proposition-level comparative classes.
COMPARATIVE = "comparative_discriminator"
ONE_SIDED = "one_sided_prediction"
SHARED = "shared_prediction"
ALL_INDETERMINATE = "all_indeterminate"
PARTIAL_CONTRAST = "partially_indeterminate_contrast"   # k > 2 only
OUT_OF_SCOPE = "generic_or_possibility_claim"
PROFILE_CLASSES = (COMPARATIVE, ONE_SIDED, SHARED, ALL_INDETERMINATE, PARTIAL_CONTRAST, OUT_OF_SCOPE)

# Proposition scope relative to the candidates (development iteration 3). A claim about a
# broader class than any candidate addresses, or a claim only that something is
# possible, cannot distinguish candidates about specific systems. Iteration 2 showed the
# state classifier ignoring this as advice, so the gate enforces it from the explicit
# scope field instead of trusting the per-hypothesis states.
SCOPES = ("within_candidates_scope", "broader_than_candidates", "possibility_only")
OUT_OF_SCOPE_SCOPES = frozenset({"broader_than_candidates", "possibility_only"})


def normalise_scope(scope: Any) -> str:
    value = str(scope or "").strip().lower().replace(" ", "_").replace("-", "_")
    if value not in SCOPES:
        raise StateError("unknown proposition scope {!r}".format(scope))
    return value

CONSTRUCT_MATCHES = ("direct", "partial", "mismatch")
# Human decision for BENCH-GRAPH-V4-DEV-001: only `direct` evidence may move comparative
# scores. `partial` is recorded and reported as sensitivity; `mismatch` contributes zero.
COMPARATIVE_CONSTRUCT_MATCHES = frozenset({"direct"})

# Evidence labels that carry information (log-LR != 0 in configs/ordinal_mappings.yaml).
UNINFORMATIVE_EVIDENCE = frozenset({"no_evidence", "mixed"})

# (state, strength) -> existing ordinal edge label, whose probability comes from the
# frozen configs/ordinal_mappings.yaml. The negative side of that scale has only two
# labels, so `moderate` and `weak` negative predictions share `unlikely`.
# `substantive_null` predicts no effect for the quantity the proposition asserts
# something about, so for scoring it uses the negative side; the state itself is kept
# distinct in every artifact.
_STATE_TO_EDGE_LABEL = {
    ("positive_or_present", "strong"): "strongly_implied",
    ("positive_or_present", "moderate"): "implied",
    ("positive_or_present", "weak"): "weakly_implied",
    ("negative_or_absent", "strong"): "strongly_contradicted",
    ("negative_or_absent", "moderate"): "unlikely",
    ("negative_or_absent", "weak"): "unlikely",
    ("substantive_null", "strong"): "strongly_contradicted",
    ("substantive_null", "moderate"): "unlikely",
    ("substantive_null", "weak"): "unlikely",
}


class StateError(ValueError):
    """A prediction-state record that cannot be used. Callers fail closed."""


def normalise_state(state: Any) -> str:
    value = str(state or "").strip().lower().replace(" ", "_").replace("-", "_")
    if value not in STATES:
        raise StateError("unknown prediction state {!r}".format(state))
    return value


def normalise_strength(state: str, strength: Any) -> Optional[str]:
    if state == "indeterminate":
        return None
    value = str(strength or "").strip().lower()
    if value not in STRENGTHS:
        raise StateError("determinate state {!r} needs a strength in {}, got {!r}".format(state, STRENGTHS, strength))
    return value


def edge_label_for(state: str, strength: Optional[str]) -> str:
    if state == "indeterminate":
        raise StateError("an indeterminate state has no likelihood and must never be scored")
    return _STATE_TO_EDGE_LABEL[(state, strength)]


def classify_profile(states: Mapping[str, str], hypothesis_ids: Sequence[str],
                     scope: Optional[str] = None) -> str:
    """Comparative class of one proposition from its per-hypothesis states.

    `scope` (iteration 3) is checked first: an out-of-scope proposition is never
    comparative, whatever states it was given. `None` means scope was not assessed
    (records from iterations 1-2) and applies no scope gating.

    Requires a state for every hypothesis: a missing hypothesis is not treated as
    indeterminate, because that would silently repeat v3's default-to-0.5.
    """
    missing = [h for h in hypothesis_ids if h not in states]
    if missing:
        raise StateError("no prediction state for {}".format(missing))
    values = [normalise_state(states[h]) for h in hypothesis_ids]
    if scope is not None and normalise_scope(scope) in OUT_OF_SCOPE_SCOPES:
        return OUT_OF_SCOPE
    determinate = [v for v in values if v in DETERMINATE]
    if not determinate:
        return ALL_INDETERMINATE
    distinct = set(determinate)
    if len(determinate) == len(values):
        return COMPARATIVE if len(distinct) > 1 else SHARED
    if len(determinate) == 1:
        return ONE_SIDED
    # k > 2 with some hypotheses indeterminate. Scoring only the determinate ones would
    # leave the indeterminate ones with an implicit likelihood; v4 does not score it.
    return PARTIAL_CONTRAST if len(distinct) > 1 else SHARED


def is_comparatively_eligible(profile_class: str) -> bool:
    return profile_class == COMPARATIVE


def gate_node(
    *,
    node_id: str,
    hypothesis_ids: Sequence[str],
    states: Optional[Mapping[str, Mapping[str, Any]]],
    evidence_label: Optional[str],
    construct_match: Optional[str],
    scope: Optional[str] = None,
) -> Dict[str, Any]:
    """Decide whether one proposition may move relative scores, and record why."""
    record: "OrderedDict[str, Any]" = OrderedDict([("node_id", node_id)])
    if not states:
        record.update(profile_class=None, comparatively_eligible=False, used_in_score=False,
                      gate_reason="prediction_states_unavailable")
        return record
    flat = {h: normalise_state(s["state"]) for h, s in states.items()}
    profile = classify_profile(flat, hypothesis_ids, scope)
    record["proposition_scope"] = scope
    eligible = is_comparatively_eligible(profile)
    record["profile_class"] = profile
    record["comparatively_eligible"] = eligible
    record["evidence_label"] = evidence_label
    record["construct_match"] = construct_match

    if not eligible:
        reason = "profile_{}".format(profile)
    elif evidence_label is None:
        reason = "no_evidence_assessment"
    elif evidence_label in UNINFORMATIVE_EVIDENCE:
        reason = "uninformative_evidence"
    elif construct_match not in COMPARATIVE_CONSTRUCT_MATCHES:
        reason = "construct_{}".format(construct_match or "unassessed")
    else:
        reason = None
    record["used_in_score"] = reason is None
    record["gate_reason"] = reason or "scored"
    return record


def score_gated(
    *,
    hypothesis_ids: Sequence[str],
    nodes: Mapping[str, str],
    states: Mapping[str, Mapping[str, Mapping[str, Any]]],
    gates: Mapping[str, Mapping[str, Any]],
    evidence_labels: Mapping[str, str],
    mappings,
    multi_parent_rule: str,
    parent_false_baseline: float,
    instance_id: str,
):
    """Relative scores from the gated propositions only.

    Builds a graph containing ONLY the nodes that passed the gate, each with a direct
    edge from every hypothesis derived from its prediction state, and scores it with
    the verifier's `score_hypotheses` under independent aggregation. Chain edges are
    deliberately absent: in v3 they let a child inherit a directional prediction
    through its parent for a hypothesis that is silent about the child.
    """
    graph = ConsequenceGraph(instance_id=instance_id, hypothesis_ids=list(hypothesis_ids))
    evidence: Dict[str, str] = {}
    for node_id, gate in gates.items():
        if not gate["used_in_score"]:
            continue
        graph.add_node(PropositionNode(id=node_id, text=nodes[node_id]))
        for h in hypothesis_ids:
            s = states[node_id][h]
            state = normalise_state(s["state"])
            label = edge_label_for(state, normalise_strength(state, s.get("strength")))
            graph.add_edge(GraphEdge(source=h, target=node_id, kind="root", ordinal_strength=label))
        evidence[node_id] = evidence_labels[node_id]
    graph.freeze()
    return score_hypotheses(graph, evidence, mappings=mappings, multi_parent_rule=multi_parent_rule,
                            parent_false_baseline=parent_false_baseline, aggregation="independent")


def summarise_gates(gates: Mapping[str, Mapping[str, Any]]) -> Dict[str, int]:
    out: Dict[str, int] = OrderedDict()
    out["n_nodes"] = len(gates)
    for cls in PROFILE_CLASSES:
        out["n_profile_" + cls] = sum(1 for g in gates.values() if g.get("profile_class") == cls)
    out["n_states_unavailable"] = sum(1 for g in gates.values() if g.get("profile_class") is None)
    out["n_comparatively_eligible"] = sum(1 for g in gates.values() if g.get("comparatively_eligible"))
    out["n_used_in_score"] = sum(1 for g in gates.values() if g.get("used_in_score"))
    for match in CONSTRUCT_MATCHES:
        out["n_construct_" + match] = sum(1 for g in gates.values() if g.get("construct_match") == match)
    out["n_eligible_blocked_by_construct"] = sum(
        1 for g in gates.values() if str(g.get("gate_reason", "")).startswith("construct_"))
    return out
