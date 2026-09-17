"""v4-scope: separate scope classification and contrast-focused evidence relevance
(BENCH-GRAPH-V4-SCOPE-001).

The directive's required checks, as executable tests:

* scope is a separate judgment, not a field of the prediction-state response, and the
  prediction-state prompt is the v4 head's, unchanged;
* broader-class facts, possibility claims and invalid propositions never score, even
  with a determinate contrast and direct evidence;
* contrast elements are parsed strictly;
* context-only, construct-mismatch and partial contrast evidence never move the main score;
* scope can never make a one-sided (or shared) prediction comparative;
* prompts obey the hidden-annotation, cutoff and no-development-case-content invariants.
"""
from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.benchmark.presentation import Presentation, PresentedHypothesis
from src.common.config import AppConfig
from src.evidence.contrast_relevance import RELEVANCE_PROMPT, parse_contrast_relevance
from src.graph.proposition_scope import (
    ELEMENT_FIELDS,
    ELEMENT_PROMPT,
    SCOPE_PROMPT,
    parse_contrast_element,
    parse_scope_class,
)
from src.inference import discrimination as d
from src.inference.parameters import load_ordinal_mappings
from src.llm.prompts import PromptLibrary

ROOT = Path(__file__).resolve().parents[1]
H = ["H1", "H2"]
CONTRAST = {"H1": {"state": "positive_or_present", "strength": "strong"},
            "H2": {"state": "negative_or_absent", "strength": "moderate"}}
ONE_SIDED = {"H1": {"state": "positive_or_present", "strength": "strong"},
             "H2": {"state": "indeterminate", "strength": None}}
SHARED = {"H1": {"state": "positive_or_present", "strength": "strong"},
          "H2": {"state": "positive_or_present", "strength": "strong"}}


@pytest.fixture(scope="module")
def mappings():
    return load_ordinal_mappings(str(ROOT / "configs" / "ordinal_mappings.yaml"))


def _pres():
    return Presentation("case", [PresentedHypothesis("A", "H1", "first", False),
                                 PresentedHypothesis("B", "H2", "second", False)], seed_key="s", order="as_loaded")


def _gate(states=CONTRAST, scope="hypothesis_specific", label="support", relevance="contrast_direct",
          has_contrast=True, **kw):
    return d.gate_node_scope(node_id="X1", hypothesis_ids=H, states=states, scope=scope, evidence_label=label,
                             has_contrast=has_contrast, contrast_relevance=relevance, **kw)


# --------------------------------------------------------------------------- #
# Gate
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("scope", ["hypothesis_specific", "mechanism_specific"])
def test_specific_scope_with_direct_contrast_evidence_scores(scope):
    g = _gate(scope=scope)
    assert g["used_in_score"] and g["gate_reason"] == "scored" and g["scope_eligible"]


@pytest.mark.parametrize("scope", ["broader_class_fact", "possibility_claim", "invalid_or_underspecified"])
def test_broad_possibility_and_invalid_propositions_never_score(scope):
    g = _gate(scope=scope, label="strong_support", relevance="contrast_direct")
    assert g["comparatively_eligible"] and g["scope_eligible"] is False and not g["used_in_score"]
    assert g["gate_reason"] == "scope_{}".format(scope)
    # ... and not under the partial-evidence sensitivity policy either
    assert not _gate(scope=scope, allowed_relevance=d.SENSITIVITY_RELEVANCE)["used_in_score"]


@pytest.mark.parametrize("relevance", ["contrast_partial", "context_only", "construct_mismatch", "no_evidence", None])
def test_only_contrast_direct_evidence_moves_the_main_score(relevance):
    g = _gate(relevance=relevance)
    assert not g["used_in_score"]
    assert g["gate_reason"] == ("relevance_{}".format(relevance) if relevance else "contrast_relevance_unavailable")


@pytest.mark.parametrize("relevance,expected", [("contrast_partial", True), ("context_only", False),
                                                 ("construct_mismatch", False), ("no_evidence", False)])
def test_partial_is_admitted_only_by_the_sensitivity_policy(relevance, expected):
    assert _gate(relevance=relevance, allowed_relevance=d.SENSITIVITY_RELEVANCE)["used_in_score"] is expected


@pytest.mark.parametrize("states,profile", [(ONE_SIDED, d.ONE_SIDED), (SHARED, d.SHARED)])
@pytest.mark.parametrize("scope", ["hypothesis_specific", "mechanism_specific"])
def test_scope_never_makes_a_non_contrast_comparative(states, profile, scope):
    g = _gate(states=states, scope=scope, label="strong_support", relevance="contrast_direct")
    assert g["profile_class"] == profile and not g["comparatively_eligible"] and not g["used_in_score"]
    assert g["gate_reason"] == "profile_{}".format(profile)


@pytest.mark.parametrize("label", ["no_evidence", "mixed", None])
def test_uninformative_evidence_never_scores(label):
    assert not _gate(label=label)["used_in_score"]


def test_missing_judgments_fail_closed():
    assert _gate(states=None)["gate_reason"] == "prediction_states_unavailable"
    assert _gate(scope=None)["gate_reason"] == "scope_unavailable"
    assert _gate(has_contrast=None)["gate_reason"] == "contrast_element_unavailable"
    with pytest.raises(d.StateError):
        _gate(scope="fairly_specific")


def test_element_without_a_contrast_never_scores_even_with_direct_relevance():
    for allowed in (d.COMPARATIVE_RELEVANCE, d.SENSITIVITY_RELEVANCE):
        g = _gate(has_contrast=False, relevance="contrast_direct", allowed_relevance=allowed)
        assert not g["used_in_score"] and g["gate_reason"] == "no_contrast_bearing_element"


def test_gate_ignores_the_origin_of_a_proposition():
    """Scope comes from what a proposition asserts; the gate has no origin input at all."""
    import inspect
    assert "origin" not in inspect.signature(d.gate_node_scope).parameters


# --------------------------------------------------------------------------- #
# Relevance categories are derived from the structured answers
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("answers,expected", [
    (("yes", "yes", "no"), "contrast_direct"),
    (("yes", "no", "no"), "contrast_direct"),
    (("partly", "yes", "no"), "contrast_partial"),
    (("partly", "no", "yes"), "contrast_partial"),
    (("no", "yes", "no"), "context_only"),
    (("no", "yes", "yes"), "construct_mismatch"),
    (("no", "no", "yes"), "construct_mismatch"),
    (("no", "no", "no"), "no_evidence"),
])
def test_relevance_category_is_derived_in_code(answers, expected):
    assert d.derive_contrast_relevance(*answers) == expected
    parsed = parse_contrast_relevance(dict(zip(("contrast_variable_reported", "shared_context_supported",
                                                "different_construct"), answers)))
    assert parsed["contrast_relevance"] == expected


@pytest.mark.parametrize("answers", [("maybe", "yes", "no"), ("yes", "partly", "no"), (None, "no", "no"),
                                     ("no", "no", None)])
def test_malformed_relevance_answers_are_rejected(answers):
    with pytest.raises(ValueError):
        d.derive_contrast_relevance(*answers)


# --------------------------------------------------------------------------- #
# Scope and element parsing
# --------------------------------------------------------------------------- #
def _scope_payload(scope="hypothesis_specific", occurs=True):
    return {"scope": scope, "system_under_dispute": "s", "proposition_is_about": "p",
            "asserts_actual_occurrence_in_system_under_dispute": occurs, "rationale": "r"}


def test_parse_scope_class_accepts_every_class():
    for scope in d.SCOPE_CLASSES:
        assert parse_scope_class(_scope_payload(scope))["scope"] == scope


@pytest.mark.parametrize("payload", [_scope_payload("within_candidates_scope"), _scope_payload(None),
                                     _scope_payload(occurs="yes"), {k: v for k, v in _scope_payload().items()
                                                                    if k != "asserts_actual_occurrence_in_system_under_dispute"}])
def test_parse_scope_class_rejects_malformed_output(payload):
    with pytest.raises(d.StateError):
        parse_scope_class(payload)


def _element(**over):
    out = {"has_contrast": True, "shared_context": "c", "contrast_variable": "v", "contrast_direction_or_state": "s",
           "system_or_population": "p", "measurement_or_observable": "m"}
    out.update(over)
    return out


def test_parse_contrast_element_keeps_exactly_the_directive_fields():
    parsed = parse_contrast_element(_element(extra="ignored"))
    assert list(parsed) == ["has_contrast"] + list(ELEMENT_FIELDS)
    assert ELEMENT_FIELDS == ("shared_context", "contrast_variable", "contrast_direction_or_state",
                              "system_or_population", "measurement_or_observable")


@pytest.mark.parametrize("payload", [_element(has_contrast="true"), _element(contrast_variable=""),
                                     _element(shared_context=None), {"has_contrast": False}])
def test_parse_contrast_element_rejects_malformed_output(payload):
    with pytest.raises(ValueError):
        parse_contrast_element(payload)


# --------------------------------------------------------------------------- #
# The layer, with a scripted LLM
# --------------------------------------------------------------------------- #
def _entry(i, state, strength="strong"):
    return {"id": i, "state": state, "strength": None if state == "indeterminate" else strength,
            "basis": "b", "rationale": "r"}


def _states(a, b):
    return {"states": [_entry("A", a), _entry("B", b)]}


def _rel(reported, context="yes", different="no"):
    return {"contrast_variable_reported": reported, "shared_context_supported": context,
            "different_construct": different, "what_the_records_report": "w", "rationale": "r"}


class ScriptedLLM:
    PURPOSES = {"graph_v4.prediction_state": "states", "graph_v4s.scope": "scopes",
                "graph_v4s.contrast_element": "elements", "graph_v4s.contrast_relevance": "relevance"}

    def __init__(self, fail=(), **tables):
        self.tables, self.fail, self.calls = tables, set(fail), []

    def complete_json(self, messages, *, purpose, prompt_version=None, validator=None):
        from src.common.errors import LLMError

        table = self.tables[self.PURPOSES[purpose]]
        text = messages[-1]["content"]
        key = next(k for k in table if "\n{}\n".format(k) in text)
        self.calls.append((purpose, key, prompt_version))
        if (purpose, key) in self.fail:
            raise LLMError("scripted failure")
        if validator:
            validator(table[key])
        return SimpleNamespace(parsed=table[key], record=lambda: {"call_id": "c"})


def _layer(llm, mappings, evidence, n=4):
    from src.methods.consequence_graph_v4_scope import run_v4_scope_layer

    graph = {"nodes": [{"id": "X{}".format(i), "text": "p{}".format(i), "generation_origin_hypothesis": "H1",
                        "metadata": {"abstraction_level": "specific"}} for i in range(1, n + 1)]}
    return run_v4_scope_layer(
        instance_id="case", question="Why does the phenomenon happen?", presentation=_pres(), graph_record=graph,
        evidence_by_node=evidence, records_for=lambda node, cited: "[1] record", llm=llm,
        prompts=PromptLibrary(ROOT / "src" / "llm" / "prompts"), mappings=mappings,
        multi_parent_rule="noisy_or", parent_false_baseline=0.5)


def _ev(label, cited=("s2:1",)):
    return {"assessment": {"evidence_label": label, "key_papers": list(cited), "supporting_spans": ["q"]}}


CON = ("positive_or_present", "negative_or_absent")


def test_layer_scores_only_specific_contrasts_with_direct_contrast_evidence(mappings):
    llm = ScriptedLLM(
        states={"p1": _states(*CON), "p2": _states(*CON), "p3": _states(*CON), "p4": _states(*CON)},
        scopes={"p1": _scope_payload("hypothesis_specific"), "p2": _scope_payload("broader_class_fact"),
                "p3": _scope_payload("mechanism_specific"), "p4": _scope_payload("possibility_claim", False)},
        elements={k: _element() for k in ("p1", "p2", "p3", "p4")},
        relevance={"p1": _rel("yes"), "p2": _rel("yes"), "p3": _rel("partly"), "p4": _rel("yes")})
    out = _layer(llm, mappings, {n: _ev("support") for n in ("X1", "X2", "X3", "X4")})
    assert [n for n, r in out["nodes"].items() if r["used_in_score"]] == ["X1"]
    assert out["scores"]["H1"] > out["scores"]["H2"]
    assert out["nodes"]["X2"]["gate_reason"] == "scope_broader_class_fact"
    assert out["nodes"]["X3"]["gate_reason"] == "relevance_contrast_partial"
    assert out["nodes"]["X3"]["sensitivity_used_in_score"] and not out["nodes"]["X2"]["sensitivity_used_in_score"]
    assert out["sensitivity_contrast_partial_allowed"]["n_used_in_score"] == 2
    assert out["nodes"]["X2"]["contribution"] == {"H1": 0.0, "H2": 0.0}
    assert set(out["nodes"]) == {"X1", "X2", "X3", "X4"}                       # nothing deleted
    assert {b["node_id"] for bs in out["buckets"].values() for b in bs} == {"X2", "X3", "X4"}
    # the assessability diagnostic covers ineligible scopes too
    assert out["nodes"]["X2"]["contrast_relevance"]["contrast_relevance"] == "contrast_direct"


def test_context_only_and_construct_mismatch_leave_scores_even(mappings):
    llm = ScriptedLLM(
        states={"p1": _states(*CON), "p2": _states(*CON)},
        scopes={"p1": _scope_payload(), "p2": _scope_payload("mechanism_specific")},
        elements={"p1": _element(), "p2": _element()},
        relevance={"p1": _rel("no", "yes", "no"), "p2": _rel("no", "no", "yes")})
    out = _layer(llm, mappings, {"X1": _ev("strong_support"), "X2": _ev("strong_contradiction")}, n=2)
    assert out["nodes"]["X1"]["gate_reason"] == "relevance_context_only"
    assert out["nodes"]["X2"]["gate_reason"] == "relevance_construct_mismatch"
    assert out["scores"] == {"H1": 0.5, "H2": 0.5}
    assert out["sensitivity_contrast_partial_allowed"]["scores"] == {"H1": 0.5, "H2": 0.5}


def test_layer_does_not_score_an_element_without_a_contrast(mappings):
    llm = ScriptedLLM(states={"p1": _states(*CON)}, scopes={"p1": _scope_payload()},
                      elements={"p1": _element(has_contrast=False)}, relevance={"p1": _rel("yes")})
    out = _layer(llm, mappings, {"X1": _ev("strong_support")}, n=1)
    assert out["nodes"]["X1"]["gate_reason"] == "no_contrast_bearing_element"
    assert out["scores"] == {"H1": 0.5, "H2": 0.5}


def test_one_sided_specific_proposition_is_not_scored(mappings):
    llm = ScriptedLLM(states={"p1": _states("positive_or_present", "indeterminate")},
                      scopes={"p1": _scope_payload("hypothesis_specific")},
                      elements={"p1": _element()}, relevance={"p1": _rel("yes")})
    out = _layer(llm, mappings, {"X1": _ev("strong_support")}, n=1)
    assert out["nodes"]["X1"]["gate_reason"] == "profile_one_sided_prediction"
    assert out["scores"] == {"H1": 0.5, "H2": 0.5}


def test_no_element_or_relevance_call_without_informative_evidence(mappings):
    llm = ScriptedLLM(states={"p1": _states(*CON), "p2": _states(*CON)},
                      scopes={"p1": _scope_payload(), "p2": _scope_payload()},
                      elements={"p1": _element(), "p2": _element()}, relevance={"p1": _rel("yes"), "p2": _rel("yes")})
    out = _layer(llm, mappings, {"X1": _ev("no_evidence"), "X2": _ev("mixed")}, n=2)
    purposes = {c[0] for c in llm.calls}
    assert purposes == {"graph_v4.prediction_state", "graph_v4s.scope"}
    assert {r["gate_reason"] for r in out["nodes"].values()} == {"uninformative_evidence"}


def test_layer_fails_closed_on_each_llm_error(mappings):
    tables = dict(states={k: _states(*CON) for k in ("p1", "p2", "p3", "p4")},
                  scopes={k: _scope_payload() for k in ("p1", "p2", "p3", "p4")},
                  elements={k: _element() for k in ("p1", "p2", "p3", "p4")},
                  relevance={k: _rel("yes") for k in ("p1", "p2", "p3", "p4")})
    llm = ScriptedLLM(fail={("graph_v4.prediction_state", "p1"), ("graph_v4s.scope", "p2"),
                            ("graph_v4s.contrast_element", "p3"), ("graph_v4s.contrast_relevance", "p4")}, **tables)
    out = _layer(llm, mappings, {n: _ev("support") for n in ("X1", "X2", "X3", "X4")})
    assert [out["nodes"]["X{}".format(i)]["gate_reason"] for i in range(1, 5)] == [
        "prediction_states_unavailable", "scope_unavailable", "contrast_element_unavailable",
        "contrast_relevance_unavailable"]
    assert out["scores"] == {"H1": 0.5, "H2": 0.5}
    assert {e["where"] for e in out["errors"]} == {"prediction_state", "scope", "contrast_element",
                                                   "contrast_relevance"}


def test_scope_is_a_separate_call_and_states_use_the_v4_head_prompt(mappings):
    import src.graph.prediction_state as ps
    import src.methods.consequence_graph_v4_scope as v4s

    llm = ScriptedLLM(states={"p1": _states(*CON)}, scopes={"p1": _scope_payload()},
                      elements={"p1": _element()}, relevance={"p1": _rel("yes")})
    out = _layer(llm, mappings, {"X1": _ev("support")}, n=1)
    by_purpose = {c[0]: c[2] for c in llm.calls}
    assert by_purpose["graph_v4.prediction_state"] == "prediction_state_v2" == ps.STATE_PROMPT == v4s.STATE_PROMPT
    assert by_purpose["graph_v4s.scope"] == SCOPE_PROMPT
    # the state response carries no scope, and the state prompt asks for none
    assert "proposition_scope" not in out["nodes"]["X1"]["states"]["H1"]
    state_text = PromptLibrary(ROOT / "src" / "llm" / "prompts").get(ps.STATE_PROMPT).text
    assert not any(cls in state_text for cls in d.SCOPE_CLASSES)


# --------------------------------------------------------------------------- #
# Registration, prompts, code invariants
# --------------------------------------------------------------------------- #
def test_v4_and_v4_scope_are_both_registered_and_distinct():
    from src.experiments.runner import METHODS
    from src.methods.consequence_graph_v4 import ConsequenceGraphV4Verifier
    from src.methods.consequence_graph_v4_scope import ConsequenceGraphV4ScopeVerifier

    assert METHODS["consequence_graph_v4"] is ConsequenceGraphV4Verifier
    assert METHODS["consequence_graph_v4_scope"] is ConsequenceGraphV4ScopeVerifier
    v4 = ConsequenceGraphV4Verifier(AppConfig()).prompt_versions()
    v4s = ConsequenceGraphV4ScopeVerifier(AppConfig()).prompt_versions()
    assert v4s[-4:] == ["prediction_state_v2", SCOPE_PROMPT, ELEMENT_PROMPT, RELEVANCE_PROMPT]
    assert "construct_match_v2" in v4 and "construct_match_v2" not in v4s


NEW_PROMPTS = (SCOPE_PROMPT, ELEMENT_PROMPT, RELEVANCE_PROMPT)


def test_v4_scope_prompts_obey_hidden_annotation_and_cutoff_invariants():
    library = PromptLibrary(ROOT / "src" / "llm" / "prompts")
    forbidden = {"resolution", "resolver", "resolving_observations", "resolution_type", "reference_discriminators",
                 "leakage_audit", "gold", "gold_hypothesis", "answer", "correct_hypothesis", "favored", "cutoff"}
    for name in NEW_PROMPTS:
        template = library.get(name)
        assert not ({p.lower() for p in template.placeholders} & forbidden), name
        text = template.text.lower()
        assert "cutoff" not in text and "json" in text, name
        assert not re.search(r"\b(19|20)\d\d\b", text), name          # no dates


# Distinctive terms from the 8 development cases (visible phenomenon text only).
DEV_CASE_TERMS = ("prefrontal", "precentral", "working memory", "gcn4", "med15", "mediator", "condensate",
                  "phase-separation", "eukaryo", "mitochondri", "endosymbio", "archae", "hemisphere",
                  "glutamine", "glnbp", "induced fit", "conformational selection", "spider", "orb", "cribellate",
                  "fragmentation", "forest", "fly", "drosophila", "wing")


def test_v4_scope_prompts_contain_no_development_case_content():
    library = PromptLibrary(ROOT / "src" / "llm" / "prompts")
    for name in NEW_PROMPTS:
        text = library.get(name).text.lower()
        for term in DEV_CASE_TERMS:
            assert not re.search(r"\b{}".format(re.escape(term)), text), (name, term)


def test_development_case_terms_come_from_the_visible_cases():
    import json
    visible = " ".join(json.loads(line)["phenomenon"].lower()
                       for line in (ROOT / "benchmark" / "explanatory" / "cases_visible.jsonl").open())
    assert sum(term in visible for term in DEV_CASE_TERMS) >= 15


def test_v4_scope_code_never_names_hidden_annotations_or_audit_prompts():
    for path in ("src/methods/consequence_graph_v4_scope.py", "src/inference/discrimination.py",
                 "src/graph/proposition_scope.py", "src/evidence/contrast_relevance.py"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert "cases_hidden" not in text and "prompts_audit" not in text, path
