"""Artifact-diagnostic baselines and the frozen pair subset."""

from __future__ import annotations

import json

import pytest

from src.baselines.artifact_baselines import (
    QuestionHiddenJudge,
    StyleArtifactBaseline,
    surface_features,
)
from src.benchmark.loader import load_instances
from src.benchmark.pairs import (
    PAIR_PROMPT_VERSION,
    PairDecision,
    PairSubset,
    build_pair_subset,
    judge_pair,
)
from src.common.errors import LLMError
from src.experiments.runner import METHODS
from src.literature.service import ForbiddenLiteratureService
from src.llm.client import MockLLMClient
from src.llm.prompts import PromptLibrary
from tests.test_baselines import make_context


class ExplodingLLM(MockLLMClient):
    """Any call is a test failure."""

    def _invoke(self, messages, *, json_mode):  # noqa: D102
        raise AssertionError("this baseline must not call a language model")


# --------------------------------------------------------------------------- #
# Style-artifact floor
# --------------------------------------------------------------------------- #
def test_style_artifact_uses_no_model_no_question_no_literature(config, tmp_path):
    ctx = make_context(
        config, tmp_path,
        literature=ForbiddenLiteratureService("style_artifact"),
        llm=ExplodingLLM(config.llm),
    )
    result = StyleArtifactBaseline(config).run_instance(ctx)

    assert result.status == "ok"
    assert set(result.scores) == set(ctx.instance.hypothesis_ids)
    # Ranked purely by length, longest first.
    lengths = {h.id: len(h.text) for h in ctx.instance.hypotheses}
    assert result.ranking == sorted(lengths, key=lambda h: (-lengths[h], result.ranking.index(h)))
    assert result.artifacts["scores"]["feature"] == "n_chars"
    assert StyleArtifactBaseline.requires_literature is False


def test_style_artifact_is_deterministic_and_reversible(config, tmp_path):
    ctx = make_context(config, tmp_path, literature=ForbiddenLiteratureService("s"), llm=ExplodingLLM(config.llm))
    first = StyleArtifactBaseline(config).run_instance(ctx)
    second = StyleArtifactBaseline(config).run_instance(ctx)
    assert first.scores == second.scores

    shortest = config.model_copy(
        update={
            "baselines": config.baselines.model_copy(
                update={"style_artifact": config.baselines.style_artifact.model_copy(update={"prefer": "shortest"})}
            )
        }
    )
    flipped = StyleArtifactBaseline(shortest).run_instance(ctx)
    assert flipped.ranking == list(reversed(first.ranking))


def test_unknown_style_feature_fails_loudly(config, tmp_path):
    cfg = config.model_copy(
        update={
            "baselines": config.baselines.model_copy(
                update={"style_artifact": config.baselines.style_artifact.model_copy(update={"feature": "vibes"})}
            )
        }
    )
    ctx = make_context(cfg, tmp_path, literature=ForbiddenLiteratureService("s"), llm=ExplodingLLM(cfg.llm))
    with pytest.raises(KeyError):
        StyleArtifactBaseline(cfg).run_instance(ctx)


def test_surface_features_are_content_free():
    values = surface_features("Two words.\nAnd 3 more 42.")
    assert values["n_words"] == 6
    assert values["n_lines"] == 2
    assert values["n_digits"] == 3


# --------------------------------------------------------------------------- #
# Question-hidden judge
# --------------------------------------------------------------------------- #
def test_question_hidden_judge_never_sees_the_question(config, tmp_path):
    llm = MockLLMClient(config.llm)
    ctx = make_context(config, tmp_path, literature=ForbiddenLiteratureService("qh"), llm=llm)
    result = QuestionHiddenJudge(config).run_instance(ctx)

    assert result.status == "ok"
    assert set(result.scores) == set(ctx.instance.hypothesis_ids)
    prompt = llm.calls[0][0]["content"]
    assert ctx.instance.question not in prompt
    # A distinctive phrase from the question must not appear either.
    assert "r-process nucleosynthesis" not in prompt.split("CANDIDATE HYPOTHESES")[0]
    assert "Hypothesis A:" in prompt


def test_question_hidden_template_has_no_question_placeholder(config):
    template = PromptLibrary(config.prompts.dir).get(
        config.baselines.question_hidden_judge.prompt_version
    )
    assert "$question" not in template.text
    # Even if a caller passes one, there is no placeholder to render it into.
    rendered = template.render(question="SECRET QUESTION", hypotheses="y", labels="A")
    assert "SECRET QUESTION" not in rendered


def test_both_artifact_baselines_are_registered():
    assert METHODS["style_artifact"] is StyleArtifactBaseline
    assert METHODS["question_hidden_judge"] is QuestionHiddenJudge
    assert all(not m.requires_literature for m in (StyleArtifactBaseline, QuestionHiddenJudge))


# --------------------------------------------------------------------------- #
# Frozen pair subset
# --------------------------------------------------------------------------- #
def pair_responder(payload):
    return lambda messages, cfg: json.dumps(payload)


def test_pair_decision_follows_the_two_criteria_not_the_stated_verdict(config, tmp_path):
    """The model's summary field cannot override the criteria it just answered."""
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    prompts = PromptLibrary(config.prompts.dir)

    llm = MockLLMClient(
        config.llm,
        responder=pair_responder(
            {"same_target": True, "disagrees_substantively": False, "decision": "PASS", "rationale": "r"}
        ),
    )
    decision = judge_pair(instance, "H1", llm=llm, prompts=prompts)
    assert decision.decision == "FAIL"

    llm = MockLLMClient(
        config.llm,
        responder=pair_responder(
            {"same_target": True, "disagrees_substantively": True, "decision": "FAIL", "rationale": "r"}
        ),
    )
    assert judge_pair(instance, "H1", llm=llm, prompts=prompts).decision == "PASS"


def test_pair_judgment_sees_only_question_gold_and_negative(config, tmp_path):
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    llm = MockLLMClient(
        config.llm,
        responder=pair_responder(
            {"same_target": True, "disagrees_substantively": True, "decision": "PASS", "rationale": "r"}
        ),
    )
    judge_pair(instance, "H2", llm=llm, prompts=PromptLibrary(config.prompts.dir))
    prompt = llm.calls[0][0]["content"]

    assert instance.gold_hypothesis.text in prompt
    assert instance.hypothesis("H2").text in prompt
    # No other candidate, and nothing about literature or cutoffs, may leak in.
    assert instance.hypothesis("H3").text not in prompt
    assert str(instance.cutoff_date) not in prompt
    assert "PASS" in prompt and "FAIL" in prompt


def test_pair_judgment_failure_is_error_not_fail(config):
    """A broken judge must not silently shrink the benchmark."""
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    llm = MockLLMClient(config.llm, responder=lambda messages, cfg: "not json")
    decision = judge_pair(instance, "H1", llm=llm, prompts=PromptLibrary(config.prompts.dir))

    assert decision.decision == "ERROR"
    assert decision.passed is False
    assert decision.error and "LLMParseError" in decision.error


def test_build_reuses_frozen_decisions_and_retries_errors(config):
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    existing = PairSubset(
        [
            PairDecision(instance_id="RBV-01", gold_id="H0", negative_id="H1", decision="PASS"),
            PairDecision(instance_id="RBV-01", gold_id="H0", negative_id="H2", decision="FAIL"),
            PairDecision(instance_id="RBV-01", gold_id="H0", negative_id="H3", decision="ERROR"),
        ]
    )
    llm = MockLLMClient(
        config.llm,
        responder=pair_responder(
            {"same_target": True, "disagrees_substantively": True, "decision": "PASS", "rationale": "r"}
        ),
    )
    decisions = build_pair_subset(
        [instance], llm=llm, prompts=PromptLibrary(config.prompts.dir), existing=existing
    )

    assert len(decisions) == len(instance.hypotheses) - 1
    by_id = {d.negative_id: d for d in decisions}
    assert by_id["H1"].decision == "PASS" and by_id["H1"].rationale is None  # reused verbatim
    assert by_id["H2"].decision == "FAIL"                                    # reused verbatim
    assert by_id["H3"].rationale == "r"                                      # errored one rejudged
    # 10 negatives - 2 frozen = 8 judged.
    assert len(llm.calls) == 8


def test_pair_subset_exposes_only_passing_negatives():
    subset = PairSubset(
        [
            PairDecision(instance_id="A", gold_id="H0", negative_id="H1", decision="PASS"),
            PairDecision(instance_id="A", gold_id="H0", negative_id="H2", decision="FAIL"),
            PairDecision(instance_id="A", gold_id="H0", negative_id="H3", decision="ERROR"),
            PairDecision(instance_id="B", gold_id="H0", negative_id="H1", decision="PASS"),
        ]
    )
    assert subset.negatives_for("A") == ["H1"]
    assert subset.negatives_for("missing") == []
    assert len(subset) == 2
    counts = subset.counts()
    assert counts["n_pairs_retained"] == 2
    assert counts["n_pairs_rejected"] == 1
    assert counts["n_pairs_error"] == 1


def test_pair_prompt_is_outcome_blind(config):
    text = PromptLibrary(config.prompts.dir).get(PAIR_PROMPT_VERSION).text.lower()
    assert "not which one is correct" in text
    assert "do not judge which hypothesis is scientifically correct" in text
    # Style must not be a screening criterion.
    assert "length" in text and "formatting" in text
    for banned in ("literature", "cutoff", "retriev"):
        assert banned not in text, banned


# --------------------------------------------------------------------------- #
# An instance with no evaluable pair is marked, not silently dropped
# --------------------------------------------------------------------------- #
def test_instance_with_no_passing_pair_is_marked(config):
    subset = PairSubset(
        [
            PairDecision(instance_id="A", gold_id="H0", negative_id="H1", decision="PASS"),
            PairDecision(instance_id="B", gold_id="H0", negative_id="H1", decision="FAIL"),
            PairDecision(instance_id="B", gold_id="H0", negative_id="H2", decision="FAIL"),
        ]
    )
    assert subset.status_for("A") == "evaluable"
    assert subset.status_for("B") == "no_evaluable_pair"
    assert subset.status_for("C") == "not_screened"
    assert subset.instances_without_pairs() == ["B"]
    assert subset.counts()["instances_no_evaluable_pair"] == ["B"]


def test_rbv14_has_no_evaluable_pair_in_the_frozen_subset(config):
    """The pair audit overturned RBV-14's row-level R2 pass (docs/DECISIONS.md §11)."""
    from src.benchmark.pairs import load_pair_subset
    from src.common.io import resolve_path

    subset = load_pair_subset(resolve_path(config.dataset.pairs_path))
    assert subset.status_for("RBV-14") == "no_evaluable_pair"
    assert subset.negatives_for("RBV-14") == []
    # Every one of its negatives was screened and failed — not merely unscreened.
    decisions = subset.all_for("RBV-14")
    assert len(decisions) == 10
    assert all(d.decision == "FAIL" for d in decisions)
    # The instance itself is untouched and still loads with all 11 candidates.
    instance = load_instances(config, instance_ids=["RBV-14"])[0]
    assert len(instance.hypotheses) == 11


def test_excluded_instance_reaches_the_run_summary(config):
    """It must be named in the artifacts, not just absent from an average."""
    from src.experiments.runner import ExperimentRunner

    cfg = config.model_copy(update={"llm": config.llm.model_copy(update={"provider": "mock"})})
    runner = ExperimentRunner(cfg, "style_artifact", instance_ids=["RBV-14", "RBV-01"])
    summary = runner.run()

    metrics = summary["metrics"]
    assert metrics["instances_no_evaluable_pair"] == ["RBV-14"]
    assert metrics["n_instances_no_evaluable_pair"] == 1
    assert metrics["n_instances_with_pairs"] == 1  # RBV-01 only
    assert summary["pairs"]["instances_no_evaluable_pair"] == ["RBV-14"]

    report = (runner.run_dir / "instances" / "RBV-14" / "report.md").read_text(encoding="utf-8")
    assert "no evaluable pair" in report
    # Still scored in the secondary listwise view.
    from src.common.io import read_json

    row = {r["instance_id"]: r for r in read_json(runner.run_dir / "metrics.json")["instances"]}
    assert row["RBV-14"]["pair_status"] == "no_evaluable_pair"
    assert row["RBV-14"]["pair_accuracy"] is None
    assert row["RBV-14"]["gold_rank"] is not None


def test_screening_correction_is_recorded_without_editing_the_frozen_screen():
    from src.common.io import read_json, read_jsonl, repo_root

    original = {r["dev_id"]: r for r in read_jsonl(
        repo_root() / "benchmark" / "dev" / "accepted_screening_decisions_v1.jsonl"
    )}
    # The frozen row-level record keeps its original verdict.
    assert original["RBV-14"]["R2_raw_candidate_comparability"] is True

    corrections = read_json(repo_root() / "benchmark" / "dev" / "screening_corrections_v1.json")
    entry = {c["dev_id"]: c for c in corrections["corrections"]}["RBV-14"]
    assert entry["original_field"] == "R2_raw_candidate_comparability"
    assert entry["original_value"] is True and entry["corrected_value"] is False
    assert "no negative was written" in entry["not_done"].lower()
