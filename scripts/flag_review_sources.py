"""Flag benchmark rows whose source paper looks like a review article.

    python3 scripts/flag_review_sources.py --slice benchmark/ranking.jsonl
    python3 scripts/flag_review_sources.py --slice benchmark/v2/researchbench_v2_pairs.jsonl

Reads venue and title from the CACHED Crossref records under `data/cache/crossref/`
-- no network, no API calls, no cost. Writes a side file next to the slice and
never edits the slice itself: frozen data stays frozen, and a flag is a finding
about a row, not a change to it.

Why this exists: a review's gold hypothesis summarises already-published work, so
the answer sits in the pre-cutoff literature by construction. See
`src/benchmark/review_sources.py`.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.review_sources import (  # noqa: E402
    ReviewSourceVerdict,
    classify_source,
    summarise,
    venue_and_title_from_crossref,
)
from src.common.config import load_config  # noqa: E402
from src.common.io import read_jsonl, resolve_path, utc_now_iso, write_json  # noqa: E402
from src.literature.crossref import normalise_doi  # noqa: E402

CACHE_DIR = Path("data/cache/crossref")
LOGGER_ERRORS: List[Dict[str, str]] = []


def _cached_message(doi: str) -> Optional[Dict]:
    path = CACHE_DIR / "{}.json".format(doi.replace("/", "_"))
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (ValueError, OSError):
        return None
    return payload.get("message") or payload


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--slice", required=True, help="a .jsonl slice with `doi` fields")
    parser.add_argument("--out", default=None, help="default: <slice dir>/review_source_flags.json")
    parser.add_argument("--fetch", action="store_true",
                        help="resolve DOIs missing from the Crossref cache (network; free, no LLM)")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    policy = config.dataset.review_sources
    slice_path = resolve_path(args.slice)
    out_path = Path(args.out) if args.out else slice_path.parent / "review_source_flags.json"

    verdicts: "OrderedDict[str, ReviewSourceVerdict]" = OrderedDict()
    rows_by_doi: Dict[str, List[str]] = {}
    n_rows = 0
    missing_metadata: List[str] = []
    crossref = None
    if args.fetch:
        from src.literature.crossref import CrossrefClient

        crossref = CrossrefClient(config.crossref)

    for row in read_jsonl(slice_path):
        n_rows += 1
        row_id = row.get("pair_id") or row.get("dev_id") or row.get("id") or "?"
        doi = normalise_doi(row.get("doi"))
        if not doi:
            continue
        first_time = doi not in rows_by_doi
        rows_by_doi.setdefault(doi, []).append(row_id)
        if not first_time:
            continue  # one classification per DOI, not per row
        message = _cached_message(doi)
        if message is None and crossref is not None:
            try:
                message = crossref.get_work(doi)
            except Exception as exc:  # noqa: BLE001 - a lookup failure is not a verdict
                LOGGER_ERRORS.append({"doi": doi, "error": str(exc)})
                message = None
        if message is None:
            missing_metadata.append(doi)
            continue
        fields = venue_and_title_from_crossref(message)
        verdicts[doi] = classify_source(
            venue=fields["venue"], title=fields["title"],
            venue_patterns=policy.venue_patterns, title_patterns=policy.title_patterns)

    summary = summarise(verdicts)
    summary.update({
        "generated_at": utc_now_iso(),
        "slice": str(slice_path),
        "n_rows": n_rows,
        "n_distinct_dois": len(rows_by_doi),
        "n_dois_without_cached_metadata": len(missing_metadata),
        "dois_without_cached_metadata": missing_metadata[:50],
        "lookup_errors": LOGGER_ERRORS,
        "policy": policy.model_dump(mode="json"),
        "affected_row_ids": sorted(
            row_id
            for doi, verdict in verdicts.items() if verdict.is_review
            for row_id in rows_by_doi.get(doi, [])
        ),
        "note": (
            "Flags only. This file does not modify the slice. For a newly built "
            "evaluation benchmark the same policy is applied as an exclusion gate "
            "at construction time."
        ),
    })
    write_json(out_path, summary)

    print("{}: {} rows, {} distinct DOIs".format(slice_path, n_rows, len(rows_by_doi)))
    print("  review-source DOIs: {} / {} checked  {}".format(
        summary["n_flagged"], summary["n_checked"], summary["by_basis"] or ""))
    if missing_metadata:
        print("  {} DOI(s) had no cached Crossref record (not classified)".format(
            len(missing_metadata)))
    for doi, record in sorted(summary["flagged"].items()):
        print("  - {}  [{}: {!r}]  {}".format(
            doi, record["basis"], record["matched"], (record["venue"] or "")[:60]))
    print("wrote {}".format(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
