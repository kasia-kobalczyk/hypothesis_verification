"""Discovery of alternate versions of a source paper.

The cutoff is meant to precede the first public appearance of the source study.
Crossref's `relation.has-preprint` links only a small minority of preprints to
their journal version (1 of the 20 development cases), so relying on it leaves
the worst leak available open: an unlinked arXiv/bioRxiv posting of the source
paper, stating the very claim under test, sitting inside the eligible window.

This module searches Crossref bibliographically for other records of the same
study and accepts a candidate when the titles are close **and** the author lists
overlap. Author overlap alone never qualifies: an earlier, unrelated paper by
the same group is legitimate prior literature, not a version of this study.

Note the asymmetry with retrieval filtering. There, a false positive costs
recall and a false negative leaks, so the rules are strict. Here, a false
positive only moves the cutoff earlier and blocks one DOI — both conservative —
while a false negative leaks. The thresholds are therefore deliberately more
permissive than `literature.dedup`, and every candidate (accepted or not) is
recorded with its scores so the decision can be audited.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional, Sequence, Set

from src.common.config import CrossrefConfig, VersionSearchConfig
from src.common.dates import PartialDate
from src.common.logging_utils import get_logger
from src.literature.crossref import CrossrefClient, normalise_doi
from src.literature.dedup import title_similarity

LOGGER = get_logger("benchmark.versions")


@dataclass
class VersionCandidate:
    """One Crossref record considered as a version of the source study."""

    doi: Optional[str]
    title: Optional[str]
    type: Optional[str] = None
    is_preprint: bool = False
    title_similarity: float = 0.0
    author_overlap: int = 0
    author_overlap_fraction: float = 0.0
    candidate_author_count: int = 0
    shared_authors: List[str] = field(default_factory=list)
    earliest_date: Optional[date] = None
    basis_field: Optional[str] = None
    granularity: Optional[str] = None
    accepted: bool = False
    reason: str = ""
    source: str = "crossref_bibliographic_search"

    def record(self) -> Dict[str, Any]:
        return {
            "doi": self.doi,
            "title": self.title,
            "type": self.type,
            "is_preprint": self.is_preprint,
            "title_similarity": round(self.title_similarity, 3),
            "author_overlap": self.author_overlap,
            "author_overlap_fraction": round(self.author_overlap_fraction, 3),
            "candidate_author_count": self.candidate_author_count,
            "shared_authors": self.shared_authors,
            "earliest_date": self.earliest_date.isoformat() if self.earliest_date else None,
            "basis_field": self.basis_field,
            "granularity": self.granularity,
            "accepted": self.accepted,
            "reason": self.reason,
            "source": self.source,
        }


def _earliest_basis_date(
    dates: Dict[str, PartialDate], basis_fields: Sequence[str]
) -> "tuple[Optional[date], Optional[str], Optional[str]]":
    """Earliest day among the allowed basis fields, with its field and granularity."""
    best: Optional[date] = None
    best_field: Optional[str] = None
    best_granularity: Optional[str] = None
    for name, partial in dates.items():
        if basis_fields is not None and name not in basis_fields:
            continue
        resolved = partial.resolve(year_only_day="first", month_only_day="first")
        if resolved is None:
            continue
        if best is None or resolved < best:
            best, best_field, best_granularity = resolved, name, partial.granularity
    return best, best_field, best_granularity


def find_source_versions(
    *,
    crossref: CrossrefClient,
    source_doi: str,
    source_title: Optional[str],
    source_authors: Sequence[str],
    basis_fields: Sequence[str],
    config: VersionSearchConfig,
    crossref_config: CrossrefConfig,
    refresh: bool = False,
) -> List[VersionCandidate]:
    """Search Crossref for other records of the same study.

    Raises whatever the provider raises: a failed version search must not be
    mistaken for "this paper has no other versions".
    """
    if not source_title:
        LOGGER.warning("%s: no source title; version search skipped", source_doi)
        return []

    items = crossref.search_works(
        bibliographic=source_title,
        rows=config.rows,
        refresh=refresh,
    )
    source_key = normalise_doi(source_doi)
    source_author_set: Set[str] = {a.lower() for a in source_authors if a}
    allowed_types = set(config.include_types)
    candidates: List[VersionCandidate] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        doi = normalise_doi(item.get("DOI"))
        titles = item.get("title") or []
        title = titles[0] if isinstance(titles, list) and titles else None
        item_type = item.get("type")
        candidate = VersionCandidate(
            doi=doi,
            title=title,
            type=item_type,
            is_preprint=item_type == "posted-content",
            title_similarity=title_similarity(title, source_title),
        )
        families = {f.lower() for f in crossref.author_families(item)}
        shared = sorted(source_author_set & families)
        candidate.author_overlap = len(shared)
        candidate.candidate_author_count = len(families)
        candidate.shared_authors = shared
        # Overlap coefficient: share of the *smaller* author list. A preprint
        # whose journal version added authors still scores high.
        smaller = min(len(source_author_set), len(families))
        candidate.author_overlap_fraction = (len(shared) / smaller) if smaller else 0.0

        if doi and source_key and doi == source_key:
            candidate.reason = "the source record itself"
            candidates.append(candidate)
            continue
        if item_type and item_type not in allowed_types:
            candidate.reason = "type {!r} is not a version of a study".format(item_type)
            candidates.append(candidate)
            continue

        has_authors = bool(families) and bool(source_author_set)
        threshold = (
            config.title_similarity_threshold
            if has_authors
            else config.title_similarity_threshold_no_authors
        )
        if candidate.title_similarity < threshold:
            candidate.reason = "title similarity {:.2f} < {:.2f}".format(
                candidate.title_similarity, threshold
            )
            candidates.append(candidate)
            continue
        if has_authors and candidate.author_overlap < config.min_author_overlap:
            # Author overlap alone must never qualify, and a title match without
            # it is how an unrelated paper on the same topic sneaks in.
            candidate.reason = "author overlap {} < {}".format(
                candidate.author_overlap, config.min_author_overlap
            )
            candidates.append(candidate)
            continue
        if has_authors and candidate.author_overlap_fraction < config.min_author_overlap_fraction:
            # A different study by one shared author is prior literature, not a
            # version of this study (decision: block versions, not co-authors).
            candidate.reason = "author overlap fraction {:.2f} < {:.2f} ({}/{} shared)".format(
                candidate.author_overlap_fraction,
                config.min_author_overlap_fraction,
                candidate.author_overlap,
                min(len(source_author_set), len(families)),
            )
            candidates.append(candidate)
            continue

        dates = crossref.extract_dates(item)
        earliest, basis_field, granularity = _earliest_basis_date(dates.dates, basis_fields)
        candidate.earliest_date = earliest
        candidate.basis_field = basis_field
        candidate.granularity = granularity
        candidate.accepted = True
        candidate.reason = "title {:.2f}, {} shared author(s) ({:.0f}% of the smaller list)".format(
            candidate.title_similarity, candidate.author_overlap,
            100 * candidate.author_overlap_fraction,
        )
        candidates.append(candidate)
        LOGGER.info(
            "%s: accepted version %s (%s, %s) dated %s",
            source_doi, doi, item_type, candidate.reason, earliest,
        )

    return candidates
