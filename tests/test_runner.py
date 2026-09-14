"""End-to-end runner behaviour and artifact completeness.

IMPLEMENTATION_SPEC.md §9, §24, §36: every run must be self-contained and
diagnosable without rerunning the model.
"""

from __future__ import annotations

import json

import pytest

from src.common.io import read_json, read_jsonl
from src.experiments.runner import ExperimentRunner
from src.literature.service import build_literature_service
from tests.conftest import FakeS2Provider, s2_record, search_payload


@pytest.fixture
def mock_config(config):
    return config.model_copy(update={"llm": config.llm.model_copy(update={"provider": "mock"})})


def test_direct_judge_run_writes_complete_artifacts(mock_config):
    runner = ExperimentRunner(mock_config, "direct_judge", instance_ids=["RBV-01", "RBV-02"])
    summary = runner.run()

    assert summary["n_instances"] == 2
    assert summary["n_ok"] == 2
    assert summary["metrics"]["n_scored"] == 2
    assert summary["metrics"]["top1_accuracy"] is not None

    run_dir = runner.run_dir
    for name in ("config.yaml", "manifest.json", "summary.json", "metrics.json", "summary.md", "events.jsonl"):
        assert (run_dir / name).exists(), name

    manifest = read_json(run_dir / "manifest.json")
    assert manifest["method"] == "direct_judge"
    assert manifest["dataset"]["sha256_16"]
    version = mock_config.baselines.direct_judge.prompt_version
    assert version in manifest["prompts"]
    assert manifest["prompts"][version]["sha256_16"]
    assert manifest["cutoffs"]["RBV-01"]["cutoff_date"]

    instance_dir = run_dir / "instances" / "RBV-01"
    for name in ("input.json", "presentation.json", "prompts.json", "model_outputs.json",
                 "scores.json", "report.md", "result.json", "events.jsonl"):
        assert (instance_dir / name).exists(), name

    # The prompt actually sent is recoverable.
    prompts = read_json(instance_dir / "prompts.json")
    assert prompts["messages"][0]["content"].startswith("You are assisting")
    assert prompts["prompt_version"] == version
    assert prompts["presentation"]["label_to_hypothesis_id"]

    # Model output, parsed scores and gold identity are all present.
    outputs = read_json(instance_dir / "model_outputs.json")
    assert outputs["response_text"]
    assert outputs["usage"] is not None
    scores = read_json(instance_dir / "scores.json")
    hypothesis_ids = {h["id"] for h in read_json(instance_dir / "input.json")["hypotheses"]}
    assert set(scores["scores"]) == hypothesis_ids
    assert scores["gold_id"] == "H0"

    report = (instance_dir / "report.md").read_text(encoding="utf-8")
    assert "# RBV-01" in report and "## Scores" in report and "gold hypothesis" in report

    events = list(read_jsonl(run_dir / "events.jsonl"))
    assert any(e["kind"] == "llm_call" for e in events)


def test_direct_rag_run_is_reproducible_from_cache(mock_config, monkeypatch):
    payload = search_payload(
        [
            s2_record("p1", title="Pre-cutoff evidence", publication_date="2019-02-02"),
            s2_record("p2", title="Post-cutoff evidence", publication_date="2030-01-01"),
        ]
    )
    provider_holder = {}

    original = build_literature_service

    def fake_build(config, registry, **kwargs):
        provider = FakeS2Provider(config.literature, payloads={}, default=payload)
        provider_holder.setdefault("providers", []).append(provider)
        return original(config, registry, provider=provider, **kwargs)

    monkeypatch.setattr("src.experiments.runner.build_literature_service", fake_build)

    first = ExperimentRunner(mock_config, "direct_rag", instance_ids=["RBV-01"])
    summary = first.run()
    assert summary["n_ok"] == 1
    assert summary["literature_stats"]["provider_calls"] > 0

    instance_dir = first.run_dir / "instances" / "RBV-01"
    for name in ("queries.json", "retrieval.json", "evidence.json", "scores.json", "report.md"):
        assert (instance_dir / name).exists(), name

    retrieval = read_json(instance_dir / "retrieval.json")
    any_hypothesis = next(iter(retrieval["by_hypothesis"].values()))
    shown = [p["paper_id"] for p in any_hypothesis["papers_shown"]]
    assert shown == ["s2:p1"], "post-cutoff evidence must never be shown"
    assert any(q["n_excluded"] >= 1 for q in any_hypothesis["queries"])

    # Second run: same cache, no provider calls, identical scores.
    second = ExperimentRunner(mock_config, "direct_rag", instance_ids=["RBV-01"])
    summary2 = second.run()
    assert summary2["literature_stats"]["provider_calls"] == 0
    assert summary2["literature_stats"]["cache_hits"] > 0
    assert read_json(second.run_dir / "instances" / "RBV-01" / "scores.json")["scores"] == \
        read_json(instance_dir / "scores.json")["scores"]


def test_instances_without_a_cutoff_are_skipped_not_guessed(mock_config, tmp_path, monkeypatch):
    empty_metadata = tmp_path / "empty_metadata.jsonl"
    empty_metadata.write_text("", encoding="utf-8")
    cfg = mock_config.model_copy(
        update={"dataset": mock_config.dataset.model_copy(update={"metadata_path": str(empty_metadata)})}
    )
    runner = ExperimentRunner(cfg, "direct_rag", instance_ids=["RBV-01"])
    summary = runner.run()
    assert summary["n_skipped"] == 1
    assert summary["metrics"]["n_scored"] == 0
    result = read_json(runner.run_dir / "instances" / "RBV-01" / "result.json")
    assert result["status"] == "skipped"
    assert "cutoff" in result["skip_reason"]


def test_direct_judge_never_constructs_a_literature_service(mock_config, monkeypatch):
    def explode(*args, **kwargs):
        raise AssertionError("direct_judge must not build a literature service")

    monkeypatch.setattr("src.experiments.runner.build_literature_service", explode)
    summary = ExperimentRunner(mock_config, "direct_judge", instance_ids=["RBV-03"]).run()
    assert summary["n_ok"] == 1
    assert summary["literature_stats"] is None


def test_llm_failures_are_recorded_and_do_not_abort_the_run(mock_config, monkeypatch):
    from src.llm import client as client_module

    def broken(messages, config):
        return "certainly not json"

    monkeypatch.setattr(client_module, "default_mock_responder", broken)
    runner = ExperimentRunner(mock_config, "direct_judge", instance_ids=["RBV-01", "RBV-02"])
    summary = runner.run()

    assert summary["n_error"] == 2
    assert summary["metrics"]["n_scored"] == 0
    errors = list(read_jsonl(runner.run_dir / "errors.jsonl"))
    assert errors and all(e["type"] == "LLMParseError" for e in errors)


def test_cli_smoke(mock_config, tmp_path, capsys):
    from src.experiments.run import main

    code = main(
        [
            "--method", "direct_judge",
            "--config", "configs/mvp.yaml",
            "--instances", "RBV-05",
            "--llm", "mock",
            "--set", "run.output_root={}".format(tmp_path / "cli_runs"),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "run:" in out
    assert json.loads(out.split("\n", 2)[2])["n_instances"] == 1


def test_a_controlled_k_set_derives_its_pair_metrics_from_the_instance():
    """Every negative in a k-set passed R2, so every gold-vs-negative pair counts.

    At k=2 this reduces exactly to Acc_pair, the protocol's headline metric; without
    it a k_sets run reported `pair_accuracy: None` while the pairwise win rate held
    the same number.
    """
    from src.benchmark.loader import BenchmarkInstance, Hypothesis
    from src.experiments.metrics import instance_metrics

    instance = BenchmarkInstance(
        id="K-0001-K3", researchbench_sample_id="K-0001", question="q",
        source_doi="10.0/x",
        hypotheses=[
            Hypothesis(id="H0", text="gold", gold=True),
            Hypothesis(id="H1", text="neg one"),
            Hypothesis(id="H2", text="neg two"),
        ],
    )
    row = instance_metrics(
        instance, {"H0": 0.9, "H1": 0.4, "H2": 0.9},
        pair_negative_ids=["H1", "H2"], pair_status="evaluable")
    # one win, one tie over two screened negatives
    assert row["pair_accuracy"] == pytest.approx(0.75)
    assert row["pair_accuracy"] == pytest.approx(row["pairwise_accuracy_all_negatives"])
