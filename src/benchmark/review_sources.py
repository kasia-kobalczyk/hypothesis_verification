"""Detect benchmark rows whose source paper is a review article.

A review source breaks task validity. The "gold hypothesis" of a review is a
summary of work already published, so the finding is in the pre-cutoff literature
by construction and retrieval can return the primary paper that established it.
Measured case: `RBV2-0012-N00`'s source is a *Trends in Cell Biology* review, and
the consequence-graph run retrieved the primary paper outright.

The ResearchBench screening rubric's R3 ("presented as supported by the source
study") does not exclude reviews, so this is an additional gate for *future
evaluation benchmarks*. It is not applied retroactively to frozen slices: those
are flagged in a side file and left untouched.

**Detection is deliberately crude and deliberately visible.** Crossref types
reviews as `journal-article` -- the disulfidptosis review above is typed exactly
that -- so there is no authoritative field to read. What is left is the venue and
the title, matched against patterns that live in `configs/mvp.yaml` rather than
here. That misses review articles in general-purpose journals, which is recorded as
a TODO rather than papered over: closing it needs the abstract or full text, and
probably a classifier.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from src.common.logging_utils import get_logger

LOGGER = get_logger("benchmark.review_sources")


@dataclass(frozen=True)
class ReviewSourceVerdict:
    """Why a source was or was not called a review. Never a bare boolean."""

    is_review: bool
    basis: Optional[str]          # venue_pattern | title_pattern | None
    matched: Optional[str]        # the pattern that fired
    venue: Optional[str]
    title: Optional[str]

    def record(self) -> Dict[str, Any]:
        return {
            "is_review": self.is_review,
            "basis": self.basis,
            "matched": self.matched,
            "venue": self.venue,
            "title": self.title,
        }


def _normalise(value: Optional[str]) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def classify_source(
    *,
    venue: Optional[str],
    title: Optional[str],
    venue_patterns: Sequence[str],
    title_patterns: Sequence[str],
) -> ReviewSourceVerdict:
    """Match venue then title against the configured patterns.

    Patterns are plain lowercase substrings, not regexes: a research owner has to
    be able to read the list in the config file and predict what it does. Venue is
    checked first because it is the more reliable signal -- a journal named
    *Annual Review of X* publishes reviews, whereas a title beginning "A review
    of" occasionally belongs to a primary paper.
    """
    normalised_venue = _normalise(venue)
    normalised_title = _normalise(title)

    for pattern in venue_patterns:
        needle = _normalise(pattern)
        if needle and needle in normalised_venue:
            return ReviewSourceVerdict(True, "venue_pattern", pattern, venue, title)
    for pattern in title_patterns:
        needle = _normalise(pattern)
        if needle and needle in normalised_title:
            return ReviewSourceVerdict(True, "title_pattern", pattern, venue, title)
    return ReviewSourceVerdict(False, None, None, venue, title)


def venue_and_title_from_crossref(message: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """Pull the two fields detection needs out of a cached Crossref record."""

    def first(value: Any) -> Optional[str]:
        if isinstance(value, list):
            return str(value[0]) if value else None
        return str(value) if value else None

    return {
        "venue": first(message.get("container-title")) or first(
            message.get("short-container-title")),
        "title": first(message.get("title")),
        "crossref_type": message.get("type"),
        "crossref_subtype": message.get("subtype"),
    }


def summarise(verdicts: Dict[str, ReviewSourceVerdict]) -> Dict[str, Any]:
    flagged = {k: v for k, v in verdicts.items() if v.is_review}
    by_basis: Dict[str, int] = {}
    for verdict in flagged.values():
        by_basis[verdict.basis or "?"] = by_basis.get(verdict.basis or "?", 0) + 1
    return {
        "n_checked": len(verdicts),
        "n_flagged": len(flagged),
        "by_basis": by_basis,
        "flagged": {k: v.record() for k, v in sorted(flagged.items())},
        "limitation": (
            "venue/title matching only. Crossref types review articles as "
            "journal-article, so a review in a general-purpose journal is not "
            "detected. TODO(research): classify from the abstract."
        ),
    }
