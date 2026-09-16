"""consequence_graph_v4_discrimination_gated (BENCH-GRAPH-V4-DEV-001).

v4 = the unchanged v3 pipeline (generation, v3 edge judgments, queries, retrieval,
evidence assessment) followed by a comparative layer that replaces v3's scoring:

  1. prediction states: for every proposition, what EVERY hypothesis commits to
     (`positive_or_present | negative_or_absent | substantive_null | indeterminate`),
     with strength only for determinate states;
  2. discrimination gate (deterministic): only propositions on which the hypotheses
     make determinate, different predictions are comparatively eligible;
  3. construct match: for propositions with informative evidence, whether the cited
     records address the proposition's construct; only `direct` may score;
  4. gated scoring: the verifier's own `score_hypotheses` on the gated propositions
     only, with each hypothesis's edge derived from its state. No chain routes, no
     pseudo-likelihood for `indeterminate`.

Nothing is deleted: ineligible propositions stay in the graph and are recorded in
one-sided / shared / all-indeterminate buckets with the evidence they received.

v3's code path is not modified. v3's scores are kept in the `scores_v3_reference`
artifact so both can be compared on the same generated graph.

`run_v4_layer` is shared with `scripts/replay_v4_on_frozen.py`, which applies the same
layer to the frozen v3 pilot artifacts.
"""
from __future__ import annotations

from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from src.common.errors import LLMError, LLMParseError
from src.common.logging_utils import get_logger
from src.evidence.construct_match import CONSTRUCT_PROMPT, assess_construct_match
from src.experiments.base import InstanceContext, InstanceResult
from src.graph.prediction_state import STATE_PROMPT, assess_prediction_states
from src.inference.discrimination import (
    COMPARATIVE_CONSTRUCT_MATCHES,
    DETERMINATE,
    StateError,
    UNINFORMATIVE_EVIDENCE,
    gate_node,
    score_gated,
    summarise_gates,
)
from src.literature.base import Paper
from src.methods.consequence_graph import ConsequenceGraphVerifier
from src.experiments.metrics import ranking_from_scores

LOGGER = get_logger("methods.consequence_graph_v4")

METHOD_VERSION = "consequence_graph_v4_discrimination_gated"
CONSTRUCT_POLICY = "direct_only"


def run_v4_layer(
    *,
    instance_id: str,
    presentation,
    graph_record: Mapping[str, Any],
    evidence_by_node: Mapping[str, Any],
    records_for: Callable[[str, Sequence[str]], Optional[str]],
    llm,
    prompts,
    mappings,
    multi_parent_rule: str,
    parent_false_baseline: float,
    max_workers: int = 1,
) -> Dict[str, Any]:
    """Apply the v4 comparative layer to one instance's graph and evidence.

    `records_for(node_id, cited_paper_ids)` returns the exact text of the records to
    show the construct-match judge (the cited records, or every shown record when the
    assessor cited none), or None if there are no records.
    """
    hypothesis_ids = [item.hypothesis_id for item in presentation.items]
    nodes = OrderedDict((n["id"], n) for n in graph_record["nodes"])
    errors: List[Dict[str, Any]] = []

    def one(node_id: str) -> Tuple[str, Dict[str, Any]]:
        node = nodes[node_id]
        entry: "OrderedDict[str, Any]" = OrderedDict([
            ("text", node["text"]), ("origin_hypothesis_id", node.get("generation_origin_hypothesis")),
        ])
        try:
            states, scope, call = assess_prediction_states(llm, prompts, proposition=node["text"],
                                                           presentation=presentation)
            entry["states"] = states
            entry["proposition_scope"] = scope["proposition_scope"] if scope else None
            entry["scope_basis"] = scope["scope_basis"] if scope else None
            entry["state_call_id"] = call.get("call_id")
        except (LLMError, LLMParseError, StateError) as exc:
            entry["states"] = None
            entry["proposition_scope"] = None
            errors.append({"where": "prediction_state", "node": node_id, "type": type(exc).__name__, "error": str(exc)})

        assessment = ((evidence_by_node.get(node_id) or {}).get("assessment") or {})
        label = assessment.get("evidence_label")
        entry["evidence_label"] = label
        entry["construct"] = None
        if label is not None and label not in UNINFORMATIVE_EVIDENCE:
            cited = list(assessment.get("key_papers") or [])
            text = records_for(node_id, cited)
            entry["construct_records"] = "cited" if cited else "all_shown_no_citation"
            if text:
                try:
                    construct, call = assess_construct_match(
                        llm, prompts, proposition=node["text"],
                        spans=list(assessment.get("supporting_spans") or []), records_text=text)
                    construct["call_id"] = call.get("call_id")
                    entry["construct"] = construct
                except (LLMError, LLMParseError, ValueError) as exc:
                    errors.append({"where": "construct_match", "node": node_id,
                                   "type": type(exc).__name__, "error": str(exc)})
        return node_id, entry

    ids = list(nodes)
    if max_workers > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            judged = OrderedDict(pool.map(one, ids))
    else:
        judged = OrderedDict(one(n) for n in ids)

    gates: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for node_id, entry in judged.items():
        gates[node_id] = gate_node(
            node_id=node_id, hypothesis_ids=hypothesis_ids, states=entry["states"],
            evidence_label=entry["evidence_label"],
            construct_match=(entry["construct"] or {}).get("construct_match"),
            scope=entry.get("proposition_scope"))

    propagation = score_gated(
        hypothesis_ids=hypothesis_ids, nodes={n: nodes[n]["text"] for n in nodes},
        states={n: e["states"] for n, e in judged.items() if e["states"]}, gates=gates,
        evidence_labels={n: e["evidence_label"] for n, e in judged.items()}, mappings=mappings,
        multi_parent_rule=multi_parent_rule, parent_false_baseline=parent_false_baseline,
        instance_id=instance_id)
    contributions: Dict[str, Dict[str, float]] = {}
    for c in propagation.contributions:
        contributions.setdefault(c.node_id, {})[c.hypothesis_id] = c.contribution

    node_records: "OrderedDict[str, Any]" = OrderedDict()
    buckets: "OrderedDict[str, List[Dict[str, Any]]]" = OrderedDict(
        (k, []) for k in ("one_sided_prediction", "shared_prediction", "all_indeterminate",
                          "generic_or_possibility_claim", "partially_indeterminate_contrast",
                          "states_unavailable"))
    for node_id, entry in judged.items():
        gate = gates[node_id]
        record = OrderedDict(entry)
        record.update((k, v) for k, v in gate.items() if k != "node_id")
        record["contribution"] = OrderedDict(
            (h, contributions.get(node_id, {}).get(h, 0.0)) for h in hypothesis_ids)
        node_records[node_id] = record
        if not gate["comparatively_eligible"]:
            bucket = gate["profile_class"] or "states_unavailable"
            states = entry["states"] or {}
            buckets[bucket].append(OrderedDict([
                ("node_id", node_id),
                ("predicting_hypotheses", OrderedDict((h, s["state"]) for h, s in states.items()
                                                      if s["state"] in DETERMINATE)),
                ("indeterminate_hypotheses", [h for h, s in states.items() if s["state"] == "indeterminate"]),
                ("evidence_label", entry["evidence_label"]),
                ("construct_match", (entry["construct"] or {}).get("construct_match")),
                ("why_gated", gate["gate_reason"]),
            ]))

    order = hypothesis_ids
    scores = dict(propagation.scores)
    return OrderedDict([
        ("method_version", METHOD_VERSION),
        ("prompts", {"prediction_state": STATE_PROMPT, "construct_match": CONSTRUCT_PROMPT}),
        ("construct_policy", CONSTRUCT_POLICY),
        ("comparative_construct_matches", sorted(COMPARATIVE_CONSTRUCT_MATCHES)),
        ("hypothesis_ids", hypothesis_ids),
        ("scores", scores),
        ("ranking", ranking_from_scores(scores, order=order)),
        ("log_scores", dict(propagation.log_scores)),
        ("contributions", propagation.record()["contributions"]),
        ("summary", summarise_gates(gates)),
        ("nodes", node_records),
        ("buckets", buckets),
        ("errors", errors),
        ("notes", list(propagation.notes) + [
            "one-sided, shared and all-indeterminate propositions are retained descriptively and "
            "contribute nothing to relative scores in v4; one-sided support may become informative "
            "under a future explicit background-probability model"]),
    ])


class ConsequenceGraphV4Verifier(ConsequenceGraphVerifier):
    name = "consequence_graph_v4"

    def prompt_versions(self) -> List[str]:
        return list(super().prompt_versions()) + [STATE_PROMPT, CONSTRUCT_PROMPT]

    def run_instance(self, ctx: InstanceContext) -> InstanceResult:
        result = super().run_instance(ctx)       # unchanged v3 pipeline
        v3_scores = result.artifacts.get("scores")
        if result.status != "ok" or not v3_scores:
            return result

        shown = {nid: [Paper(**p) for p in (entry.get("papers_shown") or [])]
                 for nid, entry in (result.artifacts.get("retrieval") or {}).get("by_node", {}).items()}

        def records_for(node_id: str, cited: Sequence[str]) -> Optional[str]:
            papers = shown.get(node_id) or []
            chosen = [p for p in papers if p.paper_id in set(cited)] if cited else papers
            if not chosen:
                return None
            # Same cutoff-enforcing renderer the evidence assessor used.
            return ctx.literature.render(chosen)

        layer = run_v4_layer(
            instance_id=ctx.instance.id, presentation=ctx.presentation,
            graph_record=result.artifacts["graph"], evidence_by_node=result.artifacts["evidence"]["by_node"],
            records_for=records_for, llm=ctx.llm, prompts=ctx.prompts, mappings=ctx.mappings,
            multi_parent_rule=ctx.config.inference.multi_parent_rule,
            parent_false_baseline=ctx.config.inference.parent_false_baseline)

        for err in layer["errors"]:
            ctx.errors.append(dict(err, instance_id=ctx.instance.id))
        result.errors = list(ctx.errors)
        result.artifacts["scores_v3_reference"] = v3_scores
        result.artifacts["discrimination"] = layer
        result.scores = dict(layer["scores"])
        result.ranking = list(layer["ranking"])
        result.artifacts["scores"] = OrderedDict([
            ("method", self.name),
            ("method_version", METHOD_VERSION),
            ("scores", result.scores),
            ("ranking", result.ranking),
            ("log_scores", layer["log_scores"]),
            ("contributions", layer["contributions"]),
            ("inference", OrderedDict([
                ("aggregation", "independent"),
                ("multi_parent_rule", ctx.config.inference.multi_parent_rule),
                ("parent_false_baseline", ctx.config.inference.parent_false_baseline),
                ("ordinal_mappings", ctx.mappings.record()),
                ("construct_policy", CONSTRUCT_POLICY),
            ])),
            ("label_to_hypothesis_id", ctx.presentation.label_to_id),
            ("v3_reference_scores", v3_scores.get("scores")),
        ])
        summary = layer["summary"]
        result.diagnostics.update({"n_v4_" + k[2:] if k.startswith("n_") else "v4_" + k: v
                                   for k, v in summary.items()})
        return result
