"""Per-case cutoff enforcement for the explanatory-hypothesis benchmark.

`tests/test_temporal_filter.py` and friends already test the filtering machinery in
general. This module tests something narrower and more specific: that for each of the
eight frozen cases, *this case's actual resolving study* cannot reach the model
through any access path.

The method is adversarial rather than observational. A provider that happened to
return only pre-cutoff records would pass a test that merely watched real traffic,
and would prove nothing about what happens when the provider does return the answer
-- which is exactly what Semantic Scholar does when the resolver is highly cited and
on-topic. So the provider here is rigged: every channel returns the real resolver
DOI, title and date for the case being queried. The assertion is that none of it
survives.

Channels covered (BENCH-GRAPH-PILOT-001, Step: cutoff enforcement):
  1. search
  2. reference expansion
  3. citation expansion  (the dangerous one: citations of a pre-cutoff paper are
     almost all post-cutoff by construction)
  4. metadata / title / abstract lookup by id
  5. prompt rendering
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from src.benchmark.loader import load_case_instances
from src.common.config import AppConfig
from src.common.errors import TemporalLeakError
from src.common.logging_utils import NULL_EVENT_LOG
from src.literature.base import Paper
from src.literature.semantic_scholar import SemanticScholarProvider
from src.literature.service import LiteratureSearchService, build_literature_service
from src.literature.temporal_filter import TemporalFilter
from src.benchmark.loader import build_cutoff_registry

ROOT = Path(__file__).resolve().parents[1]
VISIBLE_PATH = ROOT / "benchmark" / "explanatory" / "cases_visible.jsonl"
HIDDEN_PATH = ROOT / "benchmark" / "explanatory" / "cases_hidden.json"


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def instances():
    return load_case_instances(AppConfig(), dataset_path=VISIBLE_PATH)


@pytest.fixture(scope="module")
def hidden() -> Dict[str, dict]:
    return json.loads(HIDDEN_PATH.read_text(encoding="utf-8"))["cases"]


def _resolver_records(case: dict) -> List[Dict[str, Any]]:
    """Every dated, DOI-bearing resolver entry for a case."""
    out = []
    for key, entry in (case.get("resolver") or {}).items():
        if isinstance(entry, dict) and entry.get("doi") and entry.get("date"):
            out.append({"key": key, "doi": entry["doi"], "date": entry["date"],
                        "venue": entry.get("venue") or entry.get("channel") or ""})
    return out


class AdversarialProvider(SemanticScholarProvider):
    """A provider that always returns the case's real resolver, on every path.

    This is the worst case the real provider can produce, made deterministic. If the
    filter holds here it holds against Semantic Scholar returning the resolver as a
    top hit, which for a well-cited resolver is the expected outcome, not an edge
    case.

    It subclasses the real provider and overrides only the four `*_raw` methods, so
    the payloads travel through the genuine normalisation code. A hand-rolled stub
    would have tested the filter against records the real pipeline never produces.
    """

    name = "adversarial-test"
    version = "v1"

    def __init__(self, config, resolver_records: List[Dict[str, Any]], cutoff: date):
        # Skip the parent's HTTP setup; nothing here touches a network.
        self.config = config
        self.fields = []
        self.event_log = NULL_EVENT_LOG
        self.has_api_key = False
        self.http = None
        self.records = resolver_records
        self.cutoff = cutoff
        self.calls: List[str] = []

    def config_fingerprint(self) -> Dict[str, Any]:
        return {"provider": self.name, "provider_version": self.version}

    def _payload(self) -> List[Dict[str, Any]]:
        items = []
        # One clearly pre-cutoff decoy, so a filter that simply dropped everything
        # would fail the companion test rather than pass this one.
        items.append({
            "paperId": "pre-cutoff-decoy",
            "externalIds": {"DOI": "10.1000/pre.cutoff.decoy"},
            "title": "A pre-cutoff study of the phenomenon",
            "abstract": "Published well before the cutoff.",
            "publicationDate": (self.cutoff.replace(year=self.cutoff.year - 2)).isoformat(),
            "year": self.cutoff.year - 2,
            "authors": [{"name": "Early Author"}],
            "venue": "Pre-cutoff Journal",
        })
        for index, rec in enumerate(self.records):
            items.append({
                "paperId": "resolver-{}".format(index),
                "externalIds": {"DOI": rec["doi"]},
                "title": "RESOLVING STUDY ({}): decisive result".format(rec["key"]),
                "abstract": "RESOLVER ABSTRACT: reports the observation that settles the case.",
                "publicationDate": rec["date"],
                "year": int(rec["date"][:4]),
                "authors": [{"name": "Resolver Author"}],
                "venue": rec["venue"],
            })
        return items

    def search_raw(self, query: str, *, limit: int, max_date: Optional[date] = None):
        self.calls.append("search")
        return {"data": self._payload()[:limit]}

    def paper_raw(self, provider_id: str):
        self.calls.append("lookup")
        payload = self._payload()
        for item in payload:
            if item["paperId"] == provider_id:
                return item
        return payload[-1]  # a resolver record, for any unknown id

    def references_raw(self, provider_id: str, *, limit: int):
        self.calls.append("references")
        return {"data": [{"citedPaper": item} for item in self._payload()[:limit]]}

    def citations_raw(self, provider_id: str, *, limit: int):
        self.calls.append("citations")
        return {"data": [{"citingPaper": item} for item in self._payload()[:limit]]}


def _test_config(tmp_path) -> AppConfig:
    """A config that isolates the test from the network and from the shared cache.

    Crossref verification is switched off so the filter has to reject the resolver on
    the provider's own dates alone -- which is the harder case, not the easier one.
    The cache is redirected to a temp dir so these adversarial records can never be
    served to a real run.
    """
    config = AppConfig()
    config.literature.verify_dates_with_crossref = "never"
    config.literature.cache.enabled = False
    config.literature.cache.dir = str(tmp_path / "cache")
    return config


def _service_for(instance, case, config):
    registry = build_cutoff_registry([instance])
    provider = AdversarialProvider(
        config.literature, _resolver_records(case), instance.cutoff_date)
    service = build_literature_service(config, registry, provider=provider)
    return service, provider


def _case_params(instances, hidden):
    return [(inst, hidden[inst.id]) for inst in instances]


# --------------------------------------------------------------------------- #
# The benchmark's own precondition: every resolver is post-cutoff
# --------------------------------------------------------------------------- #
def test_every_resolver_postdates_its_cutoff(instances, hidden):
    """If a resolver predated the cutoff the case would be unsound regardless of any
    filtering, because the answer would be legitimately retrievable."""
    by_id = {i.id: i for i in instances}
    for case_id, case in hidden.items():
        cutoff = by_id[case_id].cutoff_date
        records = _resolver_records(case)
        assert records, "{}: no dated resolver record".format(case_id)
        for rec in records:
            when = date.fromisoformat(rec["date"])
            assert when > cutoff, (
                "{}: resolver {} dated {} does not postdate cutoff {}".format(
                    case_id, rec["key"], rec["date"], cutoff))


def test_every_case_has_a_frozen_cutoff(instances):
    for instance in instances:
        assert instance.has_cutoff
        assert instance.cutoff_basis == "frozen_benchmark_manifest"
        assert not instance.cutoff_ambiguous
        assert instance.cutoff_date >= date(2024, 1, 1)


# --------------------------------------------------------------------------- #
# Channels 1-4: the resolver must not survive any retrieval path
# --------------------------------------------------------------------------- #
def _assert_no_resolver(papers, case, where: str, case_id: str):
    dois = {rec["doi"].lower() for rec in _resolver_records(case)}
    for paper in papers:
        got = (paper.doi or "").lower()
        assert got not in dois, "{}: resolver DOI survived {}: {}".format(
            case_id, where, got)
        assert "RESOLVING STUDY" not in (paper.title or ""), (
            "{}: resolver title survived {}".format(case_id, where))
        assert "RESOLVER ABSTRACT" not in (paper.abstract or ""), (
            "{}: resolver abstract survived {}".format(case_id, where))


def test_search_is_cutoff_filtered(instances, hidden, tmp_path):
    config = _test_config(tmp_path)
    for instance in instances:
        case = hidden[instance.id]
        service, provider = _service_for(instance, case, config)
        papers = service.search_literature("what settles this question", instance.id)
        _assert_no_resolver(papers, case, "search", instance.id)
        assert "search" in provider.calls


def test_reference_expansion_is_cutoff_filtered(instances, hidden, tmp_path):
    config = _test_config(tmp_path)
    for instance in instances:
        case = hidden[instance.id]
        service, _ = _service_for(instance, case, config)
        papers = service.expand_references("pre-cutoff-decoy", instance.id)
        _assert_no_resolver(papers, case, "reference expansion", instance.id)


def test_citation_expansion_is_cutoff_filtered(instances, hidden, tmp_path):
    """Citations of a pre-cutoff paper are overwhelmingly post-cutoff. This is the
    path most likely to surface the resolver in real use."""
    config = _test_config(tmp_path)
    for instance in instances:
        case = hidden[instance.id]
        service, _ = _service_for(instance, case, config)
        papers = service.expand_citations("pre-cutoff-decoy", instance.id)
        _assert_no_resolver(papers, case, "citation expansion", instance.id)


def test_metadata_lookup_cannot_reintroduce_a_post_cutoff_record(instances, hidden, tmp_path):
    """Filtering search but not `get_paper_details` would leave an obvious hole: an
    agent that learned an id from anywhere could fetch the record directly."""
    config = _test_config(tmp_path)
    for instance in instances:
        case = hidden[instance.id]
        service, _ = _service_for(instance, case, config)
        for index in range(len(_resolver_records(case))):
            paper = service.get_paper_details("resolver-{}".format(index), instance.id)
            assert paper is None, (
                "{}: metadata lookup returned the resolver".format(instance.id))


def test_a_pre_cutoff_record_does_survive(instances, hidden, tmp_path):
    """The companion to every test above: the filter must be discriminating, not
    merely restrictive. A filter that dropped everything would pass all the leak
    tests and make the pilot meaningless."""
    config = _test_config(tmp_path)
    survived = 0
    for instance in instances:
        service, _ = _service_for(instance, hidden[instance.id], config)
        papers = service.search_literature("the phenomenon", instance.id)
        if any((p.doi or "") == "10.1000/pre.cutoff.decoy" for p in papers):
            survived += 1
    assert survived == len(instances), (
        "pre-cutoff decoy survived on only {}/{} cases".format(survived, len(instances)))


# --------------------------------------------------------------------------- #
# Channel 5: prompt rendering re-applies the filter
# --------------------------------------------------------------------------- #
def test_prompt_rendering_refuses_a_post_cutoff_paper(instances, hidden, tmp_path):
    """`render_for_prompt` is the last gate. Even if a post-cutoff record reached a
    caller by some route not covered above, it must not be renderable into context.
    """
    config = _test_config(tmp_path)
    for instance in instances:
        case = hidden[instance.id]
        records = _resolver_records(case)
        if not records:
            continue
        service, _ = _service_for(instance, case, config)
        smuggled = Paper(
            paper_id="smuggled",
            provider="adversarial-test",
            doi=records[0]["doi"],
            title="RESOLVING STUDY: decisive result",
            abstract="RESOLVER ABSTRACT",
            publication_date=records[0]["date"],
            year=int(records[0]["date"][:4]),
        )
        with pytest.raises(TemporalLeakError):
            service.render_for_prompt([smuggled], instance_id=instance.id)


def test_agent_facing_api_exposes_no_cutoff_parameter():
    """The cutoff must not be something a method can pass, override or widen: it is
    read from the registry on every call. This is enforced by signature, not by
    instruction to the model."""
    import inspect

    for name in ("search_literature", "search", "expand_references",
                 "expand_citations", "get_paper_details"):
        sig = inspect.signature(getattr(LiteratureSearchService, name))
        for param in sig.parameters:
            assert "cutoff" not in param.lower() and "date" not in param.lower(), (
                "{} exposes a cutoff parameter: {}".format(name, param))


def test_filter_blocks_the_resolver_doi_directly(instances, hidden):
    """Unit-level backstop on the filter itself, independent of the service."""
    config = AppConfig()
    config.literature.verify_dates_with_crossref = "never"
    filt = TemporalFilter(config.temporal, config.literature)
    for instance in instances:
        info = build_cutoff_registry([instance]).require(instance.id)
        for rec in _resolver_records(hidden[instance.id]):
            paper = Paper(
                paper_id="p", provider="t", doi=rec["doi"],
                title="resolver", publication_date=rec["date"],
                year=int(rec["date"][:4]),
            )
            outcome = filt.apply([paper], info)
            assert not outcome.eligible, (
                "{}: filter admitted {}".format(instance.id, rec["doi"]))
