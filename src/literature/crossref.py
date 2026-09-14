"""Crossref client: DOI and publication-date metadata.

Crossref is the project's authority for source-paper dates (spec §3) and the
cross-check for provider-reported dates (spec §4). Every response is cached to
disk so that cutoff resolution is reproducible and auditable.

A DOI that Crossref does not know is *not* an error: `get_work` returns `None`
and the caller records `crossref_not_found`. Network and server failures raise,
so they can never be mistaken for absent metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.common.config import CrossrefConfig
from src.common.dates import PartialDate, parse_date_parts, parse_partial_date
from src.common.env import CROSSREF_MAILTO_VARS, get_env
from src.common.errors import MalformedResponseError, ProviderError
from src.common.io import (
    ensure_dir,
    read_json,
    resolve_path,
    slugify,
    stable_hash,
    utc_now_iso,
    write_json,
)
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.http import HttpClient

LOGGER = get_logger("crossref")

USER_AGENT = "hypothesis-verification-mvp/0.1 (research prototype)"


def normalise_doi(doi: Optional[str]) -> Optional[str]:
    """Lower-case bare DOI, with common URL prefixes removed."""
    if not doi:
        return None
    value = str(doi).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:", "https://dx.doi.org/", "http://dx.doi.org/"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    value = value.strip()
    return value or None


@dataclass
class CrossrefDates:
    """Date fields extracted from one Crossref work record."""

    doi: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    subtype: Optional[str] = None
    is_preprint: bool = False
    dates: Dict[str, PartialDate] = field(default_factory=dict)
    preprint_dois: List[str] = field(default_factory=list)
    journal_dois: List[str] = field(default_factory=list)

    def iso_dates(self) -> Dict[str, Optional[str]]:
        return {key: value.isoformat() for key, value in self.dates.items()}


class CrossrefClient:
    def __init__(
        self,
        config: CrossrefConfig,
        *,
        event_log: Optional[EventLog] = None,
        http: Optional[HttpClient] = None,
    ):
        self.config = config
        self.event_log = event_log or NULL_EVENT_LOG
        mailto = config.mailto or get_env(*CROSSREF_MAILTO_VARS)
        headers = {"User-Agent": USER_AGENT + (" (mailto:{})".format(mailto) if mailto else "")}
        self.mailto = mailto
        self.http = http or HttpClient(
            provider="crossref", config=config.http, headers=headers, event_log=self.event_log
        )
        self.cache_dir = resolve_path(config.cache.dir) if config.cache.enabled else None
        if self.cache_dir is not None:
            ensure_dir(self.cache_dir)

    # ------------------------------------------------------------------ #
    def _cache_path(self, doi: str):
        if self.cache_dir is None:
            return None
        return self.cache_dir / "{}.json".format(slugify(doi))

    def get_work(self, doi: str, *, refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Return the Crossref `message` for `doi`, or `None` if unknown to Crossref."""
        key = normalise_doi(doi)
        if not key:
            return None
        path = self._cache_path(key)
        if path is not None and path.exists() and not refresh:
            cached = read_json(path)
            self.event_log.api_call("crossref", "works/{}".format(key), cache="hit",
                                    status=cached.get("status_code"))
            return cached.get("message")

        url = "{}/works/{}".format(self.config.base_url.rstrip("/"), key)
        params: Dict[str, Any] = {}
        if self.mailto:
            params["mailto"] = self.mailto
        try:
            payload = self.http.get_json(url, params=params, endpoint="works/{}".format(key))
        except ProviderError as exc:
            if getattr(exc, "status_code", None) == 404:
                LOGGER.info("crossref: DOI not found: %s", key)
                self.event_log.decision("crossref_not_found", doi=key)
                if path is not None:
                    write_json(path, {"doi": key, "retrieved_at": utc_now_iso(),
                                      "status_code": 404, "message": None})
                return None
            raise

        message = payload.get("message")
        if not isinstance(message, dict):
            raise MalformedResponseError(
                "crossref: missing 'message' for {}".format(key), provider="crossref"
            )
        if path is not None:
            write_json(path, {"doi": key, "retrieved_at": utc_now_iso(),
                              "status_code": 200, "message": message})
        return message

    # ------------------------------------------------------------------ #
    def search_works(
        self,
        *,
        bibliographic: str,
        author: Optional[str] = None,
        rows: int = 20,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        """Bibliographic search, used to find other versions of a known work.

        Cached like `get_work`, so version resolution is reproducible. Returns
        the raw `message.items`; interpretation belongs to the caller.
        """
        params: Dict[str, Any] = {
            "query.bibliographic": bibliographic,
            "rows": max(1, min(int(rows), 100)),
            # `subtype` is not selectable on /works; preprints are identified by
            # `type == "posted-content"`.
            "select": "DOI,title,author,type,issued,published,published-online,"
                      "published-print,posted,created,relation",
        }
        if author:
            params["query.author"] = author
        if self.mailto:
            params["mailto"] = self.mailto

        cache_key = stable_hash({"endpoint": "works_search", "params": params}, length=24)
        path = self.cache_dir / "search" / "{}.json".format(cache_key) if self.cache_dir else None
        if path is not None and path.exists() and not refresh:
            cached = read_json(path)
            self.event_log.api_call("crossref", "works?query", cache="hit")
            return cached.get("items") or []

        payload = self.http.get_json(
            "{}/works".format(self.config.base_url.rstrip("/")), params=params, endpoint="works?query"
        )
        message = payload.get("message")
        if not isinstance(message, dict):
            raise MalformedResponseError(
                "crossref: missing 'message' in search response", provider="crossref"
            )
        items = message.get("items")
        if items is None:
            items = []
        if not isinstance(items, list):
            raise MalformedResponseError(
                "crossref: 'items' is {}, expected list".format(type(items).__name__),
                provider="crossref",
            )
        if path is not None:
            write_json(path, {"params": params, "retrieved_at": utc_now_iso(), "items": items})
        return items

    @staticmethod
    def author_families(message: Dict[str, Any]) -> List[str]:
        """Lower-cased family names from a Crossref work record."""
        names: List[str] = []
        for entry in message.get("author") or []:
            if not isinstance(entry, dict):
                continue
            family = entry.get("family") or entry.get("name") or ""
            family = str(family).strip().lower()
            if family:
                names.append(family.split()[-1])
        return names

    def extract_dates(self, message: Dict[str, Any]) -> CrossrefDates:
        """Pull every configured date field out of a Crossref work record."""
        titles = message.get("title") or []
        record = CrossrefDates(
            doi=normalise_doi(message.get("DOI")),
            title=titles[0] if isinstance(titles, list) and titles else None,
            type=message.get("type"),
            subtype=message.get("subtype"),
        )
        record.is_preprint = record.type == "posted-content" or record.subtype == "preprint"

        for key in self.config.date_fields:
            value = message.get(key)
            if value is None:
                continue
            if key == "created" and isinstance(value, dict) and "date-time" in value:
                partial = parse_partial_date(value["date-time"])
            else:
                partial = parse_date_parts(value)
            if partial.known:
                record.dates[key] = partial

        relation = message.get("relation") or {}
        if isinstance(relation, dict):
            for rel_key, target in (("has-preprint", record.preprint_dois),
                                    ("is-preprint-of", record.journal_dois)):
                entries = relation.get(rel_key) or []
                if isinstance(entries, dict):
                    entries = [entries]
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    if str(entry.get("id-type", "")).lower() not in ("doi", ""):
                        continue
                    doi = normalise_doi(entry.get("id"))
                    if doi:
                        target.append(doi)
        return record

    def get_dates(self, doi: str, *, refresh: bool = False) -> Optional[CrossrefDates]:
        message = self.get_work(doi, refresh=refresh)
        if message is None:
            return None
        return self.extract_dates(message)
