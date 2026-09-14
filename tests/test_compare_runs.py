"""The comparison utility must recompute, not copy, aggregate metrics.

A 5-instance smoke run and a 20-instance run have incomparable headline numbers;
the table is only meaningful if every row is recomputed over the same instances.
"""

from __future__ import annotations

import sys

import pytest

sys.path.insert(0, "scripts")
from compare_runs import restrict  # noqa: E402


def row(instance_id, *, pair_credit, n_pairs, gold_rank=1, scored=True):
    return {
        "instance_id": instance_id,
        "scored": scored,
        "pair_accuracy": (pair_credit / n_pairs) if n_pairs else None,
        "pair_credit": pair_credit,
        "n_pairs_scored": n_pairs,
        "gold_rank": gold_rank,
        "reciprocal_rank": 1.0 / gold_rank,
        "top1_strict": 1.0 if gold_rank == 1 else 0.0,
    }


@pytest.fixture
def run():
    return {
        "rows": {
            "A": row("A", pair_credit=4, n_pairs=4),        # perfect, 4 pairs
            "B": row("B", pair_credit=0, n_pairs=6, gold_rank=9),  # lost all 6
            "C": row("C", pair_credit=1, n_pairs=2, gold_rank=3),
        }
    }


def test_restriction_changes_the_number(run):
    """The whole point: a subset is scored on the subset."""
    everything = restrict(run, ["A", "B", "C"])
    assert everything["n_pairs"] == 12
    assert everything["pair_accuracy"] == pytest.approx(5 / 12)

    subset = restrict(run, ["A"])
    assert subset["n_pairs"] == 4
    assert subset["pair_accuracy"] == 1.0


def test_pair_accuracy_is_micro_averaged_not_a_mean_of_means(run):
    """B has more pairs than A, so it must weigh more than a per-instance mean."""
    micro = restrict(run, ["A", "B"])["pair_accuracy"]
    macro = (1.0 + 0.0) / 2
    assert micro == pytest.approx(4 / 10)
    assert micro != pytest.approx(macro)


def test_missing_instances_are_skipped_not_zero_filled(run):
    out = restrict(run, ["A", "NOT-PRESENT"])
    assert out["n_instances"] == 1
    assert out["pair_accuracy"] == 1.0


def test_unscored_rows_do_not_drag_the_average(run):
    run["rows"]["D"] = row("D", pair_credit=0, n_pairs=0, scored=False)
    run["rows"]["D"]["pair_accuracy"] = None
    out = restrict(run, ["A", "D"])
    assert out["n_scored"] == 1
    assert out["pair_accuracy"] == 1.0, "an unscored instance is absent, not a zero"
