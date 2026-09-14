"""Build controlled listwise candidate sets at several k, from already-screened negatives.

    python3 scripts/build_k_slices.py --k 2 3 4

The formulation is for arbitrary k; this builds the *benchmark* side of that. Every
negative in every set has independently passed the frozen R2 comparability
criterion during the v2 build, so candidate quality does not drift with k the way
it does in ResearchBench's own 11-way task.

**No LLM calls and no literature access.** The sets are assembled from screening
decisions already on disk, and the negative ordering is frozen here -- before any
verifier runs -- so the sampling cannot be revisited after seeing a result.

Review-article sources are excluded when the configured policy says to, for the
same task-validity reason as elsewhere.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.k_slices import build_k_sets  # noqa: E402
from src.benchmark.review_sources import classify_source, venue_and_title_from_crossref  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.io import read_jsonl, resolve_path, utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import configure_logging, get_logger  # noqa: E402
from src.literature.crossref import normalise_doi  # noqa: E402

LOGGER = get_logger("scripts.build_k_slices")

V2_PROGRESS = "benchmark/v2/v2_progress.jsonl"
OUT_DIR = Path("benchmark/k_slices")


def _review_verdict(doi: str, *, policy):
    path = Path("data/cache/crossref") / "{}.json".format(doi.replace("/", "_"))
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (ValueError, OSError):
        return None
    fields = venue_and_title_from_crossref(payload.get("message") or payload)
    return classify_source(venue=fields["venue"], title=fields["title"],
                           venue_patterns=policy.venue_patterns,
                           title_patterns=policy.title_patterns)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--dataset", default="benchmark/ranking.jsonl")
    parser.add_argument("--progress", default=V2_PROGRESS)
    parser.add_argument("--k", nargs="+", type=int, default=[2, 3, 4])
    parser.add_argument("--seed", type=int, default=20260912)
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    config = load_config(args.config)
    review_policy = config.dataset.review_sources
    out_dir = Path(args.out_dir)

    by_doi: Dict[str, Dict[str, Any]] = {}
    for row in read_jsonl(resolve_path(args.dataset)):
        doi = normalise_doi(row.get("doi"))
        if doi and doi not in by_doi:
            by_doi[doi] = row

    rows: List[Dict[str, Any]] = []
    excluded_review: List[Dict[str, Any]] = []
    no_pass = 0

    for entry in read_jsonl(resolve_path(args.progress)):
        verdicts = entry.get("pairs") or {}
        passing = sorted(int(i) for i, v in verdicts.items() if v.get("decision") == "PASS")
        if not passing:
            no_pass += 1
            continue
        doi = normalise_doi(entry.get("doi"))
        source = by_doi.get(doi or "")
        if source is None:
            LOGGER.warning("screen rank %s: DOI %s not in the dataset", entry.get("screen_rank"), doi)
            continue
        if review_policy.enabled and review_policy.action == "exclude":
            verdict = _review_verdict(doi, policy=review_policy)
            if verdict is not None and verdict.is_review:
                excluded_review.append({"doi": doi, "screen_rank": entry.get("screen_rank"),
                                        **verdict.record()})
                continue
        pool = list(source.get("model_negative_hypotheses") or [])
        negatives = [
            {"source_index": i, "text": pool[i], "source_field": "model_negative_hypotheses"}
            for i in passing if i < len(pool)
        ]
        if not negatives:
            continue
        rows.append({
            "row_id": "K-{:04d}".format(int(entry.get("screen_rank") or 0)),
            "screen_rank": entry.get("screen_rank"),
            "doi": doi,
            "question": source.get("research_question", ""),
            "gold_text": source.get("gold_hypothesis", ""),
            "gold_source_index": None,
            "negatives": negatives,
            "discipline": source.get("discipline"),
            "cutoff_date": entry.get("cutoff_date"),
        })

    built = build_k_sets(rows, k_values=args.k, seed=args.seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    for k in args.k:
        path = out_dir / "k{}_sets.jsonl".format(k)
        with path.open("w", encoding="utf-8") as handle:
            for record in built["sets_by_k"][k]:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        LOGGER.info("k=%d: %d set(s) -> %s", k, len(built["sets_by_k"][k]), path)

    manifest = {
        "name": "Controlled listwise candidate sets at varying k",
        "frozen_at": utc_now_iso(),
        "status": "DEVELOPMENT / SCALABILITY ANALYSIS",
        "status_note": (
            "Built from the v2 length-gated, R2-screened pool, so these sets inherit v2's "
            "development-set status: a question-hidden judge recovers much of the pair "
            "label from candidate text alone. Use them to measure how the METHOD scales "
            "with k -- graph size, informative-evidence rate, retrieval yield, cost -- "
            "not to claim verification accuracy."
        ),
        "formulation_vs_protocol": (
            "The method is defined for arbitrary H = {H_1..H_k}. Results at different k "
            "are not directly comparable: chance top-1 is 1/k. Report stratified by k, "
            "and pool only metrics whose chance level is k-independent (normalised gold "
            "rank, pairwise win rate)."
        ),
        "seed": args.seed,
        "k_values": args.k,
        "source_of_negatives": (
            "negatives that passed the frozen R2 comparability criterion during the v2 "
            "build ({}), taken verbatim from {}".format(args.progress, args.dataset)
        ),
        "nesting": built["nesting"],
        "n_sets_by_k": built["n_sets_by_k"],
        "n_rows_short_of_k": built["n_rows_short_of_k"],
        "n_rows_with_no_passing_negative": no_pass,
        "n_balanced_panel_rows": built["n_balanced_panel_rows"],
        "balanced_panel_row_ids": built["balanced_panel_row_ids"],
        "frozen_negative_order": built["frozen_negative_order"],
        "review_source_exclusion": {
            "policy": review_policy.model_dump(mode="json"),
            "n_excluded": len(excluded_review),
            "excluded": excluded_review,
        },
        "availability_note": (
            "The v2 screen stopped at the 100-pair target after 137 of 962 rows, so the "
            "number of rows available at each k is bounded by how much screening was done, "
            "not by the dataset. Larger k needs more rows screened with R2; no negative is "
            "manufactured to reach a target size."
        ),
    }
    write_json(out_dir / "k_slices_manifest.json", manifest)

    print("\ncontrolled listwise sets (seed {}):".format(args.seed))
    for k in args.k:
        print("  k={}: {:3d} sets  ({} row(s) had fewer than {} screened negatives)".format(
            k, built["n_sets_by_k"][k], built["n_rows_short_of_k"][k], k - 1))
    print("  balanced panel (rows present at every k): {}".format(built["n_balanced_panel_rows"]))
    if excluded_review:
        print("  excluded {} review-source row(s)".format(len(excluded_review)))
    print("wrote {}".format(out_dir / "k_slices_manifest.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
