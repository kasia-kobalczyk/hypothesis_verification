"""Diagnostic prediction tests -- the new branch (docs/DIAGNOSTIC_DESIGN.md)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.diagnostics.schema import (
    COMPATIBILITY,
    PREDICTIONS,
    DiagnosticTest,
    TestSet,
    normalise_prediction,
)
from src.llm.prompts import PromptLibrary

PROMPT_DIR = Path(__file__).resolve().parents[1] / "src" / "llm" / "prompts"


def _prompt(name):
    return PromptLibrary(PROMPT_DIR).get(name)


def _test(**preds):
    return DiagnosticTest(
        test_id="T1", system="s", intervention_or_exposure="i",
        measured_outcome="m", predictions_by_hypothesis=preds)


# --------------------------------------------------------------------------- #
# The vocabulary is coarse on purpose
# --------------------------------------------------------------------------- #
def test_prediction_vocabulary_is_coarse():
    """No ordinal strength. weak_support reproduced at 0.51 in the previous branch."""
    assert set(PREDICTIONS) == {
        "positive_or_present", "neutral_or_no_change",
        "negative_or_absent", "indeterminate"}
    assert set(COMPATIBILITY) == {"match", "approximate_match", "indeterminate", "mismatch"}


def test_predictions_are_normalised_and_unknown_ones_rejected():
    assert normalise_prediction("Positive_Or_Present") == "positive_or_present"
    assert normalise_prediction("negative-or-absent") == "negative_or_absent"
    assert normalise_prediction("strong_support") is None, "old vocabulary must not leak in"
    assert normalise_prediction(None) is None


# --------------------------------------------------------------------------- #
# Discrimination
# --------------------------------------------------------------------------- #
def test_a_test_every_candidate_predicts_alike_is_not_discriminative():
    """This is the failure the whole branch exists to avoid: a generic truth."""
    t = _test(H0="positive_or_present", H1="positive_or_present")
    assert t.distinct_predictions() == 1
    assert not t.is_discriminative()
    assert t.discriminated_pairs() == []


def test_indeterminate_never_counts_as_discrimination():
    """A candidate making no prediction cannot be told apart by the test."""
    t = _test(H0="positive_or_present", H1="indeterminate")
    assert not t.is_discriminative()
    t2 = _test(H0="indeterminate", H1="indeterminate")
    assert not t2.is_discriminative()


def test_a_discriminative_test_names_the_pairs_it_separates():
    t = _test(H0="positive_or_present", H1="negative_or_absent", H2="indeterminate")
    assert t.is_discriminative()
    assert t.discriminated_pairs() == [("H0", "H1")]


# --------------------------------------------------------------------------- #
# The generation prompt
# --------------------------------------------------------------------------- #
def test_generation_is_joint_over_candidates_not_per_hypothesis():
    """Tests belong to no hypothesis: that is what removes origin asymmetry."""
    assert "candidates" in _prompt("diagnostic_test_generate_v1").placeholders


def test_generation_forbids_literature_and_asks_for_predictions():
    text = " ".join(_prompt("diagnostic_test_generate_v1").text.lower().split())
    assert "no literature access" in text
    assert "what each candidate predicts, not what is true" in text
    assert "do not consult what you know actually happened" in text


def test_generation_demands_a_measured_quantity_not_a_vague_improvement():
    raw = _prompt("diagnostic_test_generate_v1").text
    text = " ".join(raw.split())   # the prompt is hard-wrapped
    assert "measured_outcome" in raw
    assert '"The system performs better" is not a measurement' in text
    assert "tensile strength in mpa" in text.lower()


def test_generation_asks_for_honest_indeterminates():
    text = " ".join(_prompt("diagnostic_test_generate_v1").text.lower().split())
    assert "use \"indeterminate\" honestly" in text


def test_the_design_document_is_frozen():
    import hashlib

    freeze = json.loads(Path("benchmark/frozen/diagnostic_design_freeze.json").read_text())
    text = Path("docs/DIAGNOSTIC_DESIGN.md").read_text()
    assert hashlib.sha256(text.encode()).hexdigest()[:16] == freeze["sha256_16"], (
        "the design changed after being frozen; component validations run against "
        "the old hash are void"
    )
