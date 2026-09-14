"""Construction of the length-controlled v2 pair slice.

v1's artifact diagnostics showed that ranking candidates by "shortest text first"
scores 1.000 on the frozen pair subset: the gold hypothesis is systematically
shorter than the LLM-written negatives. Across the whole ResearchBench ranking
set the median negative is three times the gold's length.

v2 removes that confound by construction. It keeps v1's scientific-validity
rubric and its deterministic screening order untouched and adds exactly one new
rule — a length-ratio band applied per gold-negative pair. Nothing is rewritten
to fit: a pair either falls in the band or it is dropped.

Order of gates is cheapest-first (length is free, Crossref is cheap, model calls
are not). That is an efficiency choice only: the gates are conjunctive, so the
retained set does not depend on the order they are applied in.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from pydantic import BaseModel, ConfigDict, Field

from src.common.io import read_jsonl
from src.common.logging_utils import get_logger

LOGGER = get_logger("benchmark.v2_slice")

# --------------------------------------------------------------------------- #
# Tokenizer
# --------------------------------------------------------------------------- #
# `tiktoken` is not installed and fetches its vocabulary over the network on
# first use, so the project has no offline LLM tokenizer. This one is fully
# specified by the pattern below: a token is a run of word characters or a
# single non-space punctuation mark. Anyone can reproduce the counts exactly,
# with no dependency and no download.
TOKENIZER_NAME = "regex_word_punct_v1"
TOKENIZER_PATTERN = r"\w+|[^\w\s]"
_TOKEN_RE = re.compile(TOKENIZER_PATTERN)


def count_tokens(text: Optional[str]) -> int:
    return len(_TOKEN_RE.findall(text or ""))


def count_words(text: Optional[str]) -> int:
    return len((text or "").split())


# --------------------------------------------------------------------------- #
# The frozen length rule
# --------------------------------------------------------------------------- #
# OFFICIAL frozen band: "neither text more than 1.33x the other" (0.75 ~= 1/1.33).
#
# History, so the sequence is not mistaken for tuning:
#   1. [0.75, 1.33] specified up front;
#   2. widened to [0.67, 1.50] by the research owner after seeing base rates and
#      BEFORE any pair was screened;
#   3. reverted to [0.75, 1.33] after the diagnostics showed the widened band left
#      a larger residual length signal (shortest-text-first 0.809 vs 0.754).
# The widened slice is retained at `benchmark/v2_widened_diagnostic/` as a
# characterisation artifact, not as a benchmark.
LENGTH_RATIO_MIN = 0.75
LENGTH_RATIO_MAX = 1.33

# Kept for the record; never used as a fallback.
LENGTH_RATIO_BAND_WIDENED_DIAGNOSTIC = (0.67, 1.50)
LENGTH_RATIO_BAND_V1_PROPOSAL = (0.75, 1.33)


def length_ratio(gold: str, negative: str) -> Optional[float]:
    gold_tokens = count_tokens(gold)
    if gold_tokens == 0:
        return None
    return count_tokens(negative) / gold_tokens


def length_rule_pass(ratio: Optional[float]) -> bool:
    return ratio is not None and LENGTH_RATIO_MIN <= ratio <= LENGTH_RATIO_MAX


# --------------------------------------------------------------------------- #
# v1's deterministic screening order
# --------------------------------------------------------------------------- #
def screening_order(path: "str | Path") -> List[Tuple[int, str, Dict[str, Any]]]:
    """Reproduce v1's order: dedupe by DOI, then sort by SHA256(DOI) ascending.

    Verified against `benchmark/dev/manifest_v1.json`: this reproduces all 20
    recorded `screen_rank` values exactly.
    """
    groups: "OrderedDict[str, List[Dict[str, Any]]]" = OrderedDict()
    for row in read_jsonl(path):
        doi = row.get("doi") or ""
        groups.setdefault(doi, []).append(row)
    ordered = sorted(groups.items(), key=lambda kv: hashlib.sha256(kv[0].encode()).hexdigest())
    # One row per DOI, deterministically the first occurrence in file order.
    return [(rank, doi, rows[0]) for rank, (doi, rows) in enumerate(ordered, start=1)]


# --------------------------------------------------------------------------- #
# Records
# --------------------------------------------------------------------------- #
class V2Pair(BaseModel):
    """One retained gold-negative pair. Both texts verbatim from ResearchBench."""

    model_config = ConfigDict(extra="forbid")

    pair_id: str
    researchbench_sample_id: str
    doi: str
    question: str
    gold_hypothesis: str
    negative_hypothesis: str
    gold_token_count: int
    negative_token_count: int
    length_ratio: float
    semantic_comparable: bool
    length_rule_pass: bool

    # Provenance beyond the required fields.
    screen_rank: int = 0
    negative_index: int = 0
    discipline: Optional[str] = None
    tokenizer: str = TOKENIZER_NAME
    gold_word_count: int = 0
    negative_word_count: int = 0
    gold_char_count: int = 0
    negative_char_count: int = 0
    comparability_rationale: Optional[str] = None
    comparability_prompt_version: Optional[str] = None
    row_screen_prompt_version: Optional[str] = None
    cutoff_date: Optional[str] = None


@dataclass
class RowOutcome:
    """Why one ResearchBench row was kept or dropped, at every gate."""

    screen_rank: int
    doi: str
    sample_id: str
    discipline: Optional[str] = None
    n_negatives: int = 0
    n_length_pass: int = 0
    row_screen: Optional[Dict[str, Any]] = None
    cutoff_date: Optional[str] = None
    n_comparable: int = 0
    n_retained: int = 0
    rejected_at: Optional[str] = None  # length | row_screen | cutoff | comparability
    note: Optional[str] = None

    def record(self) -> Dict[str, Any]:
        return {
            "screen_rank": self.screen_rank,
            "doi": self.doi,
            "sample_id": self.sample_id,
            "discipline": self.discipline,
            "n_negatives": self.n_negatives,
            "n_length_pass": self.n_length_pass,
            "row_screen": self.row_screen,
            "cutoff_date": self.cutoff_date,
            "n_comparable": self.n_comparable,
            "n_retained": self.n_retained,
            "rejected_at": self.rejected_at,
            "note": self.note,
        }


def length_candidates(row: Dict[str, Any]) -> List[Tuple[int, str, float]]:
    """(index, negative_text, ratio) for negatives inside the length band."""
    gold = row.get("gold_hypothesis") or ""
    out: List[Tuple[int, str, float]] = []
    for index, negative in enumerate(row.get("model_negative_hypotheses") or []):
        if not isinstance(negative, str) or not negative:
            continue
        ratio = length_ratio(gold, negative)
        if length_rule_pass(ratio):
            out.append((index, negative, float(ratio)))
    return out


def build_pair(
    *,
    row: Dict[str, Any],
    screen_rank: int,
    negative_index: int,
    negative: str,
    ratio: float,
    comparable: bool,
    rationale: Optional[str],
    comparability_prompt_version: str,
    row_screen_prompt_version: str,
    cutoff_date: Optional[str],
) -> V2Pair:
    gold = row.get("gold_hypothesis") or ""
    return V2Pair(
        pair_id="RBV2-{:04d}-N{:02d}".format(screen_rank, negative_index),
        researchbench_sample_id=row.get("sample_id") or "",
        doi=row.get("doi") or "",
        question=row.get("research_question") or "",
        gold_hypothesis=gold,               # verbatim
        negative_hypothesis=negative,       # verbatim
        gold_token_count=count_tokens(gold),
        negative_token_count=count_tokens(negative),
        length_ratio=round(ratio, 4),
        semantic_comparable=comparable,
        length_rule_pass=True,
        screen_rank=screen_rank,
        negative_index=negative_index,
        discipline=row.get("discipline"),
        gold_word_count=count_words(gold),
        negative_word_count=count_words(negative),
        gold_char_count=len(gold),
        negative_char_count=len(negative),
        comparability_rationale=rationale,
        comparability_prompt_version=comparability_prompt_version,
        row_screen_prompt_version=row_screen_prompt_version,
        cutoff_date=cutoff_date,
    )
