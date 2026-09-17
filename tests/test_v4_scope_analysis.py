"""Deterministic pieces of scripts/analyze_v4_scope.py (BENCH-GRAPH-V4-SCOPE-001)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_v4_scope as a  # noqa: E402


def _rec(scope="hypothesis_specific", label="support", element=True, has_contrast=True, relevance="contrast_direct",
         eligible=True):
    return {"scope": {"scope": scope} if scope else None, "evidence_label": label,
            "contrast_element": {"has_contrast": has_contrast} if element else None,
            "contrast_relevance": {"contrast_relevance": relevance} if relevance else None,
            "comparatively_eligible": eligible}


@pytest.mark.parametrize("rec,column", [
    (_rec(label=None), "no_evidence_assessment"),
    (_rec(label="no_evidence"), "no_evidence"),
    (_rec(label="mixed"), "mixed"),
    (_rec(element=False, relevance=None), "element_unavailable"),
    (_rec(has_contrast=False), "contrast_direct"),          # relevance shown whatever has_contrast is
    (_rec(relevance=None), "relevance_unavailable"),
    (_rec(relevance="context_only"), "context_only"),
    (_rec(relevance="no_evidence"), "relevance_no_evidence"),
    (_rec(), "contrast_direct"),
])
def test_evidence_column(rec, column):
    assert a.evidence_column(rec) == column


def test_scope_x_evidence_counts_and_rates():
    nodes = {"1": _rec(), "2": _rec(relevance="contrast_partial"), "3": _rec(label="no_evidence"),
             "4": _rec(scope="broader_class_fact"), "5": _rec(scope="possibility_claim", relevance="context_only"),
             "6": _rec(scope="broader_class_fact", label="no_evidence", eligible=False)}
    table = a.scope_x_evidence(nodes)
    row = table["rows"]["hypothesis_specific"]
    assert (row["n"], row["contrast_direct"], row["contrast_partial"], row["no_evidence"]) == (3, 1, 1, 1)
    assert row["p_informative_evidence"] == pytest.approx(2 / 3)
    assert row["p_contrast_direct_given_informative"] == pytest.approx(1 / 2)
    broad = table["broad_(class_fact_or_possibility)"]
    assert (broad["n"], broad["p_contrast_direct"]) == (3, pytest.approx(1 / 3))
    assert a.scope_x_evidence(nodes, lambda r: r["comparatively_eligible"])["rows"]["broader_class_fact"]["n"] == 1


def test_composition_shares_sum_to_one_and_unreviewed_is_separate():
    labels = {"a": {"human_primary_category": "genuine_discriminator"},
              "b": {"human_primary_category": "generic_component_fact"}}
    comp = a.composition({"a": 1.0, "b": 3.0, "c": 4.0}, labels)
    assert comp["total_absolute_influence"] == 8.0
    assert comp["genuine_discriminator"]["share"] == 0.125 and comp["unreviewed"]["share"] == 0.5
    assert sum(v["share"] for k, v in comp.items() if k != "total_absolute_influence") == pytest.approx(1.0)
    assert a.composition({"a": 0.0}, labels)["genuine_discriminator"]["share"] is None
