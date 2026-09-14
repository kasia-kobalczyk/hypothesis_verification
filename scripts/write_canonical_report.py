"""Render `canonical_report.md` from the frozen canonical artifacts."""

from __future__ import annotations

import argparse
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import read_json, read_jsonl, resolve_path  # noqa: E402


def _fmt(value):
    return "{:.3f}".format(value) if isinstance(value, (int, float)) else "?"


CHANCE_MARGIN = 0.1
"""How close to 0.5 a style diagnostic must sit to count as removed.

The frozen protocol said "near 0.5" and "substantially below 0.870" without
numbers; this is the research owner's explicit bar, set after that omission came
to light. It is a module constant rather than a literal so the verdict cannot be
adjusted silently inside the formatting code.
"""


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="benchmark/canonical")
    args = parser.parse_args(argv)
    base = resolve_path(args.dir)

    pairs = list(read_jsonl(base / "researchbench_canonical_pairs.jsonl"))
    manifest = read_json(base / "canonical_manifest.json")
    # Prefer the counterbalanced diagnostics when present: the single-order run is
    # confounded by the judge's position preference (docs/DECISIONS.md #21).
    diag_path = base / "canonical_artifact_diagnostics_counterbalanced.json"
    if not diag_path.exists():
        diag_path = base / "canonical_artifact_diagnostics.json"
    diag = read_json(diag_path) if diag_path.exists() else {}

    L: List[str] = []
    add = L.append
    add("# Canonicalized evaluation benchmark — build report")
    add("")
    add("**{}**".format(manifest["status"]))
    add("")
    add("> {}".format(manifest["derived"]))
    add("")
    add("Built {} against `{}`, which was frozen before this ran.".format(
        manifest["frozen_at"], manifest["protocol"]))
    add("")
    add("## What was done")
    add("")
    for gate in manifest["gates"]:
        add("1. {}".format(gate))
    add("")
    add("{}".format(manifest["no_length_gate"]))
    add("")
    add("Never consulted: {}.".format(", ".join(manifest["not_used_in_construction"])))
    add("")

    add("## Yield")
    add("")
    add("| | |")
    add("| --- | --- |")
    add("| pairs | **{}** |".format(manifest["n_pairs"]))
    add("| source rows | {} |".format(manifest["n_source_rows"]))
    add("| rows canonicalised | {} |".format(manifest["n_rows_canonicalised"]))
    add("| target | {} ({}) |".format(
        manifest["target_pairs"], "reached" if manifest["target_reached"] else "NOT reached"))
    add("")
    add("Rows rejected: {}".format(manifest["rejected"] or "none"))
    add("")
    add("## Semantic preservation")
    add("")
    preserved = manifest["preservation"]
    total = sum(preserved.values()) or 1
    add("Every canonical claim was checked against its original by a separate judge "
        "that was not told the candidate's role.")
    add("")
    for key, count in sorted(preserved.items()):
        add("- {}: {} ({:.0%})".format(key, count, count / total))
    add("")
    add("A candidate whose claim was not preserved is dropped, and every pair "
        "involving it with it. A judge failure is recorded as an error, never as a pass.")
    add("")

    profile = manifest["length_profile"]
    add("## Length, as a diagnostic (never a filter)")
    add("")
    add("| | canonical |")
    add("| --- | --- |")
    add("| gold tokens (median) | {} |".format(profile["gold_tokens_median"]))
    add("| negative tokens (median) | {} |".format(profile["negative_tokens_median"]))
    add("| ratio negative/gold (min / median / max) | {} / {} / {} |".format(
        profile["ratio_min"], profile["ratio_median"], profile["ratio_max"]))
    add("| gold is the shorter text | {:.1%} |".format(profile["share_gold_shorter"]))
    add("")
    add("For comparison, the raw ResearchBench median ratio is **3.0**, and the gold is "
        "the shorter candidate in 98% of v1 pairs.")
    add("")

    if diag:
        add("## Artifact diagnostics")
        add("")
        add("The same three used on v1 and v2, so the numbers are comparable. Run after "
            "freezing; the protocol forbids adjusting anything in response to them.")
        add("")
        add("| diagnostic | v1 | v2 | canonical |")
        add("| --- | --- | --- | --- |")

        def cell(block, *path):
            node: Any = block or {}
            for key in path:
                node = (node or {}).get(key) if isinstance(node, dict) else None
            if node is None:
                return "—"
            return "{:.3f}".format(node) if isinstance(node, float) else str(node)

        v1, v2, canon = diag.get("v1"), diag.get("v2"), diag.get("canonical")
        add("| pairs | {} | {} | {} |".format(
            cell(v1, "length_profile", "n_pairs"), cell(v2, "length_profile", "n_pairs"),
            cell(canon, "length_profile", "n_pairs")))
        add("| gold is the shorter text | {} | {} | {} |".format(
            cell(v1, "length_profile", "share_gold_shorter"),
            cell(v2, "length_profile", "share_gold_shorter"),
            cell(canon, "length_profile", "share_gold_shorter")))
        add("| **shortest-text-first** | {} | {} | **{}** |".format(
            cell(v1, "shortest_text_first", "accuracy"), cell(v2, "shortest_text_first", "accuracy"),
            cell(canon, "shortest_text_first", "accuracy")))
        add("| longest-text-first | {} | {} | {} |".format(
            cell(v1, "longest_text_first", "accuracy"), cell(v2, "longest_text_first", "accuracy"),
            cell(canon, "longest_text_first", "accuracy")))
        add("| **question-hidden judge** | {} | {} | **{}** |".format(
            cell(v1, "question_hidden_judge", "accuracy"), cell(v2, "question_hidden_judge", "accuracy"),
            cell(canon, "question_hidden_judge", "accuracy")))
        add("")
        add("### Against the criterion declared in the protocol")
        add("")
        add("The protocol required, in advance: both length heuristics near 0.5, and the "
            "question-hidden judge substantially below the 0.870 it scores on v2. It put a "
            "number on neither bar. The research owner has since set both at "
            "**within {:.2f} of chance**, which is the bar applied below.".format(CHANCE_MARGIN))
        add("")
        for label, key in (("shortest-text-first", "shortest_text_first"),
                           ("longest-text-first", "longest_text_first"),
                           ("question-hidden judge", "question_hidden_judge")):
            block = (canon or {}).get(key, {})
            value = block.get("accuracy")
            if value is None:
                continue
            ok = abs(value - 0.5) <= CHANCE_MARGIN
            suffix = " (counterbalanced)" if block.get("counterbalanced") else ""
            add("- {}{} **{:.3f}** — {}".format(
                label, suffix, value,
                "within {:.2f} of chance: PASS".format(CHANCE_MARGIN) if ok
                else "off chance by {:.3f}: FAIL".format(abs(value - 0.5))))
        add("")
        judge = (canon or {}).get("question_hidden_judge", {})
        if judge.get("counterbalanced"):
            add("#### Where the remaining style cue sits")
            add("")
            add("Each pair is judged in both orders, so a pure position-guesser scores "
                "exactly 0.500 and the accuracy splits cleanly into two populations.")
            add("")
            add("| | share of pairs | accuracy on them |")
            add("| --- | --- | --- |")
            add("| judge answers the same way in both orders | {} | {} |".format(
                _fmt(judge.get("order_consistency")), _fmt(judge.get("accuracy_when_consistent"))))
            add("| answer flips with order (guessing) | {} | 0.500 by construction |".format(
                _fmt(1 - judge["order_consistency"]) if judge.get("order_consistency")
                else "?"))
            add("")
            add("Read that way, canonicalisation cut the *number of pairs carrying a "
                "usable text-only cue* rather than weakening the cue itself. The "
                "remaining signal is concentrated in a minority of pairs, which is a "
                "more tractable target than a diffuse one — though any rule for "
                "dropping them has to be declared before it is applied, not chosen "
                "from this table.")
            add("")
        add("A FAIL here is a finding about what canonicalisation can remove, not a "
            "reason to rebuild the slice until the number improves.")
        add("")
        add("> Two caveats on the criterion itself, recorded because they matter more than "
            "the verdict. (1) The protocol's bars were words, not numbers; an earlier "
            "version of this report operationalised \"substantially below\" as `< 0.75` "
            "*after* the result was known, which turned 0.686 into a pass. See "
            "`docs/DECISIONS.md` #16. (2) The question-hidden judge is not deterministic: "
            "the same prompt over the same 100 official v2 pairs scored 0.870 and 0.890 on "
            "two runs 43 minutes apart. Treat ~0.02 as noise.")
        add("")

    add("## Worked examples")
    add("")
    for pair in pairs[:3]:
        add("**{}** ({})".format(pair["pair_id"], pair.get("discipline")))
        add("")
        add("- question: {}".format(pair["question"][:200]))
        add("- gold original ({} tok): {}...".format(
            len(pair["gold_original"].split()), pair["gold_original"][:160]))
        add("- **gold canonical**: {}".format(pair["gold_hypothesis"]))
        add("- negative original ({} tok): {}...".format(
            len(pair["negative_original"].split()), pair["negative_original"][:160]))
        add("- **negative canonical**: {}".format(pair["negative_hypothesis"]))
        add("")

    add("## Files")
    add("")
    for name, what in [
        ("researchbench_canonical_pairs.jsonl", "the slice; canonical claims plus both originals"),
        ("canonical_manifest.json", "gates, prompts with hashes, yield, preservation counts"),
        ("canonical_artifact_diagnostics_counterbalanced.json",
         "the three diagnostics with every pair judged in BOTH orders (authoritative)"),
        ("canonical_artifact_diagnostics.json",
         "the earlier single-order run, kept for provenance; its question-hidden "
         "number is confounded by position preference"),
        ("canonical_progress.jsonl", "every canonicalisation and judgment, for audit"),
    ]:
        add("- `{}` — {}".format(name, what))
    add("")

    out = base / "canonical_report.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("wrote {}".format(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
