"""Render `v2_screening_report.md` from the frozen v2 artifacts.

Generated rather than hand-written so the prose cannot drift from the data.
"""

from __future__ import annotations

import argparse
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.v2_slice import (  # noqa: E402
    LENGTH_RATIO_BAND_V1_PROPOSAL,
    LENGTH_RATIO_BAND_WIDENED_DIAGNOSTIC,
    LENGTH_RATIO_MAX,
    LENGTH_RATIO_MIN,
)
from src.common.io import read_json, read_jsonl, resolve_path  # noqa: E402


def shortest_first(pairs: List[Dict[str, Any]]) -> Optional[float]:
    if not pairs:
        return None
    wins = sum(1 for p in pairs if p["gold_token_count"] < p["negative_token_count"])
    ties = sum(1 for p in pairs if p["gold_token_count"] == p["negative_token_count"])
    return (wins + 0.5 * ties) / len(pairs)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="benchmark/v2")
    args = parser.parse_args(argv)
    base = resolve_path(args.dir)

    pairs = list(read_jsonl(base / "researchbench_v2_pairs.jsonl"))
    manifest = read_json(base / "v2_manifest.json")
    outcomes = list(read_jsonl(base / "v2_row_outcomes.jsonl"))
    # Prefer the counterbalanced judge results: the single-order run is confounded
    # by the judge's position preference (docs/DECISIONS.md #21).
    diagnostics_path = base / "v2_artifact_diagnostics_counterbalanced.json"
    if not diagnostics_path.exists():
        diagnostics_path = base / "v2_artifact_diagnostics.json"
    diag = read_json(diagnostics_path) if diagnostics_path.exists() else {}

    ratios = [p["length_ratio"] for p in pairs]
    stats = manifest["length_statistics_full_dataset"]
    per_doi = Counter(p["doi"] for p in pairs)
    disciplines = Counter(p["discipline"] for p in pairs)
    rejected = manifest["rejected_at"]

    L: List[str] = []
    add = L.append
    add("# v2 screening report — length-controlled ResearchBench pair slice")
    add("")
    add("Frozen {}. {} pairs across {} source rows.".format(
        manifest["frozen_at"], len(pairs), manifest["n_source_rows_represented"]))
    add("")
    add("## Why v2 exists")
    add("")
    add(manifest["motivation"])
    add("")
    add("## What was inherited from v1, and what is new")
    add("")
    for item in manifest["inherited_from_v1"]:
        add("- inherited: {}".format(item))
    add("- **new**: length ratio `{}` — {}".format(
        manifest["new_rule_in_v2"]["length_ratio"], manifest["new_rule_in_v2"]["applied"]))
    add("")
    add("The band was specified as [{}, {}] before any pair was screened, widened once to "
        "[{}, {}] by the research owner on the interpretive ground \"neither text more than "
        "1.5x the other\", and then **re-frozen at the original [{}, {}]**. The widened slice "
        "is kept as a diagnostic artifact only "
        "(`benchmark/v2_widened_diagnostic/`); it is not the official v2. "
        "Both bands were fixed before any diagnostic was run, and neither was chosen on the "
        "basis of a diagnostic result.".format(
            LENGTH_RATIO_MIN, LENGTH_RATIO_MAX,
            LENGTH_RATIO_BAND_WIDENED_DIAGNOSTIC[0], LENGTH_RATIO_BAND_WIDENED_DIAGNOSTIC[1],
            LENGTH_RATIO_MIN, LENGTH_RATIO_MAX))
    add("")
    add("Not used anywhere in selection: {}.".format(", ".join(manifest["not_used_in_selection"])))
    add("")
    add("> **Provenance caveat.** {}".format(manifest["provenance_caveat"]))
    add("")
    add("## Tokenizer")
    add("")
    add("`{}` — pattern `{}`. {}".format(
        manifest["tokenizer"]["name"], manifest["tokenizer"]["pattern"], manifest["tokenizer"]["note"]))
    add("")
    add("## The length artifact in the full dataset")
    add("")
    add("| statistic | value |")
    add("| --- | --- |")
    add("| gold-negative pairs in the 962 deduped rows | {} |".format(stats["n_pairs"]))
    add("| median ratio tokens(negative)/tokens(gold) | **{}** |".format(stats["ratio_median"]))
    add("| negative shorter than the band | {:.1%} |".format(stats["share_negative_shorter"]))
    add("| inside the band | {:.1%} |".format(stats["share_in_band"]))
    add("| negative longer than the band | {:.1%} |".format(stats["share_negative_longer"]))
    add("")
    add("The median ResearchBench negative is three times the length of the gold it competes with.")
    add("")
    add("## Selection funnel")
    add("")
    add("Rows are walked in v1's deterministic screening order and gates applied cheapest first. "
        "The gates are conjunctive, so the order does not change which pairs survive.")
    add("")
    add("| gate | rows rejected |")
    add("| --- | --- |")
    add("| no negative inside the length band | {} |".format(rejected.get("length", 0)))
    add("| R1/R3/R5/R6 row screen | {} |".format(rejected.get("row_screen", 0)))
    add("| R4 temporal cutoff not establishable | {} |".format(rejected.get("cutoff", 0)))
    add("| R2 no comparable pair among length-passing negatives | {} |".format(
        rejected.get("comparability", 0)))
    add("| **rows contributing at least one pair** | **{}** |".format(
        manifest["n_source_rows_represented"]))
    add("")
    add("{} rows were walked; {} were screened with a model. Target of {} pairs {}.".format(
        len(outcomes), manifest["n_rows_screened_with_model"], manifest["target_pairs"],
        "reached" if manifest["target_reached"] else "NOT reached — the threshold was not adjusted"))
    add("")
    add("## The slice")
    add("")
    add("| property | value |")
    add("| --- | --- |")
    add("| pairs | {} |".format(len(pairs)))
    add("| distinct source rows | {} |".format(manifest["n_source_rows_represented"]))
    add("| pairs per row (min/median/max) | {}/{}/{} |".format(
        min(per_doi.values()), int(statistics.median(list(per_doi.values()))), max(per_doi.values())))
    add("| length ratio (min/median/max) | {:.2f}/{:.2f}/{:.2f} |".format(
        min(ratios), statistics.median(ratios), max(ratios)))
    add("| most common discipline | {} ({:.0%} of pairs) |".format(
        disciplines.most_common(1)[0][0], disciplines.most_common(1)[0][1] / len(pairs)))
    add("")
    add("Disciplines: {}.".format(", ".join(
        "{} {}".format(name, count) for name, count in disciplines.most_common())))
    add("")

    if diag:
        add("## Artifact diagnostics")
        add("")
        add(diag["note"])
        add("")
        add("| diagnostic | v1 | v2 |")
        add("| --- | --- | --- |")
        v1, v2 = diag.get("v1", {}), diag.get("v2", {})

        def cell(block: Dict[str, Any], *path: str) -> str:
            node: Any = block
            for key in path:
                node = (node or {}).get(key) if isinstance(node, dict) else None
            return "—" if node is None else ("{:.3f}".format(node) if isinstance(node, float) else str(node))

        add("| pairs | {} | {} |".format(
            cell(v1, "length_profile", "n_pairs"), cell(v2, "length_profile", "n_pairs")))
        add("| median length ratio | {} | {} |".format(
            cell(v1, "length_profile", "ratio_median"), cell(v2, "length_profile", "ratio_median")))
        add("| max length ratio | {} | {} |".format(
            cell(v1, "length_profile", "ratio_max"), cell(v2, "length_profile", "ratio_max")))
        add("| gold is the shorter text | {} | {} |".format(
            cell(v1, "length_profile", "share_gold_shorter"), cell(v2, "length_profile", "share_gold_shorter")))
        add("| **shortest-text-first** | **{}** | **{}** |".format(
            cell(v1, "shortest_text_first", "accuracy"), cell(v2, "shortest_text_first", "accuracy")))
        add("| longest-text-first | {} | {} |".format(
            cell(v1, "longest_text_first", "accuracy"), cell(v2, "longest_text_first", "accuracy")))
        add("| **question-hidden judge** | **{}** | **{}** |".format(
            cell(v1, "question_hidden_judge", "accuracy"), cell(v2, "question_hidden_judge", "accuracy")))
        add("")
        add("### Reading these")
        add("")
        add("1. **The length artifact is reduced, not removed.** Shortest-text-first falls from "
            "{} on v1 to {} on v2, but stays well above chance: inside the band the gold is still "
            "the shorter text in {} of pairs (median ratio {}).".format(
                cell(v1, "shortest_text_first", "accuracy"), cell(v2, "shortest_text_first", "accuracy"),
                cell(v2, "length_profile", "share_gold_shorter"), cell(v2, "length_profile", "ratio_median")))
        add("")
        sub = [
            ("as frozen [{}, {}]".format(LENGTH_RATIO_MIN, LENGTH_RATIO_MAX),
             [p for p in pairs if LENGTH_RATIO_MIN <= p["length_ratio"] <= LENGTH_RATIO_MAX]),
            ("original proposal [{}, {}]".format(*LENGTH_RATIO_BAND_V1_PROPOSAL),
             [p for p in pairs if LENGTH_RATIO_BAND_V1_PROPOSAL[0] <= p["length_ratio"] <= LENGTH_RATIO_BAND_V1_PROPOSAL[1]]),
            ("[0.90, 1.11]", [p for p in pairs if 0.90 <= p["length_ratio"] <= 1.11]),
        ]
        add("   Sensitivity of the residual signal to the band, computed on the frozen slice "
            "(reported so the band can be reconsidered deliberately — it was **not** used to "
            "choose the band):")
        add("")
        add("   | band | pairs | shortest-text-first |")
        add("   | --- | --- | --- |")
        for label, subset in sub:
            accuracy = shortest_first(subset)
            add("   | {} | {} | {} |".format(
                label, len(subset), "—" if accuracy is None else "{:.3f}".format(accuracy)))
        add("")
        add("2. **A second artifact is now visible, and it is larger.** The question-hidden judge "
            "*rises* from {} on v1 to {} on v2. With length controlled, a model still recovers the "
            "gold in most pairs from the two texts alone — no question, no literature. Length was "
            "not the only surface cue; genre is a candidate (a reported finding reads differently "
            "from a proposal), and v2's discipline concentration may also contribute.".format(
                cell(v1, "question_hidden_judge", "accuracy"), cell(v2, "question_hidden_judge", "accuracy")))
        add("")
        add("3. **Concentration.** {:.0%} of v2 pairs come from one discipline and {} rows supply "
            "{} pairs, so pairs are not independent. Report per-row as well as per-pair numbers."
            .format(disciplines.most_common(1)[0][1] / len(pairs),
                    manifest["n_source_rows_represented"], len(pairs)))
        add("")

    add("## Files")
    add("")
    for name, what in [
        ("researchbench_v2_pairs.jsonl", "the frozen slice, one record per retained pair"),
        ("v2_manifest.json", "rules, prompts with hashes, funnel counts, provenance"),
        ("v2_artifact_diagnostics_counterbalanced.json",
         "the three diagnostics with every pair judged in BOTH orders (authoritative)"),
        ("v2_artifact_diagnostics.json",
         "the earlier single-order run, kept for provenance; its question-hidden number "
         "is confounded by position preference"),
        ("v2_row_outcomes.jsonl", "every row walked and the gate it was rejected at"),
        ("v2_progress.jsonl", "raw screening decisions, for resuming and auditing"),
    ]:
        add("- `{}` — {}".format(name, what))
    add("")

    out = base / "v2_screening_report.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("wrote {}".format(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
