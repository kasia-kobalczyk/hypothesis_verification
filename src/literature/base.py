"""Provider-independent literature data model and provider interface.

IMPLEMENTATION_SPEC.md §5: one stable structured representation for every
literature result, carrying enough provenance to reproduce why a paper was
returned.

Two fields deserve attention:

* `publication_date` is what the provider reported, verbatim, possibly partial.
* `eligible_date` is the single concrete date the cutoff decision was made on,
  together with `date_source` and `date_granularity` explaining how it was
  derived. Filtering never re-derives a date; it reads `eligible_date`.
"""

from __future__ import annotations

import abc
from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.common.dates import Granularity


class Author(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = ""
    author_id: Optional[str] = None

    @property
    def family_name(self) -> str:
        parts = [p for p in self.name.replace(",", " ").split() if p]
        return parts[-1].lower() if parts else ""


class Paper(BaseModel):
    """A single literature record, normalised across providers."""

    model_config = ConfigDict(extra="forbid")

    # Identity / provenance
    paper_id: str
    provider: str
    provider_id: Optional[str] = None
    doi: Optional[str] = None

    # Bibliographic content
    title: str = ""
    abstract: Optional[str] = None
    authors: List[Author] = Field(default_factory=list)
    year: Optional[int] = None
    publication_date: Optional[str] = None  # as reported, may be partial
    venue: Optional[str] = None
    url: Optional[str] = None
    is_preprint: bool = False
    open_access_pdf: Optional[str] = None

    # Retrieval provenance
    retrieval_query: Optional[str] = None
    retrieval_rank: Optional[int] = None
    retrieval_path: str = "search"  # search | references | citations | lookup

    # Temporal decision (set by src.literature.temporal_filter, never by a model)
    date_granularity: Granularity = "none"
    date_source: str = "none"  # provider | crossref | year_fallback | none
    eligible_date: Optional[date] = None
    cutoff_date: Optional[date] = None
    temporal_eligible: bool = False
    exclusion_reason: Optional[str] = None
    date_notes: List[str] = Field(default_factory=list)

    # Version linking (src.literature.dedup)
    duplicate_group: Optional[str] = None
    duplicate_of: Optional[str] = None
    # Other records collapsed into this one (set on the group representative).
    versions: List[str] = Field(default_factory=list)
    # Below the confident threshold: kept separate, flagged for the assessor.
    possibly_related_to: List[str] = Field(default_factory=list)

    # Raw provider record. Never rendered into a prompt.
    raw: Dict[str, Any] = Field(default_factory=dict)

    def citation_line(self) -> str:
        authors = ", ".join(a.name for a in self.authors[:3])
        if len(self.authors) > 3:
            authors += " et al."
        bits = [b for b in [authors, self.venue, self.publication_date or (str(self.year) if self.year else None)] if b]
        return "{} ({})".format(self.title, "; ".join(bits)) if bits else self.title


class RetrievalRecord(BaseModel):
    """Everything that happened for one query, kept for post-hoc diagnosis."""

    model_config = ConfigDict(extra="forbid")

    query: str
    instance_id: str
    provider: str
    provider_version: str
    top_k: int
    cutoff_date: Optional[date]
    retrieval_path: str = "search"
    cache_status: str = "miss"  # hit | miss | refresh | disabled | offline_hit
    retrieved_at: Optional[str] = None
    n_raw: int = 0
    n_normalised: int = 0
    n_eligible: int = 0
    n_excluded: int = 0
    n_duplicates_collapsed: int = 0
    eligible: List[Paper] = Field(default_factory=list)
    # Post-cutoff / undated records. Stored for debugging only; §7 forbids these
    # from ever entering model context.
    excluded: List[Paper] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    error: Optional[str] = None

    def public_papers(self) -> List[Paper]:
        return list(self.eligible)


class LiteratureProvider(abc.ABC):
    """Raw access to an external literature provider.

    Implementations return provider-shaped payloads and normalise them into
    `Paper` objects. They do **not** apply the temporal cutoff: filtering is the
    responsibility of `src.literature.service.LiteratureSearchService`, so that
    there is exactly one enforcement point for every access path.
    """

    name: str = "abstract"
    version: str = "0"

    @abc.abstractmethod
    def search_raw(
        self,
        query: str,
        *,
        limit: int,
        max_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Relevance search. `max_date` is an optional provider-side prefilter."""

    @abc.abstractmethod
    def paper_raw(self, provider_id: str) -> Dict[str, Any]:
        """Metadata lookup for a single paper."""

    @abc.abstractmethod
    def references_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        """Outgoing references of a paper."""

    @abc.abstractmethod
    def citations_raw(self, provider_id: str, *, limit: int) -> Dict[str, Any]:
        """Incoming citations of a paper."""

    @abc.abstractmethod
    def normalise(
        self,
        payload: Dict[str, Any],
        *,
        query: Optional[str] = None,
        retrieval_path: str = "search",
    ) -> List[Paper]:
        """Convert a raw payload into `Paper` records (no temporal decisions)."""

    def config_fingerprint(self) -> Dict[str, Any]:
        """Provider configuration that must participate in the cache key."""
        return {"provider": self.name, "provider_version": self.version}
