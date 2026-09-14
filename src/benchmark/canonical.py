"""Symmetric candidate canonicalisation (docs/CANONICAL_PROTOCOL.md).

Every candidate — gold and negative alike — is rewritten by one fixed procedure
into a short declarative scientific claim. The canonicaliser is given the
research question and one candidate, and is never told which role that candidate
plays, so the transformation cannot treat the two differently. That symmetry is
the property the benchmark rests on; everything else here exists to record that
it held.

This replaces filtering. v2 showed that discarding raw pairs until the length cue
vanishes does not work, because the surviving cue is genre rather than length.
Rewriting both sides through the same funnel removes the register; whether it
does so is measured afterwards by the same three diagnostics used on v1 and v2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field

from src.benchmark.v2_slice import count_tokens, count_words
from src.common.errors import LLMError, LLMParseError
from src.common.io import utc_now_iso
from src.common.logging_utils import get_logger
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

LOGGER = get_logger("benchmark.canonical")

CANONICALISE_PROMPT = "canonicalise_claim_v1"
PRESERVATION_PROMPT = "canonical_preservation_v1"
PAIR_PROMPT = "pair_comparability_v1"

# Target length for a canonical claim, in words. A cap, not a filter: candidates
# are not dropped for exceeding it.
MAX_CLAIM_WORDS = 30


class CanonicalCandidate(BaseModel):
    """One candidate, before and after the transformation."""

    model_config = ConfigDict(extra="forbid")

    role: str                     # "gold" | "negative"; NOT shown to any judge
    source_index: Optional[int]
    original: str
    claim: Optional[str] = None
    central_relationship: Optional[str] = None
    preserved: Optional[bool] = None
    preservation_detail: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

    @property
    def usable(self) -> bool:
        return bool(self.claim) and self.preserved is True


class CanonicalPair(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pair_id: str
    researchbench_sample_id: str
    doi: str
    question: str
    # The canonical claims are what a verifier sees.
    gold_hypothesis: str
    negative_hypothesis: str
    # The originals are kept so the transformation can always be audited.
    gold_original: str
    negative_original: str
    gold_token_count: int
    negative_token_count: int
    length_ratio: float
    semantic_comparable: bool
    length_rule_pass: bool = True     # no length gate in this benchmark
    gold_preserved: bool = True
    negative_preserved: bool = True

    screen_rank: int = 0
    negative_index: int = 0
    discipline: Optional[str] = None
    cutoff_date: Optional[str] = None
    gold_word_count: int = 0
    negative_word_count: int = 0
    comparability_rationale: Optional[str] = None
    canonicalise_prompt_version: str = CANONICALISE_PROMPT
    preservation_prompt_version: str = PRESERVATION_PROMPT
    comparability_prompt_version: str = PAIR_PROMPT
    built_at: Optional[str] = None


def _validator(keys: Tuple[str, ...]):
    def validate(parsed: Dict[str, Any]) -> None:
        for key in keys:
            if not isinstance(parsed.get(key), bool):
                raise ValueError("{!r} must be a boolean".format(key))
    return validate


def canonicalise(
    question: str,
    candidate: str,
    *,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    max_words: int = MAX_CLAIM_WORDS,
) -> Dict[str, Any]:
    """Rewrite one candidate. The caller must not reveal its role."""
    template = prompts.get(CANONICALISE_PROMPT)
    messages = [{"role": "user", "content": template.render(
        question=question, candidate=candidate, max_tokens=max_words)}]

    def validate(parsed: Dict[str, Any]) -> None:
        if "claim" not in parsed:
            raise ValueError("missing 'claim'")
        claim = parsed.get("claim")
        if claim is not None and not str(claim).strip():
            raise ValueError("'claim' must be a non-empty string or null")

    try:
        response = llm.complete_json(
            messages, purpose="canonical.canonicalise",
            prompt_version=CANONICALISE_PROMPT, validator=validate)
    except (LLMParseError, LLMError) as exc:
        return {"error": "{}: {}".format(type(exc).__name__, exc)}
    parsed = response.parsed or {}
    claim = parsed.get("claim")
    return {
        "claim": str(claim).strip() if claim else None,
        "central_relationship": parsed.get("central_relationship"),
    }


def check_preservation(
    original: str,
    canonical: str,
    *,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
) -> Dict[str, Any]:
    """Did the restatement keep the claim? Judged without the candidate's role."""
    template = prompts.get(PRESERVATION_PROMPT)
    messages = [{"role": "user", "content": template.render(
        original=original, canonical=canonical)}]
    keys = ("same_subject", "same_direction", "no_new_mechanism")
    try:
        response = llm.complete_json(
            messages, purpose="canonical.preservation",
            prompt_version=PRESERVATION_PROMPT, validator=_validator(keys))
    except (LLMParseError, LLMError) as exc:
        # An error is neither a pass nor a fail.
        return {"error": "{}: {}".format(type(exc).__name__, exc), "preserved": None}
    parsed = response.parsed or {}
    detail = {key: bool(parsed.get(key)) for key in keys}
    # Derived from the criteria, not from the model's own summary field.
    detail["preserved"] = all(detail.values())
    detail["rationale"] = parsed.get("rationale")
    return detail


def canonicalise_row(
    row: Dict[str, Any],
    *,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    max_words: int = MAX_CLAIM_WORDS,
) -> List[CanonicalCandidate]:
    """Transform the gold and every negative of one row, blind to role.

    The candidates are processed in a fixed order and each call sees only the
    question and one candidate text.
    """
    candidates: List[CanonicalCandidate] = [
        CanonicalCandidate(role="gold", source_index=None, original=row.get("gold_hypothesis") or "")
    ]
    for index, negative in enumerate(row.get("model_negative_hypotheses") or []):
        if isinstance(negative, str) and negative:
            candidates.append(CanonicalCandidate(role="negative", source_index=index, original=negative))

    question = row.get("research_question") or ""
    for candidate in candidates:
        result = canonicalise(question, candidate.original, llm=llm, prompts=prompts,
                              max_words=max_words)
        if result.get("error"):
            candidate.error = result["error"]
            continue
        candidate.claim = result.get("claim")
        candidate.central_relationship = result.get("central_relationship")
        if not candidate.claim:
            candidate.preserved = False
            candidate.preservation_detail = {"reason": "candidate asserts no claim about the world"}
            continue
        detail = check_preservation(candidate.original, candidate.claim, llm=llm, prompts=prompts)
        candidate.preservation_detail = detail
        candidate.preserved = detail.get("preserved")
        if detail.get("error"):
            candidate.error = detail["error"]
    return candidates


def build_pair(
    *,
    row: Dict[str, Any],
    screen_rank: int,
    gold: CanonicalCandidate,
    negative: CanonicalCandidate,
    comparable: bool,
    rationale: Optional[str],
    cutoff_date: Optional[str],
) -> CanonicalPair:
    gold_tokens = count_tokens(gold.claim)
    negative_tokens = count_tokens(negative.claim)
    return CanonicalPair(
        pair_id="RBC-{:04d}-N{:02d}".format(screen_rank, negative.source_index or 0),
        researchbench_sample_id=row.get("sample_id") or "",
        doi=row.get("doi") or "",
        question=row.get("research_question") or "",
        gold_hypothesis=gold.claim or "",
        negative_hypothesis=negative.claim or "",
        gold_original=gold.original,
        negative_original=negative.original,
        gold_token_count=gold_tokens,
        negative_token_count=negative_tokens,
        length_ratio=round(negative_tokens / gold_tokens, 4) if gold_tokens else 0.0,
        semantic_comparable=comparable,
        gold_preserved=bool(gold.preserved),
        negative_preserved=bool(negative.preserved),
        screen_rank=screen_rank,
        negative_index=negative.source_index or 0,
        discipline=row.get("discipline"),
        cutoff_date=cutoff_date,
        gold_word_count=count_words(gold.claim),
        negative_word_count=count_words(negative.claim),
        comparability_rationale=rationale,
        built_at=utc_now_iso(),
    )
