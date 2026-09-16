"""Sanity checks for the GP1 human review packet (BENCH-GRAPH-REVIEW-001 §9).

The packet will become the basis for human ground truth about the pilot failure
mode. These tests check that it is faithful to the frozen run, not merely
well-formed:

* every record is a real node of the preserved run;
* the packet's contributions add up to the frozen case scores;
* the evidence text is exactly what the assessor read;
* no hidden benchmark annotation sits in a verifier-output field;
* selection does not depend on the post-hoc auditor;
* the committed files are exactly what the builder produces now.
"""
from __future__ import annotations

import json
import math
import re
import tempfile
from pathlib import Path

import pytest

import scripts.build_review_packet as bp

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "benchmark" / "review" / "graph_pilot_001"
VERIFIER_FIELDS = ("proposition", "case_context", "verifier_graph", "verifier_evidence", "score_influence")


@pytest.fixture(scope="module")
def extracted():
    # The archive is deliberately not in the public repository (full model traffic and
    # ~3,800 third-party abstracts). Where it is absent, the tests that need the frozen
    # run skip; the ones that check only the committed packet still run.
    if not bp.ARCHIVE.exists():
        pytest.skip("private pilot archive not present: {} (see {})".format(
            bp.ARCHIVE.relative_to(ROOT), (bp.PRESERVED / "PROVENANCE.md").relative_to(ROOT)))
    with tempfile.TemporaryDirectory() as tmp:
        yield bp.extract_verified(Path(tmp))


@pytest.fixture(scope="module")
def built(extracted):
    return bp.build(extracted / "run", extracted / "supplementary_scratch")


@pytest.fixture(scope="module")
def records(built):
    return built[0]


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Provenance
# --------------------------------------------------------------------------- #
def test_packet_is_built_from_the_checksummed_archive(extracted):
    """extract_verified raises on any checksum mismatch; reaching here means every
    archived file matched SHA256SUMS."""
    assert (extracted / "run" / "summary.json").exists()


def test_builder_makes_no_llm_calls():
    source = (ROOT / "scripts" / "build_review_packet.py").read_text(encoding="utf-8")
    assert "src.llm" not in source
    assert "complete_json" not in source and "build_llm_client" not in source


# --------------------------------------------------------------------------- #
# Records map to the frozen run
# --------------------------------------------------------------------------- #
def test_every_record_is_a_real_frozen_graph_node(records, extracted):
    for r in records:
        graph = _load(extracted / "run" / "instances" / r["case_id"] / "graph.json")
        nodes = {n["id"]: n for n in graph["nodes"]}
        assert r["node_id"] in nodes, r["review_id"]
        assert r["proposition"]["text"] == nodes[r["node_id"]]["text"]
        assert r["proposition"]["origin_hypothesis_id"] == nodes[r["node_id"]]["generation_origin_hypothesis"]


def test_hypotheses_are_exactly_those_given_to_the_verifier(records, extracted):
    for r in records:
        instance = _load(extracted / "run" / "instances" / r["case_id"] / "input.json")
        assert r["case_context"]["hypotheses_as_shown_to_verifier"] == {h["id"]: h["text"] for h in instance["hypotheses"]}
        assert r["case_context"]["historical_cutoff"] == instance["cutoff_date"]


def test_review_ids_are_unique_and_stable(records):
    ids = [r["review_id"] for r in records]
    assert len(ids) == len(set(ids))
    assert all(i == "GP1-{}-{}".format(r["case_id"], r["node_id"]) for i, r in zip(ids, records))


def test_cross_evaluation_covers_every_hypothesis(records):
    for r in records:
        judgments = r["verifier_graph"]["cross_hypothesis_judgments"]
        assert set(judgments) == set(r["case_context"]["hypotheses_as_shown_to_verifier"])
        assert sum(v["is_origin_of_proposition"] for v in judgments.values()) == 1


# --------------------------------------------------------------------------- #
# Scores reproduce the frozen aggregate
# --------------------------------------------------------------------------- #
def test_packet_contributions_sum_to_the_frozen_case_log_odds(records, extracted):
    """Non-moving nodes add equally to both hypotheses, so the packet's nodes alone
    must account for the whole frozen log-odds between them."""
    by_case = {}
    for r in records:
        by_case.setdefault(r["case_id"], []).append(r)
    assert len(by_case) == 8
    for case_id, recs in by_case.items():
        scores = _load(extracted / "run" / "instances" / case_id / "scores.json")["scores"]
        h1, h2 = list(recs[0]["score_influence"]["log_likelihood_contribution_by_hypothesis"])
        frozen_log_odds = math.log(scores[h1] / scores[h2])
        packet_sum = sum(r["score_influence"]["log_odds_contribution"]["value"] for r in recs)
        assert packet_sum == pytest.approx(frozen_log_odds, abs=1e-4), case_id
        assert recs[0]["score_influence"]["case_total_log_odds"]["value"] == pytest.approx(frozen_log_odds, abs=1e-4)


def test_influence_is_the_spread_of_contributions(records):
    for r in records:
        c = r["score_influence"]["log_likelihood_contribution_by_hypothesis"]
        assert r["score_influence"]["absolute_influence"] == pytest.approx(max(c.values()) - min(c.values()))
        assert r["score_influence"]["absolute_influence"] > bp.INFLUENCE_TOL


def test_priority_set_is_the_minimal_prefix_reaching_80_percent(records):
    ordered = sorted(records, key=lambda r: r["score_influence"]["rank_global"])
    total = sum(r["score_influence"]["absolute_influence"] for r in ordered)
    n_priority = sum(r["score_influence"]["in_priority_set"] for r in ordered)
    covered = sum(r["score_influence"]["absolute_influence"] for r in ordered[:n_priority])
    assert covered / total >= 0.80
    assert (covered - ordered[n_priority - 1]["score_influence"]["absolute_influence"]) / total < 0.80
    assert all(r["score_influence"]["in_priority_set"] for r in ordered[:n_priority])


def test_evidence_withheld_counterfactual_is_arithmetic(records):
    for r in records:
        si = r["score_influence"]
        expected = si["case_total_log_odds"]["value"] - si["log_odds_contribution"]["value"]
        assert si["counterfactual_evidence_withheld"]["case_log_odds"] == pytest.approx(expected, abs=1e-5)


# --------------------------------------------------------------------------- #
# Evidence text is exactly what the assessor saw
# --------------------------------------------------------------------------- #
def test_evidence_text_is_verbatim_from_the_rendered_assessor_prompt(records, extracted):
    events_cache = {}
    for r in records:
        case_id = r["case_id"]
        if case_id not in events_cache:
            path = extracted / "run" / "instances" / case_id / "events.jsonl"
            events_cache[case_id] = {e.get("call_id"): e for e in
                                     (json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip())}
        ev = r["verifier_evidence"]
        call = events_cache[case_id][ev["assessor_call_id"]]
        assert call["purpose"] == "graph.evidence_assess"
        prompt = call["messages"][-1]["content"]
        assert "PROPOSITION:\n{}\n".format(r["proposition"]["text"]) in prompt
        literature = re.search(r"RETRIEVED LITERATURE:\n(.*?)\n\nReturn a single JSON object", prompt, re.S).group(1)
        joined = ev["papers_shown_separator"].join(p["exact_text_shown_to_assessor"] for p in ev["papers_shown"])
        assert joined == literature, r["review_id"]
        assert ev["assessor_raw_response"] == call["response_text"]


def test_evidence_judgment_matches_frozen_evidence_file(records, extracted):
    for r in records:
        frozen = _load(extracted / "run" / "instances" / r["case_id"] / "evidence.json")["by_node"][r["node_id"]]["assessment"]
        ev = r["verifier_evidence"]
        assert ev["evidence_label_used_in_score"] == frozen["evidence_label"]
        assert [s["text"] for s in ev["supporting_spans"]] == (frozen.get("supporting_spans") or [])
        assert ev["key_papers"] == sorted(frozen.get("key_papers") or [])
        assert ev["assessor_rationale"] == frozen.get("rationale")


def test_shown_papers_carry_the_cutoff_filter_date(records):
    for r in records:
        cutoff = r["case_context"]["historical_cutoff"]
        for p in r["verifier_evidence"]["papers_shown"]:
            assert p["eligible_date_used_by_cutoff_filter"], (r["review_id"], p["paper_id"])
            assert p["eligible_date_used_by_cutoff_filter"] <= cutoff, (r["review_id"], p["paper_id"])


# --------------------------------------------------------------------------- #
# Hidden context is kept out of verifier fields
# --------------------------------------------------------------------------- #
def _hidden_needles():
    hidden = _load(bp.HIDDEN)["cases"]
    needles = {}
    for case_id, case in hidden.items():
        phrases = set()
        texts = list(case["reference_discriminators"]) + list(case["resolving_observations"]) + [case["resolution"]["summary"]]
        for text in texts:
            words = text.lower().split()
            span = 8
            if len(words) <= span:
                phrases.add(" ".join(words))
            else:
                phrases.update(" ".join(words[i:i + span]) for i in range(len(words) - span + 1))
        dois = set(re.findall(r"10\.\d{4,9}/[^\s\"'),;]+", json.dumps(case["resolver"]).lower()))
        needles[case_id] = (phrases, dois)
    return needles


def test_no_hidden_annotation_in_any_verifier_field(records):
    needles = _hidden_needles()
    for r in records:
        phrases, dois = needles[r["case_id"]]
        blob = " ".join(json.dumps(r[f], ensure_ascii=False).lower() for f in VERIFIER_FIELDS)
        blob = re.sub(r"\s+", " ", blob)
        for doi in dois:
            assert doi not in blob, (r["review_id"], doi)
        for phrase in phrases:
            assert phrase not in blob, (r["review_id"], phrase)


def test_post_hoc_metadata_is_labelled_and_separate(records):
    for r in records:
        audit = r["posthoc_automated_audit"]
        assert "NON_AUTHORITATIVE" in audit
        for field in VERIFIER_FIELDS:
            assert "posthoc" not in json.dumps(r[field]).lower()


def test_hidden_context_is_only_in_the_labelled_appendix_and_audit(built):
    hidden = built[2]
    assert set(hidden) == {"eukaryogenesis_mito_timing", "fly_wing_constraint_vs_selection",
                           "forest_fragmentation_resilience", "gcn4_med15_complex_vs_condensate",
                           "glnbp_induced_fit_vs_conformational_selection", "pfc_interhemispheric_architecture",
                           "pfc_storage_vs_control", "spider_orb_web_origin"}
    md = (PACKET / "review_full.md").read_text(encoding="utf-8")
    for case in hidden.values():
        assert case["resolution_summary"] not in md


LABEL_FILE = PACKET / "human_labels_D045.json"
D045_LINE = re.compile(r"^(\d+)\.?\s+`?([A-Za-z0-9_]+-X\d+)`?\s+—\s+`?([a-z_]+)`?\s*$", re.M)
RECORDED_BY_D045 = {"human_primary_category", "human_is_genuinely_discriminative",
                    "human_silence_as_null_error", "human_reviewer", "human_review_source",
                    "human_review_status"}


def _d045_from_decisions():
    text = (ROOT / ".agent" / "DECISIONS.md").read_text(encoding="utf-8")
    section = text[text.index("## D045"):]
    section = section[section.index("NODE-LEVEL PRIMARY LABELS"):section.index("KEY INTERPRETATION")]
    return [(int(n), key, cat) for n, key, cat in D045_LINE.findall(section)]


def test_label_file_is_an_exact_transcription_of_d045():
    """The label file must equal D045 as recorded by the Research Director: same
    numbering, same node keys, same categories, and the stated category counts."""
    parsed = _d045_from_decisions()
    labels = _load(LABEL_FILE)["labels"]
    assert len(parsed) == 40
    assert [(l["d045_number"], l["d045_key"], l["human_primary_category"]) for l in labels] == parsed
    from collections import Counter
    assert Counter(c for _, _, c in parsed) == Counter({
        "generic_component_fact": 14, "silence_as_null_error": 8, "compatible_non_discriminative": 8,
        "genuine_discriminator": 4, "evidence_construct_mismatch": 3, "invalid_or_weak_implication": 3})


def test_d045_keys_resolve_to_the_priority_set_in_rank_order():
    labels = _load(LABEL_FILE)["labels"]
    full = {json.loads(l)["review_id"]: json.loads(l)
            for l in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()}
    priority = {rid for rid, r in full.items() if r["score_influence"]["in_priority_set"]}
    assert {l["review_id"] for l in labels} == priority
    for l in labels:
        prefix, node = l["d045_key"].rsplit("-", 1)
        assert l["node_id"] == node and (l["case_id"] == prefix or l["case_id"].startswith(prefix + "_"))
        assert full[l["review_id"]]["score_influence"]["rank_global"] == l["d045_number"]


LABEL_FILE_D046 = PACKET / "human_labels_D046.json"


def _all_labelled_ids():
    ids = set()
    for path in sorted(PACKET.glob("human_labels_*.json")):
        ids |= {l["review_id"] for l in _load(path)["labels"]}
    return ids


def test_unlabelled_nodes_have_blank_human_fields(records):
    labelled = _all_labelled_ids()
    for r in records:
        if r["review_id"] in labelled:
            continue
        for key, value in r["human_review"].items():
            if key == "human_prediction_for_each_hypothesis":
                assert all(v is None for v in value.values())
            elif key == "human_secondary_flags":
                assert value == []
            else:
                assert value is None, (r["review_id"], key)


def test_labelled_nodes_carry_exactly_d045_and_nothing_inferred(records):
    labels = {l["review_id"]: l for l in _load(LABEL_FILE)["labels"]}
    seen = 0
    for r in records:
        if r["review_id"] not in labels:
            continue
        seen += 1
        h = r["human_review"]
        category = labels[r["review_id"]]["human_primary_category"]
        assert h["human_primary_category"] == category
        assert h["human_is_genuinely_discriminative"] is (category == "genuine_discriminator")
        assert h["human_silence_as_null_error"] is (category == "silence_as_null_error")
        assert (h["human_reviewer"], h["human_review_source"], h["human_review_status"]) == \
            ("Research Director", "D045", "first_pass_model_based_review")
        for key, value in h.items():
            if key in RECORDED_BY_D045:
                continue
            if key == "human_prediction_for_each_hypothesis":
                assert all(v is None for v in value.values()), r["review_id"]
            elif key == "human_secondary_flags":
                assert value == [], r["review_id"]
            else:
                assert value is None, (r["review_id"], key)
    assert seen == 40


# --------------------------------------------------------------------------- #
# Selection does not depend on the post-hoc auditor
# --------------------------------------------------------------------------- #
def test_selection_is_identical_without_any_auditor_data(extracted, records, monkeypatch):
    monkeypatch.setattr(bp, "attach_audit_metadata", lambda *a, **k: None)
    monkeypatch.setattr(bp, "audit_instability", lambda *a, **k: {})
    monkeypatch.setattr(bp, "review_statistics", lambda *a, **k: {})
    stripped, _, _ = bp.build(extracted / "run", extracted / "supplementary_scratch")
    assert [r["review_id"] for r in stripped] == [r["review_id"] for r in records]
    assert [r["score_influence"]["in_priority_set"] for r in stripped] == \
           [r["score_influence"]["in_priority_set"] for r in records]


# --------------------------------------------------------------------------- #
# Committed packet is current and deterministic
# --------------------------------------------------------------------------- #
def test_committed_packet_matches_a_fresh_build(built, tmp_path):
    records, stats, hidden = built
    bp.write_outputs(records, stats, hidden, tmp_path)
    for name in ("review_set_full.jsonl", "review_set_priority.jsonl", "review_full.md",
                 "review_priority.md", "hidden_case_context.md", "hidden_case_context.json", "stats.json"):
        assert (tmp_path / name).read_bytes() == (PACKET / name).read_bytes(), name


def test_priority_jsonl_is_the_flagged_subset_of_full():
    full = [json.loads(l) for l in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()]
    pri = [json.loads(l) for l in (PACKET / "review_set_priority.jsonl").read_text(encoding="utf-8").splitlines()]
    assert pri == [r for r in full if r["score_influence"]["in_priority_set"]]


# --------------------------------------------------------------------------- #
# D046: extended review with per-hypothesis prediction states
# --------------------------------------------------------------------------- #
def _d046_blocks():
    text = (ROOT / ".agent" / "DECISIONS.md").read_text(encoding="utf-8")
    section = text[text.index("## D046"):]
    section = section[section.index("ADJUDICATION:"):section.index("KEY NEW METHOD DIAGNOSIS")]
    return re.split(r"\n(?=\d+\. `)", section)[1:]


def test_d046_label_file_matches_decisions_independently_parsed():
    """Re-derived here with its own minimal parsing, not the transcription script's,
    so a parser bug cannot pass by agreeing with itself."""
    labels = {l["d046_number"]: l for l in _load(LABEL_FILE_D046)["labels"]}
    blocks = _d046_blocks()
    assert len(blocks) == len(labels) == 12
    for block in blocks:
        number = int(block.split(".", 1)[0])
        label = labels[number]
        assert "`{}`".format(label["d046_key"]) in block.splitlines()[0]
        primary_line = next(l for l in block.splitlines() if l.startswith("Primary category"))
        assert primary_line.split("`")[1] == label["human_primary_category"]
        for line in block.splitlines():
            if line.startswith("- H1") or line.startswith("- H2"):
                hyp = line[2:4]
                first_state = next(tok for tok in line.split("`")[1::2]
                                   if tok in ("positive_or_present", "negative_or_absent",
                                              "substantive_null", "indeterminate"))
                assert label["human_prediction_for_each_hypothesis"][hyp] == first_state, (number, hyp)
                assert label["human_prediction_qualifiers"][hyp]["line_verbatim"] in line


def test_d046_qualified_states_are_exactly_the_hedged_ones():
    qualified = sorted((l["d046_key"], h) for l in _load(LABEL_FILE_D046)["labels"]
                       for h, q in l["human_prediction_qualifiers"].items() if q["qualified"])
    assert qualified == [("forest_fragmentation_resilience-X21", "H1"),
                         ("pfc_interhemispheric_architecture-X23", "H2"),
                         ("spider_orb_web_origin-X17", "H1"),
                         ("spider_orb_web_origin-X24", "H1")]


def test_d046_nodes_were_unlabelled_score_moving_nodes(records):
    d045 = {l["review_id"] for l in _load(LABEL_FILE)["labels"]}
    d046 = {l["review_id"] for l in _load(LABEL_FILE_D046)["labels"]}
    ids = {r["review_id"]: r for r in records}
    assert not (d045 & d046)
    assert d046 <= set(ids)
    assert not any(ids[rid]["score_influence"]["in_priority_set"] for rid in d046)


def test_d046_nodes_carry_recorded_fields_and_nothing_else(records):
    labels = {l["review_id"]: l for l in _load(LABEL_FILE_D046)["labels"]}
    seen = 0
    for r in records:
        if r["review_id"] not in labels:
            continue
        seen += 1
        h, l = r["human_review"], labels[r["review_id"]]
        assert h["human_primary_category"] == l["human_primary_category"]
        assert h["human_secondary_flags"] == l["human_secondary_flags"]
        assert h["human_prediction_for_each_hypothesis"] == l["human_prediction_for_each_hypothesis"]
        assert h["human_prediction_qualifiers"] == l["human_prediction_qualifiers"]
        assert h["human_is_genuinely_discriminative"] is (l["human_primary_category"] == "genuine_discriminator")
        assert h["human_silence_as_null_error"] is ("silence_as_null_error" in
                                                    [l["human_primary_category"]] + l["human_secondary_flags"])
        assert h["human_evidence_relevance"] == l["human_evidence_relevance"]
        assert h["human_confidence"] == l["human_confidence"]
        assert h["human_notes"] == l["human_notes"]
        assert h["human_review_source"] == "D046"
        assert h["human_implication_validity"] is None
    assert seen == 12
