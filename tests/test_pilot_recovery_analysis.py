"""The Step-6 recovery analysis must not invent discrimination that was not there.

The analysis is where a pilot most easily flatters itself: it is post-hoc, it has
the answer key in hand, and every judgment is a judgment call. So the parts that
can be made mechanical are made mechanical and tested here -- above all the rule
that decides whether the verifier itself treated a proposition as discriminating,
which is read out of the run's edge labels rather than inferred.
"""
from __future__ import annotations

import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

from scripts.analyze_pilot_recovery import (
    CATEGORIES,
    STATUSES,
    _validator,
    reconcile,
    summarise,
    system_discrimination,
)

HYPS = ["H1", "H2"]


def _edges(*pairs):
    return [{"source": h, "target": "X1", "ordinal_strength": label} for h, label in pairs]


# --------------------------------------------------------------------------- #
# The verifier's own claim
# --------------------------------------------------------------------------- #
def test_same_label_under_both_hypotheses_is_not_discriminative():
    out = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "implied")), HYPS)
    assert out["system_treated_as_discriminative"] is False
    assert out["n_distinct_labels"] == 1


def test_different_labels_are_discriminative():
    out = system_discrimination(
        "X1", _edges(("H1", "strongly_implied"), ("H2", "unlikely")), HYPS)
    assert out["system_treated_as_discriminative"] is True


def test_a_proposition_generated_from_one_hypothesis_is_not_automatically_discriminative():
    """The directive's explicit warning. Origin is not evidence of contrast: what
    matters is how the proposition was judged against every hypothesis."""
    out = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "implied")), HYPS)
    assert out["system_treated_as_discriminative"] is False
    assert out["cross_evaluated_against_all_hypotheses"] is True


def test_a_missing_cross_evaluation_is_never_counted_as_discriminative():
    """If a hypothesis never got an edge, the comparison was not made. Treating the
    absent edge as a difference would manufacture contrast out of a gap in the run.
    """
    out = system_discrimination("X1", _edges(("H1", "implied")), HYPS)
    assert out["system_treated_as_discriminative"] is False
    assert out["cross_evaluated_against_all_hypotheses"] is False
    assert out["hypotheses_without_an_edge"] == ["H2"]


def test_edges_for_other_nodes_are_ignored():
    edges = _edges(("H1", "implied"), ("H2", "unlikely"))
    edges.append({"source": "H2", "target": "X9", "ordinal_strength": "neutral"})
    out = system_discrimination("X1", edges, HYPS)
    assert set(out["edge_label_by_hypothesis"]) == {"H1", "H2"}


# --------------------------------------------------------------------------- #
# Reconciliation: silence must not become contrast
# --------------------------------------------------------------------------- #
def _judged(statuses, discriminative, category="compatible_non_discriminative"):
    return {"status_under_each": statuses, "is_discriminative": discriminative,
            "category": category}


def test_silence_inflation_is_flagged():
    """The verifier separated the hypotheses; the auditor says one of them is simply
    silent. This is the directive's named failure mode."""
    system = system_discrimination(
        "X1", _edges(("H1", "strongly_implied"), ("H2", "unlikely")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "indeterminate"}, False,
                     "silence_as_null_error")
    out = reconcile(system, judged)
    assert out["silence_inflation"] is True
    assert out["agree"] is False


def test_a_real_contrast_is_not_flagged_as_silence_inflation():
    system = system_discrimination(
        "X1", _edges(("H1", "strongly_implied"), ("H2", "unlikely")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "negative_or_absent"}, True)
    out = reconcile(system, judged)
    assert out["silence_inflation"] is False
    assert out["agree"] is True


def test_a_genuine_null_prediction_is_not_silence():
    """`neutral_or_no_change` is a prediction; `indeterminate` is a silence. A
    hypothesis that positively predicts no change DOES contrast with one that
    predicts an increase, and must not be written off as silence."""
    system = system_discrimination(
        "X1", _edges(("H1", "implied"), ("H2", "neutral")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "neutral_or_no_change"}, True)
    out = reconcile(system, judged)
    assert out["silence_inflation"] is False
    assert out["n_hypotheses_indeterminate"] == 0


def test_missed_discrimination_is_flagged():
    system = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "implied")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "negative_or_absent"}, True)
    out = reconcile(system, judged)
    assert out["missed_discrimination"] is True


def test_a_judge_error_is_not_silently_treated_as_agreement():
    system = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "unlikely")), HYPS)
    out = reconcile(system, None)
    assert out["comparable"] is False
    assert "agree" not in out


# --------------------------------------------------------------------------- #
# Validation of judge output
# --------------------------------------------------------------------------- #
def test_validator_rejects_an_unknown_category():
    with pytest.raises(ValueError):
        _validator({"status_under_each": {"H1": "indeterminate"},
                    "is_discriminative": False, "category": "looks_fine_to_me"})


def test_validator_rejects_an_unknown_status():
    with pytest.raises(ValueError):
        _validator({"status_under_each": {"H1": "probably_yes"},
                    "is_discriminative": False, "category": CATEGORIES[0]})


def test_validator_accepts_every_documented_category_and_status():
    for category in CATEGORIES:
        for status in STATUSES:
            _validator({"status_under_each": {"H1": status},
                        "is_discriminative": False, "category": category})


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #
def _case(case_id, rows, n_ref=2, refs=None):
    return {"case_id": case_id, "n_nodes": len(rows),
            "n_reference_discriminators": n_ref,
            "reference_discriminators": refs or ["ref A", "ref B"],
            "propositions": rows}


def _row(category, matched=None, system_disc=False, judge_disc=False, indeterminate=0,
         h2_edge="unlikely"):
    statuses = {"H1": "positive_or_present"}
    statuses["H2"] = "indeterminate" if indeterminate else "negative_or_absent"
    system = {"system_treated_as_discriminative": system_disc,
              "edge_label_by_hypothesis": {"H1": "implied", "H2": h2_edge}}
    judged = {"status_under_each": statuses, "is_discriminative": judge_disc,
              "category": category, "matched_reference_discriminator": matched}
    return {"node_id": "X", "system": system, "judge": judged,
            "reconciliation": reconcile(system, judged)}


def test_recovered_reference_discriminators_are_counted_once_each():
    """Two propositions hitting the same reference discriminator is one recovery,
    not two. Counting them twice would let verbosity inflate coverage."""
    rows = [_row("reference_discriminator_recovered", "ref A", True, True),
            _row("reference_discriminator_recovered", "ref A", True, True)]
    out = summarise([_case("c1", rows)])
    assert out["per_case"][0]["n_reference_discriminators_recovered"] == 1


def test_judge_errors_are_counted_and_not_categorised():
    rows = [{"node_id": "X", "system": {"system_treated_as_discriminative": False},
             "judge": None, "judge_error": "boom", "reconciliation": reconcile(
                 {"system_treated_as_discriminative": False}, None)}]
    out = summarise([_case("c1", rows)])
    assert out["n_judge_errors"] == 1
    assert sum(out["categories"].values()) == 0


def test_summary_keeps_the_two_readings_separate():
    """The verifier's count and the auditor's count are reported side by side, never
    merged: their disagreement is the finding."""
    rows = [_row("silence_as_null_error", None, system_disc=True, judge_disc=False,
                 indeterminate=1)]
    out = summarise([_case("c1", rows)])
    assert out["n_system_treated_as_discriminative"] == 1
    assert out["n_judge_treated_as_discriminative"] == 0
    assert out["n_silence_inflation"] == 1


# --------------------------------------------------------------------------- #
# How silences were labelled
# --------------------------------------------------------------------------- #
from scripts.analyze_pilot_recovery import silence_handling  # noqa: E402


def _silent_row(label_for_h2):
    system = {"edge_label_by_hypothesis": {"H1": "implied", "H2": label_for_h2},
              "system_treated_as_discriminative": label_for_h2 != "implied"}
    judged = {"status_under_each": {"H1": "positive_or_present", "H2": "indeterminate"},
              "is_discriminative": False, "category": "silence_as_null_error"}
    return {"node_id": "X", "system": system, "judge": judged,
            "reconciliation": reconcile(system, judged)}


def test_only_silent_pairs_are_counted():
    """A hypothesis that genuinely predicts something is not a silence, however its
    edge was labelled."""
    system = {"edge_label_by_hypothesis": {"H1": "implied", "H2": "unlikely"},
              "system_treated_as_discriminative": True}
    judged = {"status_under_each": {"H1": "positive_or_present",
                                    "H2": "negative_or_absent"},
              "is_discriminative": True, "category": "novel_plausible_discriminator"}
    out = silence_handling([_case("c1", [{"node_id": "X", "system": system,
                                          "judge": judged,
                                          "reconciliation": reconcile(system, judged)}])])
    assert out["n_silent_hypothesis_proposition_pairs"] == 0
    assert out["share_labelled_neutral"] is None


def test_neutral_on_a_silence_injects_nothing():
    out = silence_handling([_case("c1", [_silent_row("neutral")])])
    assert out["share_labelled_neutral"] == 1.0
    assert out["mean_abs_probability_deviation_from_half"] == 0.0


def test_a_directional_label_on_a_silence_is_measured_in_the_methods_own_units():
    """`unlikely` maps to 0.30 in configs/ordinal_mappings.yaml, so calling a
    silence `unlikely` moves that posterior 0.20 off the inert midpoint."""
    out = silence_handling([_case("c1", [_silent_row("unlikely")])])
    assert out["share_labelled_neutral"] == 0.0
    assert out["mean_abs_probability_deviation_from_half"] == pytest.approx(0.20)


def test_the_probability_table_matches_the_configured_mappings():
    """The copy used for measurement must not drift from the method's real values."""
    import yaml

    from scripts.analyze_pilot_recovery import _EDGE_PROBABILITY

    config_path = ROOT_DIR / "configs" / "ordinal_mappings.yaml"
    configured = yaml.safe_load(config_path.read_text(encoding="utf-8"))["edge_probabilities"]
    assert _EDGE_PROBABILITY == configured


def test_a_paraphrased_reference_match_is_not_counted_as_a_recovery():
    """The judge is asked for the discriminator verbatim. If it paraphrases, two
    wordings of one discriminator would otherwise read as two recoveries."""
    rows = [_row("reference_discriminator_recovered", "ref A", True, True),
            _row("reference_discriminator_recovered", "a loose paraphrase of ref A",
                 True, True)]
    out = summarise([_case("c1", rows, refs=["ref A", "ref B"])])
    assert out["per_case"][0]["n_reference_discriminators_recovered"] == 1
    assert len(out["unverbatim_reference_matches"]) == 1
    assert out["unverbatim_reference_matches"][0]["returned"].startswith("a loose")



# --------------------------------------------------------------------------- #
# Silence handled correctly is not an error
# --------------------------------------------------------------------------- #
def test_a_silence_labelled_neutral_is_correct_handling_not_inflation():
    """One hypothesis predicts X, the other is silent and got `neutral` (0.50,
    inert). That is the right treatment. An earlier version of reconcile() counted
    it as silence inflation because the two edge labels differ."""
    system = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "neutral")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "indeterminate"}, False,
                     "silence_as_null_error")
    out = reconcile(system, judged)
    assert out["one_sided_proposition"] is True
    assert out["silent_hypotheses_handled_as_neutral"] == ["H2"]
    assert out["silence_inflation"] is False
    assert out["manufactured_opposition"] is False


def test_silence_read_as_presence_is_inflation_but_not_opposition():
    system = system_discrimination("X1", _edges(("H1", "strongly_implied"), ("H2", "implied")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "indeterminate"}, False,
                     "silence_as_null_error")
    out = reconcile(system, judged)
    assert out["silent_hypotheses_read_as_presence"] == ["H2"]
    assert out["silence_inflation"] is True
    assert out["manufactured_opposition"] is False


def test_silence_read_as_absence_with_opposite_signs_is_manufactured_opposition():
    system = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "unlikely")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "indeterminate"}, False,
                     "silence_as_null_error")
    out = reconcile(system, judged)
    assert out["silent_hypotheses_read_as_absence"] == ["H2"]
    assert out["system_sign_opposed"] is True
    assert out["manufactured_opposition"] is True


def test_a_genuine_sign_opposed_discriminator_is_not_manufactured():
    system = system_discrimination("X1", _edges(("H1", "implied"), ("H2", "unlikely")), HYPS)
    judged = _judged({"H1": "positive_or_present", "H2": "negative_or_absent"}, True,
                     "reference_discriminator_recovered")
    out = reconcile(system, judged)
    assert out["system_sign_opposed"] is True
    assert out["manufactured_opposition"] is False
