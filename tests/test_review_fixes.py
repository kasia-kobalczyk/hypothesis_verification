"""Regression tests for defects found in review.

Each test names the invariant it protects; they are grouped here so the reasons
stay visible rather than being scattered across the suite.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from src.baselines.direct_rag import DirectRag
from src.benchmark.loader import load_instances
from src.benchmark.temporal import CutoffInfo, resolve_source_dates
from src.common.errors import ConfigError, ProviderError, TemporalLeakError
from src.common.io import read_json, read_jsonl
from src.experiments.runner import ExperimentRunner
from src.literature.base import Author, Paper
from src.literature.dedup import deduplicate
from src.literature.service import InstanceSearchTool
from src.literature.temporal_filter import TemporalFilter
from tests.conftest import CUTOFF, INSTANCE_ID, SOURCE_DOI, make_paper, s2_record, search_payload
from tests.test_baselines import make_context, make_rag_service
from tests.test_temporal_metadata import StubCrossref, parts, work


# --------------------------------------------------------------------------- #
# A leak must abort the experiment, not degrade one instance
# --------------------------------------------------------------------------- #
def test_direct_rag_does_not_swallow_a_temporal_leak(config, tmp_path):
    """`TemporalLeakError` subclasses the base error the retrieval loop catches."""
    instances = load_instances(config, instance_ids=["RBV-01"])
    service, provider = make_rag_service(config, {}, instances)
    provider.error = TemporalLeakError("post-cutoff paper reached the caller")
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, "RBV-01"))

    with pytest.raises(TemporalLeakError):
        DirectRag(config).run_instance(ctx)


def test_direct_rag_still_records_ordinary_provider_failures(config, tmp_path):
    instances = load_instances(config, instance_ids=["RBV-01"])
    service, provider = make_rag_service(config, {}, instances)
    provider.error = ProviderError("503", provider="semantic_scholar", status_code=503)
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, "RBV-01"))

    result = DirectRag(config).run_instance(ctx)
    assert result.status == "error"
    assert result.scores == {}


# --------------------------------------------------------------------------- #
# The final gate must not be weaker than the filter it backstops
# --------------------------------------------------------------------------- #
def test_final_gate_blocks_the_source_doi_without_a_blocklist(config):
    """`apply` blocked it via `source_doi`; `assert_no_leak` must agree."""
    info = CutoffInfo(
        instance_id=INSTANCE_ID, source_doi=SOURCE_DOI, cutoff_date=CUTOFF, blocked_dois=frozenset()
    )
    temporal_filter = TemporalFilter(config.temporal, config.literature)
    paper = make_paper("source", CUTOFF - timedelta(days=100), doi=SOURCE_DOI)

    assert temporal_filter.apply([paper], info).eligible == []
    paper.temporal_eligible = True
    with pytest.raises(TemporalLeakError):
        temporal_filter.assert_no_leak([paper], info)


# --------------------------------------------------------------------------- #
# An unlinked preprint of the source paper is the worst leak available
# --------------------------------------------------------------------------- #
SOURCE_TITLE = "JWST detection of a supernova associated with GRB 221009A"


def _source_info(**overrides) -> CutoffInfo:
    base = dict(
        instance_id=INSTANCE_ID,
        source_doi=SOURCE_DOI,
        cutoff_date=CUTOFF,
        blocked_dois=frozenset({SOURCE_DOI}),
        source_title=SOURCE_TITLE,
    )
    base.update(overrides)
    return CutoffInfo(**base)


def test_source_preprint_is_blocked_by_title_when_crossref_links_nothing(config):
    """A bioRxiv/arXiv posting of the source paper has a different DOI."""
    temporal_filter = TemporalFilter(config.temporal, config.literature)
    preprint = make_paper(
        "arxiv-version",
        CUTOFF - timedelta(days=200),
        title="JWST Detection of a Supernova Associated with GRB 221009A",
        doi="10.48550/arxiv.2302.00001",
        is_preprint=True,
    )
    outcome = temporal_filter.apply([preprint], _source_info())
    assert outcome.eligible == []
    assert outcome.excluded[0].exclusion_reason == "blocked_source_title_match"

    preprint.temporal_eligible = True
    with pytest.raises(TemporalLeakError):
        temporal_filter.assert_no_leak([preprint], _source_info())


def test_title_blocking_does_not_remove_ordinary_literature(config):
    temporal_filter = TemporalFilter(config.temporal, config.literature)
    other = make_paper(
        "other", CUTOFF - timedelta(days=200),
        title="Gamma-ray burst afterglow modelling in the optical",
        doi="10.1/other",
    )
    assert [p.paper_id for p in temporal_filter.apply([other], _source_info()).eligible] == ["other"]


def test_title_blocking_is_configurable_and_off_without_a_title(config):
    relaxed = config.temporal.model_copy(update={"block_source_by_title": False})
    preprint = make_paper("arx", CUTOFF - timedelta(days=200), title=SOURCE_TITLE, doi="10.48550/x")
    assert TemporalFilter(relaxed, config.literature).apply([preprint], _source_info()).eligible
    # And with no known source title there is nothing to match against.
    assert TemporalFilter(config.temporal, config.literature).apply(
        [make_paper("arx2", CUTOFF - timedelta(days=200), title=SOURCE_TITLE, doi="10.48550/y")],
        _source_info(source_title=None),
    ).eligible


def test_loader_supplies_the_source_title_to_the_registry(config):
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    assert instance.source_title
    assert instance.cutoff_info().source_title == instance.source_title


def test_version_search_outcome_is_always_reported(config):
    doi = "10.1/lonely"
    crossref = StubCrossref(config.crossref, {doi: work(doi, **{"published-online": parts(2020, 5, 10)})})
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=config.crossref
    )
    assert "version search found no other record" in record.notes
    assert record.ambiguous is False  # informational, not an unresolved date
    assert crossref.searches, "the version search must actually run"


def test_version_search_disabled_is_flagged(config):
    doi = "10.1/lonely"
    crossref = StubCrossref(config.crossref, {doi: work(doi, **{"published-online": parts(2020, 5, 10)})})
    temporal = config.temporal.model_copy(
        update={"version_search": config.temporal.version_search.model_copy(update={"enabled": False})}
    )
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=temporal, crossref_config=config.crossref
    )
    assert record.ambiguous is True
    assert "version search disabled" in record.notes


# --------------------------------------------------------------------------- #
# Failures have to be visible at run level
# --------------------------------------------------------------------------- #
def test_provider_failures_are_counted_in_service_stats(make_service):
    service, provider = make_service({"q": search_payload([])})
    provider.error = ProviderError("boom", provider="semantic_scholar")
    with pytest.raises(ProviderError):
        service.search("q", INSTANCE_ID)
    assert service.stats["errors"] == 1


def test_summary_reports_ambiguous_cutoffs(config):
    cfg = config.model_copy(update={"llm": config.llm.model_copy(update={"provider": "mock"})})
    runner = ExperimentRunner(cfg, "direct_judge", instance_ids=["RBV-13", "RBV-01"])
    summary = runner.run()
    assert summary["cutoffs"]["n_ambiguous"] >= 1
    assert "RBV-13" in summary["cutoffs"]["ambiguous_instances"]
    assert summary["cutoffs"]["n_ambiguous_scored"] >= 1
    rows = read_json(runner.run_dir / "metrics.json")["instances"]
    assert {r["instance_id"]: r["cutoff_ambiguous"] for r in rows}["RBV-13"] is True


def test_ambiguous_cutoffs_can_be_refused(config):
    cfg = config.model_copy(
        update={
            "llm": config.llm.model_copy(update={"provider": "mock"}),
            "literature": config.literature.model_copy(update={"provider": "mock"}),
            "dataset": config.dataset.model_copy(update={"require_unambiguous_cutoff": True}),
        }
    )
    summary = ExperimentRunner(cfg, "direct_rag", instance_ids=["RBV-13"]).run()
    assert summary["n_skipped"] == 1


# --------------------------------------------------------------------------- #
# Degenerate configuration must not manufacture `no_evidence`
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("key", ["queries_per_hypothesis", "top_k", "max_papers_in_prompt"])
def test_zero_retrieval_budgets_are_rejected(tmp_path, key):
    from src.common.config import load_config

    with pytest.raises(ConfigError):
        load_config("configs/mvp.yaml", overrides=["baselines.direct_rag.{}=0".format(key)])


def test_enforced_no_evidence_label_keeps_the_model_original(config, tmp_path):
    from src.llm.client import MockLLMClient

    llm = MockLLMClient(
        config.llm,
        responder=lambda messages, cfg: json.dumps({"queries": ["a", "b"]})
        if "search queries" in messages[0]["content"].lower()
        else json.dumps({"evidence_label": "support", "score": 80, "rationale": "r", "key_papers": []}),
    )
    instances = load_instances(config, instance_ids=["RBV-01"])
    service, provider = make_rag_service(config, {}, instances)
    provider.default = search_payload([])
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, "RBV-01"), llm=llm)

    result = DirectRag(config).run_instance(ctx)
    entry = next(iter(result.artifacts["evidence"]["by_hypothesis"].values()))["assessment"]
    assert entry["evidence_label"] == "no_evidence"
    assert entry["model_evidence_label"] == "support"
    assert entry["label_enforced_by_harness"] is True


# --------------------------------------------------------------------------- #
# Artifact fidelity
# --------------------------------------------------------------------------- #
def test_config_excluded_preprints_keep_their_dates(config, make_service):
    """Otherwise you cannot tell from retrieval.json whether one was pre-cutoff."""
    cfg = config.model_copy(
        update={"literature": config.literature.model_copy(update={"include_preprints": False})}
    )
    record_payload = search_payload(
        [s2_record("arx", venue="arXiv", publication_date="2019-01-01")]
    )
    service, _ = make_service({"q": record_payload}, cfg=cfg)
    record = service.search("q", INSTANCE_ID)
    assert record.eligible == []
    excluded = record.excluded[0]
    assert excluded.exclusion_reason == "preprint_excluded_by_config"
    assert excluded.eligible_date == date(2019, 1, 1)
    assert excluded.cutoff_date == CUTOFF


def test_version_chains_survive_a_second_dedup_pass(config):
    def paper(pid, title, authors, doi=None):
        p = make_paper(pid, date(2019, 1, 1), title=title, doi=doi)
        p.authors = [Author(name=name) for name in authors]
        return p

    v1 = paper("v1", "One mechanism described twice", ["A Author"])
    v2 = paper("v2", "One mechanism described twice", ["A Author"], doi="10.1/v2")
    first = deduplicate([v1, v2], config.literature.dedup)
    assert first.papers[0].versions == ["v2"]

    v3 = paper("v3", "One mechanism described twice", ["A Author"], doi="10.1/v3")
    second = deduplicate([v3] + first.papers, config.literature.dedup)
    assert second.papers[0].paper_id == "v3"
    assert set(second.papers[0].versions) == {"v1", "v2"}, "the v2 link must not be lost"


# --------------------------------------------------------------------------- #
# Frozen metadata must never be partially overwritten
# --------------------------------------------------------------------------- #
def test_resolving_a_subset_preserves_the_other_records(config, tmp_path, monkeypatch):
    from src.benchmark import resolve_dates as module

    out = Path(tmp_path) / "source_dates.jsonl"
    full = list(read_jsonl(config.dataset.metadata_path if Path(config.dataset.metadata_path).is_absolute()
                           else Path("data/metadata/source_dates.jsonl")))
    out.write_text("\n".join(json.dumps(row) for row in full) + "\n", encoding="utf-8")

    code = module.main(
        ["--config", "configs/mvp.yaml", "--out", str(out), "--instances", "RBV-01"]
    )
    assert code == 0
    after = list(read_jsonl(out))
    assert len(after) == len(full), "resolving one instance must not drop the others"
    assert {row["doi"] for row in after} == {row["doi"] for row in full}


def test_crossref_basis_fields_can_exclude_created(config):
    doi = "10.1/basis"
    crossref = StubCrossref(
        config.crossref,
        {doi: work(doi, created={"date-time": "2023-01-28T00:00:00Z"}, issued=parts(2023, 9))},
    )
    restricted = config.crossref.model_copy(
        update={"cutoff_basis_fields": ["published-online", "published-print", "published", "issued", "posted"]}
    )
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=restricted
    )
    assert record.selected_cutoff_basis == "issued"
    assert record.cutoff_date == date(2023, 8, 31)
    assert "excluded from the cutoff basis" in record.notes
    # Still recorded for provenance.
    assert record.other_dates.get("created") == "2023-01-28"


def test_same_authors_alone_never_blocks_a_paper(config):
    """Decision: block alternate versions of the study, not the group's earlier work."""
    info = _source_info(source_authors=frozenset({"levan", "malesani"}))
    temporal_filter = TemporalFilter(config.temporal, config.literature)
    earlier = make_paper(
        "earlier", CUTOFF - timedelta(days=900),
        title="Late-time observations of gamma-ray burst host galaxies",
        doi="10.1/earlier",
    )
    earlier.authors = [Author(name="A. J. Levan"), Author(name="D. B. Malesani")]
    assert [p.paper_id for p in temporal_filter.apply([earlier], info).eligible] == ["earlier"]


def test_title_match_needs_a_shared_author_when_both_are_known(config):
    info = _source_info(source_authors=frozenset({"levan"}))
    temporal_filter = TemporalFilter(config.temporal, config.literature)

    impostor = make_paper("impostor", CUTOFF - timedelta(days=100), title=SOURCE_TITLE, doi="10.1/x")
    impostor.authors = [Author(name="Someone Else")]
    assert [p.paper_id for p in temporal_filter.apply([impostor], info).eligible] == ["impostor"]

    real = make_paper("real-preprint", CUTOFF - timedelta(days=100), title=SOURCE_TITLE, doi="10.48550/z")
    real.authors = [Author(name="A. J. Levan")]
    assert temporal_filter.apply([real], info).excluded[0].exclusion_reason == "blocked_source_title_match"
