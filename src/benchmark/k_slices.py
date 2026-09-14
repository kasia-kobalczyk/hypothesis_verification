"""Controlled listwise candidate sets at several values of k.

The method is defined for an arbitrary candidate set H = {H_1, ..., H_k}; the
benchmark protocol is a separate matter. Results at different k are NOT directly
comparable -- picking the gold out of 2 is a different problem from picking it out
of 10, and chance top-1 is 1/k -- so k is varied deliberately and reported
stratified, never averaged.

Why not just use ResearchBench's own 11-way task: candidate quality there is uneven,
mixing genuine alternatives with irrelevant distractors. Here every negative in
every set has independently passed the frozen R2 comparability criterion.

**Nested by construction.** A row's screened negatives are placed in one frozen
order, and the set at k uses the first k-1 of them. So the k=2 set is a subset of
the k=3 set, which is a subset of the k=4 set, and a row present at the largest k
is present at every smaller one. That makes the k comparison within-row: the
candidates do not change identity as k grows, only more of them are added. The
alternative -- sampling independently per k -- would confound k with which
negatives happened to be drawn.

The negative ordering is frozen (seeded by row) BEFORE any verifier runs, and the
manifest records the seed and the resulting order, so the sets cannot be reshuffled
after seeing a result.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from src.common.io import stable_hash
from src.common.logging_utils import get_logger

LOGGER = get_logger("benchmark.k_slices")

DEFAULT_K_VALUES = (2, 3, 4)


@dataclass
class KSet:
    """One listwise task: the gold plus k-1 screened comparable negatives."""

    instance_id: str
    k: int
    row_id: str
    doi: str
    screen_rank: Optional[int]
    question: str
    gold_text: str
    gold_source_index: Optional[int]
    negatives: List[Dict[str, Any]] = field(default_factory=list)
    discipline: Optional[str] = None
    cutoff_date: Optional[str] = None

    def record(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "k": self.k,
            "row_id": self.row_id,
            "doi": self.doi,
            "screen_rank": self.screen_rank,
            "question": self.question,
            "gold_hypothesis": self.gold_text,
            "gold_source_index": self.gold_source_index,
            "negatives": self.negatives,
            "discipline": self.discipline,
            "cutoff_date": self.cutoff_date,
        }


def frozen_negative_order(row_id: str, negatives: Sequence[Dict[str, Any]],
                          *, seed: int) -> List[Dict[str, Any]]:
    """One deterministic order per row, fixed before any verifier runs.

    Seeded by `(seed, row_id)` so it is reproducible and independent of the order
    the negatives happened to be screened in. The k-set at each k takes a prefix of
    this list, which is what makes the sets nested.
    """
    ordered = list(negatives)
    rng = random.Random(int(stable_hash("{}:{}".format(seed, row_id)), 16))
    rng.shuffle(ordered)
    return ordered


def build_k_sets(
    rows: Sequence[Dict[str, Any]],
    *,
    k_values: Sequence[int] = DEFAULT_K_VALUES,
    seed: int,
) -> Dict[str, Any]:
    """Build nested candidate sets for each k from rows carrying screened negatives.

    Each row needs `row_id`, `question`, `gold_text`, and `negatives` (each a dict
    with at least `text`); only negatives that passed comparability should be
    supplied. A row with fewer than k-1 of them simply does not appear at that k --
    no negative is ever manufactured to reach a target size.
    """
    by_k: Dict[int, List[KSet]] = {k: [] for k in k_values}
    order_record: Dict[str, List[Any]] = {}
    skipped: Dict[int, int] = {k: 0 for k in k_values}

    for row in rows:
        row_id = str(row["row_id"])
        ordered = frozen_negative_order(row_id, row.get("negatives") or [], seed=seed)
        order_record[row_id] = [n.get("source_index", n.get("text", "")[:40]) for n in ordered]
        for k in k_values:
            needed = k - 1
            if len(ordered) < needed:
                skipped[k] += 1
                continue
            by_k[k].append(KSet(
                instance_id="{}-K{}".format(row_id, k),
                k=k,
                row_id=row_id,
                doi=row.get("doi", ""),
                screen_rank=row.get("screen_rank"),
                question=row.get("question", ""),
                gold_text=row["gold_text"],
                gold_source_index=row.get("gold_source_index"),
                negatives=ordered[:needed],
                discipline=row.get("discipline"),
                cutoff_date=row.get("cutoff_date"),
            ))

    largest = max(k_values)
    balanced_rows = sorted({s.row_id for s in by_k[largest]})
    return {
        "k_values": list(k_values),
        "seed": seed,
        "sets_by_k": {k: [s.record() for s in sets] for k, sets in by_k.items()},
        "n_sets_by_k": {k: len(sets) for k, sets in by_k.items()},
        "n_rows_short_of_k": skipped,
        "frozen_negative_order": order_record,
        # Rows present at EVERY k: the within-row panel where k is the only thing
        # that changes. Prefer this for the scaling analysis; the per-k sets above
        # differ in row membership as well as in k.
        "balanced_panel_row_ids": balanced_rows,
        "n_balanced_panel_rows": len(balanced_rows),
        "nesting": (
            "the set at k uses the first k-1 negatives of the row's frozen order, "
            "so sets are nested: k=2 subset of k=3 subset of ... "
        ),
    }
