"""v4 discrimination-gated verifier (BENCH-GRAPH-V4-DEV-001).

The directive's acceptance criteria, as executable checks:

* prediction state is separate from strength, and `indeterminate` has no likelihood;
* an indeterminate hypothesis contributes zero relative score, including the D046
  "neutral-mapping pseudo-discrimination" case that v3 scored;
* gating happens before aggregation, and only determinate contrasts are eligible;
* construct `partial` and `mismatch` evidence cannot move scores (direct only);
* one-sided propositions are retained descriptively, not deleted;
* malformed or missing judgments fail closed;
* v3 stays registered and untouched; v4 prompts obey the hidden-annotation and
  cutoff invariants.
"""
from __future__ import annotations

import math
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.benchmark.presentation import Presentation, PresentedHypothesis
from src.common.config import AppConfig, load_config
from src.graph.prediction_state import parse_states
from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode
from src.inference import discrimination as d
from src.inference.bayes import score_hypotheses
from src.inference.parameters import load_ordinal_mappings
from src.evidence.construct_match import CONSTRUCT_PROMPT, derive_construct_match, parse_construct_match
from src.graph.prediction_state import STATE_PROMPT

ROOT = Path(__file__).resolve().parents[1]
H = ["H1", "H2"]


@pytest.fixture(scope="module")
def mappings():
    return load_ordinal_mappings(str(ROOT / "configs" / "ordinal_mappings.yaml"))


def _pres():
    return Presentation("case", [PresentedHypothesis("A", "H1", "first", False),
                                 PresentedHypothesis("B", "H2", "second", False)], seed_key="s", order="as_loaded")


def _s(state, strength=None):
    return {"state": state, "strength": strength}


# --------------------------------------------------------------------------- #
# State vocabulary
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("states,expected", [
    ({"H1": "positive_or_present", "H2": "negative_or_absent"}, d.COMPARATIVE),
    ({"H1": "positive_or_present", "H2": "substantive_null"}, d.COMPARATIVE),
    ({"H1": "negative_or_absent", "H2": "substantive_null"}, d.COMPARATIVE),
    ({"H1": "positive_or_present", "H2": "indeterminate"}, d.ONE_SIDED),
    ({"H1": "indeterminate", "H2": "negative_or_absent"}, d.ONE_SIDED),
    ({"H1": "substantive_null", "H2": "indeterminate"}, d.ONE_SIDED),
    ({"H1": "positive_or_present", "H2": "positive_or_present"}, d.SHARED),
    ({"H1": "indeterminate", "H2": "indeterminate"}, d.ALL_INDETERMINATE),
])
def test_profile_classes_follow_the_directive(states, expected):
    assert d.classify_profile(states, H) == expected
    assert d.is_comparatively_eligible(expected) is (expected == d.COMPARATIVE)


def test_indeterminate_is_not_substantive_null():
    assert "indeterminate" not in d.DETERMINATE and "substantive_null" in d.DETERMINATE


def test_missing_hypothesis_is_an_error_not_indeterminate():
    """v3 silently scored a missing judgment as 0.5; v4 must refuse."""
    with pytest.raises(d.StateError):
        d.classify_profile({"H1": "positive_or_present"}, H)


def test_k3_with_an_indeterminate_hypothesis_is_never_eligible():
    states = {"H1": "positive_or_present", "H2": "negative_or_absent", "H3": "indeterminate"}
    assert d.classify_profile(states, ["H1", "H2", "H3"]) == d.PARTIAL_CONTRAST
    assert not d.is_comparatively_eligible(d.PARTIAL_CONTRAST)


def test_indeterminate_has_no_likelihood_and_determinate_needs_strength():
    with pytest.raises(d.StateError):
        d.edge_label_for("indeterminate", None)
    assert d.normalise_strength("indeterminate", "strong") is None
    with pytest.raises(d.StateError):
        d.normalise_strength("positive_or_present", None)


def test_state_to_edge_label_reuses_the_frozen_scale_only(mappings):
    for (state, strength), label in d._STATE_TO_EDGE_LABEL.items():
        assert label in mappings.edge_probabilities
        assert label != "neutral"
        assert (mappings.edge_value(label) > 0.5) is (state == "positive_or_present")


# --------------------------------------------------------------------------- #
# Gate
# --------------------------------------------------------------------------- #
def _gate(states, label="support", construct="direct"):
    return d.gate_node(node_id="X1", hypothesis_ids=H, states=states, evidence_label=label, construct_match=construct)


CONTRAST = {"H1": _s("positive_or_present", "strong"), "H2": _s("negative_or_absent", "moderate")}
ONE_SIDED = {"H1": _s("positive_or_present", "strong"), "H2": _s("indeterminate")}


def test_contrast_with_direct_informative_evidence_is_scored():
    g = _gate(CONTRAST)
    assert g["used_in_score"] and g["gate_reason"] == "scored"


@pytest.mark.parametrize("construct", ["partial", "mismatch", None])
def test_only_direct_construct_matches_may_score(construct):
    g = _gate(CONTRAST, construct=construct)
    assert g["comparatively_eligible"] and not g["used_in_score"]
    assert g["gate_reason"] == "construct_{}".format(construct or "unassessed")


def test_one_sided_is_never_scored_even_with_strong_direct_evidence():
    g = _gate(ONE_SIDED, label="strong_support", construct="direct")
    assert g["profile_class"] == d.ONE_SIDED and not g["used_in_score"]


def test_missing_states_fail_closed():
    g = _gate(None)
    assert not g["used_in_score"] and g["gate_reason"] == "prediction_states_unavailable"


@pytest.mark.parametrize("label", ["no_evidence", "mixed", None])
def test_uninformative_evidence_is_not_scored(label):
    assert not _gate(CONTRAST, label=label)["used_in_score"]


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def _score(gates, states, labels, mappings, texts=None):
    return d.score_gated(hypothesis_ids=H, nodes=texts or {k: k for k in gates}, states=states, gates=gates,
                         evidence_labels=labels, mappings=mappings, multi_parent_rule="noisy_or",
                         parent_false_baseline=0.5, instance_id="case")


def test_one_sided_support_leaves_relative_scores_exactly_even(mappings):
    gates = {"X1": _gate(ONE_SIDED, label="strong_support")}
    result = _score(gates, {"X1": ONE_SIDED}, {"X1": "strong_support"}, mappings)
    assert result.scores == {"H1": 0.5, "H2": 0.5}
    assert result.contributions == []


def test_neutral_mapping_pseudo_discrimination_moved_v3_but_not_v4(mappings):
    """D046 KEY NEW METHOD DIAGNOSIS B: a correct `neutral` for a silent hypothesis
    still let support move v3's scores; the same situation must not move v4's."""
    graph = ConsequenceGraph(instance_id="case", hypothesis_ids=H)
    graph.add_node(PropositionNode(id="X1", text="x"))
    graph.add_edge(GraphEdge(source="H1", target="X1", kind="root", ordinal_strength="implied"))
    graph.add_edge(GraphEdge(source="H2", target="X1", kind="root", ordinal_strength="neutral"))
    v3 = score_hypotheses(graph.freeze(), {"X1": "support"}, mappings=mappings, aggregation="independent")
    assert v3.scores["H1"] > 0.5

    states = {"X1": {"H1": _s("positive_or_present", "moderate"), "H2": _s("indeterminate")}}
    v4 = _score({"X1": _gate(states["X1"])}, states, {"X1": "support"}, mappings)
    assert v4.scores == {"H1": 0.5, "H2": 0.5}


def test_contrast_moves_score_toward_the_supported_prediction(mappings):
    gates = {"X1": _gate(CONTRAST)}
    result = _score(gates, {"X1": CONTRAST}, {"X1": "support"}, mappings)
    assert result.scores["H1"] > result.scores["H2"]
    lam = mappings.evidence_value("support")
    p1, p2 = mappings.edge_value("strongly_implied"), mappings.edge_value("unlikely")
    expected = math.log(p1 * math.exp(lam) + 1 - p1) - math.log(p2 * math.exp(lam) + 1 - p2)
    assert result.log_scores["H1"] - result.log_scores["H2"] == pytest.approx(expected)


def test_blocked_and_ineligible_nodes_contribute_nothing(mappings):
    states = {"X1": CONTRAST, "X2": ONE_SIDED, "X3": CONTRAST}
    gates = {"X1": _gate(CONTRAST), "X2": _gate(ONE_SIDED), "X3": _gate(CONTRAST, construct="partial")}
    result = _score(gates, states, {"X1": "support", "X2": "strong_support", "X3": "strong_support"}, mappings)
    assert {c.node_id for c in result.contributions} == {"X1"}


def test_summary_counts(mappings):
    gates = {"X1": _gate(CONTRAST), "X2": _gate(ONE_SIDED), "X3": _gate(CONTRAST, construct="mismatch"),
             "X4": _gate(None)}
    s = d.summarise_gates(gates)
    assert (s["n_used_in_score"], s["n_comparatively_eligible"], s["n_profile_one_sided_prediction"],
            s["n_eligible_blocked_by_construct"], s["n_states_unavailable"]) == (1, 2, 1, 1, 1)


# --------------------------------------------------------------------------- #
# Parsing LLM output fails closed
# --------------------------------------------------------------------------- #
def _entry(i, state, strength="strong"):
    return {"id": i, "state": state, "strength": None if state == "indeterminate" else strength,
            "basis": "b", "rationale": "r"}


def test_parse_states_maps_labels_to_hypotheses_in_presentation_order():
    out = parse_states({"proposition_scope": "within_candidates_scope", "states": [_entry("B", "indeterminate"), _entry("A", "positive_or_present")]}, _pres())
    assert list(out) == ["H1", "H2"]
    assert out["H1"]["state"] == "positive_or_present" and out["H2"]["strength"] is None


@pytest.mark.parametrize("payload", [
    {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present")]},                                   # missing B
    {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("A", "indeterminate")]},     # duplicate
    {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("C", "indeterminate")]},     # unknown id
    {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "probably"), _entry("B", "indeterminate")]},                # unknown state
    {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present", None), _entry("B", "indeterminate")]},  # no strength
    {},
])
def test_parse_states_rejects_malformed_output(payload):
    with pytest.raises(d.StateError):
        parse_states(payload, _pres())


def _cm(*statuses, impression="partial"):
    return {"elements": [{"element": "e{}".format(i), "status": s, "note": ""} for i, s in enumerate(statuses)],
            "overall_impression": impression}


@pytest.mark.parametrize("statuses,expected", [
    (("established",), "direct"),
    (("established", "established"), "direct"),
    (("established", "not_established"), "partial"),      # compound claim, one part missing
    (("established", "partly"), "partial"),
    (("partly",), "partial"),
    (("not_established",), "mismatch"),
    (("not_established", "not_established"), "mismatch"),
    ((), "mismatch"),
])
def test_construct_label_is_derived_from_elements(statuses, expected):
    assert derive_construct_match(statuses) == expected


def test_holistic_impression_never_overrides_the_elements():
    out = parse_construct_match(_cm("established", "not_established", impression="direct"))
    assert out["construct_match"] == "partial" and out["model_overall_impression"] == "direct"


@pytest.mark.parametrize("payload", [{}, {"elements": []}, _cm("maybe"), _cm("established", impression="mostly")])
def test_parse_construct_match_rejects_malformed_output(payload):
    with pytest.raises(ValueError):
        parse_construct_match(payload)


# --------------------------------------------------------------------------- #
# The shared layer, with a scripted LLM
# --------------------------------------------------------------------------- #
class ScriptedLLM:
    """Returns canned parsed JSON by purpose and proposition; raises when told to."""

    def __init__(self, states, constructs, fail=()):
        self.states, self.constructs, self.fail = states, constructs, set(fail)
        self.calls = []

    def complete_json(self, messages, *, purpose, prompt_version=None, validator=None):
        from src.common.errors import LLMError

        text = messages[-1]["content"]
        key = next(k for k in list(self.states) + list(self.constructs) if "\n{}\n".format(k) in text)
        self.calls.append((purpose, key))
        if (purpose, key) in self.fail:
            raise LLMError("scripted failure")
        parsed = self.states[key] if purpose == "graph_v4.prediction_state" else self.constructs[key]
        if validator:
            validator(parsed)
        return SimpleNamespace(parsed=parsed, record=lambda: {"call_id": "c"})


def _layer(llm, mappings, evidence):
    from src.llm.prompts import PromptLibrary
    from src.methods.consequence_graph_v4 import run_v4_layer

    graph = {"nodes": [{"id": "X1", "text": "p1", "generation_origin_hypothesis": "H1"},
                       {"id": "X2", "text": "p2", "generation_origin_hypothesis": "H1"},
                       {"id": "X3", "text": "p3", "generation_origin_hypothesis": "H2"}]}
    return run_v4_layer(instance_id="case", presentation=_pres(), graph_record=graph, evidence_by_node=evidence,
                        records_for=lambda node, cited: "[1] record", llm=llm,
                        prompts=PromptLibrary(ROOT / "src" / "llm" / "prompts"), mappings=mappings,
                        multi_parent_rule="noisy_or", parent_false_baseline=0.5)


def _ev(label, cited=("s2:1",)):
    return {"assessment": {"evidence_label": label, "key_papers": list(cited), "supporting_spans": ["q"]}}


def test_layer_scores_only_direct_contrasts_and_keeps_the_rest_descriptively(mappings):
    llm = ScriptedLLM(
        states={"p1": {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]},
                "p2": {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("B", "indeterminate")]},
                "p3": {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "negative_or_absent"), _entry("B", "positive_or_present")]}},
        constructs={"p1": _cm("established", impression="direct"), "p2": _cm("established", impression="direct"),
                    "p3": _cm("not_established", impression="mismatch")})
    out = _layer(llm, mappings, {"X1": _ev("support"), "X2": _ev("strong_support"), "X3": _ev("strong_support")})
    assert [n for n, r in out["nodes"].items() if r["used_in_score"]] == ["X1"]
    assert out["scores"]["H1"] > out["scores"]["H2"]
    assert [b["node_id"] for b in out["buckets"]["one_sided_prediction"]] == ["X2"]
    assert out["buckets"]["one_sided_prediction"][0]["predicting_hypotheses"] == {"H1": "positive_or_present"}
    assert out["nodes"]["X3"]["gate_reason"] == "construct_mismatch"
    assert out["nodes"]["X2"]["contribution"] == {"H1": 0.0, "H2": 0.0}
    assert set(out["nodes"]) == {"X1", "X2", "X3"}          # nothing deleted


def test_layer_fails_closed_on_llm_errors(mappings):
    llm = ScriptedLLM(
        states={"p1": {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]},
                "p2": {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]},
                "p3": {"proposition_scope": "within_candidates_scope", "states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]}},
        constructs={"p1": _cm("established", impression="direct"), "p2": _cm("established", impression="direct"),
                    "p3": _cm("established", impression="direct")},
        fail={("graph_v4.prediction_state", "p1"), ("graph_v4.construct_match", "p2")})
    out = _layer(llm, mappings, {"X1": _ev("support"), "X2": _ev("support"), "X3": _ev("no_evidence")})
    assert out["nodes"]["X1"]["gate_reason"] == "prediction_states_unavailable"
    assert out["nodes"]["X2"]["gate_reason"] == "construct_unassessed"
    assert out["nodes"]["X3"]["gate_reason"] == "uninformative_evidence"
    assert out["scores"] == {"H1": 0.5, "H2": 0.5}
    assert {e["where"] for e in out["errors"]} == {"prediction_state", "construct_match"}
    assert ("graph_v4.construct_match", "p3") not in llm.calls   # no construct call for uninformative evidence


# --------------------------------------------------------------------------- #
# v3 untouched, registration, prompts, config
# --------------------------------------------------------------------------- #
def test_v3_and_v4_are_both_registered_and_distinct():
    from src.experiments.runner import METHODS
    from src.methods.consequence_graph import ConsequenceGraphVerifier
    from src.methods.consequence_graph_v4 import ConsequenceGraphV4Verifier

    assert METHODS["consequence_graph"] is ConsequenceGraphVerifier
    assert METHODS["consequence_graph_v4"] is ConsequenceGraphV4Verifier
    v3 = ConsequenceGraphVerifier(AppConfig()).prompt_versions()
    v4 = ConsequenceGraphV4Verifier(AppConfig()).prompt_versions()
    assert STATE_PROMPT not in v3 and CONSTRUCT_PROMPT not in v3
    assert v4[:len(v3)] == v3 and v4[len(v3):] == [STATE_PROMPT, CONSTRUCT_PROMPT]


def test_v4_prompts_obey_hidden_annotation_and_cutoff_invariants():
    from src.llm.prompts import PromptLibrary

    library = PromptLibrary(ROOT / "src" / "llm" / "prompts")
    forbidden = {"resolution", "resolver", "resolving_observations", "resolution_type", "reference_discriminators",
                 "leakage_audit", "gold", "gold_hypothesis", "answer", "correct_hypothesis", "favored", "cutoff"}
    for name in ("prediction_state_v1", "construct_match_v1", "prediction_state_v2", "construct_match_v2",
                 "prediction_state_v3"):
        template = library.get(name)
        assert not ({p.lower() for p in template.placeholders} & forbidden), name
        assert "cutoff" not in template.text.lower() and "json" in template.text.lower()


def test_v4_code_never_names_hidden_annotations():
    for path in ("src/methods/consequence_graph_v4.py", "src/inference/discrimination.py",
                 "src/graph/prediction_state.py", "src/evidence/construct_match.py"):
        assert "cases_hidden" not in (ROOT / path).read_text(encoding="utf-8"), path


def test_v4_dev_config_differs_from_pilot_only_in_dataset_status():
    def flat(node, prefix=""):
        if isinstance(node, dict):
            for k, v in node.items():
                yield from flat(v, "{}.{}".format(prefix, k) if prefix else k)
        else:
            yield prefix, node

    pilot = dict(flat(load_config(str(ROOT / "configs" / "pilot_explanatory.yaml")).model_dump()))
    dev = dict(flat(load_config(str(ROOT / "configs" / "v4_dev_explanatory.yaml")).model_dump()))
    assert {k for k in pilot if pilot[k] != dev[k]} == {"source_path", "dataset.status"}
    assert dev["dataset.status"] == "development"


# --------------------------------------------------------------------------- #
# Iteration 3: proposition scope is gated deterministically
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("scope", ["broader_than_candidates", "possibility_only"])
def test_out_of_scope_proposition_is_never_comparative_even_with_a_contrast(scope):
    states = {"H1": "positive_or_present", "H2": "negative_or_absent"}
    assert d.classify_profile(states, H, scope) == d.OUT_OF_SCOPE
    g = d.gate_node(node_id="X1", hypothesis_ids=H, states=CONTRAST, evidence_label="strong_support",
                    construct_match="direct", scope=scope)
    assert not g["comparatively_eligible"] and not g["used_in_score"]
    assert g["gate_reason"] == "profile_generic_or_possibility_claim"


def test_within_scope_contrast_is_still_eligible():
    g = d.gate_node(node_id="X1", hypothesis_ids=H, states=CONTRAST, evidence_label="support",
                    construct_match="direct", scope="within_candidates_scope")
    assert g["used_in_score"]


def test_scope_none_applies_no_scope_gating_for_older_records():
    assert d.classify_profile({"H1": "positive_or_present", "H2": "negative_or_absent"}, H, None) == d.COMPARATIVE


def test_unknown_or_missing_scope_fails_closed():
    from src.graph.prediction_state import parse_scope

    with pytest.raises(d.StateError):
        parse_scope({"states": []})
    with pytest.raises(d.StateError):
        parse_scope({"proposition_scope": "somewhat_general"})


def test_layer_buckets_out_of_scope_propositions(mappings, monkeypatch):
    import src.graph.prediction_state as ps
    monkeypatch.setattr(ps, "STATE_PROMPT", "prediction_state_v3")
    llm = ScriptedLLM(
        states={"p1": {"proposition_scope": "broader_than_candidates",
                       "states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]},
                "p2": {"proposition_scope": "within_candidates_scope",
                       "states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]},
                "p3": {"states": [_entry("A", "positive_or_present"), _entry("B", "negative_or_absent")]}},
        constructs={"p1": _cm("established"), "p2": _cm("established"), "p3": _cm("established")})
    out = _layer(llm, mappings, {"X1": _ev("support"), "X2": _ev("support"), "X3": _ev("support")})
    assert out["nodes"]["X1"]["profile_class"] == d.OUT_OF_SCOPE
    assert [b["node_id"] for b in out["buckets"]["generic_or_possibility_claim"]] == ["X1"]
    assert out["nodes"]["X2"]["used_in_score"]
    assert out["nodes"]["X3"]["gate_reason"] == "prediction_states_unavailable"   # no scope -> fail closed


def test_development_head_uses_the_iteration_2_state_prompt_without_scope():
    """Iteration 3 regressed on both replicates; the head reverted to v2 (see V4_DEV_REPORT)."""
    import src.graph.prediction_state as ps
    assert ps.STATE_PROMPT == "prediction_state_v2" and ps.STATE_PROMPT not in ps.SCOPE_PROMPTS
