"""Ranking metrics (IMPLEMENTATION_SPEC.md §25)."""

from __future__ import annotations

import pytest

from src.benchmark.loader import load_instances
from src.experiments.metrics import (
    aggregate_metrics,
    competition_ranks,
    instance_metrics,
    pair_metrics,
    ranking_from_scores,
)


def _instance(k):
    """A k-candidate instance with gold = H0, for metrics that depend only on k."""
    from src.benchmark.loader import BenchmarkInstance, Hypothesis

    hypotheses = [
        Hypothesis(id="H%d" % i, text="candidate %d" % i, gold=(i == 0), source_index=i)
        for i in range(k)
    ]
    return BenchmarkInstance(id="T%d" % k, researchbench_sample_id="rb-%d" % k,
                             question="q", hypotheses=hypotheses, source_doi="10.0/x")


@pytest.fixture
def instance(config):
    return load_instances(config, instance_ids=["RBV-01"])[0]


def test_competition_ranks_share_the_best_rank_on_ties():
    ranks = competition_ranks({"a": 10.0, "b": 10.0, "c": 5.0})
    assert ranks == {"a": 1, "b": 1, "c": 3}


def test_ranking_is_deterministic_under_ties():
    scores = {"a": 1.0, "b": 1.0, "c": 2.0}
    assert ranking_from_scores(scores, order=["b", "a", "c"]) == ["c", "b", "a"]
    assert ranking_from_scores(scores, order=["a", "b", "c"]) == ["c", "a", "b"]


def test_gold_first_gives_perfect_scores(instance):
    scores = {h.id: 10.0 for h in instance.hypotheses}
    scores[instance.gold_hypothesis.id] = 99.0
    row = instance_metrics(instance, scores)
    assert row["gold_rank"] == 1
    assert row["top1_strict"] == 1.0
    assert row["reciprocal_rank"] == 1.0
    assert row["pairwise_accuracy_all_negatives"] == 1.0
    assert row["tied_with_gold"] == 0


def test_gold_last_gives_worst_scores(instance):
    scores = {h.id: 10.0 + i for i, h in enumerate(instance.hypotheses)}
    scores[instance.gold_hypothesis.id] = 0.0
    row = instance_metrics(instance, scores)
    assert row["gold_rank"] == len(instance.hypotheses)
    assert row["top1_strict"] == 0.0
    assert row["pairwise_accuracy_all_negatives"] == 0.0
    assert row["reciprocal_rank"] == pytest.approx(1.0 / len(instance.hypotheses))


def test_ties_are_reported_not_hidden(instance):
    """An all-tie judgment must not count as a win."""
    scores = {h.id: 50.0 for h in instance.hypotheses}
    row = instance_metrics(instance, scores)
    assert row["gold_rank"] == 1
    assert row["top1_strict"] == 0.0
    assert row["top1_tie_aware"] == pytest.approx(1.0 / len(instance.hypotheses))
    assert row["pairwise_accuracy_all_negatives"] == 0.5
    assert row["tied_with_gold"] == len(instance.hypotheses) - 1


def test_unscored_instances_are_marked_and_excluded_from_aggregates(instance):
    row = instance_metrics(instance, {})
    assert row["scored"] is False
    assert row["gold_rank"] is None

    good = instance_metrics(instance, {h.id: (100.0 if h.gold else 1.0) for h in instance.hypotheses})
    summary = aggregate_metrics([row, good])
    assert summary["n_instances"] == 2
    assert summary["n_scored"] == 1
    assert summary["n_unscored"] == 1
    assert summary["top1_accuracy"] == 1.0
    assert summary["mrr"] == 1.0


def test_diagnostics_are_aggregated(instance):
    rows = [
        instance_metrics(instance, {h.id: 1.0 for h in instance.hypotheses},
                         diagnostics={"n_queries": 4, "n_eligible_papers": 10}),
        instance_metrics(instance, {h.id: 1.0 for h in instance.hypotheses},
                         diagnostics={"n_queries": 6, "n_eligible_papers": 0}),
    ]
    summary = aggregate_metrics(rows)
    assert summary["total_n_queries"] == 10
    assert summary["mean_n_eligible_papers"] == 5.0


def test_missing_gold_score_is_unscored(instance):
    scores = {h.id: 1.0 for h in instance.hypotheses if not h.gold}
    assert instance_metrics(instance, scores)["scored"] is False


# --------------------------------------------------------------------------- #
# Frozen pairs are the primary evaluation unit
# --------------------------------------------------------------------------- #
def test_pair_accuracy_counts_only_frozen_pairs(instance):
    """Unscreened negatives must not influence the primary metric."""
    gold = instance.gold_hypothesis.id
    scores = {h.id: 10.0 for h in instance.hypotheses}
    scores[gold] = 50.0
    scores["H1"] = 90.0  # a frozen pair the method loses
    scores["H9"] = 99.0  # not in the frozen subset: must be ignored

    row = pair_metrics(instance, scores, ["H1", "H2", "H3"])
    assert row["n_pairs_frozen"] == 3
    assert row["pair_wins"] == 2 and row["pair_ties"] == 0
    assert row["pair_accuracy"] == pytest.approx(2 / 3)


def test_pair_ties_score_half(instance):
    gold = instance.gold_hypothesis.id
    scores = {h.id: 0.0 for h in instance.hypotheses}  # every label `no_evidence`
    row = pair_metrics(instance, scores, ["H1", "H2"])
    assert row["pair_ties"] == 2
    assert row["pair_accuracy"] == 0.5


def test_pair_metrics_absent_without_a_frozen_subset(instance):
    scores = {h.id: 1.0 for h in instance.hypotheses}
    row = instance_metrics(instance, scores)
    assert "pair_accuracy" not in row
    summary = aggregate_metrics([row])
    assert summary["primary_metric"] == "pair_accuracy"
    assert summary["pair_accuracy"] is None
    assert summary["n_pairs_evaluated"] == 0


def test_pair_accuracy_is_micro_averaged_over_pairs(instance):
    gold = instance.gold_hypothesis.id
    good = {h.id: (100.0 if h.gold else 1.0) for h in instance.hypotheses}
    bad = {h.id: (0.0 if h.gold else 1.0) for h in instance.hypotheses}
    rows = [
        instance_metrics(instance, good, pair_negative_ids=["H1", "H2", "H3", "H4"]),
        instance_metrics(instance, bad, pair_negative_ids=["H5"]),
    ]
    summary = aggregate_metrics(rows)
    assert summary["n_pairs_evaluated"] == 5
    assert summary["pair_accuracy"] == pytest.approx(4 / 5)      # micro
    assert summary["pair_accuracy_macro"] == pytest.approx(0.5)  # macro


# --------------------------------------------------------------------------- #
# Comparing across candidate-set sizes
# --------------------------------------------------------------------------- #
def test_normalised_gold_rank_is_comparable_across_k():
    """1.0 for first and 0.0 for last, whatever k is.

    Top-1 and MRR both have a chance baseline that moves with k (1/k), so they
    cannot be averaged over mixed candidate-set sizes. This can.
    """
    from src.experiments.metrics import instance_metrics

    for k in (2, 3, 5, 11):
        best = {"H0": 1.0}
        worst = {"H0": 0.0}
        for i in range(1, k):
            best["H%d" % i] = 0.0
            worst["H%d" % i] = 1.0
        first = instance_metrics(_instance(k), best)
        last = instance_metrics(_instance(k), worst)
        assert first["gold_rank_normalised"] == pytest.approx(1.0), "k=%d" % k
        assert last["gold_rank_normalised"] == pytest.approx(0.0), "k=%d" % k


def test_a_middle_rank_normalises_to_the_midpoint():
    from src.experiments.metrics import instance_metrics

    # k=5, gold third: (1 - (3-1)/(5-1)) = 0.5
    scores = {"H0": 0.5, "H1": 0.9, "H2": 0.8, "H3": 0.2, "H4": 0.1}
    row = instance_metrics(_instance(5), scores)
    assert row["gold_rank"] == 3
    assert row["gold_rank_normalised"] == pytest.approx(0.5)


def test_pairwise_win_rate_scores_ties_as_half():
    from src.experiments.metrics import instance_metrics

    scores = {"H0": 0.5, "H1": 0.4, "H2": 0.5, "H3": 0.9}
    row = instance_metrics(_instance(4), scores)
    # one win, one tie, one loss over three negatives -> (1 + 0.5) / 3
    assert row["pairwise_accuracy_all_negatives"] == pytest.approx(0.5)


def test_listwise_metrics_are_stratified_by_k_and_carry_their_chance_baseline():
    """Averaging top-1 over mixed k is the mistake this guards against."""
    from src.experiments.metrics import aggregate_metrics, instance_metrics

    rows = [
        instance_metrics(_instance(2), {"H0": 1.0, "H1": 0.0}),
        instance_metrics(_instance(5), {"H0": 0.0, "H1": 1.0, "H2": 0.9,
                                        "H3": 0.8, "H4": 0.7}),
    ]
    summary = aggregate_metrics(rows)
    by_k = {entry["k"]: entry for entry in summary["by_k"]}
    assert set(by_k) == {2, 5}
    assert by_k[2]["chance_top1"] == pytest.approx(0.5)
    assert by_k[5]["chance_top1"] == pytest.approx(0.2)
    assert by_k[2]["top1_accuracy_tie_aware"] == pytest.approx(1.0)
    assert by_k[5]["top1_accuracy_tie_aware"] == pytest.approx(0.0)
    # The pooled figure that IS comparable across k is reported too.
    assert summary["gold_rank_normalised"] == pytest.approx((1.0 + 0.0) / 2)


# --------------------------------------------------------------------------- #
# Abstention decomposition (DECISIONS #33)
# --------------------------------------------------------------------------- #
def test_coverage_and_selective_accuracy_decompose_overall_accuracy():
    """overall = coverage x selective + (1 - coverage) x 0.5

    The identity is the point: a forced tie on a row where nothing was found is
    not a 50%-correct answer, it is an abstention, and folding it into accuracy
    hid that the broad assessor was at chance whenever it did speak.
    """
    rows = [
        # three rows with discriminative evidence: 2 correct, 1 wrong
        {"scored": True, "score_spread": 0.4, "pair_accuracy": 1.0,
         "n_pairs_scored": 1, "pair_credit": 1.0},
        {"scored": True, "score_spread": 0.2, "pair_accuracy": 1.0,
         "n_pairs_scored": 1, "pair_credit": 1.0},
        {"scored": True, "score_spread": 0.1, "pair_accuracy": 0.0,
         "n_pairs_scored": 1, "pair_credit": 0.0},
        # one row where the posterior never moved -> forced tie
        {"scored": True, "score_spread": 0.0, "pair_accuracy": 0.5,
         "n_pairs_scored": 1, "pair_credit": 0.5},
    ]
    summary = aggregate_metrics(rows)
    assert summary["n_rows_with_discriminative_evidence"] == 3
    assert summary["coverage"] == pytest.approx(0.75)
    assert summary["selective_pair_accuracy"] == pytest.approx(2 / 3)
    identity = (summary["coverage"] * summary["selective_pair_accuracy"]
                + (1 - summary["coverage"]) * 0.5)
    assert summary["pair_accuracy"] == pytest.approx(identity)


def test_a_row_where_every_candidate_scores_alike_is_marked_abstained():
    from src.experiments.metrics import instance_metrics

    row = instance_metrics(_instance(2), {"H0": 0.5, "H1": 0.5})
    assert row["score_spread"] == pytest.approx(0.0)
    assert row["abstained"] is True
    moved = instance_metrics(_instance(2), {"H0": 0.7, "H1": 0.3})
    assert moved["abstained"] is False


def test_coverage_is_about_discriminative_evidence_not_merely_informative():
    """A node every candidate predicts equally is informative and still inert.

    So coverage is keyed on the posterior having moved, not on the assessor having
    returned a label.
    """
    rows = [{"scored": True, "score_spread": 0.0, "pair_accuracy": 0.5,
             "n_pairs_scored": 1, "pair_credit": 0.5,
             "n_informative_assessments": 12}]
    summary = aggregate_metrics(rows)
    assert summary["coverage"] == pytest.approx(0.0), (
        "12 informative nodes that moved nothing must not count as coverage"
    )
