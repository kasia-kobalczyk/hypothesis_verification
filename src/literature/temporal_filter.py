"""The single enforcement point for the literature cutoff.

IMPLEMENTATION_SPEC.md §7. Design rules encoded here:

1. The cutoff arrives as a frozen `CutoffInfo`; no caller supplies a date.
2. Every record gets exactly one `eligible_date`, derived once, with its source
   and granularity recorded, and the decision is made on that field alone.
3. Uncertainty is resolved *against* eligibility: partial dates collapse to the
   last day they could denote and, under `conflict_policy: latest`, disagreeing
   sources collapse to the latest estimate. A record with no usable date is
   excluded (`unknown_date_policy: exclude`).
4. `assert_no_leak` re-runs the cutoff comparison, the source-paper checks and
   the undated-record policy immediately before anything is shown to a model,
   using the same helpers as `apply`. It reads `eligible_date` rather than
   re-parsing the provider fields, so it catches a flipped `temporal_eligible`
   flag or a record that never went through `apply`, but not a forged
   `eligible_date`. `eligible_date` is written only by `assign_eligible_date`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from src.benchmark.temporal import CutoffInfo
from src.common.config import LiteratureConfig, TemporalConfig
from src.common.dates import PartialDate, parse_partial_date
from src.common.errors import MissingCutoffError, TemporalLeakError
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.base import Paper
from src.literature.crossref import normalise_doi
from src.literature.dedup import title_similarity

LOGGER = get_logger("literature.temporal_filter")

# `verifier(doi) -> earliest known public availability` (Crossref, in practice).
# Returning a `PartialDate` keeps the granularity of the external record, so the
# audit trail does not claim day precision for a year-only Crossref date. A bare
# `date` is also accepted and treated as day precision.
DateVerifier = Callable[[str], Optional["date | PartialDate"]]


@dataclass
class FilterOutcome:
    eligible: List[Paper] = field(default_factory=list)
    excluded: List[Paper] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @property
    def counts(self) -> Dict[str, int]:
        reasons: Dict[str, int] = {}
        for paper in self.excluded:
            key = paper.exclusion_reason or "unknown"
            reasons[key] = reasons.get(key, 0) + 1
        return reasons


class TemporalFilter:
    """Applies the frozen cutoff to candidate literature records."""

    def __init__(
        self,
        temporal: TemporalConfig,
        literature: LiteratureConfig,
        *,
        date_verifier: Optional[DateVerifier] = None,
        event_log: Optional[EventLog] = None,
    ):
        self.temporal = temporal
        self.literature = literature
        self.date_verifier = date_verifier
        self.event_log = event_log or NULL_EVENT_LOG

    # ------------------------------------------------------------------ #
    # Date derivation
    # ------------------------------------------------------------------ #
    def _provider_estimate(self, paper: Paper) -> Tuple[Optional[date], str, str]:
        """Best estimate of public availability from the provider's own fields."""
        partial: PartialDate = parse_partial_date(paper.publication_date)
        if partial.known:
            resolved = partial.resolve(
                year_only_day=self.temporal.year_only_day,
                month_only_day=self.temporal.month_only_day,
            )
            source = "provider" if partial.granularity == "day" else "provider_partial"
            return resolved, source, partial.granularity
        if paper.year is not None:
            resolved = PartialDate(year=paper.year).resolve(
                year_only_day=self.temporal.year_only_day,
                month_only_day=self.temporal.month_only_day,
            )
            return resolved, "provider_year_fallback", "year"
        return None, "none", "none"

    def _needs_verification(self, estimate: Optional[date], cutoff: Optional[date]) -> bool:
        mode = self.literature.verify_dates_with_crossref
        if mode == "never" or self.date_verifier is None:
            return False
        if mode == "always":
            return True
        # boundary_only: verify when undated, or close enough to the cutoff to matter.
        if estimate is None or cutoff is None:
            return True
        window = timedelta(days=self.literature.verify_boundary_window_days)
        return abs((estimate - cutoff).days) <= window.days

    def assign_eligible_date(self, paper: Paper, cutoff: Optional[date]) -> Paper:
        """Populate `eligible_date`, `date_source`, `date_granularity`, `date_notes`."""
        estimate, source, granularity = self._provider_estimate(paper)
        notes: List[str] = []
        estimates: List[Tuple[date, str]] = []
        if estimate is not None:
            estimates.append((estimate, source))

        doi = normalise_doi(paper.doi)
        verified_granularity: Optional[str] = None
        if doi and self._needs_verification(estimate, cutoff):
            try:
                verified = self.date_verifier(doi) if self.date_verifier else None
            except Exception as exc:  # provider failure must not silently pass
                verified = None
                notes.append("crossref_verification_failed: {}".format(exc))
                self.event_log.decision(
                    "date_verification_failed", paper_id=paper.paper_id, doi=doi, error=str(exc)
                )
            if isinstance(verified, PartialDate):
                verified_granularity = verified.granularity
                verified = verified.resolve(
                    year_only_day=self.temporal.year_only_day,
                    month_only_day=self.temporal.month_only_day,
                )
            elif verified is not None:
                verified_granularity = "day"
            if verified is not None:
                estimates.append((verified, "crossref"))
                if estimate is not None and verified != estimate:
                    notes.append(
                        "provider date {} disagrees with Crossref {}".format(
                            estimate.isoformat(), verified.isoformat()
                        )
                    )

        if not estimates:
            paper.eligible_date = None
            paper.date_source = "none"
            paper.date_granularity = granularity
            paper.date_notes = notes
            return paper

        if self.temporal.conflict_policy == "latest":
            chosen, chosen_source = max(estimates, key=lambda item: item[0])
        else:
            chosen, chosen_source = min(estimates, key=lambda item: item[0])

        if chosen_source == "crossref" and verified_granularity is not None:
            # Crossref supplied the date the decision is made on; record its
            # granularity rather than the provider's.
            granularity = verified_granularity
        if len(estimates) > 1:
            chosen_source = "{}({})".format(self.temporal.conflict_policy, chosen_source)
        paper.eligible_date = chosen
        paper.date_source = chosen_source
        paper.date_granularity = granularity
        paper.date_notes = notes
        return paper

    # ------------------------------------------------------------------ #
    # Filtering
    # ------------------------------------------------------------------ #
    def blocked_dois(self, cutoff_info: CutoffInfo) -> Set[Optional[str]]:
        """DOIs that must never be returned, whatever their date.

        `apply` and `assert_no_leak` share this so the final gate cannot be
        weaker than the filter it backstops.
        """
        blocked = {normalise_doi(d) for d in cutoff_info.blocked_dois if d}
        if cutoff_info.source_doi:
            blocked.add(normalise_doi(cutoff_info.source_doi))
        return blocked

    def is_source_by_title(self, paper: Paper, cutoff_info: CutoffInfo) -> bool:
        """Whether `paper` is an alternate version of the source study.

        Most alternate versions are caught by DOI (the version search records
        them at cutoff-resolution time). This covers the rest: a near-identical
        title plus a shared author.

        Author overlap alone is never sufficient — an earlier, unrelated paper by
        the same group is legitimate prior literature, not a version of this
        study — so the title test always has to pass first.
        """
        if not self.temporal.block_source_by_title or not cutoff_info.source_title:
            return False
        if not paper.title:
            return False
        if title_similarity(paper.title, cutoff_info.source_title) < self.temporal.source_title_similarity_threshold:
            return False
        if not self.temporal.block_source_requires_author_overlap:
            return True
        source_authors = {a.lower() for a in cutoff_info.source_authors if a}
        paper_authors = {a.family_name for a in paper.authors if a.family_name}
        if not source_authors or not paper_authors:
            # Nothing to check against: fall back to the title match alone, which
            # errs towards excluding a record rather than leaking the source.
            return True
        return bool(source_authors & paper_authors)

    def _is_eligible(self, when: date, cutoff: date) -> bool:
        if self.temporal.boundary == "inclusive":
            return when <= cutoff
        return when < cutoff

    def apply(self, papers: Sequence[Paper], cutoff_info: CutoffInfo) -> FilterOutcome:
        """Split `papers` into eligible/excluded according to the frozen cutoff."""
        cutoff = cutoff_info.cutoff_date
        if cutoff is None:
            raise MissingCutoffError(
                "instance {} has no frozen cutoff; refusing to filter literature".format(
                    cutoff_info.instance_id
                )
            )

        outcome = FilterOutcome()
        blocked = self.blocked_dois(cutoff_info)

        for paper in papers:
            paper.cutoff_date = cutoff
            self.assign_eligible_date(paper, cutoff)
            doi = normalise_doi(paper.doi)

            if self.temporal.block_source_doi and doi and doi in blocked:
                paper.temporal_eligible = False
                paper.exclusion_reason = "blocked_source_doi"
                outcome.excluded.append(paper)
                self.event_log.decision(
                    "excluded", instance_id=cutoff_info.instance_id, paper_id=paper.paper_id,
                    doi=doi, reason="blocked_source_doi",
                )
                continue

            if self.is_source_by_title(paper, cutoff_info):
                paper.temporal_eligible = False
                paper.exclusion_reason = "blocked_source_title_match"
                outcome.excluded.append(paper)
                outcome.notes.append(
                    "{}: title matches the source paper; treated as the source itself".format(
                        paper.paper_id
                    )
                )
                self.event_log.decision(
                    "excluded", instance_id=cutoff_info.instance_id, paper_id=paper.paper_id,
                    title=paper.title, reason="blocked_source_title_match",
                )
                continue

            if paper.eligible_date is None:
                if self.temporal.unknown_date_policy == "include":
                    paper.temporal_eligible = True
                    paper.exclusion_reason = None
                    paper.date_notes = list(paper.date_notes) + [
                        "included without a publication date (unknown_date_policy=include)"
                    ]
                    outcome.eligible.append(paper)
                    outcome.notes.append(
                        "{}: included without a date (policy=include)".format(paper.paper_id)
                    )
                else:
                    paper.temporal_eligible = False
                    paper.exclusion_reason = "unknown_publication_date"
                    outcome.excluded.append(paper)
                self.event_log.decision(
                    "undated_record", instance_id=cutoff_info.instance_id,
                    paper_id=paper.paper_id, policy=self.temporal.unknown_date_policy,
                )
                continue

            if self._is_eligible(paper.eligible_date, cutoff):
                paper.temporal_eligible = True
                paper.exclusion_reason = None
                outcome.eligible.append(paper)
            else:
                paper.temporal_eligible = False
                paper.exclusion_reason = "post_cutoff"
                outcome.excluded.append(paper)
                self.event_log.decision(
                    "excluded", instance_id=cutoff_info.instance_id, paper_id=paper.paper_id,
                    reason="post_cutoff", eligible_date=paper.eligible_date.isoformat(),
                    cutoff_date=cutoff.isoformat(),
                )

        return outcome

    # ------------------------------------------------------------------ #
    # Final gate
    # ------------------------------------------------------------------ #
    def assert_no_leak(self, papers: Iterable[Paper], cutoff_info: CutoffInfo) -> None:
        """Re-verify eligibility immediately before model exposure.

        Independent of the `temporal_eligible` flag, so a mutated or hand-built
        record cannot smuggle a post-cutoff paper into a prompt.
        """
        cutoff = cutoff_info.cutoff_date
        if cutoff is None:
            raise MissingCutoffError(
                "instance {} has no frozen cutoff; refusing to expose literature".format(
                    cutoff_info.instance_id
                )
            )
        blocked = self.blocked_dois(cutoff_info)
        for paper in papers:
            doi = normalise_doi(paper.doi)
            if self.temporal.block_source_doi and doi and doi in blocked:
                raise TemporalLeakError(
                    "instance {}: blocked source DOI {} reached model context".format(
                        cutoff_info.instance_id, doi
                    )
                )
            if self.is_source_by_title(paper, cutoff_info):
                raise TemporalLeakError(
                    "instance {}: paper {!r} has the source paper's title and reached "
                    "model context".format(cutoff_info.instance_id, paper.paper_id)
                )
            if paper.eligible_date is None:
                if self.temporal.unknown_date_policy != "include":
                    raise TemporalLeakError(
                        "instance {}: undated paper {!r} reached model context".format(
                            cutoff_info.instance_id, paper.paper_id
                        )
                    )
                continue
            if not self._is_eligible(paper.eligible_date, cutoff):
                raise TemporalLeakError(
                    "instance {}: paper {!r} dated {} is after cutoff {}".format(
                        cutoff_info.instance_id,
                        paper.paper_id,
                        paper.eligible_date.isoformat(),
                        cutoff.isoformat(),
                    )
                )
            if not paper.temporal_eligible:
                raise TemporalLeakError(
                    "instance {}: paper {!r} is marked ineligible ({}) but was about to be "
                    "exposed".format(cutoff_info.instance_id, paper.paper_id, paper.exclusion_reason)
                )
