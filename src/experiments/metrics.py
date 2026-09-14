"""Ranking metrics (IMPLEMENTATION_SPEC.md §25).

The **primary** metric is accuracy over the frozen gold-vs-negative pair subset
(`benchmark/dev/pairs_v1.jsonl`): every pair there was screened to be a genuine
scientific disagreement about the same target. Listwise metrics (top-1, MRR,
mean gold rank) are reported as **secondary**, because a listwise ranking over
all eleven candidates mixes screened disagreements with unscreened candidates
that may simply answer a different question.

Tie handling is explicit, because a holistic judge frequently returns identical
scores for several candidates and silently breaking ties would flatter the
method:

* ranks are *competition* ranks — rank = 1 + (number of strictly better scores),
  so three candidates tied at the top all have rank 1;
* `top1_strict` requires the gold hypothesis to be strictly above every other
  candidate; `top1_tie_aware` gives partial credit 1/m when the gold is in an
  m-way tie for the lead. Both are reported;
* pairwise accuracy scores a tie as 0.5.

Results on the 20-case development slice are diagnostics, not benchmark
performance (§25).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence

from src.benchmark.loader import BenchmarkInstance


def competition_ranks(scores: Dict[str, float]) -> Dict[str, int]:
    """hypothesis_id -> 1-based rank, ties sharing the best rank."""
    ranks: Dict[str, int] = {}
    for key, value in scores.items():
        better = sum(1 for other in scores.values() if other > value)
        ranks[key] = better + 1
    return ranks


def ranking_from_scores(scores: Dict[str, float], *, order: Optional[Sequence[str]] = None) -> List[str]:
    """Descending ranking. Ties are broken by `order` (presentation order) so
    the result is deterministic without favouring any particular hypothesis id."""
    position = {key: index for index, key in enumerate(order or sorted(scores))}
    return sorted(scores, key=lambda key: (-scores[key], position.get(key, len(position))))


def pair_metrics(
    instance: BenchmarkInstance,
    scores: Dict[str, float],
    negative_ids: Sequence[str],
    *,
    pair_status: str = "evaluable",
) -> Dict[str, Any]:
    """Accuracy over the frozen pairs for one instance.

    A tie scores 0.5: under the primary `ordinal_map` rule, two hypotheses with
    the same evidence label genuinely tie, and breaking the tie would invent a
    preference the method did not express.
    """
    gold_id = instance.gold_hypothesis.id
    usable = [n for n in negative_ids if n in scores]
    out: Dict[str, Any] = {
        "pair_status": pair_status if negative_ids else "no_evaluable_pair",
        "n_pairs_frozen": len(negative_ids),
        "n_pairs_scored": len(usable),
    }
    if gold_id not in scores or not usable:
        out.update({"pair_wins": None, "pair_ties": None, "pair_credit": None, "pair_accuracy": None})
        return out

    gold_score = scores[gold_id]
    wins = sum(1 for n in usable if gold_score > scores[n])
    ties = sum(1 for n in usable if gold_score == scores[n])
    credit = wins + 0.5 * ties
    out.update(
        {
            "pair_wins": wins,
            "pair_ties": ties,
            "pair_credit": credit,
            "pair_accuracy": credit / len(usable),
        }
    )
    return out


def instance_metrics(
    instance: BenchmarkInstance,
    scores: Dict[str, float],
    *,
    diagnostics: Optional[Dict[str, Any]] = None,
    pair_negative_ids: Optional[Sequence[str]] = None,
    pair_status: str = "evaluable",
) -> Dict[str, Any]:
    gold_id = instance.gold_hypothesis.id
    out: Dict[str, Any] = {
        "instance_id": instance.id,
        "n_hypotheses": len(instance.hypotheses),
        "gold_id": gold_id,
        "scores": dict(scores),
    }
    out.update(diagnostics or {})
    if pair_negative_ids is not None:
        out.update(pair_metrics(instance, scores, pair_negative_ids, pair_status=pair_status))

    if not scores or gold_id not in scores:
        out.update(
            {
                "scored": False,
                "gold_rank": None,
                "reciprocal_rank": None,
                "top1_strict": None,
                "top1_tie_aware": None,
                "pairwise_accuracy_all_negatives": None,
                "tied_with_gold": None,
            }
        )
        return out

    ranks = competition_ranks(scores)
    gold_score = scores[gold_id]
    others = [value for key, value in scores.items() if key != gold_id]
    tied = sum(1 for value in others if value == gold_score)
    gold_rank = ranks[gold_id]

    wins = sum(1 for value in others if gold_score > value)
    draws = sum(1 for value in others if gold_score == value)
    pairwise = (wins + 0.5 * draws) / len(others) if others else None

    # Spread of the posterior. Exactly 0 means no node carried discriminative
    # evidence and every candidate scored identically -- the method abstained in
    # all but name. `coverage` in the aggregate is built on this.
    ordered = sorted(scores.values(), reverse=True)
    score_spread = ordered[0] - ordered[-1] if len(ordered) > 1 else None

    # Normalised gold rank: 1.0 when gold is first, 0.0 when last, whatever k is.
    # Top-1 and MRR both move with k on their own (chance top-1 is 1/k), so they
    # cannot be averaged across candidate-set sizes; this can.
    k = len(scores)
    rank_normalised = (1.0 - (gold_rank - 1) / (k - 1)) if k > 1 else None

    out.update(
        {
            "scored": True,
            "n_candidates_scored": k,
            "score_spread": score_spread,
            "abstained": bool(score_spread == 0),
            "gold_rank": gold_rank,
            "gold_rank_normalised": rank_normalised,
            "reciprocal_rank": 1.0 / gold_rank,
            "top1_strict": 1.0 if gold_rank == 1 and tied == 0 else 0.0,
            "top1_tie_aware": (1.0 / (tied + 1)) if gold_rank == 1 else 0.0,
            # (1/(k-1)) * sum_j 1[S(H+) > S(Hj-)], ties at 0.5. Interpretable
            # across k in a way top-1 is not: chance is 0.5 for every k.
            "pairwise_accuracy_all_negatives": pairwise,
            "tied_with_gold": tied,
        }
    )
    return out


def _mean(values: Iterable[Optional[float]]) -> Optional[float]:
    kept = [float(v) for v in values if v is not None]
    return sum(kept) / len(kept) if kept else None


def aggregate_metrics(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    scored = [row for row in rows if row.get("scored")]
    with_pairs = [row for row in scored if row.get("pair_accuracy") is not None]
    total_pairs = sum(int(row.get("n_pairs_scored") or 0) for row in with_pairs)
    total_credit = sum(float(row.get("pair_credit") or 0.0) for row in with_pairs)

    summary: Dict[str, Any] = {
        "primary_metric": "pair_accuracy",
        "n_instances": len(rows),
        "n_scored": len(scored),
        "n_unscored": len(rows) - len(scored),
        # --- abstention decomposition (DECISIONS #33) ---
        # A method that has no discriminative evidence on a row should be seen to
        # say so, rather than having a forced 0.5 tie folded invisibly into
        # accuracy. Measured on 20 held-out rows, the broad assessor had HIGHER
        # coverage (0.65 vs 0.60) and yet was at chance when it spoke (0.538 vs
        # 0.667) -- the aggregate hid that completely.
        #
        #   overall = coverage * selective_accuracy + (1 - coverage) * 0.5
        #
        "coverage": None,
        "selective_pair_accuracy": None,
        "n_rows_with_discriminative_evidence": None,
        # --- primary: frozen gold-vs-negative pairs ---
        "pair_accuracy": (total_credit / total_pairs) if total_pairs else None,
        "pair_accuracy_macro": _mean(row.get("pair_accuracy") for row in with_pairs),
        "n_pairs_evaluated": total_pairs,
        "n_instances_with_pairs": len(with_pairs),
        # Instances the pair audit found to have no genuine disagreement at all.
        # They are excluded from the primary metric by construction, never
        # silently averaged in.
        "n_instances_no_evaluable_pair": sum(
            1 for row in rows if row.get("pair_status") == "no_evaluable_pair"
        ),
        "instances_no_evaluable_pair": [
            row["instance_id"] for row in rows if row.get("pair_status") == "no_evaluable_pair"
        ],
        # --- secondary: listwise over the full candidate set ---
        "top1_accuracy": _mean(row.get("top1_strict") for row in scored),
        "top1_accuracy_tie_aware": _mean(row.get("top1_tie_aware") for row in scored),
        "mean_gold_rank": _mean(row.get("gold_rank") for row in scored),
        "mrr": _mean(row.get("reciprocal_rank") for row in scored),
        "pairwise_accuracy_all_negatives": _mean(
            row.get("pairwise_accuracy_all_negatives") for row in scored
        ),
        "mean_n_hypotheses": _mean(row.get("n_hypotheses") for row in rows),
        # Chance-normalised, so it is meaningful pooled across candidate-set sizes.
        "gold_rank_normalised": _mean(row.get("gold_rank_normalised") for row in scored),
    }

    # Listwise metrics stratified by k. Top-1 and MRR have a k-dependent chance
    # baseline (1/k), so a single pooled number over mixed k is uninterpretable;
    # `by_k` is where those belong, and the pooled entries above are limited to
    # metrics whose chance level does not move with k.
    by_k: Dict[int, List[Dict[str, Any]]] = {}
    for row in scored:
        k = row.get("n_candidates_scored") or row.get("n_hypotheses")
        if k:
            by_k.setdefault(int(k), []).append(row)
    summary["by_k"] = [
        {
            "k": k,
            "n_instances": len(group),
            "chance_top1": round(1.0 / k, 4),
            "top1_accuracy_tie_aware": _mean(r.get("top1_tie_aware") for r in group),
            "mrr": _mean(r.get("reciprocal_rank") for r in group),
            "mean_gold_rank": _mean(r.get("gold_rank") for r in group),
            "gold_rank_normalised": _mean(r.get("gold_rank_normalised") for r in group),
            "pairwise_win_rate": _mean(
                r.get("pairwise_accuracy_all_negatives") for r in group),
        }
        for k, group in sorted(by_k.items())
    ]

    # Coverage is about DISCRIMINATIVE evidence, not merely informative evidence: a
    # node every candidate predicts equally is informative and still moves no
    # ranking. `score_spread` is 0 exactly when the posterior never moved.
    spread_known = [row for row in scored if row.get("score_spread") is not None]
    if spread_known:
        speaking = [row for row in spread_known if (row.get("score_spread") or 0) > 0]
        summary["n_rows_with_discriminative_evidence"] = len(speaking)
        summary["coverage"] = len(speaking) / len(spread_known)
        with_pair = [row for row in speaking if row.get("pair_accuracy") is not None]
        if with_pair:
            summary["selective_pair_accuracy"] = _mean(
                row.get("pair_accuracy") for row in with_pair)

    # Retrieval / graph diagnostics, reported when the method produced them.
    for key in (
        "n_queries",
        "n_searches",
        "n_zero_result_searches",
        "n_eligible_papers",
        "n_excluded_papers",
        "n_informative_assessments",
        "n_no_evidence_assessments",
        "n_retrieval_errors",
        "n_assessment_errors",
        "n_graph_nodes",
        "n_searchable_nodes",
        "n_shared_nodes",
        "n_merged_nodes",
        "n_nodes_unobserved",
        "n_nodes_with_informative_evidence",
        "n_queries_needing_backoff",
    ):
        values = [row.get(key) for row in rows if row.get(key) is not None]
        if values:
            summary["mean_" + key] = _mean(values)
            summary["total_" + key] = sum(float(v) for v in values)
    return summary
