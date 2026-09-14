"""Deterministic offline literature provider.

For plumbing checks and CI only: it fabricates records from a hash of the query,
deliberately including post-cutoff items so that the filtering path is exercised.

Never report numbers produced with `literature.provider: mock` — the "evidence"
is synthetic. The runner logs a warning whenever it is used.
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from typing import Any, Dict, List, Optional

from src.common.config import LiteratureConfig
from src.common.io import stable_hash
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.semantic_scholar import SemanticScholarProvider

LOGGER = get_logger("literature.mock")


class MockLiteratureProvider(SemanticScholarProvider):
    """Synthetic provider reusing the real normalisation code."""

    name = "mock"
    version = "synthetic-v1"

    def __init__(self, config: LiteratureConfig, *, event_log: Optional[EventLog] = None, n_records: int = 6):
        # Skip the HTTP setup of the parent; nothing here talks to a network.
        self.config = config
        self.fields = []
        self.event_log = event_log or NULL_EVENT_LOG
        self.has_api_key = False
        self.http = None
        self.n_records = n_records
        LOGGER.warning("using the SYNTHETIC literature provider; results are not scientific evidence")

    def config_fingerprint(self) -> Dict[str, Any]:
        return {"provider": self.name, "provider_version": self.version, "n_records": self.n_records}

    def _records_for(self, key: str, max_date: Optional[date]) -> List[Dict[str, Any]]:
        rng = random.Random(int(stable_hash(key), 16))
        anchor = max_date or date(2020, 1, 1)
        records: List[Dict[str, Any]] = []
        for index in range(self.n_records):
            # Roughly two thirds pre-cutoff, one third after, plus one undated.
            offset = rng.randint(-2000, 400)
            when: Optional[date] = anchor + timedelta(days=offset)
            undated = index == self.n_records - 1
            records.append(
                {
                    "paperId": "mock-{}-{}".format(stable_hash(key, length=6), index),
                    "externalIds": {"DOI": "10.9999/mock.{}.{}".format(stable_hash(key, length=6), index)},
                    "title": "Synthetic study {} concerning: {}".format(index + 1, key[:80]),
                    "abstract": (
                        "Synthetic abstract for offline plumbing checks. It reports a measurement "
                        "related to the query terms and contains no real scientific content."
                    ),
                    "authors": [{"authorId": None, "name": "Mock Author {}".format(index)}],
                    "year": None if undated else when.year,
                    "publicationDate": None if undated else when.isoformat(),
                    "venue": "Journal of Synthetic Results",
                    "url": None,
                    "openAccessPdf": None,
                    "publicationTypes": ["JournalArticle"],
                }
            )
        return records

    def search_raw(self, query: str, *, limit: int, max_date: Optional[date] = None) -> Dict[str, Any]:
        records = self._records_for(query, max_date)[:limit]
        return {"total": len(records), "offset": 0, "data": records}

    def paper_raw(self, provider_id: str) -> Dict[str, Any]:
        return self._records_for(provider_id, None)[0]

    def references_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        return {"data": [{"citedPaper": r} for r in self._records_for("refs:" + provider_id, None)[:limit]]}

    def citations_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        return {"data": [{"citingPaper": r} for r in self._records_for("cites:" + provider_id, None)[:limit]]}
