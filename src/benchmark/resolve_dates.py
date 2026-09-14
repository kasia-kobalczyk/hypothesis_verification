"""Resolve source-paper publication dates and freeze the literature cutoffs.

    python -m src.benchmark.resolve_dates --config configs/mvp.yaml

Writes `data/metadata/source_dates.jsonl` (one `SourceDateRecord` per DOI) plus
`data/metadata/source_dates_summary.json`, and keeps every raw Crossref response
under `data/cache/crossref/`.

This must be run before any literature-based method: the loader joins these
records onto the frozen slice, and instances without a resolved cutoff are
refused by the literature layer rather than run with a guessed date.
"""

from __future__ import annotations

import argparse
import sys
from collections import OrderedDict
from typing import Dict, List, Optional

from src.benchmark.temporal import (
    SourceDateRecord,
    load_source_date_records,
    resolve_source_dates,
    write_source_date_records,
)
from src.common.config import load_config
from src.common.io import read_jsonl, resolve_path, utc_now_iso, write_json
from src.common.logging_utils import EventLog, configure_logging, get_logger
from src.literature.crossref import CrossrefClient, normalise_doi

LOGGER = get_logger("benchmark.resolve_dates")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.benchmark.resolve_dates",
        description="Resolve Crossref temporal metadata for the development slice.",
    )
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--dataset", default=None, help="override dataset.path")
    parser.add_argument("--out", default=None, help="override dataset.metadata_path")
    parser.add_argument("--refresh", action="store_true", help="bypass the Crossref cache")
    parser.add_argument("--instances", nargs="*", default=None, help="subset of dev ids")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.log_level)
    config = load_config(args.config)

    dataset_path = resolve_path(args.dataset or config.dataset.path)
    out_path = resolve_path(args.out or config.dataset.metadata_path)
    event_log = EventLog(out_path.parent / "resolve_dates_events.jsonl")
    crossref = CrossrefClient(config.crossref, event_log=event_log)

    wanted = set(args.instances) if args.instances else None
    by_doi: "OrderedDict[str, List[str]]" = OrderedDict()
    for row in read_jsonl(dataset_path):
        instance_id = row.get("dev_id") or row.get("id") or row.get("pair_id")
        if wanted is not None and instance_id not in wanted:
            continue
        doi = normalise_doi(row.get("doi"))
        if not doi:
            LOGGER.error("%s: row has no DOI; cutoff cannot be established", instance_id)
            continue
        by_doi.setdefault(doi, []).append(instance_id)

    # Resolving a subset must never drop the other instances' frozen cutoffs, so
    # start from whatever is already on disk and merge.
    existing: Dict[str, SourceDateRecord] = {}
    if out_path.exists():
        existing = load_source_date_records(out_path)
        LOGGER.info("merging into %d existing record(s) in %s", len(existing), out_path)

    records: List[SourceDateRecord] = []
    failures: List[Dict[str, str]] = []

    for index, (doi, instance_ids) in enumerate(by_doi.items(), start=1):
        LOGGER.info("[%d/%d] resolving %s (%s)", index, len(by_doi), doi, ", ".join(instance_ids))
        try:
            record = resolve_source_dates(
                doi,
                crossref=crossref,
                temporal=config.temporal,
                crossref_config=config.crossref,
                instance_ids=instance_ids,
                refresh=args.refresh,
            )
        except Exception as exc:
            # A failure is not "no date": leave the DOI unresolved, keep whatever
            # was resolved before it, and keep any previously frozen record.
            LOGGER.error("%s: resolution failed: %s", doi, exc)
            failures.append({"doi": doi, "error": str(exc), "type": type(exc).__name__})
            event_log.error("resolve_dates", str(exc), doi=doi)
            continue
        records.append(record)
        LOGGER.info(
            "  -> public=%s basis=%s cutoff=%s%s",
            record.selected_public_date, record.selected_cutoff_basis, record.cutoff_date,
            "  [AMBIGUOUS: {}]".format(record.notes) if record.ambiguous else "",
        )

    merged: Dict[str, SourceDateRecord] = dict(existing)
    for record in records:
        merged[record.doi] = record
    kept = [r for doi, r in merged.items() if doi not in {x.doi for x in records}]
    if kept:
        LOGGER.info("preserved %d record(s) not covered by this run", len(kept))
    write_source_date_records(out_path, list(merged.values()))

    ambiguous = [r for r in merged.values() if r.ambiguous]
    unresolved = [r for r in merged.values() if r.cutoff_date is None]
    summary = {
        "generated_at": utc_now_iso(),
        "dataset": str(dataset_path),
        "output": str(out_path),
        "n_dois": len(by_doi),
        "n_records": len(merged),
        "n_resolved_this_run": len(records),
        "n_resolved": len(merged) - len(unresolved),
        "n_ambiguous": len(ambiguous),
        "n_unresolved": len(unresolved),
        "n_request_failures": len(failures),
        "policy": {
            "cutoff_offset_days": config.temporal.cutoff_offset_days,
            "include_preprints_in_cutoff_basis": config.temporal.include_preprints_in_cutoff_basis,
            "date_fields": list(config.crossref.date_fields),
        },
        "needs_manual_inspection": [
            {
                "doi": r.doi,
                "instance_ids": r.instance_ids,
                "cutoff_date": r.cutoff_date.isoformat() if r.cutoff_date else None,
                "basis": r.selected_cutoff_basis,
                "notes": r.notes,
            }
            for r in ambiguous
        ],
        "request_failures": failures,
        "cutoffs": {
            instance_id: {
                "doi": r.doi,
                "cutoff_date": r.cutoff_date.isoformat() if r.cutoff_date else None,
                "basis": r.selected_cutoff_basis,
                "ambiguous": r.ambiguous,
            }
            for r in merged.values()
            for instance_id in r.instance_ids
        },
    }
    write_json(out_path.parent / "source_dates_summary.json", summary)

    print("\nresolved {}/{} DOIs -> {}".format(summary["n_resolved"], summary["n_dois"], out_path))
    if ambiguous:
        print("{} item(s) flagged for manual inspection:".format(len(ambiguous)))
        for item in summary["needs_manual_inspection"]:
            print("  {} ({}): {}".format(item["doi"], ", ".join(item["instance_ids"]), item["notes"]))
    if failures:
        print("{} DOI(s) failed to resolve; re-run to retry.".format(len(failures)))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
