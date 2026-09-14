"""Counterbalanced pair judging: a position-guesser must score exactly chance."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path("scripts").resolve()))

from src.llm.prompts import PromptLibrary  # noqa: E402
from v2_artifact_diagnostics import question_hidden_judge  # noqa: E402


class _Response:
    def __init__(self, parsed):
        self.parsed = parsed


class AlwaysA:
    """The degenerate judge the counterbalancing exists to neutralise."""

    def __init__(self):
        self.calls = 0

    def complete_json(self, messages, **kwargs):
        self.calls += 1
        return _Response({"choice": "A", "confidence": 99})


class AlwaysGold:
    """Reads the text perfectly: picks whichever option is the gold."""

    def complete_json(self, messages, **kwargs):
        content = messages[0]["content"]
        a_index = content.index("HYPOTHESIS A") if "HYPOTHESIS A" in content else content.index("A:")
        b_index = content.index("HYPOTHESIS B") if "HYPOTHESIS B" in content else content.index("B:")
        block_a = content[a_index:b_index]
        return _Response({"choice": "A" if "GOLDMARK" in block_a else "B", "confidence": 99})


def _pairs(n):
    return [{"pair_id": "P%d" % i, "gold_hypothesis": "GOLDMARK claim %d" % i,
             "negative_hypothesis": "alternative claim %d" % i} for i in range(n)]


@pytest.fixture
def prompts():
    return PromptLibrary("src/llm/prompts")


def test_a_position_guesser_scores_exactly_chance(prompts):
    llm = AlwaysA()
    out = question_hidden_judge(_pairs(20), llm=llm, prompts=prompts, seed=1)
    assert out["accuracy"] == pytest.approx(0.5), (
        "always answering A must score chance once both orders are averaged")
    assert out["position_preference_chose_a"] == pytest.approx(1.0)
    assert out["order_consistency"] == pytest.approx(0.0)
    assert llm.calls == 40, "every pair must be judged twice"


def test_single_order_lets_a_position_guesser_beat_chance(prompts):
    """Why the flag exists and why it is not the default."""
    out = question_hidden_judge(_pairs(20), llm=AlwaysA(), prompts=prompts, seed=1,
                                counterbalance=False)
    assert out["accuracy"] != pytest.approx(0.5), (
        "with one order the score is whatever the seeded coin happened to give")


def test_a_judge_that_reads_the_text_scores_one(prompts):
    out = question_hidden_judge(_pairs(20), llm=AlwaysGold(), prompts=prompts, seed=1)
    assert out["accuracy"] == pytest.approx(1.0)
    assert out["order_consistency"] == pytest.approx(1.0)
    assert out["position_preference_chose_a"] == pytest.approx(0.5), (
        "a content-reading judge picks A exactly half the time under counterbalancing")
