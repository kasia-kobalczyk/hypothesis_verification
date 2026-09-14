"""Shared test fixtures.

Tests never touch the network: the Semantic Scholar provider is subclassed so
that real normalisation code runs over canned payloads, and the LLM is the
deterministic mock client.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

import pytest

from src.benchmark.temporal import CutoffInfo, CutoffRegistry
from src.common.config import AppConfig
from src.literature.base import Paper
from src.literature.cache import LiteratureCache
from src.literature.semantic_scholar import SemanticScholarProvider
from src.literature.service import LiteratureSearchService
from src.literature.temporal_filter import TemporalFilter

INSTANCE_ID = "T-01"
CUTOFF = date(2020, 6, 15)
SOURCE_DOI = "10.1234/source-paper"


def s2_record(
    paper_id: str,
    *,
    title: str = "A study",
    publication_date: Optional[str] = None,
    year: Optional[int] = None,
    doi: Optional[str] = None,
    abstract: Optional[str] = "An abstract.",
    authors: Optional[List[str]] = None,
    venue: str = "Journal of Testing",
    external_ids: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """A Semantic Scholar-shaped record."""
    ids: Dict[str, str] = dict(external_ids or {})
    if doi:
        ids.setdefault("DOI", doi)
    return {
        "paperId": paper_id,
        "externalIds": ids,
        "title": title,
        "abstract": abstract,
        "authors": [{"authorId": None, "name": name} for name in (authors or ["A. Author"])],
        "year": year if year is not None else (int(publication_date[:4]) if publication_date else None),
        "publicationDate": publication_date,
        "venue": venue,
        "url": "https://example.org/" + paper_id,
        "openAccessPdf": None,
        "publicationTypes": ["JournalArticle"],
    }


def search_payload(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"total": len(records), "offset": 0, "data": records}


class FakeS2Provider(SemanticScholarProvider):
    """Semantic Scholar provider with canned payloads and call counting."""

    def __init__(self, config, *, payloads: Optional[Dict[str, Dict[str, Any]]] = None, default: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(config, **kwargs)
        self.payloads = payloads or {}
        self.default = default if default is not None else search_payload([])
        self.calls: List[Dict[str, Any]] = []
        self.error: Optional[Exception] = None

    def _payload(self, key: str) -> Dict[str, Any]:
        if self.error is not None:
            raise self.error
        return self.payloads.get(key, self.default)

    def search_raw(self, query: str, *, limit: int, max_date=None) -> Dict[str, Any]:
        self.calls.append({"path": "search", "query": query, "limit": limit, "max_date": max_date})
        return self._payload(query)

    def paper_raw(self, provider_id: str) -> Dict[str, Any]:
        self.calls.append({"path": "lookup", "id": provider_id})
        return self._payload("paper:" + provider_id)

    def references_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        self.calls.append({"path": "references", "id": provider_id, "limit": limit})
        return self._payload("references:" + provider_id)

    def citations_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        self.calls.append({"path": "citations", "id": provider_id, "limit": limit})
        return self._payload("citations:" + provider_id)


@pytest.fixture
def config(tmp_path) -> AppConfig:
    """Base config: mock LLM, temp caches, no Crossref verification."""
    return AppConfig(
        **{
            "run": {"seed": 1234, "output_root": str(tmp_path / "runs")},
            "dataset": {"path": "data/researchbench_dev20.jsonl"},
            "literature": {
                "top_k": 10,
                "verify_dates_with_crossref": "never",
                "cache": {"enabled": True, "dir": str(tmp_path / "cache")},
            },
            "crossref": {"cache": {"enabled": True, "dir": str(tmp_path / "crossref")}},
            "llm": {"provider": "mock"},
        }
    )


@pytest.fixture
def cutoff_info() -> CutoffInfo:
    return CutoffInfo(
        instance_id=INSTANCE_ID,
        source_doi=SOURCE_DOI,
        cutoff_date=CUTOFF,
        basis="published-online",
        blocked_dois=frozenset({SOURCE_DOI}),
    )


@pytest.fixture
def registry(cutoff_info) -> CutoffRegistry:
    return CutoffRegistry([cutoff_info])


@pytest.fixture
def make_service(config, registry):
    """Factory: payload dict -> (service, provider)."""

    def _make(payloads: Optional[Dict[str, Dict[str, Any]]] = None, *, default=None, cfg: Optional[AppConfig] = None):
        cfg = cfg or config
        provider = FakeS2Provider(cfg.literature, payloads=payloads, default=default)
        service = LiteratureSearchService(
            provider=provider,
            cutoff_registry=registry,
            temporal_filter=TemporalFilter(cfg.temporal, cfg.literature),
            cache=LiteratureCache(cfg.literature.cache),
            config=cfg,
        )
        return service, provider

    return _make


def make_paper(paper_id: str, when: Optional[date], **kwargs: Any) -> Paper:
    """A `Paper` already carrying a resolved eligible date."""
    return Paper(
        paper_id=paper_id,
        provider="test",
        title=kwargs.pop("title", "Test paper"),
        publication_date=when.isoformat() if when else None,
        eligible_date=when,
        date_source="provider" if when else "none",
        date_granularity="day" if when else "none",
        temporal_eligible=kwargs.pop("temporal_eligible", True),
        **kwargs,
    )
