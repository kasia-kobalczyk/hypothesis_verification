"""Provider-layer robustness (IMPLEMENTATION_SPEC.md §29).

Missing abstracts, missing DOIs, missing dates, rate limits, transient failures
and malformed payloads must each be handled explicitly — and a failure must
never turn into an empty result set.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

import pytest
import requests

from src.common.config import HTTPConfig
from src.common.errors import (
    MalformedResponseError,
    ProviderError,
    RateLimitError,
    TransientProviderError,
)
from src.literature.http import HttpClient
from src.literature.semantic_scholar import SemanticScholarProvider
from tests.conftest import s2_record, search_payload


class FakeResponse:
    def __init__(self, status_code: int, payload: Any = None, *, text: str = "", headers=None):
        self.status_code = status_code
        self._payload = payload
        self.text = text or (json.dumps(payload) if payload is not None else "")
        self.headers = headers or {}

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


class FakeSession:
    def __init__(self, responses: List[Any]):
        self.responses = list(responses)
        self.calls: List[Dict[str, Any]] = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append({"url": url, "params": params})
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def make_client(responses, **overrides) -> HttpClient:
    config = HTTPConfig(**{"max_retries": 3, "backoff_base_s": 0.0, "min_request_interval_s": 0.0, **overrides})
    return HttpClient(
        provider="test", config=config, session=FakeSession(responses), sleep=lambda _s: None
    )


# --------------------------------------------------------------------------- #
# HTTP behaviour
# --------------------------------------------------------------------------- #
def test_rate_limit_is_retried_then_succeeds():
    client = make_client([FakeResponse(429, headers={"Retry-After": "0"}), FakeResponse(200, {"ok": True})])
    assert client.get_json("http://x") == {"ok": True}
    assert len(client.session.calls) == 2


def test_rate_limit_exhaustion_raises_rather_than_returning_nothing():
    client = make_client([FakeResponse(429) for _ in range(3)])
    with pytest.raises(RateLimitError):
        client.get_json("http://x")


def test_transient_server_errors_are_retried():
    client = make_client([FakeResponse(503), FakeResponse(500), FakeResponse(200, {"ok": 1})])
    assert client.get_json("http://x") == {"ok": 1}


def test_connection_errors_are_retried_then_raised():
    client = make_client([requests.ConnectionError("boom")] * 3)
    with pytest.raises(TransientProviderError):
        client.get_json("http://x")


def test_client_errors_are_not_retried():
    client = make_client([FakeResponse(404, text="missing"), FakeResponse(200, {"ok": 1})])
    with pytest.raises(ProviderError) as excinfo:
        client.get_json("http://x")
    assert excinfo.value.status_code == 404
    assert len(client.session.calls) == 1


def test_non_json_bodies_raise_malformed():
    client = make_client([FakeResponse(200, None, text="<html>nope</html>")])
    with pytest.raises(MalformedResponseError):
        client.get_json("http://x")


def test_json_arrays_are_rejected():
    client = make_client([FakeResponse(200, [1, 2, 3])])
    with pytest.raises(MalformedResponseError):
        client.get_json("http://x")


# --------------------------------------------------------------------------- #
# Semantic Scholar normalisation
# --------------------------------------------------------------------------- #
@pytest.fixture
def provider(config):
    return SemanticScholarProvider(config.literature)


def test_missing_fields_are_tolerated(provider):
    payload = search_payload(
        [
            s2_record("a", abstract=None, doi=None, publication_date="2019-01-01"),
            s2_record("b", publication_date=None, year=None, doi="10.1/b"),
            {"paperId": "c", "title": "Bare record"},
        ]
    )
    papers = provider.normalise(payload, query="q")
    assert [p.paper_id for p in papers] == ["s2:a", "s2:b", "s2:c"]
    assert papers[0].abstract is None and papers[0].doi is None
    assert papers[1].publication_date is None
    assert papers[2].authors == []


def test_records_without_any_identifier_are_dropped(provider):
    payload = search_payload([{"externalIds": {}}, s2_record("ok", publication_date="2019-01-01")])
    assert [p.paper_id for p in provider.normalise(payload)] == ["s2:ok"]


def test_empty_results_are_not_an_error(provider):
    assert provider.normalise(search_payload([])) == []
    assert provider.normalise({"total": 0, "data": None}) == []


def test_unrecognised_payload_shape_raises(provider):
    with pytest.raises(MalformedResponseError):
        provider.normalise({"unexpected": "shape"})
    with pytest.raises(MalformedResponseError):
        provider.normalise({"data": "not a list"})


def test_reference_and_citation_envelopes_are_unwrapped(provider):
    record = s2_record("x", publication_date="2019-01-01")
    assert [p.paper_id for p in provider.normalise({"data": [{"citedPaper": record}]})] == ["s2:x"]
    assert [p.paper_id for p in provider.normalise({"data": [{"citingPaper": record}]})] == ["s2:x"]


def test_retrieval_provenance_is_recorded(provider):
    papers = provider.normalise(
        search_payload([s2_record("a", publication_date="2019-01-01"), s2_record("b", publication_date="2018-01-01")]),
        query="my query",
        retrieval_path="search",
    )
    assert [p.retrieval_rank for p in papers] == [1, 2]
    assert all(p.retrieval_query == "my query" for p in papers)
    assert all(p.raw for p in papers)


@pytest.mark.parametrize(
    "record,expected",
    [
        (s2_record("a", venue="arXiv", publication_date="2019-01-01"), True),
        (s2_record("b", doi="10.48550/arXiv.1901.00001", publication_date="2019-01-01"), True),
        (s2_record("c", venue="bioRxiv", publication_date="2019-01-01"), True),
        (s2_record("d", venue="Nature", doi="10.1038/x", publication_date="2019-01-01"), False),
    ],
)
def test_preprint_detection(provider, record, expected):
    assert provider.normalise(search_payload([record]))[0].is_preprint is expected


def test_doi_is_lowercased_from_external_ids(provider):
    paper = provider.normalise(search_payload([s2_record("a", doi="10.1038/S41586-024-07098-5")]))[0]
    assert paper.doi == "10.1038/s41586-024-07098-5"


# --------------------------------------------------------------------------- #
# Synthetic provider (offline plumbing only)
# --------------------------------------------------------------------------- #
def test_mock_provider_exercises_the_filter_path(config, registry):
    from datetime import date

    from src.literature.mock import MockLiteratureProvider
    from src.literature.cache import LiteratureCache
    from src.literature.service import LiteratureSearchService
    from src.literature.temporal_filter import TemporalFilter
    from tests.conftest import INSTANCE_ID

    provider = MockLiteratureProvider(config.literature)
    service = LiteratureSearchService(
        provider=provider,
        cutoff_registry=registry,
        temporal_filter=TemporalFilter(config.temporal, config.literature),
        cache=LiteratureCache(config.literature.cache),
        config=config,
    )
    record = service.search("a query", INSTANCE_ID)
    assert record.n_eligible > 0, "synthetic provider should yield some pre-cutoff records"
    assert record.n_excluded > 0, "and some that the filter must remove"
    assert all(p.eligible_date <= date(2020, 6, 15) for p in record.eligible)
    # Deterministic across instantiations.
    assert provider.search_raw("a query", limit=6) == MockLiteratureProvider(
        config.literature
    ).search_raw("a query", limit=6)
