"""Source-paper temporal metadata resolution and the frozen cutoff registry.

IMPLEMENTATION_SPEC.md §3. Policy implemented here:

* `cutoff_date` = earliest eligible public availability of the source paper
  minus `temporal.cutoff_offset_days` (default 1 day).
* Partial dates resolve to the *earliest* day they could denote, so an imprecise
  source date produces an earlier — never a later — cutoff.
* Preprint postings of the source work count as public availability when
  `temporal.include_preprints_in_cutoff_basis` is true.
* Ambiguity is never resolved silently: `ambiguous=True` plus a note, and the
  item is reported for manual inspection.

The `CutoffRegistry` is the only object the literature layer consults for a
cutoff. It is immutable and exposes no setter, so no agent-facing code path can
move a cutoff.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.common.config import CrossrefConfig, TemporalConfig
from src.common.errors import MissingCutoffError
from src.common.io import read_jsonl, slugify, utc_now_iso, write_jsonl
from src.common.logging_utils import get_logger
from src.benchmark.versions import VersionCandidate, find_source_versions
from src.literature.crossref import CrossrefClient, normalise_doi

LOGGER = get_logger("benchmark.temporal")

# Crossref field -> the spec's record field names (§3).
_FIELD_ALIASES = {
    "published-online": "online_date",
    "published-print": "print_date",
    "posted": "posted_date",
}

# If Crossref's registration date ("created") precedes every stated publication
# date by more than this many days, the record is flagged rather than trusted.
CREATED_AMBIGUITY_GAP_DAYS = 30


class SourceDateRecord(BaseModel):
    """Resolved temporal metadata for one source paper (spec §3)."""

    model_config = ConfigDict(extra="forbid")

    doi: str
    instance_ids: List[str] = Field(default_factory=list)
    source_title: Optional[str] = None
    source_authors: List[str] = Field(default_factory=list)
    online_date: Optional[date] = None
    print_date: Optional[date] = None
    posted_date: Optional[date] = None
    other_dates: Dict[str, Optional[str]] = Field(default_factory=dict)
    selected_public_date: Optional[date] = None
    selected_cutoff_basis: Optional[str] = None
    cutoff_date: Optional[date] = None
    ambiguous: bool = False
    notes: Optional[str] = None
    # Provenance
    provider: str = "crossref"
    retrieved_at: Optional[str] = None
    raw_path: Optional[str] = None
    granularity: Optional[str] = None
    preprint_dois: List[str] = Field(default_factory=list)
    blocked_dois: List[str] = Field(default_factory=list)
    # Every candidate the version search considered, accepted or not (§3 provenance).
    version_candidates: List[Dict[str, Any]] = Field(default_factory=list)
    policy: Dict[str, Any] = Field(default_factory=dict)


@dataclass(frozen=True)
class CutoffInfo:
    """Immutable per-instance temporal constraint."""

    instance_id: str
    source_doi: Optional[str]
    cutoff_date: Optional[date]
    basis: Optional[str] = None
    ambiguous: bool = False
    blocked_dois: FrozenSet[str] = frozenset()
    notes: Optional[str] = None
    # Used to recognise an alternate version of the source study by title+author.
    source_title: Optional[str] = None
    source_authors: FrozenSet[str] = frozenset()

    @property
    def has_cutoff(self) -> bool:
        return self.cutoff_date is not None


class CutoffRegistry:
    """Frozen instance_id -> CutoffInfo mapping.

    Deliberately read-only: there is no `set`/`update`/`override` method, so the
    cutoff cannot be changed by anything downstream, including an agent-facing
    tool wrapper.
    """

    def __init__(self, entries: Iterable[CutoffInfo]):
        self._entries: Dict[str, CutoffInfo] = {}
        for entry in entries:
            self._entries[entry.instance_id] = entry

    def __contains__(self, instance_id: object) -> bool:
        return instance_id in self._entries

    def __len__(self) -> int:
        return len(self._entries)

    def instance_ids(self) -> List[str]:
        return list(self._entries)

    def get(self, instance_id: str) -> CutoffInfo:
        try:
            return self._entries[instance_id]
        except KeyError:
            raise MissingCutoffError(
                "no temporal metadata registered for instance {!r}".format(instance_id)
            )

    def require(self, instance_id: str) -> CutoffInfo:
        """Like `get`, but also refuses instances whose cutoff is unresolved."""
        info = self.get(instance_id)
        if info.cutoff_date is None:
            raise MissingCutoffError(
                "instance {!r} has no frozen cutoff date ({}); literature-based "
                "methods must not run on it".format(instance_id, info.notes or "unresolved")
            )
        return info


# --------------------------------------------------------------------------- #
# Resolution
# --------------------------------------------------------------------------- #
def _earliest_day(partial) -> Optional[date]:
    return partial.resolve(year_only_day="first", month_only_day="first")


def resolve_source_dates(
    doi: str,
    *,
    crossref: CrossrefClient,
    temporal: TemporalConfig,
    crossref_config: CrossrefConfig,
    instance_ids: Optional[List[str]] = None,
    refresh: bool = False,
) -> SourceDateRecord:
    """Resolve one source DOI into a `SourceDateRecord`."""
    key = normalise_doi(doi) or doi
    record = SourceDateRecord(
        doi=key,
        instance_ids=list(instance_ids or []),
        retrieved_at=utc_now_iso(),
        raw_path=str(Path(crossref_config.cache.dir) / "{}.json".format(slugify(key)))
        if crossref_config.cache.enabled
        else None,
        policy={
            "cutoff_offset_days": temporal.cutoff_offset_days,
            "include_preprints_in_cutoff_basis": temporal.include_preprints_in_cutoff_basis,
            "date_fields": list(crossref_config.date_fields),
            "partial_date_resolution": "earliest_day_of_period",
            "version_search": temporal.version_search.model_dump(mode="json"),
        },
    )

    basis_fields = crossref_config.cutoff_basis_fields
    record.policy["cutoff_basis_fields"] = list(basis_fields) if basis_fields else "all"

    dates = crossref.get_dates(key, refresh=refresh)
    if dates is None:
        record.ambiguous = True
        record.notes = "crossref_not_found: DOI unknown to Crossref; cutoff must be set manually"
        LOGGER.warning("%s: %s", key, record.notes)
        return record

    record.source_title = dates.title
    record.source_authors = crossref.author_families(crossref.get_work(key) or {})
    notes: List[str] = []
    candidates: Dict[str, date] = {}
    granularity: Dict[str, str] = {}
    # Fields recorded for provenance but not allowed to set the cutoff.
    excluded_from_basis: Dict[str, date] = {}

    for field_name, partial in dates.dates.items():
        resolved = _earliest_day(partial)
        if resolved is None:
            continue
        if basis_fields is not None and field_name not in basis_fields:
            excluded_from_basis[field_name] = resolved
        else:
            candidates[field_name] = resolved
            granularity[field_name] = partial.granularity
        alias = _FIELD_ALIASES.get(field_name)
        if alias == "online_date":
            record.online_date = resolved
        elif alias == "print_date":
            record.print_date = resolved
        elif alias == "posted_date":
            record.posted_date = resolved
        else:
            record.other_dates[field_name] = partial.isoformat()

    blocked = {key}
    blocked.update(dates.preprint_dois)
    blocked.update(dates.journal_dois)
    record.preprint_dois = sorted(dates.preprint_dois)

    # Preprint postings of the same work count as public availability.
    if temporal.include_preprints_in_cutoff_basis and dates.preprint_dois:
        for preprint_doi in dates.preprint_dois:
            preprint = crossref.get_dates(preprint_doi, refresh=refresh)
            if preprint is None:
                notes.append("preprint {} not resolvable in Crossref".format(preprint_doi))
                record.ambiguous = True
                continue
            preprint_candidates = [
                d for d in (_earliest_day(p) for p in preprint.dates.values()) if d is not None
            ]
            if not preprint_candidates:
                notes.append("preprint {} has no usable date".format(preprint_doi))
                record.ambiguous = True
                continue
            earliest = min(preprint_candidates)
            label = "preprint:{}".format(preprint_doi)
            candidates[label] = earliest
            granularity[label] = "day"
            record.other_dates[label] = earliest.isoformat()
            blocked.update(preprint.journal_dois)
    elif dates.preprint_dois and not temporal.include_preprints_in_cutoff_basis:
        notes.append(
            "source has {} linked preprint(s) excluded from the cutoff basis by "
            "configuration".format(len(dates.preprint_dois))
        )

    # Alternate versions of the same study, including preprints Crossref does not
    # link. A failed search is never read as "there are no other versions".
    version_candidates: List[VersionCandidate] = []
    accepted_versions: List[VersionCandidate] = []
    if temporal.version_search.enabled:
        try:
            version_candidates = find_source_versions(
                crossref=crossref,
                source_doi=key,
                source_title=record.source_title,
                source_authors=record.source_authors,
                basis_fields=basis_fields or crossref_config.date_fields,
                config=temporal.version_search,
                crossref_config=crossref_config,
                refresh=refresh,
            )
        except Exception as exc:
            record.ambiguous = True
            notes.append(
                "version search failed ({}); unlinked versions of this study may "
                "exist inside the eligible window".format(exc)
            )
            LOGGER.error("%s: version search failed: %s", key, exc)
        record.version_candidates = [c.record() for c in version_candidates]

        for version in version_candidates:
            if not version.accepted or not version.doi:
                continue
            accepted_versions.append(version)
            blocked.add(version.doi)
            if version.is_preprint and not temporal.include_preprints_in_cutoff_basis:
                notes.append(
                    "version {} excluded from the cutoff basis by configuration".format(version.doi)
                )
                continue
            if version.earliest_date is None:
                record.ambiguous = True
                notes.append("version {} has no usable date".format(version.doi))
                continue
            label = "version:{}".format(version.doi)
            candidates[label] = version.earliest_date
            granularity[label] = version.granularity or "day"
            record.other_dates[label] = version.earliest_date.isoformat()

        if accepted_versions:
            notes.append(
                "version search found {} other record(s) of this study: {}".format(
                    len(accepted_versions), ", ".join(str(v.doi) for v in accepted_versions)
                )
            )
        else:
            notes.append("version search found no other record of this study")
    else:
        record.ambiguous = True
        notes.append(
            "version search disabled; an unlinked preprint of this paper would not "
            "move the cutoff"
        )

    if excluded_from_basis:
        notes.append(
            "date field(s) {} recorded but excluded from the cutoff basis by "
            "configuration".format(", ".join(sorted(excluded_from_basis)))
        )

    record.blocked_dois = sorted(blocked)

    if not candidates:
        record.ambiguous = True
        notes.append("no usable publication date in Crossref record")
        record.notes = "; ".join(notes)
        LOGGER.warning("%s: no usable publication date", key)
        return record

    basis = min(candidates, key=lambda name: (candidates[name], name))
    selected = candidates[basis]
    record.selected_public_date = selected
    record.selected_cutoff_basis = basis
    record.granularity = granularity.get(basis)
    record.cutoff_date = selected - timedelta(days=temporal.cutoff_offset_days)

    if granularity.get(basis) not in ("day", None):
        record.ambiguous = True
        notes.append(
            "selected basis {!r} has {} granularity; resolved to the earliest day of the "
            "period".format(basis, granularity.get(basis))
        )

    # `created` (the Crossref deposit timestamp) is diagnostic only: it does not
    # set the cutoff, but when it long precedes the selected basis it suggests an
    # article-in-press was public earlier, i.e. the cutoff may be too late.
    created = excluded_from_basis.get("created") or candidates.get("created")
    if created is not None and (selected - created).days > CREATED_AMBIGUITY_GAP_DAYS:
        record.ambiguous = True
        notes.append(
            "Crossref 'created' ({}) precedes the selected basis {!r} by {} days; the "
            "article may have been public before the cutoff".format(
                created.isoformat(), basis, (selected - created).days
            )
        )

    if dates.is_preprint:
        notes.append("source DOI is itself a preprint/posted-content record")

    record.notes = "; ".join(notes) if notes else None
    return record


def write_source_date_records(path: "str | Path", records: Iterable[SourceDateRecord]) -> Path:
    return write_jsonl(path, [r.model_dump(mode="json") for r in records])


def load_source_date_records(path: "str | Path") -> Dict[str, SourceDateRecord]:
    """Load the frozen metadata file, keyed by normalised DOI."""
    out: Dict[str, SourceDateRecord] = {}
    for row in read_jsonl(path):
        record = SourceDateRecord(**row)
        key = normalise_doi(record.doi) or record.doi
        out[key] = record
    return out
