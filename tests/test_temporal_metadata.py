"""Source-paper date resolution and cutoff assignment (IMPLEMENTATION_SPEC.md §3)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Dict, Optional

from src.benchmark.temporal import resolve_source_dates
from src.common.dates import PartialDate, parse_date_parts, parse_partial_date
from src.literature.crossref import CrossrefClient, normalise_doi


class StubCrossref(CrossrefClient):
    """CrossrefClient with `get_work` replaced by a fixture table."""

    def __init__(self, config, works: Dict[str, Optional[Dict[str, Any]]], search_items=None):
        super().__init__(config)
        self.works = works
        self.requested = []
        self.search_items = list(search_items or [])
        self.searches = []

    def search_works(self, *, bibliographic, author=None, rows=20, refresh=False):
        self.searches.append({"bibliographic": bibliographic, "author": author, "rows": rows})
        return list(self.search_items)

    def get_work(self, doi: str, *, refresh: bool = False) -> Optional[Dict[str, Any]]:
        key = normalise_doi(doi)
        self.requested.append(key)
        return self.works.get(key)


def work(doi: str, **fields: Any) -> Dict[str, Any]:
    record = {"DOI": doi, "title": ["A source paper"], "type": "journal-article"}
    record.update(fields)
    return record


def parts(*values: int) -> Dict[str, Any]:
    return {"date-parts": [list(values)]}


# --------------------------------------------------------------------------- #
# Partial date parsing
# --------------------------------------------------------------------------- #
def test_partial_dates_track_granularity():
    assert parse_partial_date("2020-03-05").granularity == "day"
    assert parse_partial_date("2020-03").granularity == "month"
    assert parse_partial_date("2020").granularity == "year"
    assert parse_partial_date(None).granularity == "none"
    assert parse_partial_date("not a date").granularity == "none"


def test_partial_date_resolution_directions():
    partial = PartialDate(2020, 2)
    assert partial.resolve(month_only_day="last") == date(2020, 2, 29)  # leap year
    assert partial.resolve(month_only_day="first") == date(2020, 2, 1)
    assert PartialDate(2021).resolve(year_only_day="last") == date(2021, 12, 31)
    assert PartialDate(2021).resolve(year_only_day="first") == date(2021, 1, 1)


def test_crossref_date_parts_parsing():
    assert parse_date_parts(parts(2020, 3, 5)).isoformat() == "2020-03-05"
    assert parse_date_parts(parts(2020, 3)).isoformat() == "2020-03"
    assert parse_date_parts(parts(2020)).isoformat() == "2020"
    assert parse_date_parts({"date-time": "2020-03-05T10:00:00Z"}).isoformat() == "2020-03-05"
    assert parse_date_parts({}).known is False


def test_doi_normalisation():
    assert normalise_doi("https://doi.org/10.1/ABC") == "10.1/abc"
    assert normalise_doi("  doi:10.1/abc ") == "10.1/abc"
    assert normalise_doi(None) is None


# --------------------------------------------------------------------------- #
# Cutoff resolution
# --------------------------------------------------------------------------- #
def test_cutoff_is_the_day_before_earliest_public_availability(config):
    doi = "10.1/paper"
    crossref = StubCrossref(
        config.crossref,
        {doi: work(doi, **{"published-online": parts(2020, 5, 10), "published-print": parts(2020, 9, 1)})},
    )
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=config.crossref,
        instance_ids=["X-01"],
    )
    assert record.online_date == date(2020, 5, 10)
    assert record.print_date == date(2020, 9, 1)
    assert record.selected_public_date == date(2020, 5, 10)
    assert record.selected_cutoff_basis == "published-online"
    assert record.cutoff_date == date(2020, 5, 9)
    assert record.ambiguous is False


def test_preprint_posting_moves_the_cutoff_earlier(config):
    doi, preprint = "10.1/journal", "10.1101/2019.01.01.123456"
    crossref = StubCrossref(
        config.crossref,
        {
            doi: work(doi, **{
                "published-online": parts(2020, 5, 10),
                "relation": {"has-preprint": [{"id-type": "doi", "id": preprint}]},
            }),
            preprint: work(preprint, type="posted-content", subtype="preprint", posted=parts(2019, 1, 2)),
        },
    )
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=config.crossref
    )
    assert record.selected_public_date == date(2019, 1, 2)
    assert record.cutoff_date == date(2019, 1, 1)
    assert record.selected_cutoff_basis == "preprint:" + preprint
    assert preprint in record.blocked_dois and doi in record.blocked_dois


def test_preprints_can_be_excluded_from_the_cutoff_basis(config):
    doi, preprint = "10.1/journal", "10.1101/2019.01.01.123456"
    crossref = StubCrossref(
        config.crossref,
        {
            doi: work(doi, **{
                "published-online": parts(2020, 5, 10),
                "relation": {"has-preprint": [{"id-type": "doi", "id": preprint}]},
            }),
            preprint: work(preprint, posted=parts(2019, 1, 2)),
        },
    )
    temporal = config.temporal.model_copy(update={"include_preprints_in_cutoff_basis": False})
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=temporal, crossref_config=config.crossref
    )
    assert record.cutoff_date == date(2020, 5, 9)
    assert "excluded from the cutoff basis" in (record.notes or "")
    # Still blocked from retrieval even though it does not set the cutoff.
    assert preprint in record.blocked_dois


def test_partial_source_dates_resolve_early_and_flag_ambiguity(config):
    doi = "10.1/partial"
    crossref = StubCrossref(config.crossref, {doi: work(doi, issued=parts(2020, 4))})
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=config.crossref
    )
    assert record.selected_public_date == date(2020, 4, 1)  # earliest day of the month
    assert record.cutoff_date == date(2020, 3, 31)
    assert record.ambiguous is True
    assert "granularity" in record.notes


def test_created_is_diagnostic_only_and_never_sets_the_cutoff(config):
    """Crossref `created` is a deposit timestamp, not public availability."""
    doi = "10.1/created"
    crossref = StubCrossref(
        config.crossref,
        {doi: work(doi, created={"date-time": "2023-01-28T00:00:00Z"}, issued=parts(2023, 9))},
    )
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=config.crossref
    )
    assert record.selected_cutoff_basis == "issued"
    assert record.cutoff_date == date(2023, 8, 31)
    # Still recorded, and still flagged: a deposit long before the stated date
    # suggests an article-in-press was public earlier.
    assert record.other_dates.get("created") == "2023-01-28"
    assert record.ambiguous is True
    assert "precedes the selected basis" in record.notes


def test_unknown_doi_is_flagged_not_guessed(config):
    crossref = StubCrossref(config.crossref, {})
    record = resolve_source_dates(
        "10.1/missing", crossref=crossref, temporal=config.temporal, crossref_config=config.crossref
    )
    assert record.cutoff_date is None
    assert record.ambiguous is True
    assert "crossref_not_found" in record.notes


def test_record_without_dates_is_flagged(config):
    doi = "10.1/nodates"
    crossref = StubCrossref(config.crossref, {doi: work(doi)})
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=config.temporal, crossref_config=config.crossref
    )
    assert record.cutoff_date is None
    assert record.ambiguous is True
    assert "no usable publication date" in record.notes


def test_cutoff_offset_is_configurable(config):
    doi = "10.1/offset"
    crossref = StubCrossref(config.crossref, {doi: work(doi, **{"published-online": parts(2020, 5, 10)})})
    temporal = config.temporal.model_copy(update={"cutoff_offset_days": 30})
    record = resolve_source_dates(
        doi, crossref=crossref, temporal=temporal, crossref_config=config.crossref
    )
    assert record.cutoff_date == date(2020, 4, 10)


def test_frozen_metadata_file_matches_the_development_slice(config):
    """The committed metadata must cover every DOI in the frozen slice."""
    from src.benchmark.temporal import load_source_date_records
    from src.common.io import read_jsonl, resolve_path

    records = load_source_date_records(resolve_path(config.dataset.metadata_path))
    dois = {normalise_doi(row["doi"]) for row in read_jsonl(resolve_path(config.dataset.path))}
    assert dois <= set(records)
    for doi in dois:
        record = records[doi]
        assert record.cutoff_date is not None
        assert record.selected_public_date == record.cutoff_date + timedelta(
            days=config.temporal.cutoff_offset_days
        )
