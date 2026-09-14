"""Cutoff filtering: boundary policy, undated records, blocked DOIs, conflicts.

IMPLEMENTATION_SPEC.md §30 ("temporal filtering", "boundary date").
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from src.benchmark.temporal import CutoffInfo
from src.common.errors import MissingCutoffError, TemporalLeakError
from src.literature.base import Paper
from src.literature.temporal_filter import TemporalFilter
from tests.conftest import CUTOFF, INSTANCE_ID, SOURCE_DOI, make_paper


def build_filter(config, **temporal_overrides):
    temporal = config.temporal.model_copy(update=temporal_overrides)
    return TemporalFilter(temporal, config.literature)


def test_post_cutoff_paper_is_excluded(config, cutoff_info):
    papers = [
        make_paper("pre", CUTOFF - timedelta(days=1)),
        make_paper("post", CUTOFF + timedelta(days=1)),
    ]
    outcome = build_filter(config).apply(papers, cutoff_info)
    assert [p.paper_id for p in outcome.eligible] == ["pre"]
    assert [p.paper_id for p in outcome.excluded] == ["post"]
    assert outcome.excluded[0].exclusion_reason == "post_cutoff"
    assert outcome.excluded[0].temporal_eligible is False


def test_boundary_date_inclusive_by_default(config, cutoff_info):
    outcome = build_filter(config).apply([make_paper("on-cutoff", CUTOFF)], cutoff_info)
    assert [p.paper_id for p in outcome.eligible] == ["on-cutoff"]


def test_boundary_date_exclusive_when_configured(config, cutoff_info):
    outcome = build_filter(config, boundary="exclusive").apply([make_paper("on-cutoff", CUTOFF)], cutoff_info)
    assert outcome.eligible == []
    assert outcome.excluded[0].exclusion_reason == "post_cutoff"


def test_year_only_dates_resolve_to_the_end_of_the_period(config, cutoff_info):
    """A paper dated "2020" might have appeared in December, so it is excluded
    from a June cutoff rather than assumed to be early in the year."""
    paper = Paper(paper_id="year-only", provider="test", title="t", publication_date="2020", year=2020)
    outcome = build_filter(config).apply([paper], cutoff_info)
    assert outcome.eligible == []
    assert outcome.excluded[0].eligible_date == date(2020, 12, 31)

    paper_2019 = Paper(paper_id="earlier", provider="test", title="t", publication_date="2019", year=2019)
    outcome = build_filter(config).apply([paper_2019], cutoff_info)
    assert [p.paper_id for p in outcome.eligible] == ["earlier"]


def test_month_granularity_resolves_to_month_end(config, cutoff_info):
    paper = Paper(paper_id="june", provider="test", title="t", publication_date="2020-06", year=2020)
    outcome = build_filter(config).apply([paper], cutoff_info)
    assert outcome.excluded[0].eligible_date == date(2020, 6, 30)


def test_undated_papers_are_excluded_by_default(config, cutoff_info):
    paper = Paper(paper_id="undated", provider="test", title="t")
    outcome = build_filter(config).apply([paper], cutoff_info)
    assert outcome.eligible == []
    assert outcome.excluded[0].exclusion_reason == "unknown_publication_date"


def test_undated_papers_can_be_admitted_by_configuration(config, cutoff_info):
    paper = Paper(paper_id="undated", provider="test", title="t")
    outcome = build_filter(config, unknown_date_policy="include").apply([paper], cutoff_info)
    assert [p.paper_id for p in outcome.eligible] == ["undated"]
    assert outcome.notes


def test_source_paper_is_blocked_even_when_pre_cutoff(config, cutoff_info):
    paper = make_paper("source", CUTOFF - timedelta(days=400), doi=SOURCE_DOI.upper())
    outcome = build_filter(config).apply([paper], cutoff_info)
    assert outcome.eligible == []
    assert outcome.excluded[0].exclusion_reason == "blocked_source_doi"


def test_conflicting_dates_resolve_to_the_latest_estimate(config):
    """Provider says pre-cutoff, Crossref says post-cutoff -> exclude."""
    calls = []

    def verifier(doi):
        calls.append(doi)
        return CUTOFF + timedelta(days=10)

    temporal_filter = TemporalFilter(
        config.temporal,
        config.literature.model_copy(update={"verify_dates_with_crossref": "always"}),
        date_verifier=verifier,
    )
    paper = make_paper("conflict", CUTOFF - timedelta(days=5), doi="10.5555/conflict")
    info = CutoffInfo(instance_id=INSTANCE_ID, source_doi=None, cutoff_date=CUTOFF)
    outcome = temporal_filter.apply([paper], info)
    assert calls == ["10.5555/conflict"]
    assert outcome.eligible == []
    assert "disagrees" in " ".join(outcome.excluded[0].date_notes)


def test_earliest_conflict_policy_keeps_the_paper(config):
    temporal_filter = TemporalFilter(
        config.temporal.model_copy(update={"conflict_policy": "earliest"}),
        config.literature.model_copy(update={"verify_dates_with_crossref": "always"}),
        date_verifier=lambda doi: CUTOFF + timedelta(days=10),
    )
    paper = make_paper("conflict", CUTOFF - timedelta(days=5), doi="10.5555/conflict")
    info = CutoffInfo(instance_id=INSTANCE_ID, source_doi=None, cutoff_date=CUTOFF)
    outcome = temporal_filter.apply([paper], info)
    assert [p.paper_id for p in outcome.eligible] == ["conflict"]


def test_verifier_failure_is_recorded_not_swallowed(config):
    def verifier(doi):
        raise RuntimeError("crossref down")

    temporal_filter = TemporalFilter(
        config.temporal,
        config.literature.model_copy(update={"verify_dates_with_crossref": "always"}),
        date_verifier=verifier,
    )
    paper = make_paper("p", CUTOFF - timedelta(days=5), doi="10.5555/x")
    info = CutoffInfo(instance_id=INSTANCE_ID, source_doi=None, cutoff_date=CUTOFF)
    outcome = temporal_filter.apply([paper], info)
    assert [p.paper_id for p in outcome.eligible] == ["p"]
    assert any("crossref_verification_failed" in note for note in outcome.eligible[0].date_notes)


def test_missing_cutoff_refuses_to_filter(config):
    info = CutoffInfo(instance_id="no-cutoff", source_doi=None, cutoff_date=None)
    with pytest.raises(MissingCutoffError):
        build_filter(config).apply([make_paper("p", CUTOFF)], info)


def test_assert_no_leak_catches_tampered_records(config, cutoff_info):
    """A record whose eligibility flag was flipped by hand still cannot pass."""
    tampered = make_paper("tampered", CUTOFF + timedelta(days=30))
    tampered.temporal_eligible = True  # as if a buggy/malicious path set this
    with pytest.raises(TemporalLeakError):
        build_filter(config).assert_no_leak([tampered], cutoff_info)


def test_assert_no_leak_catches_undated_and_blocked(config, cutoff_info):
    undated = make_paper("undated", None)
    undated.temporal_eligible = True
    with pytest.raises(TemporalLeakError):
        build_filter(config).assert_no_leak([undated], cutoff_info)

    blocked = make_paper("source", CUTOFF - timedelta(days=10), doi=SOURCE_DOI)
    with pytest.raises(TemporalLeakError):
        build_filter(config).assert_no_leak([blocked], cutoff_info)


def test_assert_no_leak_accepts_clean_records(config, cutoff_info):
    ok = make_paper("ok", CUTOFF - timedelta(days=10))
    build_filter(config).assert_no_leak([ok], cutoff_info)  # must not raise
