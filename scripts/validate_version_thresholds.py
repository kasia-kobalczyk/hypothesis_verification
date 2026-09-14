"""Check the frozen version-search thresholds on an independent labelled set.

    python scripts/validate_version_thresholds.py --labelled data/version_validation.jsonl
    python scripts/validate_version_thresholds.py --template   # write a starter file

The thresholds in `configs/mvp.yaml` were chosen on the 20 development cases and
are frozen (see `docs/DECISIONS.md` §12). This script reports how they perform on
data they were *not* chosen on, before they are used for a final benchmark.

It deliberately does **not** search for better thresholds. It scores the labelled
pairs at the frozen values and prints precision, recall and the score
distributions on each side, so a human can see whether the separation survives.
Sample the labelled set from source papers outside the development slice.

Input: JSONL, one object per pair:

    {"source_doi": "10.1038/...", "candidate_doi": "10.1101/...",
     "same_study": true, "note": "bioRxiv preprint of the source"}

`same_study` is the human label: true for a genuine alternate version (preprint,
proceedings version, corrected republication), false for a different study —
ideally one by an overlapping author, since that is the hard case.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.io import read_jsonl, resolve_path, write_json  # noqa: E402
from src.common.logging_utils import configure_logging, get_logger  # noqa: E402
from src.literature.crossref import CrossrefClient, normalise_doi  # noqa: E402
from src.literature.dedup import title_similarity  # noqa: E402

LOGGER = get_logger("scripts.validate_version_thresholds")

TEMPLATE = [
    {
        "source_doi": "10.1038/s41586-000-00000-0",
        "candidate_doi": "10.1101/2023.01.01.000000",
        "same_study": True,
        "note": "example: unlinked preprint of the source paper",
    },
    {
        "source_doi": "10.1038/s41586-000-00000-0",
        "candidate_doi": "10.1016/j.example.2022.100000",
        "same_study": False,
        "note": "example: different study sharing one author (the hard case)",
    },
]


def score_pair(crossref: CrossrefClient, source_doi: str, candidate_doi: str) -> Dict[str, Any]:
    """Title similarity and author-overlap fraction for one labelled pair."""
    source = crossref.get_work(source_doi)
    candidate = crossref.get_work(candidate_doi)
    out: Dict[str, Any] = {
        "source_doi": normalise_doi(source_doi),
        "candidate_doi": normalise_doi(candidate_doi),
        "resolved": bool(source) and bool(candidate),
    }
    if not out["resolved"]:
        out["error"] = "not found in Crossref: {}".format(
            "source" if not source else "candidate"
        )
        return out

    source_titles = source.get("title") or []
    candidate_titles = candidate.get("title") or []
    source_title = source_titles[0] if source_titles else None
    candidate_title = candidate_titles[0] if candidate_titles else None

    source_authors = {a.lower() for a in crossref.author_families(source)}
    candidate_authors = {a.lower() for a in crossref.author_families(candidate)}
    shared = source_authors & candidate_authors
    smaller = min(len(source_authors), len(candidate_authors))

    out.update(
        {
            "source_title": source_title,
            "candidate_title": candidate_title,
            "candidate_type": candidate.get("type"),
            "title_similarity": round(title_similarity(candidate_title, source_title), 3),
            "author_overlap": len(shared),
            "author_overlap_fraction": round((len(shared) / smaller) if smaller else 0.0, 3),
            "n_source_authors": len(source_authors),
            "n_candidate_authors": len(candidate_authors),
        }
    )
    return out


def classify(row: Dict[str, Any], config) -> bool:
    """Apply the frozen rule exactly as `find_source_versions` does."""
    search = config.temporal.version_search
    has_authors = row.get("n_source_authors") and row.get("n_candidate_authors")
    threshold = (
        search.title_similarity_threshold
        if has_authors
        else search.title_similarity_threshold_no_authors
    )
    if row.get("candidate_type") and row["candidate_type"] not in search.include_types:
        return False
    if row["title_similarity"] < threshold:
        return False
    if has_authors and row["author_overlap"] < search.min_author_overlap:
        return False
    if has_authors and row["author_overlap_fraction"] < search.min_author_overlap_fraction:
        return False
    return True


def _spread(values: List[float]) -> str:
    if not values:
        return "n/a"
    return "min {:.2f}  median {:.2f}  max {:.2f}".format(
        min(values), sorted(values)[len(values) // 2], max(values)
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--labelled", default="data/version_validation.jsonl")
    parser.add_argument("--out", default=None, help="where to write the full report JSON")
    parser.add_argument("--template", action="store_true", help="write a starter labelled file")
    parser.add_argument("--log-level", default="WARNING")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    path = resolve_path(args.labelled)
    if args.template:
        if path.exists():
            print("refusing to overwrite {}".format(path))
            return 1
        from src.common.io import write_jsonl

        write_jsonl(path, TEMPLATE)
        print("wrote a starter labelled file to {}\nFill it from source papers "
              "OUTSIDE the 20 development cases, then re-run without --template.".format(path))
        return 0

    if not path.exists():
        print("labelled set not found: {}\nCreate one with --template.".format(path))
        return 1

    config = load_config(args.config)
    crossref = CrossrefClient(config.crossref)
    search = config.temporal.version_search

    rows: List[Dict[str, Any]] = []
    for entry in read_jsonl(path):
        if "same_study" not in entry:
            print("every row needs a `same_study` label; got {}".format(sorted(entry)))
            return 1
        row = score_pair(crossref, entry["source_doi"], entry["candidate_doi"])
        row["same_study"] = bool(entry["same_study"])
        row["note"] = entry.get("note")
        if row["resolved"]:
            row["accepted"] = classify(row, config)
        rows.append(row)

    usable = [r for r in rows if r["resolved"]]
    unresolved = [r for r in rows if not r["resolved"]]
    tp = [r for r in usable if r["same_study"] and r["accepted"]]
    fn = [r for r in usable if r["same_study"] and not r["accepted"]]
    fp = [r for r in usable if not r["same_study"] and r["accepted"]]
    tn = [r for r in usable if not r["same_study"] and not r["accepted"]]

    report = {
        "labelled_set": str(path),
        "thresholds": search.model_dump(mode="json"),
        "n_pairs": len(rows),
        "n_unresolved": len(unresolved),
        "true_positive": len(tp),
        "false_negative": len(fn),
        "false_positive": len(fp),
        "true_negative": len(tn),
        "precision": len(tp) / (len(tp) + len(fp)) if (tp or fp) else None,
        "recall": len(tp) / (len(tp) + len(fn)) if (tp or fn) else None,
        "rows": rows,
    }
    out_path = resolve_path(args.out) if args.out else path.with_name(path.stem + "_report.json")
    write_json(out_path, report)

    print("frozen thresholds: title >= {}, author overlap fraction >= {}".format(
        search.title_similarity_threshold, search.min_author_overlap_fraction))
    print("labelled pairs: {} ({} unresolved in Crossref)".format(len(rows), len(unresolved)))
    print("  same study     : {:3} accepted, {:3} missed".format(len(tp), len(fn)))
    print("  different study: {:3} accepted (false positives), {:3} rejected".format(len(fp), len(tn)))
    if report["precision"] is not None:
        print("  precision {:.3f}   recall {:.3f}".format(report["precision"], report["recall"] or 0.0))
    print()
    print("title similarity   same study : {}".format(
        _spread([r["title_similarity"] for r in usable if r["same_study"]])))
    print("                   different  : {}".format(
        _spread([r["title_similarity"] for r in usable if not r["same_study"]])))
    print("author overlap     same study : {}".format(
        _spread([r["author_overlap_fraction"] for r in usable if r["same_study"]])))
    print("                   different  : {}".format(
        _spread([r["author_overlap_fraction"] for r in usable if not r["same_study"]])))
    print()
    for row in fn:
        print("MISSED   {} -> {} (title {:.2f}, authors {:.2f}) {}".format(
            row["source_doi"], row["candidate_doi"], row["title_similarity"],
            row["author_overlap_fraction"], row.get("note") or ""))
    for row in fp:
        print("FALSE +  {} -> {} (title {:.2f}, authors {:.2f}) {}".format(
            row["source_doi"], row["candidate_doi"], row["title_similarity"],
            row["author_overlap_fraction"], row.get("note") or ""))
    print("\nfull report: {}".format(out_path))
    print("This script reports; it does not tune. Any threshold change is a "
          "research decision to record in docs/DECISIONS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
