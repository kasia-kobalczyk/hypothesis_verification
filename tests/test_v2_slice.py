"""The v2 length-controlled slice: tokenizer, length rule, ordering, outputs."""

from __future__ import annotations

import json

import pytest

from src.benchmark.v2_slice import (
    LENGTH_RATIO_BAND_V1_PROPOSAL,
    LENGTH_RATIO_BAND_WIDENED_DIAGNOSTIC,
    LENGTH_RATIO_MAX,
    LENGTH_RATIO_MIN,
    TOKENIZER_NAME,
    count_tokens,
    length_candidates,
    length_ratio,
    length_rule_pass,
    screening_order,
)
from src.common.io import read_json, read_jsonl, repo_root

V2 = repo_root() / "benchmark" / "v2"


# --------------------------------------------------------------------------- #
# Tokenizer
# --------------------------------------------------------------------------- #
def test_tokenizer_is_deterministic_and_needs_no_download():
    text = "Bi2O3 content increases, so micro-hardness decreases (p < 0.05)."
    assert count_tokens(text) == count_tokens(text)
    assert count_tokens("") == 0
    assert count_tokens(None) == 0
    # Words and single punctuation marks, nothing else.
    assert count_tokens("a b c") == 3
    assert count_tokens("a, b") == 3


def test_tokenizer_name_is_recorded_in_the_manifest():
    assert read_json(V2 / "v2_manifest.json")["tokenizer"]["name"] == TOKENIZER_NAME


# --------------------------------------------------------------------------- #
# The length rule
# --------------------------------------------------------------------------- #
def test_length_ratio_is_negative_over_gold():
    assert length_ratio("a b c d", "a b") == 0.5
    assert length_ratio("a b", "a b c d") == 2.0
    assert length_ratio("", "a b") is None, "an empty gold has no ratio, not a zero one"


@pytest.mark.parametrize(
    "ratio,expected",
    [(0.74, False), (0.75, True), (1.0, True), (1.33, True), (1.34, False), (None, False)],
)
def test_band_edges(ratio, expected):
    assert length_rule_pass(ratio) is expected


def test_the_official_band_is_the_originally_specified_one():
    """Widened to [0.67, 1.50], then reverted after the diagnostics. Both on record."""
    assert (LENGTH_RATIO_MIN, LENGTH_RATIO_MAX) == (0.75, 1.33)
    assert LENGTH_RATIO_BAND_V1_PROPOSAL == (0.75, 1.33)
    assert LENGTH_RATIO_BAND_WIDENED_DIAGNOSTIC == (0.67, 1.50)


def test_the_widened_slice_is_kept_as_a_diagnostic_not_a_benchmark():
    from src.common.io import repo_root

    widened = repo_root() / "benchmark" / "v2_widened_diagnostic"
    assert (widened / "researchbench_v2_pairs.jsonl").exists()
    official = read_json(V2 / "v2_manifest.json")
    assert "DEVELOPMENT" in official["status"]
    assert "must NOT be reported as evidence" in official["status_note"]


def test_candidates_are_not_reordered_or_preferred():
    row = {
        "gold_hypothesis": "a b c d",          # 4 tokens
        "model_negative_hypotheses": [
            "a b c d e",                        # ratio 1.25 -> in band
            "a b c d e f g h i j k l",          # ratio 3.0  -> out
            "a b c",                            # ratio 0.75 -> in band
        ],
    }
    got = length_candidates(row)
    assert [index for index, _, _ in got] == [0, 2], "all passing negatives kept, original order"


# --------------------------------------------------------------------------- #
# v1's screening order is reproduced, not reinvented
# --------------------------------------------------------------------------- #
def test_screening_order_reproduces_every_v1_screen_rank():
    order = screening_order(repo_root() / "benchmark" / "ranking.jsonl")
    assert len(order) == 962, "v1 manifest records 962 unique DOI groups"
    rank_of = {doi: rank for rank, doi, _ in order}
    dev = list(read_jsonl(repo_root() / "benchmark" / "dev" / "researchbench_dev20_v1.jsonl"))
    assert dev, "v1 slice must be present"
    for item in dev:
        assert rank_of[item["doi"]] == item["screen_rank"], item["dev_id"]


def test_screening_order_is_stable_across_calls():
    path = repo_root() / "benchmark" / "ranking.jsonl"
    assert [d for _, d, _ in screening_order(path)] == [d for _, d, _ in screening_order(path)]


# --------------------------------------------------------------------------- #
# The frozen slice
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def pairs():
    return list(read_jsonl(V2 / "researchbench_v2_pairs.jsonl"))


def test_every_pair_has_the_required_fields(pairs):
    required = {
        "pair_id", "researchbench_sample_id", "doi", "question", "gold_hypothesis",
        "negative_hypothesis", "gold_token_count", "negative_token_count",
        "length_ratio", "semantic_comparable", "length_rule_pass",
    }
    assert pairs
    for pair in pairs:
        assert required <= set(pair), sorted(required - set(pair))


def test_every_retained_pair_passed_both_gates(pairs):
    for pair in pairs:
        assert pair["semantic_comparable"] is True
        assert pair["length_rule_pass"] is True
        assert LENGTH_RATIO_MIN <= pair["length_ratio"] <= LENGTH_RATIO_MAX, pair["pair_id"]


def test_token_counts_match_the_recorded_texts(pairs):
    """The counts are the ones the rule was applied to, not stale copies."""
    for pair in pairs:
        assert pair["gold_token_count"] == count_tokens(pair["gold_hypothesis"])
        assert pair["negative_token_count"] == count_tokens(pair["negative_hypothesis"])
        expected = pair["negative_token_count"] / pair["gold_token_count"]
        assert pair["length_ratio"] == pytest.approx(expected, abs=1e-4)


def test_hypothesis_text_is_verbatim_researchbench(pairs):
    """Nothing was rewritten to fit the band."""
    source = {}
    for row in read_jsonl(repo_root() / "benchmark" / "ranking.jsonl"):
        source.setdefault(row["doi"], row)
    for pair in pairs:
        row = source[pair["doi"]]
        assert pair["gold_hypothesis"] == row["gold_hypothesis"]
        assert pair["negative_hypothesis"] == row["model_negative_hypotheses"][pair["negative_index"]]
        assert pair["question"] == row["research_question"]


def test_pair_ids_are_unique(pairs):
    ids = [p["pair_id"] for p in pairs]
    assert len(ids) == len(set(ids))


def test_manifest_records_what_was_not_used_in_selection():
    manifest = read_json(V2 / "v2_manifest.json")
    excluded = " ".join(manifest["not_used_in_selection"]).lower()
    for forbidden in ("literature retrieval", "direct-rag", "consequence-graph", "verifier"):
        assert forbidden in excluded
    assert manifest["provenance_caveat"], "the R1/R3/R5/R6 re-implementation must be disclosed"


def test_diagnostics_were_run_after_freezing_and_did_not_feed_back():
    diag = read_json(V2 / "v2_artifact_diagnostics.json")
    assert "did not influence selection" in diag["note"]
    for key in ("shortest_text_first", "longest_text_first", "question_hidden_judge"):
        assert diag["v2"][key]["accuracy"] is not None, key
    # Complementary heuristics must sum to 1 (ties counted half to each).
    assert diag["v2"]["shortest_text_first"]["accuracy"] + \
        diag["v2"]["longest_text_first"]["accuracy"] == pytest.approx(1.0, abs=1e-3)
