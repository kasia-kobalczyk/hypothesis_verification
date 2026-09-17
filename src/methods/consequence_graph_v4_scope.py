"""consequence_graph_v4_scope (BENCH-GRAPH-V4-SCOPE-001).

v4-scope = the unchanged v3 pipeline, then a comparative layer that extends v4 with:

  1. prediction states          -- v4's head prompt (prediction_state_v2), unchanged;
  2. proposition scope          -- separate judgment; only hypothesis_specific or
                                   mechanism_specific propositions may score;
  3. contrast-bearing element   -- the variable that actually separates the candidates;
  4. contrast relevance         -- evidence judged against that element; only
                                   contrast_direct may score;
  5. gated scoring              -- verifier's score_hypotheses on gated nodes only.

For the specificity-assessability diagnostic, scope is classified for every proposition,
and element + relevance for every proposition with informative evidence, whether or not
it is otherwise eligible. Only the gate decides what scores.

The previous v4 method (`consequence_graph_v4`) is not modified.
"""
from __future__ import annotations

from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from src.common.errors import LLMError, LLMParseError
from src.evidence.contrast_relevance import RELEVANCE_PROMPT, assess_contrast_relevance
from src.experiments.base import InstanceContext, InstanceResult
from src.experiments.metrics import ranking_from_scores
from src.graph.prediction_state import assess_prediction_states
from src.graph.proposition_scope import ELEMENT_PROMPT, SCOPE_PROMPT, assess_scope, extract_contrast_element
from src.inference.discrimination import (
    COMPARATIVE_RELEVANCE,
    COMPARATIVE_SCOPE_CLASSES,
    DETERMINATE,
    SENSITIVITY_RELEVANCE,
    StateError,
    UNINFORMATIVE_EVIDENCE,
    gate_node_scope,
    score_gated,
)
from src.literature.base import Paper
from src.methods.consequence_graph import ConsequenceGraphVerifier

METHOD_VERSION = "consequence_graph_v4_scope"
STATE_PROMPT = "prediction_state_v2"    # v4 head, pinned by name so v4-scope cannot drift with it
LLM_ERRORS = (LLMError, LLMParseError, StateError, ValueError)


def _summary(gates: Mapping[str, Mapping[str, Any]]) -> "OrderedDict[str, int]":
    from collections import Counter

    out: "OrderedDict[str, int]" = OrderedDict()
    out["n_nodes"] = len(gates)
    out["n_comparatively_eligible"] = sum(1 for g in gates.values() if g.get("comparatively_eligible"))
    out["n_comparative_and_scope_eligible"] = sum(
        1 for g in gates.values() if g.get("comparatively_eligible") and g.get("scope_eligible"))
    out["n_used_in_score"] = sum(1 for g in gates.values() if g["used_in_score"])
    for key, value in sorted(Counter(g.get("scope") for g in gates.values()).items(), key=lambda kv: str(kv[0])):
        out["n_scope_{}".format(key)] = value
    for key, value in sorted(Counter(g.get("contrast_relevance") for g in gates.values()
                                     if g.get("contrast_relevance")).items()):
        out["n_relevance_{}".format(key)] = value
    for key, value in sorted(Counter(g["gate_reason"] for g in gates.values()).items()):
        out["n_gate_{}".format(key)] = value
    return out


def run_v4_scope_layer(
    *,
    instance_id: str,
    question: str,
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
    hypothesis_ids = [item.hypothesis_id for item in presentation.items]
    nodes = OrderedDict((n["id"], n) for n in graph_record["nodes"])
    errors: List[Dict[str, Any]] = []

    def err(where, node_id, exc):
        errors.append({"where": where, "node": node_id, "type": type(exc).__name__, "error": str(exc)})

    def one(node_id: str) -> Tuple[str, Dict[str, Any]]:
        node = nodes[node_id]
        entry: "OrderedDict[str, Any]" = OrderedDict([
            ("text", node["text"]), ("origin_hypothesis_id", node.get("generation_origin_hypothesis")),
            ("abstraction_level", (node.get("metadata") or {}).get("abstraction_level")),
            ("states", None), ("scope", None), ("contrast_element", None), ("contrast_relevance", None),
        ])
        try:
            states, _, call = assess_prediction_states(llm, prompts, proposition=node["text"],
                                                       presentation=presentation, prompt_name=STATE_PROMPT)
            entry["states"] = states
            entry["state_call_id"] = call.get("call_id")
        except LLM_ERRORS as exc:
            err("prediction_state", node_id, exc)
        try:
            entry["scope"], call = assess_scope(llm, prompts, question=question, proposition=node["text"],
                                                presentation=presentation)
            entry["scope"]["call_id"] = call.get("call_id")
        except LLM_ERRORS as exc:
            err("scope", node_id, exc)

        assessment = ((evidence_by_node.get(node_id) or {}).get("assessment") or {})
        label = assessment.get("evidence_label")
        entry["evidence_label"] = label
        entry["historical_evidence_informative"] = label is not None and label not in UNINFORMATIVE_EVIDENCE
        if entry["historical_evidence_informative"] and entry["states"]:
            try:
                entry["contrast_element"], call = extract_contrast_element(
                    llm, prompts, proposition=node["text"], presentation=presentation, states=entry["states"])
                entry["contrast_element"]["call_id"] = call.get("call_id")
            except LLM_ERRORS as exc:
                err("contrast_element", node_id, exc)
            if entry["contrast_element"]:
                cited = list(assessment.get("key_papers") or [])
                text = records_for(node_id, cited)
                entry["relevance_records"] = "cited" if cited else "all_shown_no_citation"
                if text:
                    try:
                        entry["contrast_relevance"], call = assess_contrast_relevance(
                            llm, prompts, proposition=node["text"], element=entry["contrast_element"],
                            spans=list(assessment.get("supporting_spans") or []), records_text=text)
                        entry["contrast_relevance"]["call_id"] = call.get("call_id")
                    except LLM_ERRORS as exc:
                        err("contrast_relevance", node_id, exc)
        return node_id, entry

    ids = list(nodes)
    if max_workers > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            judged = OrderedDict(pool.map(one, ids))
    else:
        judged = OrderedDict(one(n) for n in ids)

    def gates_for(allowed):
        return OrderedDict((nid, gate_node_scope(
            node_id=nid, hypothesis_ids=hypothesis_ids, states=e["states"],
            scope=(e["scope"] or {}).get("scope"), evidence_label=e["evidence_label"],
            contrast_relevance=(e["contrast_relevance"] or {}).get("contrast_relevance"),
            allowed_relevance=allowed)) for nid, e in judged.items())

    def score(gates):
        return score_gated(
            hypothesis_ids=hypothesis_ids, nodes={n: nodes[n]["text"] for n in nodes},
            states={n: e["states"] for n, e in judged.items() if e["states"]}, gates=gates,
            evidence_labels={n: e["evidence_label"] for n, e in judged.items()}, mappings=mappings,
            multi_parent_rule=multi_parent_rule, parent_false_baseline=parent_false_baseline,
            instance_id=instance_id)

    gates = gates_for(COMPARATIVE_RELEVANCE)
    main = score(gates)
    sens_gates = gates_for(SENSITIVITY_RELEVANCE)
    sens = score(sens_gates)

    contributions: Dict[str, Dict[str, float]] = {}
    for c in main.contributions:
        contributions.setdefault(c.node_id, {})[c.hypothesis_id] = c.contribution

    node_records: "OrderedDict[str, Any]" = OrderedDict()
    for nid, entry in judged.items():
        record = OrderedDict(entry)
        record.update((k, v) for k, v in gates[nid].items() if k not in ("node_id", "scope", "contrast_relevance",
                                                                          "evidence_label"))
        record["sensitivity_used_in_score"] = sens_gates[nid]["used_in_score"]
        record["contribution"] = OrderedDict((h, contributions.get(nid, {}).get(h, 0.0)) for h in hypothesis_ids)
        node_records[nid] = record

    buckets: "OrderedDict[str, List[Dict[str, Any]]]" = OrderedDict()
    for nid, g in gates.items():
        if g["used_in_score"]:
            continue
        states = judged[nid]["states"] or {}
        buckets.setdefault(g["gate_reason"], []).append(OrderedDict([
            ("node_id", nid),
            ("predicting_hypotheses", OrderedDict((h, s["state"]) for h, s in states.items()
                                                  if s["state"] in DETERMINATE)),
            ("indeterminate_hypotheses", [h for h, s in states.items() if s["state"] == "indeterminate"]),
            ("scope", g.get("scope")), ("evidence_label", g.get("evidence_label")),
            ("contrast_relevance", g.get("contrast_relevance")),
        ]))

    return OrderedDict([
        ("method_version", METHOD_VERSION),
        ("prompts", OrderedDict([("prediction_state", STATE_PROMPT), ("scope", SCOPE_PROMPT),
                                 ("contrast_element", ELEMENT_PROMPT), ("contrast_relevance", RELEVANCE_PROMPT)])),
        ("comparative_scope_classes", sorted(COMPARATIVE_SCOPE_CLASSES)),
        ("comparative_relevance", sorted(COMPARATIVE_RELEVANCE)),
        ("hypothesis_ids", hypothesis_ids),
        ("scores", dict(main.scores)),
        ("ranking", ranking_from_scores(dict(main.scores), order=hypothesis_ids)),
        ("log_scores", dict(main.log_scores)),
        ("contributions", main.record()["contributions"]),
        ("summary", _summary(gates)),
        ("sensitivity_contrast_partial_allowed", OrderedDict([
            ("NOT_THE_METHOD", "sensitivity analysis only (directive section 9)"),
            ("scores", dict(sens.scores)),
            ("n_used_in_score", sum(1 for g in sens_gates.values() if g["used_in_score"])),
        ])),
        ("nodes", node_records),
        ("buckets", buckets),
        ("errors", errors),
    ])


class ConsequenceGraphV4ScopeVerifier(ConsequenceGraphVerifier):
    name = "consequence_graph_v4_scope"

    def prompt_versions(self) -> List[str]:
        return list(super().prompt_versions()) + [STATE_PROMPT, SCOPE_PROMPT, ELEMENT_PROMPT, RELEVANCE_PROMPT]

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
            return ctx.literature.render(chosen) if chosen else None

        layer = run_v4_scope_layer(
            instance_id=ctx.instance.id, question=ctx.instance.question, presentation=ctx.presentation,
            graph_record=result.artifacts["graph"], evidence_by_node=result.artifacts["evidence"]["by_node"],
            records_for=records_for, llm=ctx.llm, prompts=ctx.prompts, mappings=ctx.mappings,
            multi_parent_rule=ctx.config.inference.multi_parent_rule,
            parent_false_baseline=ctx.config.inference.parent_false_baseline)
        for e in layer["errors"]:
            ctx.errors.append(dict(e, instance_id=ctx.instance.id))
        result.errors = list(ctx.errors)
        result.artifacts["scores_v3_reference"] = v3_scores
        result.artifacts["discrimination"] = layer
        result.scores = dict(layer["scores"])
        result.ranking = list(layer["ranking"])
        result.artifacts["scores"] = OrderedDict([
            ("method", self.name), ("method_version", METHOD_VERSION),
            ("scores", result.scores), ("ranking", result.ranking), ("log_scores", layer["log_scores"]),
            ("contributions", layer["contributions"]),
            ("inference", OrderedDict([
                ("aggregation", "independent"),
                ("multi_parent_rule", ctx.config.inference.multi_parent_rule),
                ("parent_false_baseline", ctx.config.inference.parent_false_baseline),
                ("ordinal_mappings", ctx.mappings.record()),
                ("comparative_scope_classes", sorted(COMPARATIVE_SCOPE_CLASSES)),
                ("comparative_relevance", sorted(COMPARATIVE_RELEVANCE)),
            ])),
            ("label_to_hypothesis_id", ctx.presentation.label_to_id),
            ("v3_reference_scores", v3_scores.get("scores")),
            ("sensitivity_contrast_partial_allowed_scores", layer["sensitivity_contrast_partial_allowed"]["scores"]),
        ])
        result.diagnostics.update({"n_v4s_" + k[2:]: v for k, v in layer["summary"].items()
                                   if k in ("n_nodes", "n_comparatively_eligible", "n_comparative_and_scope_eligible",
                                            "n_used_in_score")})
        return result
