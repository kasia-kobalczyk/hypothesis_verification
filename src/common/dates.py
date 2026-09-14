"""Partial-date handling.

Bibliographic dates arrive at three granularities ("2020", "2020-03",
"2020-03-05") and sometimes not at all. Collapsing them to a single `date` is a
scientific decision, not a formatting detail, so granularity is tracked
explicitly and the collapse is performed by one configurable function.

Under `policy="latest"` (the project default) a partial date resolves to the
last day it could denote. That is the conservative choice for temporal safety:
a paper dated "2020" is assumed to have appeared on 2020-12-31, so it is
excluded from a 2020-06 cutoff rather than leaked into the model's context.
"""

from __future__ import annotations

import calendar
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, List, Optional, Sequence

try:  # Python 3.8
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore

Granularity = Literal["day", "month", "year", "none"]
ConflictPolicy = Literal["latest", "earliest"]
DayChoice = Literal["first", "last"]

_ISO_RE = re.compile(r"^\s*(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?")


@dataclass(frozen=True)
class PartialDate:
    """A date that may be known only to year or month precision."""

    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    raw: Optional[str] = None

    @property
    def granularity(self) -> Granularity:
        if self.year is None:
            return "none"
        if self.month is None:
            return "year"
        if self.day is None:
            return "month"
        return "day"

    @property
    def known(self) -> bool:
        return self.year is not None

    def isoformat(self) -> Optional[str]:
        if self.year is None:
            return None
        if self.month is None:
            return "{:04d}".format(self.year)
        if self.day is None:
            return "{:04d}-{:02d}".format(self.year, self.month)
        return "{:04d}-{:02d}-{:02d}".format(self.year, self.month, self.day)

    def resolve(
        self,
        *,
        year_only_day: DayChoice = "last",
        month_only_day: DayChoice = "last",
    ) -> Optional[date]:
        """Collapse to a concrete `date`, or `None` if the year is unknown.

        `year_only_day` / `month_only_day` decide which end of the denoted period
        a partial date collapses to. Candidate-paper eligibility uses "last"
        (assume the paper appeared as late as possible -> exclude near the
        boundary); source-paper cutoff resolution uses "first" (assume the source
        became public as early as possible -> earlier cutoff). Both directions
        shrink the eligible set, which is the safe direction.
        """
        if self.year is None:
            return None
        if self.month is not None and self.day is not None:
            return _safe_date(self.year, self.month, self.day)
        if self.month is not None:
            day = calendar.monthrange(self.year, self.month)[1] if month_only_day == "last" else 1
            return _safe_date(self.year, self.month, day)
        if year_only_day == "last":
            return date(self.year, 12, 31)
        return date(self.year, 1, 1)


def _safe_date(year: int, month: int, day: int) -> Optional[date]:
    month = max(1, min(12, month))
    last_day = calendar.monthrange(year, month)[1]
    day = max(1, min(last_day, day))
    try:
        return date(year, month, day)
    except ValueError:  # pragma: no cover - defensive
        return None


def parse_partial_date(value: Any) -> PartialDate:
    """Parse ISO-ish strings, `datetime`/`date` objects, or ints (years)."""
    if value is None:
        return PartialDate()
    if isinstance(value, datetime):
        return PartialDate(value.year, value.month, value.day, raw=value.isoformat())
    if isinstance(value, date):
        return PartialDate(value.year, value.month, value.day, raw=value.isoformat())
    if isinstance(value, int):
        return PartialDate(year=value, raw=str(value))
    if not isinstance(value, str):
        return PartialDate()
    match = _ISO_RE.match(value)
    if not match:
        return PartialDate(raw=value)
    year = int(match.group(1))
    month = int(match.group(2)) if match.group(2) else None
    day = int(match.group(3)) if match.group(3) else None
    if month is not None and not 1 <= month <= 12:
        month, day = None, None
    return PartialDate(year, month, day, raw=value)


def parse_date_parts(date_parts: Any) -> PartialDate:
    """Parse Crossref's `{"date-parts": [[2020, 3, 5]]}` structure."""
    parts: Optional[Sequence[Any]] = None
    if isinstance(date_parts, dict):
        candidate = date_parts.get("date-parts")
        if isinstance(candidate, list) and candidate:
            parts = candidate[0]
        elif "date-time" in date_parts:
            return parse_partial_date(date_parts.get("date-time"))
    elif isinstance(date_parts, list) and date_parts:
        parts = date_parts[0] if isinstance(date_parts[0], list) else date_parts
    if not parts:
        return PartialDate()
    values: List[Optional[int]] = []
    for item in list(parts)[:3]:
        try:
            values.append(int(item))
        except (TypeError, ValueError):
            values.append(None)
    while len(values) < 3:
        values.append(None)
    year, month, day = values[0], values[1], values[2]
    if year is None:
        return PartialDate()
    if month is None:
        day = None
    return PartialDate(year, month, day, raw=str(parts))


def parse_date(value: Any) -> Optional[date]:
    """Strict parse of a full ISO date; `None` when not a complete date."""
    partial = parse_partial_date(value)
    if partial.granularity != "day":
        return None
    return partial.resolve()


def to_iso(value: Optional[date]) -> Optional[str]:
    return value.isoformat() if value is not None else None
