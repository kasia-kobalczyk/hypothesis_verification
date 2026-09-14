"""Query shaping: length cap, direction-word removal, lexical backoff.

Measured on the development slice, Semantic Scholar's `/paper/search` behaves
close to an AND over terms: the same question returns 2 results as a ten-word
keyword string, 39 at five words and 252 at three. Long generated queries
therefore return nothing, and "nothing" is indistinguishable from "the
literature is silent" unless the query itself is controlled.

Three policies, all deterministic and all outcome-neutral:

* **Length cap** — a query is truncated to `max_terms` content words. The prompt
  asks for short queries; this enforces it, because a prompt is a request.
* **Direction-word removal** — outcome words ("increase", "supports",
  "evidence") encode the answer the searcher wants (spec §17). They are stripped
  as standalone tokens, never inside a protected entity phrase, and every
  removal is recorded.
* **Lexical backoff** — a query returning zero *provider results* is retried,
  shortened by one trailing term at a time. The trigger is the absence of
  results, never their content, so backoff cannot chase a favourable outcome.
  The ladder is a pure function of the query text: same query, same attempts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from src.common.logging_utils import get_logger

LOGGER = get_logger("literature.query_policy")

_TOKEN = re.compile(r"[^\s]+")


@dataclass
class ShapedQuery:
    """A generated query, and every deterministic edit made to it."""

    original: str
    query: str
    removed_direction_words: List[str] = field(default_factory=list)
    removed_stopwords: List[str] = field(default_factory=list)
    truncated_from: Optional[int] = None
    protected_phrases: List[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return self.query != self.original

    def record(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "query": self.query,
            "removed_direction_words": self.removed_direction_words,
            "removed_stopwords": self.removed_stopwords,
            "truncated_from": self.truncated_from,
            "protected_phrases": self.protected_phrases,
            "changed": self.changed,
        }


def _norm(token: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", token.lower())


def shape_query(
    query: str,
    *,
    max_terms: int,
    direction_words: Sequence[str],
    stopwords: Sequence[str] = (),
    strip_direction_words: bool = True,
    protected_phrases: Sequence[str] = (),
) -> ShapedQuery:
    """Apply the direction-word and length policies to one generated query."""
    text = " ".join(str(query).split())
    shaped = ShapedQuery(original=text, query=text)
    if not text:
        return shaped

    # Protect entity names that legitimately contain a direction word
    # ("reduced graphene oxide") by masking them before the token pass.
    masked = text
    placeholders: Dict[str, str] = {}
    for index, phrase in enumerate(protected_phrases):
        if not phrase:
            continue
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        if pattern.search(masked):
            token = "\x00p{}\x00".format(index)
            masked = pattern.sub(token, masked)
            placeholders[token] = phrase
            shaped.protected_phrases.append(phrase)

    tokens = _TOKEN.findall(masked)
    blocked = {_norm(word) for word in direction_words if word} if strip_direction_words else set()
    # Function words are separate from direction words: they encode no outcome,
    # they just waste slots under the length cap.
    noise = {_norm(word) for word in stopwords if word}
    if blocked or noise:
        kept: List[str] = []
        for token in tokens:
            if token in placeholders:
                kept.append(token)
                continue
            key = _norm(token)
            if key in blocked:
                shaped.removed_direction_words.append(token)
                continue
            if key in noise:
                shaped.removed_stopwords.append(token)
                continue
            kept.append(token)
        tokens = kept

    if max_terms and len(tokens) > max_terms:
        shaped.truncated_from = len(tokens)
        tokens = tokens[:max_terms]

    restored = " ".join(tokens)
    for token, phrase in placeholders.items():
        restored = restored.replace(token, phrase)
    shaped.query = " ".join(restored.split())

    if shaped.changed:
        LOGGER.debug("shaped %r -> %r", shaped.original, shaped.query)
    return shaped


def lexical_ladder(query: str, *, min_terms: int, steps: int) -> List[str]:
    """Progressively shorter variants, dropping one trailing term at a time.

    Returns only the *fallback* variants (the original is not included), at most
    `steps` of them, never shorter than `min_terms`. A pure function of the text.
    """
    tokens = _TOKEN.findall(" ".join(str(query).split()))
    out: List[str] = []
    for _ in range(max(0, steps)):
        if len(tokens) <= max(1, min_terms):
            break
        tokens = tokens[:-1]
        out.append(" ".join(tokens))
    return out


@dataclass
class RetrievalAttempt:
    """One search actually issued, and what it returned."""

    query: str
    step: int  # 0 = the shaped query, 1+ = backoff rungs
    n_results: int
    n_eligible: int

    def record(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "step": self.step,
            "n_results": self.n_results,
            "n_eligible": self.n_eligible,
        }
