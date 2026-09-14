"""Semantic Scholar Graph API provider.

IMPLEMENTATION_SPEC.md §4: the primary literature-retrieval and relevance-ranking
provider. This module only talks to the API and normalises records; it makes no
temporal decisions (that is `temporal_filter`, reached through `service`).

Malformed or partial records are tolerated field-by-field — a missing abstract
or a missing DOI is normal and must not abort a query — but a payload without a
recognisable envelope raises `MalformedResponseError` rather than quietly
becoming zero results.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from src.common.config import LiteratureConfig
from src.common.env import S2_KEY_VARS, get_env
from src.common.errors import MalformedResponseError
from src.common.io import stable_hash
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.base import Author, LiteratureProvider, Paper
from src.literature.crossref import normalise_doi
from src.literature.http import HttpClient

LOGGER = get_logger("literature.semantic_scholar")

BASE_URL = "https://api.semanticscholar.org/graph/v1"

DEFAULT_FIELDS = (
    "paperId",
    "externalIds",
    "title",
    "abstract",
    "authors",
    "year",
    "publicationDate",
    "venue",
    "publicationVenue",
    "url",
    "openAccessPdf",
    "publicationTypes",
    "journal",
    "citationCount",
)

PREPRINT_VENUE_HINTS = ("arxiv", "biorxiv", "medrxiv", "chemrxiv", "ssrn", "research square", "preprints.org")
PREPRINT_DOI_PREFIXES = ("10.48550/", "10.1101/", "10.21203/", "10.26434/", "10.20944/")


class SemanticScholarProvider(LiteratureProvider):
    name = "semantic_scholar"
    version = "graph-v1"

    def __init__(
        self,
        config: LiteratureConfig,
        *,
        event_log: Optional[EventLog] = None,
        http: Optional[HttpClient] = None,
        base_url: str = BASE_URL,
        fields: Optional[List[str]] = None,
    ):
        self.config = config
        self.base_url = base_url.rstrip("/")
        self.fields = list(fields or DEFAULT_FIELDS)
        self.event_log = event_log or NULL_EVENT_LOG
        api_key = get_env(*S2_KEY_VARS)
        headers = {"User-Agent": "hypothesis-verification-mvp/0.1"}
        if api_key:
            headers["x-api-key"] = api_key
        self.has_api_key = bool(api_key)
        self.http = http or HttpClient(
            provider=self.name, config=config.http, headers=headers, event_log=self.event_log
        )

    # ------------------------------------------------------------------ #
    def config_fingerprint(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "provider_version": self.version,
            "fields": sorted(self.fields),
            "provider_prefilter_by_date": self.config.provider_prefilter_by_date,
        }

    # ------------------------------------------------------------------ #
    # Raw access
    # ------------------------------------------------------------------ #
    def search_raw(
        self,
        query: str,
        *,
        limit: int,
        max_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "query": query,
            "limit": max(1, min(int(limit), 100)),
            "fields": ",".join(self.fields),
        }
        # Provider-side prefilter. This is an efficiency measure so that the
        # top-k slots are not consumed by post-cutoff hits; the authoritative
        # filter still runs locally on everything that comes back.
        if max_date is not None and self.config.provider_prefilter_by_date:
            params["publicationDateOrYear"] = ":{}".format(max_date.isoformat())
        return self.http.get_json(self.base_url + "/paper/search", params=params, endpoint="paper/search")

    def paper_raw(self, provider_id: str) -> Dict[str, Any]:
        return self.http.get_json(
            "{}/paper/{}".format(self.base_url, provider_id),
            params={"fields": ",".join(self.fields)},
            endpoint="paper/{id}",
        )

    def references_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        return self.http.get_json(
            "{}/paper/{}/references".format(self.base_url, provider_id),
            params={"fields": ",".join(self.fields), "limit": max(1, min(int(limit), 1000))},
            endpoint="paper/{id}/references",
        )

    def citations_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        return self.http.get_json(
            "{}/paper/{}/citations".format(self.base_url, provider_id),
            params={"fields": ",".join(self.fields), "limit": max(1, min(int(limit), 1000))},
            endpoint="paper/{id}/citations",
        )

    # ------------------------------------------------------------------ #
    # Normalisation
    # ------------------------------------------------------------------ #
    @staticmethod
    def _records(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Unwrap search / reference / citation / single-paper envelopes."""
        if "data" in payload:
            data = payload.get("data")
            if data is None:
                return []
            if not isinstance(data, list):
                raise MalformedResponseError(
                    "semantic_scholar: 'data' is {}, expected list".format(type(data).__name__),
                    provider="semantic_scholar",
                )
            records: List[Dict[str, Any]] = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                nested = item.get("citedPaper") or item.get("citingPaper")
                records.append(nested if isinstance(nested, dict) else item)
            return records
        if "paperId" in payload or "title" in payload:
            return [payload]
        if "total" in payload or "next" in payload or "offset" in payload:
            # A search envelope that reports no hits may omit `data` entirely.
            # That is a genuine empty result, not a malformed payload.
            return []
        raise MalformedResponseError(
            "semantic_scholar: unrecognised payload keys {}".format(sorted(payload)[:10]),
            provider="semantic_scholar",
        )

    @staticmethod
    def _is_preprint(record: Dict[str, Any], doi: Optional[str]) -> bool:
        venue_obj = record.get("publicationVenue") or {}
        if isinstance(venue_obj, dict) and str(venue_obj.get("type", "")).lower() == "preprint":
            return True
        types = record.get("publicationTypes") or []
        if isinstance(types, list) and any(str(t).lower() == "preprint" for t in types):
            return True
        venue = str(record.get("venue") or "").lower()
        if any(hint in venue for hint in PREPRINT_VENUE_HINTS):
            return True
        if doi and any(doi.startswith(prefix) for prefix in PREPRINT_DOI_PREFIXES):
            return True
        external = record.get("externalIds") or {}
        if isinstance(external, dict) and "ArXiv" in external and not external.get("DOI"):
            return True
        return False

    def normalise(
        self,
        payload: Dict[str, Any],
        *,
        query: Optional[str] = None,
        retrieval_path: str = "search",
    ) -> List[Paper]:
        papers: List[Paper] = []
        for rank, record in enumerate(self._records(payload), start=1):
            paper = self._normalise_record(record, query=query, rank=rank, retrieval_path=retrieval_path)
            if paper is not None:
                papers.append(paper)
        return papers

    def _normalise_record(
        self,
        record: Dict[str, Any],
        *,
        query: Optional[str],
        rank: int,
        retrieval_path: str,
    ) -> Optional[Paper]:
        if not isinstance(record, dict):
            return None
        provider_id = record.get("paperId")
        external = record.get("externalIds") if isinstance(record.get("externalIds"), dict) else {}
        doi = normalise_doi(external.get("DOI") or record.get("doi"))

        if not provider_id and not doi and not record.get("title"):
            self.event_log.decision("dropped_record", reason="no_identifier", retrieval_path=retrieval_path)
            LOGGER.debug("dropping unidentifiable record: %s", str(record)[:200])
            return None

        paper_id = (
            "s2:{}".format(provider_id)
            if provider_id
            else "doi:{}".format(doi)
            if doi
            else "title:{}".format(stable_hash(str(record.get("title")), length=12))
        )

        authors: List[Author] = []
        for entry in record.get("authors") or []:
            if isinstance(entry, dict):
                authors.append(Author(name=entry.get("name") or "", author_id=entry.get("authorId")))
            elif isinstance(entry, str):
                authors.append(Author(name=entry))

        open_access = record.get("openAccessPdf")
        pdf_url = open_access.get("url") if isinstance(open_access, dict) else None

        venue = record.get("venue") or None
        if not venue:
            journal = record.get("journal")
            if isinstance(journal, dict):
                venue = journal.get("name") or None

        year = record.get("year")
        try:
            year = int(year) if year is not None else None
        except (TypeError, ValueError):
            year = None

        if record.get("abstract") is None:
            self.event_log.decision(
                "missing_abstract", paper_id=paper_id, retrieval_path=retrieval_path
            )

        return Paper(
            paper_id=paper_id,
            provider=self.name,
            provider_id=provider_id,
            doi=doi,
            title=record.get("title") or "",
            abstract=record.get("abstract"),
            authors=authors,
            year=year,
            publication_date=record.get("publicationDate") or (str(year) if year else None),
            venue=venue,
            url=record.get("url"),
            is_preprint=self._is_preprint(record, doi),
            open_access_pdf=pdf_url,
            retrieval_query=query,
            retrieval_rank=rank,
            retrieval_path=retrieval_path,
            raw=record,
        )
