"""Frozen gold-vs-negative pair subset.

The dev slice was selected by requiring that *at least one* raw ResearchBench
negative addresses the same scientific target as the gold and disagrees with a
substantive part of it (screening criterion R2). The other negatives were never
screened, so a listwise ranking over all eleven candidates mixes genuine
scientific disagreements with candidates that simply answer a different question.

This module applies the same R2 criterion to every gold-negative pair and freezes
the passing pairs as the primary evaluation unit. Listwise ranking remains
available as a secondary view.

Two properties matter for validity:

* the judgment sees only `(question, gold, negative)` — never literature, never a
  method's output, never which pairs a method happens to get right, so the subset
  is outcome-blind exactly like the slice itself (§35.6);
* the frozen file is written once and read thereafter; `build_pair_subset`
  refuses to overwrite an existing decision unless explicitly asked to refresh.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from pydantic import BaseModel, ConfigDict, Field

from src.benchmark.loader import BenchmarkInstance
from src.common.errors import LLMError, LLMParseError
from src.common.io import read_jsonl, utc_now_iso, write_jsonl
from src.common.logging_utils import get_logger
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

LOGGER = get_logger("benchmark.pairs")

PAIR_PROMPT_VERSION = "pair_comparability_v1"


class PairDecision(BaseModel):
    """One screened (gold, negative) pair."""

    model_config = ConfigDict(extra="forbid")

    instance_id: str
    gold_id: str
    negative_id: str
    # Provenance inside the original ResearchBench row.
    negative_source_field: str = ""
    negative_source_index: Optional[int] = None

    same_target: Optional[bool] = None
    disagrees_substantively: Optional[bool] = None
    decision: str = "ERROR"  # PASS | FAIL | ERROR
    rationale: Optional[str] = None

    # Provenance of the judgment itself
    prompt_version: str = PAIR_PROMPT_VERSION
    prompt_sha: Optional[str] = None
    model: Optional[str] = None
    judged_at: Optional[str] = None
    error: Optional[str] = None

    @property
    def key(self) -> Tuple[str, str]:
        return (self.instance_id, self.negative_id)

    @property
    def passed(self) -> bool:
        return self.decision == "PASS"


class PairSubset:
    """The frozen set of evaluable pairs, keyed by instance."""

    def __init__(self, decisions: Iterable[PairDecision]):
        self.decisions: List[PairDecision] = list(decisions)
        self._by_instance: Dict[str, List[PairDecision]] = {}
        for decision in self.decisions:
            self._by_instance.setdefault(decision.instance_id, []).append(decision)

    def __len__(self) -> int:
        return sum(1 for d in self.decisions if d.passed)

    @property
    def instance_ids(self) -> List[str]:
        return sorted(self._by_instance)

    def all_for(self, instance_id: str) -> List[PairDecision]:
        return list(self._by_instance.get(instance_id, []))

    def negatives_for(self, instance_id: str) -> List[str]:
        """Negative hypothesis ids that passed screening for this instance."""
        return [d.negative_id for d in self._by_instance.get(instance_id, []) if d.passed]

    def status_for(self, instance_id: str) -> str:
        """`evaluable` | `no_evaluable_pair` | `not_screened`.

        An instance whose every negative failed R2 is marked
        `no_evaluable_pair` rather than quietly contributing nothing: it is
        excluded from the primary metric by construction, and that exclusion has
        to be visible in the run artifacts.
        """
        if instance_id not in self._by_instance:
            return "not_screened"
        return "evaluable" if self.negatives_for(instance_id) else "no_evaluable_pair"

    def instances_without_pairs(self) -> List[str]:
        return sorted(
            iid for iid in self._by_instance if self.status_for(iid) == "no_evaluable_pair"
        )

    def counts(self) -> Dict[str, Any]:
        return {
            "n_pairs_screened": len(self.decisions),
            "n_pairs_retained": len(self),
            "n_pairs_rejected": sum(1 for d in self.decisions if d.decision == "FAIL"),
            "n_pairs_error": sum(1 for d in self.decisions if d.decision == "ERROR"),
            "n_instances": len(self._by_instance),
            "n_instances_with_pairs": sum(
                1 for iid in self._by_instance if self.negatives_for(iid)
            ),
            "instances_no_evaluable_pair": self.instances_without_pairs(),
        }


def load_pair_subset(path: "str | Path") -> PairSubset:
    return PairSubset(PairDecision(**row) for row in read_jsonl(path))


def write_pair_subset(path: "str | Path", decisions: Sequence[PairDecision]) -> Path:
    return write_jsonl(path, [d.model_dump(mode="json") for d in decisions])


# --------------------------------------------------------------------------- #
def judge_pair(
    instance: BenchmarkInstance,
    negative_id: str,
    *,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    prompt_version: str = PAIR_PROMPT_VERSION,
) -> PairDecision:
    """Apply the R2 comparability criterion to one pair.

    A model or parse failure is recorded as `decision="ERROR"`, never as FAIL:
    dropping a pair because the judge broke would silently shrink the benchmark.
    """
    gold = instance.gold_hypothesis
    negative = instance.hypothesis(negative_id)
    template = prompts.get(prompt_version)
    decision = PairDecision(
        instance_id=instance.id,
        gold_id=gold.id,
        negative_id=negative.id,
        negative_source_field=negative.source_field,
        negative_source_index=negative.source_index,
        prompt_version=prompt_version,
        prompt_sha=template.sha,
        judged_at=utc_now_iso(),
    )

    messages = [
        {
            "role": "user",
            "content": template.render(
                question=instance.question,
                gold=gold.text,  # verbatim
                alternative=negative.text,  # verbatim
            ),
        }
    ]

    def validator(parsed: Dict[str, Any]) -> None:
        for key in ("same_target", "disagrees_substantively"):
            if not isinstance(parsed.get(key), bool):
                raise ValueError("{!r} must be a boolean".format(key))
        if str(parsed.get("decision", "")).upper() not in ("PASS", "FAIL"):
            raise ValueError("decision must be PASS or FAIL")

    try:
        response = llm.complete_json(
            messages, purpose="pair_comparability", prompt_version=prompt_version, validator=validator
        )
    except (LLMParseError, LLMError) as exc:
        decision.error = "{}: {}".format(type(exc).__name__, exc)
        LOGGER.warning("%s/%s: judgment failed: %s", instance.id, negative_id, exc)
        return decision

    parsed = response.parsed or {}
    decision.model = response.model
    decision.same_target = bool(parsed.get("same_target"))
    decision.disagrees_substantively = bool(parsed.get("disagrees_substantively"))
    stated = str(parsed.get("decision", "")).upper()
    # Both criteria must hold; the model's summary field does not override them.
    derived = "PASS" if (decision.same_target and decision.disagrees_substantively) else "FAIL"
    if stated != derived:
        LOGGER.info(
            "%s/%s: stated %s but criteria give %s; using %s",
            instance.id, negative_id, stated, derived, derived,
        )
    decision.decision = derived
    decision.rationale = parsed.get("rationale")
    return decision


def build_pair_subset(
    instances: Sequence[BenchmarkInstance],
    *,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    existing: Optional[PairSubset] = None,
    prompt_version: str = PAIR_PROMPT_VERSION,
    on_decision: Optional[Any] = None,
) -> List[PairDecision]:
    """Screen every gold-negative pair, reusing any decision already frozen."""
    done: Dict[Tuple[str, str], PairDecision] = {}
    if existing is not None:
        for decision in existing.decisions:
            # A recorded ERROR is retried; PASS/FAIL are kept as frozen.
            if decision.decision in ("PASS", "FAIL"):
                done[decision.key] = decision

    decisions: List[PairDecision] = []
    for instance in instances:
        for hypothesis in instance.hypotheses:
            if hypothesis.gold:
                continue
            key = (instance.id, hypothesis.id)
            if key in done:
                decisions.append(done[key])
                continue
            decision = judge_pair(
                instance, hypothesis.id, llm=llm, prompts=prompts, prompt_version=prompt_version
            )
            decisions.append(decision)
            if on_decision is not None:
                on_decision(decision)
    return decisions
