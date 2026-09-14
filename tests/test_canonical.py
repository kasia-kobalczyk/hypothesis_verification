"""The canonicalized benchmark: symmetry, preservation, and the frozen protocol.

The benchmark's whole claim is that one transformation was applied identically to
gold and negative. These tests pin that down, because it is not verifiable from
the output alone.
"""

from __future__ import annotations

import json

import pytest

from src.benchmark.canonical import (
    CANONICALISE_PROMPT,
    PRESERVATION_PROMPT,
    CanonicalCandidate,
    canonicalise,
    canonicalise_row,
    check_preservation,
)
from src.common.io import read_json, read_jsonl, repo_root
from src.llm.client import MockLLMClient
from src.llm.prompts import PromptLibrary

CANON = repo_root() / "benchmark" / "canonical"


def responder(payload):
    return lambda messages, cfg: json.dumps(payload)


@pytest.fixture
def prompts(config):
    return PromptLibrary(config.prompts.dir)


# --------------------------------------------------------------------------- #
# Symmetry: the transformation cannot know which side it is on
# --------------------------------------------------------------------------- #
def test_the_canonicaliser_is_never_told_the_candidate_role(config, prompts):
    """The prompt has no slot for it, so it cannot leak even by accident."""
    template = prompts.get(CANONICALISE_PROMPT)
    assert "$role" not in template.text
    assert "gold" not in template.text.lower()
    assert "negative" not in template.text.lower()
    rendered = template.render(question="Q", candidate="C", max_tokens=30)
    assert "gold" not in rendered.lower()


def test_the_preservation_judge_is_never_told_the_candidate_role(prompts):
    template = prompts.get(PRESERVATION_PROMPT)
    text = template.text.lower()
    assert "$role" not in template.text
    for word in ("gold", "negative"):
        assert word not in text, word
    # And it is told not to judge the science, only the faithfulness of restatement.
    assert "do not judge whether either version is scientifically correct" in text
    assert "faithfulness of restatement only" in text


def test_gold_and_negative_go_through_an_identical_call(config, prompts):
    """Same prompt, same parameters — only the candidate text differs."""
    llm = MockLLMClient(config.llm, responder=responder({"claim": "X causes Y",
                                                         "central_relationship": "X->Y"}))
    row = {
        "research_question": "Does X cause Y?",
        "gold_hypothesis": "The study concludes X causes Y.",
        "model_negative_hypotheses": ["We propose a study of whether X prevents Y."],
    }
    canonicalise_row(row, llm=llm, prompts=prompts)

    canonical_calls = [c[0]["content"] for c in llm.calls if "CANDIDATE:" in c[0]["content"]]
    assert len(canonical_calls) == 2
    gold_call, negative_call = canonical_calls
    # Everything except the candidate block is byte-identical.
    strip = lambda text: text.split("CANDIDATE:")[0]
    assert strip(gold_call) == strip(negative_call)


def test_a_candidate_asserting_no_claim_is_dropped_not_invented(config, prompts):
    llm = MockLLMClient(config.llm, responder=responder({"claim": None,
                                                         "central_relationship": None}))
    row = {"research_question": "Q", "gold_hypothesis": "We will measure things.",
           "model_negative_hypotheses": []}
    candidates = canonicalise_row(row, llm=llm, prompts=prompts)
    assert candidates[0].claim is None
    assert candidates[0].preserved is False
    assert candidates[0].usable is False


# --------------------------------------------------------------------------- #
# Preservation is derived from the criteria, and an error is neither verdict
# --------------------------------------------------------------------------- #
def test_preservation_is_derived_not_taken_from_a_summary_field(config, prompts):
    llm = MockLLMClient(config.llm, responder=responder({
        "same_subject": True, "same_direction": False, "no_new_mechanism": True,
        "preserved": True, "rationale": "r"}))
    detail = check_preservation("original", "canonical", llm=llm, prompts=prompts)
    assert detail["preserved"] is False, "a flipped direction cannot be overridden"


def test_a_preservation_judge_failure_is_an_error_not_a_verdict(config, prompts):
    llm = MockLLMClient(config.llm, responder=lambda m, c: "not json")
    detail = check_preservation("original", "canonical", llm=llm, prompts=prompts)
    assert detail["preserved"] is None
    assert "LLMParseError" in detail["error"]


def test_a_canonicalisation_failure_is_recorded(config, prompts):
    llm = MockLLMClient(config.llm, responder=lambda m, c: "not json")
    assert "error" in canonicalise("Q", "C", llm=llm, prompts=prompts)


# --------------------------------------------------------------------------- #
# The frozen slice
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def pairs():
    path = CANON / "researchbench_canonical_pairs.jsonl"
    if not path.exists():
        pytest.skip("canonical benchmark not built")
    return list(read_jsonl(path))


def test_the_slice_keeps_both_the_canonical_and_the_original_text(pairs):
    for pair in pairs:
        for key in ("gold_hypothesis", "negative_hypothesis",
                    "gold_original", "negative_original", "question"):
            assert pair.get(key), key
        # The canonical form is genuinely shorter than what it replaced.
        assert len(pair["gold_hypothesis"]) < len(pair["gold_original"]) or \
            pair["gold_hypothesis"] == pair["gold_original"]


def test_every_retained_pair_passed_preservation_and_comparability(pairs):
    for pair in pairs:
        assert pair["gold_preserved"] is True
        assert pair["negative_preserved"] is True
        assert pair["semantic_comparable"] is True


def test_there_is_no_length_gate(pairs):
    """The protocol forbids one; ratios must therefore range freely."""
    ratios = [p["length_ratio"] for p in pairs]
    assert min(ratios) < 0.75 or max(ratios) > 1.33, (
        "with no length gate, some pair should fall outside the v2 band"
    )


def test_the_manifest_says_it_is_derived_and_names_the_protocol():
    manifest = read_json(CANON / "canonical_manifest.json")
    assert "DERIVED" in manifest["derived"]
    assert "not untouched ResearchBench" in manifest["derived"]
    assert manifest["protocol"].startswith("docs/CANONICAL_PROTOCOL.md")
    forbidden = " ".join(manifest["not_used_in_construction"]).lower()
    for item in ("literature retrieval", "verifier", "which candidate is the gold"):
        assert item in forbidden


def test_the_protocol_was_frozen_before_the_build():
    protocol = (repo_root() / "docs" / "CANONICAL_PROTOCOL.md").read_text(encoding="utf-8")
    assert "FROZEN" in protocol
    assert "before the consequence verifier was run" in protocol
    # The success criterion has to be stated in advance to mean anything.
    assert "success criterion is declared in advance" in protocol


def test_diagnostics_beat_v2_on_the_style_cue():
    path = CANON / "canonical_artifact_diagnostics.json"
    if not path.exists():
        pytest.skip("diagnostics not run")
    diag = read_json(path)
    canonical, v1 = diag["canonical"], diag["v1"]
    assert canonical["shortest_text_first"]["accuracy"] < v1["shortest_text_first"]["accuracy"]
    assert canonical["question_hidden_judge"]["accuracy"] < diag["v2"]["question_hidden_judge"]["accuracy"]


# --------------------------------------------------------------------------- #
# Review-article sources (task validity)
# --------------------------------------------------------------------------- #
def test_a_review_venue_is_detected_and_says_why():
    from src.benchmark.review_sources import classify_source

    verdict = classify_source(
        venue="Trends in Cell Biology",
        title="Disulfidptosis: disulfide stress-induced cell death",
        venue_patterns=["Trends in ", "Nature Reviews"],
        title_patterns=["a review of"])
    assert verdict.is_review
    assert verdict.basis == "venue_pattern"
    assert verdict.matched == "Trends in "
    # A bare boolean would not be auditable; the record must name the evidence.
    assert verdict.record()["venue"] == "Trends in Cell Biology"


def test_a_primary_paper_is_not_flagged():
    from src.benchmark.review_sources import classify_source

    verdict = classify_source(
        venue="Nature Communications",
        title="IL-10 induces a Myc-dependent metabolic shift in macrophages",
        venue_patterns=["Trends in ", "Nature Reviews"],
        title_patterns=["a review of"])
    assert not verdict.is_review
    assert verdict.basis is None


def test_the_configured_patterns_do_not_flag_primary_research_journals():
    """Regression: 'Advances in ' and 'Progress in ' matched primary journals.

    Excluding *Advances in Space Research* or *Progress in Natural Science* would
    drop valid rows and skew the remaining set by discipline, which is worse than
    missing a review.
    """
    from src.benchmark.review_sources import classify_source
    from src.common.config import load_config

    policy = load_config("configs/mvp.yaml").dataset.review_sources
    for venue in ("Advances in Space Research",
                  "Progress in Natural Science: Materials International",
                  "Nature Communications",
                  "Physical Review Letters",
                  "Journal of Geophysical Research: Atmospheres"):
        verdict = classify_source(venue=venue, title="some primary finding",
                                  venue_patterns=policy.venue_patterns,
                                  title_patterns=policy.title_patterns)
        assert not verdict.is_review, "{} must not be treated as a review venue".format(venue)


def test_the_configured_patterns_still_catch_the_known_review_venues():
    from src.benchmark.review_sources import classify_source
    from src.common.config import load_config

    policy = load_config("configs/mvp.yaml").dataset.review_sources
    for venue in ("Trends in Cell Biology", "Trends in Ecology & Evolution",
                  "Nature Reviews Microbiology", "Nature Reviews Molecular Cell Biology",
                  "Annual Review of Genetics", "Chemical Reviews"):
        verdict = classify_source(venue=venue, title="t",
                                  venue_patterns=policy.venue_patterns,
                                  title_patterns=policy.title_patterns)
        assert verdict.is_review, "{} should be flagged".format(venue)


def test_missing_metadata_is_not_a_verdict():
    """An absent Crossref record must not be read as 'not a review'."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path("scripts").resolve()))
    from build_canonical_benchmark import _review_verdict
    from src.common.config import load_config

    policy = load_config("configs/mvp.yaml").dataset.review_sources
    assert _review_verdict("10.9999/definitely-not-cached", policy=policy) is None
