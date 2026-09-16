"""Checks for the BENCH-GRAPH-ATTRIBUTION-001 score attribution.

The attribution turns 40 human labels into claims such as "this case's apparent
success rests on component facts". Those claims are only as good as the
arithmetic, so the arithmetic is tested independently of the code that produced it:

* category buckets add up exactly to each case's frozen log-odds;
* every counterfactual view equals the sum of the categories it keeps;
* node classes and categories agree with the label file and the review packet;
* unreviewed nodes are never labelled;
* the committed outputs equal a fresh build (where the private archive exists).

Most checks read only the committed outputs, so they run on a clean clone.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import pytest

import scripts.analyze_review_attribution as ar

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "benchmark" / "review" / "graph_pilot_001" / "attribution"
OUT_COMBINED = ROOT / "benchmark" / "review" / "graph_pilot_001" / "attribution_d045_d046"
OUT_DIRS = [OUT, OUT_COMBINED]
PACKET = ROOT / "benchmark" / "review" / "graph_pilot_001"
CATS = ar.REVIEWED_CATEGORIES
ALL_BUCKETS = CATS + ["unreviewed_score_moving", "non_moving"]


def _load(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def attribution():
    return _load("case_category_attribution.json")


@pytest.fixture(scope="module")
def views():
    return _load("counterfactual_views.json")


@pytest.fixture(scope="module")
def coverage():
    return _load("coverage.json")


@pytest.fixture(scope="module")
def nodes():
    return [json.loads(l) for l in (OUT / "node_contributions.jsonl").read_text(encoding="utf-8").splitlines()]


def test_analysis_makes_no_llm_calls():
    source = (ROOT / "scripts" / "analyze_review_attribution.py").read_text(encoding="utf-8")
    assert "src.llm" not in source and "complete_json" not in source


# --------------------------------------------------------------------------- #
# Exact decomposition
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("out_dir", OUT_DIRS, ids=["D045", "D045+D046"])
def test_categories_sum_to_frozen_log_odds_all_label_sets(out_dir):
    attribution = json.loads((out_dir / "case_category_attribution.json").read_text(encoding="utf-8"))
    assert len(attribution["cases"]) == 8
    for cid, c in attribution["cases"].items():
        total = sum(c["categories"][k]["log_odds_H2_over_H1"] for k in ALL_BUCKETS)
        assert total == pytest.approx(c["original"]["log_odds_H2_over_H1"], abs=1e-9), cid


@pytest.mark.parametrize("out_dir", OUT_DIRS, ids=["D045", "D045+D046"])
def test_views_equal_kept_categories_all_label_sets(out_dir):
    attribution = json.loads((out_dir / "case_category_attribution.json").read_text(encoding="utf-8"))
    views = json.loads((out_dir / "counterfactual_views.json").read_text(encoding="utf-8"))
    for cid, c in attribution["cases"].items():
        for name, keep in EXPECTED_KEEP.items():
            expected = sum(c["categories"][k]["log_odds_H2_over_H1"] for k in keep)
            got = views["cases"][cid]["views"][name]["evidence_zeroed"]["log_odds_H2_over_H1"]
            assert got == pytest.approx(expected, abs=1e-9), (cid, name)


def test_label_sets_agree_on_frozen_scores_and_non_moving_nodes():
    a = json.loads((OUT / "case_category_attribution.json").read_text(encoding="utf-8"))["cases"]
    b = json.loads((OUT_COMBINED / "case_category_attribution.json").read_text(encoding="utf-8"))["cases"]
    for cid in a:
        assert a[cid]["original"] == b[cid]["original"]
        assert a[cid]["categories"]["non_moving"] == b[cid]["categories"]["non_moving"]
        for k in ("genuine_discriminator", "generic_component_fact"):   # D046 labelled none of these
            assert a[cid]["categories"][k] == b[cid]["categories"][k], (cid, k)


def test_combined_counts_and_labels():
    nodes = [json.loads(l) for l in (OUT_COMBINED / "node_contributions.jsonl").read_text(encoding="utf-8").splitlines()]
    assert Counter(n["node_class"] for n in nodes) == Counter(
        {"reviewed": 52, "unreviewed_score_moving": 26, "non_moving": 114})
    labels = {}
    for name in ("human_labels_D045.json", "human_labels_D046.json"):
        for l in json.loads((PACKET / name).read_text(encoding="utf-8"))["labels"]:
            labels[l["review_id"]] = l["human_primary_category"]
    assert {n["review_id"]: n["human_primary_category"] for n in nodes if n["human_primary_category"]} == labels


def test_one_sided_split_is_rederived_exactly():
    """Recompute the D046 split from the label file and the packet's verifier edges."""
    split = json.loads((OUT_COMBINED / "one_sided_split.json").read_text(encoding="utf-8"))
    packet = {json.loads(l)["review_id"]: json.loads(l)
              for l in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()}
    labels = json.loads((PACKET / "human_labels_D046.json").read_text(encoding="utf-8"))["labels"]
    got = {r["review_id"]: r["one_sided_kind"] for r in split["nodes_with_recorded_states"]}
    assert len(got) == 12
    for l in labels:
        states = l["human_prediction_for_each_hypothesis"]
        silent = [h for h, s in states.items() if s == "indeterminate"]
        det = [h for h, s in states.items() if s != "indeterminate"]
        edges = packet[l["review_id"]]["verifier_graph"]["cross_hypothesis_judgments"]
        if len(det) == 1 and len(silent) == 1:
            want = ("neutral_mapping_pseudo_discrimination" if edges[silent[0]]["direct_edge_label"] == "neutral"
                    else "categorical_silence_error")
        elif not det:
            want = "all_indeterminate"
        elif not silent and len({states[h] for h in det}) == 1:
            want = "shared_determinate"
        else:
            want = "determinate_contrast"
        assert got[l["review_id"]] == want, l["review_id"]


def test_neutral_edge_proxy_is_rederived():
    split = json.loads((OUT_COMBINED / "one_sided_split.json").read_text(encoding="utf-8"))
    packet = [json.loads(l) for l in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()]
    hits = [r for r in packet if all(v["direct_edge_label"] == "neutral"
                                     for v in r["verifier_graph"]["cross_hypothesis_judgments"].values()
                                     if not v["is_origin_of_proposition"])]
    proxy = split["verifier_proxy_non_origin_neutral_score_moving"]
    assert proxy["n_nodes"] == len(hits)
    assert proxy["absolute_influence"] == pytest.approx(sum(r["score_influence"]["absolute_influence"] for r in hits),
                                                         abs=1e-5)


def test_categories_sum_to_frozen_log_odds(attribution):
    assert len(attribution["cases"]) == 8
    for cid, c in attribution["cases"].items():
        total = sum(c["categories"][k]["log_odds_H2_over_H1"] for k in ALL_BUCKETS)
        assert total == pytest.approx(c["original"]["log_odds_H2_over_H1"], abs=1e-9), cid
        frozen = math.log(c["original"]["scores"]["H2"] / c["original"]["scores"]["H1"])
        assert c["original"]["log_odds_H2_over_H1"] == pytest.approx(frozen, abs=1e-6), cid


def test_non_moving_nodes_contribute_nothing_to_log_odds(attribution):
    for cid, c in attribution["cases"].items():
        assert abs(c["categories"]["non_moving"]["log_odds_H2_over_H1"]) < 1e-6, cid


def test_node_table_sums_to_category_buckets(attribution, nodes):
    for cid, c in attribution["cases"].items():
        for key in ALL_BUCKETS:
            if key in CATS:
                members = [n for n in nodes if n["case_id"] == cid and n["human_primary_category"] == key]
            else:
                members = [n for n in nodes if n["case_id"] == cid and n["node_class"] == key]
            assert len(members) == c["categories"][key]["n_nodes"], (cid, key)
            assert sum(n["log_odds_H2_over_H1"] for n in members) == pytest.approx(
                c["categories"][key]["log_odds_H2_over_H1"], abs=1e-9), (cid, key)


# --------------------------------------------------------------------------- #
# Views are exactly the categories they keep
# --------------------------------------------------------------------------- #
EXPECTED_KEEP = {
    "original": set(ALL_BUCKETS),
    "A1_genuine_reviewed_plus_unreviewed": {"genuine_discriminator", "unreviewed_score_moving", "non_moving"},
    "A2_genuine_reviewed_only": {"genuine_discriminator", "non_moving"},
    "B1_remove_confirmed_errors": {"genuine_discriminator", "generic_component_fact",
                                   "compatible_non_discriminative", "unreviewed_score_moving", "non_moving"},
    "B2_remove_confirmed_errors_reviewed_only": {"genuine_discriminator", "generic_component_fact",
                                                 "compatible_non_discriminative", "non_moving"},
    "R_unreviewed_only": {"unreviewed_score_moving", "non_moving"},
}


def test_every_view_equals_the_sum_of_kept_categories(attribution, views):
    assert set(views["views"]) == set(EXPECTED_KEEP)
    for cid, c in attribution["cases"].items():
        for name, keep in EXPECTED_KEEP.items():
            expected = sum(c["categories"][k]["log_odds_H2_over_H1"] for k in keep)
            got = views["cases"][cid]["views"][name]["evidence_zeroed"]["log_odds_H2_over_H1"]
            assert got == pytest.approx(expected, abs=1e-9), (cid, name)


def test_confirmed_errors_are_exactly_the_three_named_categories():
    assert ar.CONFIRMED_ERRORS == {"silence_as_null_error", "evidence_construct_mismatch",
                                   "invalid_or_weak_implication"}


def test_view_scores_tops_and_relations_are_consistent(views):
    for cid, c in views["cases"].items():
        favoured = c["later_resolution_favours"]
        for name, v in c["views"].items():
            for part in ("evidence_zeroed", "graph_deleted_sensitivity"):
                z = v[part]
                lo = z["log_odds_H2_over_H1"]
                assert z["scores"]["H2"] == pytest.approx(1 / (1 + math.exp(-lo)), abs=1e-12)
                assert z["top"] == ("tie" if abs(lo) <= ar.TIE_TOL else ("H2" if lo > 0 else "H1"))
                if favoured is None:
                    assert z["relation_to_later_resolution"] == "not_applicable_non_directional_resolution"
                elif z["top"] == "tie":
                    assert z["relation_to_later_resolution"] == "no_ordering"
                else:
                    assert z["relation_to_later_resolution"] == ("agrees" if z["top"] == favoured else "opposes")


def test_original_graph_deleted_equals_evidence_zeroed(views):
    """Removing nothing must not change anything under either decomposition."""
    for cid, c in views["cases"].items():
        o = c["views"]["original"]
        assert o["graph_deleted_sensitivity"]["log_odds_H2_over_H1"] == pytest.approx(
            o["evidence_zeroed"]["log_odds_H2_over_H1"], abs=1e-9), cid


def test_non_directional_cases_are_never_scored_as_agreement(views):
    non_directional = {"forest_fragmentation_resilience", "gcn4_med15_complex_vs_condensate",
                       "pfc_interhemispheric_architecture", "spider_orb_web_origin"}
    for cid in non_directional:
        assert views["cases"][cid]["later_resolution_favours"] is None
    assert set(ar.FAVOURED) == set(views["cases"]) - non_directional
    assert set(ar.FAVOURED.values()) == {"H2"}


# --------------------------------------------------------------------------- #
# Labels, classes and coverage
# --------------------------------------------------------------------------- #
def test_node_categories_match_the_label_file_exactly(nodes):
    labels = {l["review_id"]: l["human_primary_category"]
              for l in json.loads((PACKET / "human_labels_D045.json").read_text(encoding="utf-8"))["labels"]}
    labelled = {n["review_id"]: n["human_primary_category"] for n in nodes if n["human_primary_category"]}
    assert labelled == labels
    assert all(n["node_class"] == "reviewed" for n in nodes if n["human_primary_category"])
    assert all(n["human_primary_category"] is None for n in nodes if n["node_class"] != "reviewed")
    assert Counter(labels.values())["genuine_discriminator"] == 4


def test_node_classes_match_the_review_packet(nodes):
    packet = {json.loads(l)["review_id"]: json.loads(l)
              for l in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()}
    moving = {n["review_id"] for n in nodes if n["node_class"] != "non_moving"}
    assert moving == set(packet)
    for n in nodes:
        if n["review_id"] in packet:
            assert (n["node_class"] == "reviewed") == packet[n["review_id"]]["score_influence"]["in_priority_set"]
    assert len(nodes) == 192
    assert Counter(n["node_class"] for n in nodes) == Counter(
        {"reviewed": 40, "unreviewed_score_moving": 38, "non_moving": 114})


def test_coverage_is_consistent(coverage, nodes, attribution):
    moving = [n for n in nodes if n["node_class"] != "non_moving"]
    total = sum(n["absolute_influence"] for n in moving)
    reviewed = sum(n["absolute_influence"] for n in moving if n["node_class"] == "reviewed")
    assert coverage["total_absolute_influence"] == pytest.approx(total)
    assert coverage["reviewed_absolute_influence"] == pytest.approx(reviewed)
    assert coverage["reviewed_share"] == pytest.approx(reviewed / total)
    assert (coverage["reviewed_nodes"], coverage["unreviewed_nodes"]) == (40, 38)
    batch = coverage["recommended_next_review_batch"]
    queued = batch["first_low_coverage_cases"] + batch["then_remaining_by_influence"]
    assert sorted(queued) == sorted(n["review_id"] for n in nodes if n["node_class"] == "unreviewed_score_moving")
    low = {"fly_wing_constraint_vs_selection", "pfc_interhemispheric_architecture", "spider_orb_web_origin"}
    assert all(any(rid.startswith("GP1-{}-".format(c)) for c in low) for rid in batch["first_low_coverage_cases"])


def test_report_states_the_labels_are_not_expert_ground_truth():
    report = (OUT / "ATTRIBUTION_REPORT.md").read_text(encoding="utf-8")
    assert "not external expert ground truth" in report
    assert "no fix is proposed" in report.lower()


# --------------------------------------------------------------------------- #
# Freshness against the private archive
# --------------------------------------------------------------------------- #
def test_committed_outputs_match_a_fresh_build(tmp_path, monkeypatch):
    import scripts.build_review_packet as bp

    if not bp.ARCHIVE.exists():
        pytest.skip("private pilot archive not present (see benchmark/frozen_runs/pilot_explanatory_001/PROVENANCE.md)")
    monkeypatch.setattr(ar, "OUT", tmp_path / "d045")
    monkeypatch.setattr(ar, "OUT_COMBINED", tmp_path / "combined")
    (tmp_path / "d045").mkdir()
    # the combined report reads the D045 outputs for its before/after columns
    for name in ("coverage.json", "case_category_attribution.json"):
        (tmp_path / "d045" / name).write_bytes((OUT / name).read_bytes())
    assert ar.main() == 0
    for name in ("node_contributions.jsonl", "case_category_attribution.json", "counterfactual_views.json",
                 "coverage.json", "ATTRIBUTION_REPORT.md"):
        assert (tmp_path / "d045" / name).read_bytes() == (OUT / name).read_bytes(), name
    for name in ("node_contributions.jsonl", "case_category_attribution.json", "counterfactual_views.json",
                 "coverage.json", "one_sided_split.json", "ATTRIBUTION_REPORT.md"):
        assert (tmp_path / "combined" / name).read_bytes() == (OUT_COMBINED / name).read_bytes(), name
