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


# =========================================================================== #
# v4-scope (BENCH-GRAPH-V4-SCOPE-001)
# =========================================================================== #
# Scope is classified by a SEPARATE judgment from prediction state (the directive
# forbids overloading the state prompt; iteration 3 of V4-DEV showed doing so made the
# state classifier assign more contrasts). Evidence is judged against the proposition's
# contrast-bearing element rather than its whole wording.

SCOPE_CLASSES = ("hypothesis_specific", "mechanism_specific", "broader_class_fact",
                 "possibility_claim", "invalid_or_underspecified")
COMPARATIVE_SCOPE_CLASSES = frozenset({"hypothesis_specific", "mechanism_specific"})

CONTRAST_RELEVANCE = ("contrast_direct", "contrast_partial", "context_only",
                      "construct_mismatch", "no_evidence")
# Main method: only evidence that directly bears on the contrast variable may score.
# `contrast_partial` is recorded and reported as a separate sensitivity analysis.
COMPARATIVE_RELEVANCE = frozenset({"contrast_direct"})
SENSITIVITY_RELEVANCE = frozenset({"contrast_direct", "contrast_partial"})


def normalise_scope_class(value: Any) -> str:
    v = str(value or "").strip().lower().replace(" ", "_").replace("-", "_")
    if v not in SCOPE_CLASSES:
        raise StateError("unknown scope class {!r}".format(value))
    return v


def derive_contrast_relevance(contrast_variable_reported: Any, shared_context_supported: Any,
                              different_construct: Any) -> str:
    """Relevance category from the three structured answers, never from a holistic label.

    * contrast variable reported `yes`      -> contrast_direct
    * contrast variable reported `partly`   -> contrast_partial
    * not reported, different construct     -> construct_mismatch
    * not reported, shared context only     -> context_only
    * not reported, nothing relevant        -> no_evidence

    When the records neither report the contrast variable but DO concern a different
    construct, `construct_mismatch` wins over `context_only`: it is the more specific
    failure, and both contribute zero.
    """
    def yn(x, allowed):
        s = str(x or "").strip().lower()
        if s not in allowed:
            raise ValueError("expected one of {}, got {!r}".format(allowed, x))
        return s

    reported = yn(contrast_variable_reported, ("yes", "partly", "no"))
    context = yn(shared_context_supported, ("yes", "no"))
    different = yn(different_construct, ("yes", "no"))
    if reported == "yes":
        return "contrast_direct"
    if reported == "partly":
        return "contrast_partial"
    if different == "yes":
        return "construct_mismatch"
    if context == "yes":
        return "context_only"
    return "no_evidence"


def gate_node_scope(
    *,
    node_id: str,
    hypothesis_ids: Sequence[str],
    states: Optional[Mapping[str, Mapping[str, Any]]],
    scope: Optional[str],
    evidence_label: Optional[str],
    has_contrast: Optional[bool],
    contrast_relevance: Optional[str],
    allowed_relevance: frozenset = COMPARATIVE_RELEVANCE,
) -> Dict[str, Any]:
    """v4-scope gate. A proposition scores only if ALL hold, checked in this order:

    1. prediction states exist and form a determinate contrast (unchanged v4 rule);
    2. its scope is hypothesis- or mechanism-specific;
    3. its evidence label is informative;
    4. a contrast-bearing element was extracted and actually carries a contrast
       (`has_contrast`), so there is a specific element for the evidence to bear on;
    5. the evidence bears directly on that element.

    The order fixes which reason is recorded; each check is necessary on its own, so a
    later check can never re-admit what an earlier one excluded. In particular a scope
    judgment can never make a one-sided proposition comparative.
    """
    record: "OrderedDict[str, Any]" = OrderedDict([("node_id", node_id)])
    if not states:
        record.update(profile_class=None, comparatively_eligible=False, scope=scope,
                      scope_eligible=None, used_in_score=False, gate_reason="prediction_states_unavailable")
        return record
    flat = {h: normalise_state(s["state"]) for h, s in states.items()}
    profile = classify_profile(flat, hypothesis_ids)
    record["profile_class"] = profile
    record["comparatively_eligible"] = is_comparatively_eligible(profile)
    record["scope"] = scope
    record["scope_eligible"] = None if scope is None else normalise_scope_class(scope) in COMPARATIVE_SCOPE_CLASSES
    record["evidence_label"] = evidence_label
    record["has_contrast"] = has_contrast
    record["contrast_relevance"] = contrast_relevance

    if not record["comparatively_eligible"]:
        reason = "profile_{}".format(profile)
    elif scope is None:
        reason = "scope_unavailable"
    elif not record["scope_eligible"]:
        reason = "scope_{}".format(normalise_scope_class(scope))
    elif evidence_label is None:
        reason = "no_evidence_assessment"
    elif evidence_label in UNINFORMATIVE_EVIDENCE:
        reason = "uninformative_evidence"
    elif has_contrast is None:
        reason = "contrast_element_unavailable"
    elif not has_contrast:
        reason = "no_contrast_bearing_element"
    elif contrast_relevance is None:
        reason = "contrast_relevance_unavailable"
    elif contrast_relevance not in allowed_relevance:
        reason = "relevance_{}".format(contrast_relevance)
    else:
        reason = None
    record["used_in_score"] = reason is None
    record["gate_reason"] = reason or "scored"
    return record
