"""Deterministic, position-neutral presentation of candidate hypotheses.

In the frozen slice the gold hypothesis is always the first element of the row.
Showing candidates in load order would let a model exploit position rather than
science, so the default presentation:

* permutes the candidates with a per-instance deterministic RNG, and
* relabels them ("Hypothesis A", "Hypothesis B", ...) so internal ids (`H0` is
  always gold) never reach the model.

The permutation is a function of `(run.seed, instance.id)` only — never of any
retrieval outcome — and the label map is written to the run artifacts so every
model output can be mapped back to hypothesis ids.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from src.benchmark.loader import BenchmarkInstance
from src.common.config import RunConfig
from src.common.io import stable_hash


def _label_for(index: int) -> str:
    """0 -> 'A', 25 -> 'Z', 26 -> 'AA'."""
    label = ""
    n = index
    while True:
        label = chr(ord("A") + n % 26) + label
        n = n // 26 - 1
        if n < 0:
            break
    return label


@dataclass(frozen=True)
class PresentedHypothesis:
    label: str
    hypothesis_id: str
    text: str
    gold: bool


class Presentation:
    """An ordering + labelling of one instance's candidate hypotheses."""

    def __init__(self, instance_id: str, items: List[PresentedHypothesis], *, seed_key: str, order: str):
        self.instance_id = instance_id
        self.items = items
        self.seed_key = seed_key
        self.order = order
        self.label_to_id: Dict[str, str] = {item.label: item.hypothesis_id for item in items}
        self.id_to_label: Dict[str, str] = {item.hypothesis_id: item.label for item in items}

    @property
    def labels(self) -> List[str]:
        return [item.label for item in self.items]

    def resolve(self, label: str) -> Optional[str]:
        """Map a model-facing label back to the internal hypothesis id."""
        if label is None:
            return None
        key = str(label).strip()
        if key in self.label_to_id:
            return self.label_to_id[key]
        # Tolerate "Hypothesis A" / "hypothesis a" style answers.
        cleaned = key.lower().replace("hypothesis", "").replace(":", "").strip().upper()
        return self.label_to_id.get(cleaned)

    def render(self, *, header: str = "Hypothesis") -> str:
        blocks = []
        for item in self.items:
            blocks.append("{} {}:\n{}".format(header, item.label, item.text))
        return "\n\n".join(blocks)

    def to_record(self) -> Dict[str, object]:
        return {
            "instance_id": self.instance_id,
            "order": self.order,
            "seed_key": self.seed_key,
            "label_to_hypothesis_id": dict(self.label_to_id),
            "presentation_order": [item.hypothesis_id for item in self.items],
        }


def build_presentation(instance: BenchmarkInstance, run_config: RunConfig) -> Presentation:
    hypotheses = list(instance.hypotheses)
    seed_key = "{}:{}".format(run_config.seed, instance.id)
    if run_config.hypothesis_order == "shuffled":
        rng = random.Random(int(stable_hash(seed_key), 16))
        rng.shuffle(hypotheses)

    items: List[PresentedHypothesis] = []
    for index, hypothesis in enumerate(hypotheses):
        label = _label_for(index) if run_config.anonymise_labels else hypothesis.id
        items.append(
            PresentedHypothesis(
                label=label,
                hypothesis_id=hypothesis.id,
                text=hypothesis.text,  # verbatim
                gold=hypothesis.gold,
            )
        )
    return Presentation(instance.id, items, seed_key=seed_key, order=run_config.hypothesis_order)
