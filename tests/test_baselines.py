"""Baseline behaviour: isolation, missing evidence, failure handling.

IMPLEMENTATION_SPEC.md §10, §11, §29, §30.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.baselines.direct_judge import DirectJudge
from src.baselines.direct_rag import DirectRag
from src.benchmark.loader import build_cutoff_registry, load_instances
from src.benchmark.presentation import build_presentation
from src.common.errors import (
    BaselineIsolationError,
    CacheMissError,
    ProviderError,
    RateLimitError,
)
from src.common.logging_utils import EventLog
from src.experiments.base import InstanceContext
from src.inference.parameters import load_ordinal_mappings
from src.literature.cache import LiteratureCache
from src.literature.service import (
    ForbiddenLiteratureService,
    InstanceSearchTool,
    LiteratureSearchService,
)
from src.literature.temporal_filter import TemporalFilter
from src.llm.client import MockLLMClient
from src.llm.prompts import PromptLibrary
from tests.conftest import FakeS2Provider, s2_record, search_payload

INSTANCE_ID = "RBV-01"


def make_context(config, tmp_path, *, literature, llm=None, instance_id=INSTANCE_ID) -> InstanceContext:
    instance = load_instances(config, instance_ids=[instance_id])[0]
    return InstanceContext(
        instance=instance,
        config=config,
        llm=llm or MockLLMClient(config.llm),
        prompts=PromptLibrary(config.prompts.dir),
        presentation=build_presentation(instance, config.run),
        literature=literature,
        mappings=load_ordinal_mappings(config.ordinal_mappings_path),
        event_log=EventLog(Path(tmp_path) / "events.jsonl"),
        output_dir=Path(tmp_path),
    )


def make_rag_service(config, payloads, instances):
    provider = FakeS2Provider(config.literature, payloads=payloads)
    service = LiteratureSearchService(
        provider=provider,
        cutoff_registry=build_cutoff_registry(instances),
        temporal_filter=TemporalFilter(config.temporal, config.literature),
        cache=LiteratureCache(config.literature.cache),
        config=config,
    )
    return service, provider


# --------------------------------------------------------------------------- #
# Direct judge
# --------------------------------------------------------------------------- #
def test_direct_judge_never_touches_the_literature(config, tmp_path):
    """Isolation is structural: any access raises (§30 'baseline isolation')."""
    forbidden = ForbiddenLiteratureService("direct_judge")
    ctx = make_context(config, tmp_path, literature=forbidden)
    result = DirectJudge(config).run_instance(ctx)

    assert result.status == "ok"
    assert set(result.scores) == set(ctx.instance.hypothesis_ids)
    assert result.diagnostics["n_queries"] == 0
    with pytest.raises(BaselineIsolationError):
        forbidden.search("anything")
    assert DirectJudge.requires_literature is False


def test_direct_judge_prompt_hides_internal_ids(config, tmp_path):
    llm = MockLLMClient(config.llm)
    ctx = make_context(config, tmp_path, literature=ForbiddenLiteratureService("direct_judge"), llm=llm)
    DirectJudge(config).run_instance(ctx)
    prompt = llm.calls[0][0]["content"]
    assert "Hypothesis A:" in prompt
    assert "H0" not in prompt
    # The cutoff date must not be revealed to the model (§7: the backend
    # enforces the window; the prompt must not disclose when the source appeared).
    # Asserted only against a real date — `"None" not in prompt` would be vacuous.
    assert ctx.instance.cutoff_date is not None, "frozen metadata is required for this test"
    assert str(ctx.instance.cutoff_date) not in prompt
    # The template itself must not mark or hint at the gold hypothesis
    # ("gold" also occurs as a chemical element inside hypothesis text).
    template = ctx.prompts.get(config.baselines.direct_judge.prompt_version).text.lower()
    assert "gold" not in template


def test_direct_judge_reports_parse_failure_as_an_error(config, tmp_path):
    llm = MockLLMClient(config.llm, responder=lambda messages, cfg: "not json at all")
    ctx = make_context(config, tmp_path, literature=ForbiddenLiteratureService("dj"), llm=llm)
    result = DirectJudge(config).run_instance(ctx)

    assert result.status == "error"
    assert result.scores == {}
    assert result.errors and result.errors[0]["type"] == "LLMParseError"
    assert result.artifacts["model_outputs"]["error_type"] == "LLMParseError"


def test_direct_judge_rejects_incomplete_score_vectors(config, tmp_path):
    """A reply missing hypotheses is a parse failure, not a partial ranking."""
    llm = MockLLMClient(
        config.llm,
        responder=lambda messages, cfg: json.dumps({"scores": [{"id": "A", "score": 50}]}),
    )
    ctx = make_context(config, tmp_path, literature=ForbiddenLiteratureService("dj"), llm=llm)
    result = DirectJudge(config).run_instance(ctx)
    assert result.status == "error"


# --------------------------------------------------------------------------- #
# Direct RAG
# --------------------------------------------------------------------------- #
def test_direct_rag_runs_end_to_end_with_mock_backends(config, tmp_path):
    instances = load_instances(config, instance_ids=[INSTANCE_ID])
    payload = search_payload(
        [
            s2_record("p1", title="Relevant pre-cutoff study", publication_date="2019-05-05"),
            s2_record("p2", title="Post-cutoff study", publication_date="2025-01-01"),
        ]
    )
    service, provider = make_rag_service(config, {}, instances)
    provider.default = payload
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, INSTANCE_ID))

    result = DirectRag(config).run_instance(ctx)

    assert result.status == "ok"
    assert set(result.scores) == set(ctx.instance.hypothesis_ids)
    assert result.diagnostics["n_queries"] == 2 * len(ctx.instance.hypotheses)
    assert result.diagnostics["n_retrieval_errors"] == 0

    shown = result.artifacts["retrieval"]["by_hypothesis"][ctx.instance.hypotheses[0].id]["papers_shown"]
    assert [p["paper_id"] for p in shown] == ["s2:p1"]
    assert all(p["temporal_eligible"] for p in shown)


def test_direct_rag_marks_zero_results_as_no_evidence(config, tmp_path):
    """Missing literature is `no_evidence`, never a contradiction (§20, §30)."""
    instances = load_instances(config, instance_ids=[INSTANCE_ID])
    service, provider = make_rag_service(config, {}, instances)
    provider.default = search_payload([])
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, INSTANCE_ID))

    result = DirectRag(config).run_instance(ctx)

    # A search that succeeds and returns nothing is an outcome, not a failure.
    assert result.status == "ok"
    assert result.diagnostics["n_retrieval_errors"] == 0
    assert result.diagnostics["n_eligible_papers"] == 0
    labels = {
        entry["assessment"]["evidence_label"]
        for entry in result.artifacts["evidence"]["by_hypothesis"].values()
    }
    assert labels == {"no_evidence"}
    assert all(
        entry["assessment"]["n_papers_shown"] == 0
        for entry in result.artifacts["evidence"]["by_hypothesis"].values()
    )
    assert result.diagnostics["n_no_evidence_assessments"] == len(ctx.instance.hypotheses)
    assert result.diagnostics["n_informative_assessments"] == 0
    # The harness guard itself is tested in
    # `test_assessor_cannot_claim_support_without_retrieved_papers`.


def test_no_evidence_is_neutral_under_the_ordinal_mapping(config, tmp_path):
    cfg = config.model_copy(
        update={
            "baselines": config.baselines.model_copy(
                update={
                    "direct_rag": config.baselines.direct_rag.model_copy(
                        update={"ranking_signal": "ordinal_map"}
                    )
                }
            )
        }
    )
    instances = load_instances(cfg, instance_ids=[INSTANCE_ID])
    service, provider = make_rag_service(cfg, {}, instances)
    provider.default = search_payload([])
    ctx = make_context(cfg, tmp_path, literature=InstanceSearchTool(service, INSTANCE_ID))

    result = DirectRag(cfg).run_instance(ctx)
    assert set(result.scores.values()) == {0.0}, "no_evidence must not push a hypothesis down"


def test_assessor_cannot_claim_support_without_retrieved_papers(config, tmp_path):
    """A model that answers `support` with an empty evidence set is corrected."""
    llm = MockLLMClient(
        config.llm,
        responder=lambda messages, cfg: json.dumps({"queries": ["a", "b"]})
        if "search queries" in messages[0]["content"].lower()
        else json.dumps({"evidence_label": "strong_support", "score": 90, "rationale": "r", "key_papers": []}),
    )
    instances = load_instances(config, instance_ids=[INSTANCE_ID])
    service, provider = make_rag_service(config, {}, instances)
    provider.default = search_payload([])
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, INSTANCE_ID), llm=llm)

    result = DirectRag(config).run_instance(ctx)
    labels = {
        entry["assessment"]["evidence_label"]
        for entry in result.artifacts["evidence"]["by_hypothesis"].values()
    }
    assert labels == {"no_evidence"}


@pytest.mark.parametrize(
    "error",
    [
        RateLimitError("throttled", provider="semantic_scholar"),
        ProviderError("500", provider="semantic_scholar", status_code=500),
        CacheMissError("offline miss"),
    ],
)
def test_retrieval_failure_is_an_error_not_no_evidence(config, tmp_path, error):
    """§29: API failure != no_evidence. The instance must not be scored."""
    instances = load_instances(config, instance_ids=[INSTANCE_ID])
    service, provider = make_rag_service(config, {}, instances)
    provider.error = error
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, INSTANCE_ID))

    result = DirectRag(config).run_instance(ctx)

    assert result.status == "error"
    assert result.scores == {}
    assert result.diagnostics["n_retrieval_errors"] > 0
    assert result.diagnostics["n_no_evidence_assessments"] == 0
    assert all(e["where"] == "direct_rag.retrieval" for e in result.errors)
    assert result.artifacts["evidence"]["by_hypothesis"] == {}


def test_direct_rag_queries_are_frozen_before_retrieval(config, tmp_path):
    """Queries are generated from (question, hypothesis) only — never from results."""
    seen: List[Dict[str, Any]] = []

    def responder(messages, cfg):
        content = messages[0]["content"]
        seen.append({"content": content})
        if "search queries" in content.lower():
            assert "RETRIEVED LITERATURE" not in content
            return json.dumps({"queries": ["neutral query one", "neutral query two"]})
        return json.dumps(
            {"evidence_label": "weak_support", "score": 55, "rationale": "r", "key_papers": []}
        )

    instances = load_instances(config, instance_ids=[INSTANCE_ID])
    service, provider = make_rag_service(config, {}, instances)
    provider.default = search_payload([s2_record("p1", publication_date="2019-01-01")])
    ctx = make_context(
        config, tmp_path, literature=InstanceSearchTool(service, INSTANCE_ID),
        llm=MockLLMClient(config.llm, responder=responder),
    )
    result = DirectRag(config).run_instance(ctx)

    queries = result.artifacts["queries"]["by_hypothesis"]
    assert all(entry["queries"] == ["neutral query one", "neutral query two"] for entry in queries.values())
    assert result.status == "ok"
