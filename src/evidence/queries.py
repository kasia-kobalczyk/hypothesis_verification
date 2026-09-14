"""Outcome-neutral literature queries for a proposition (IMPLEMENTATION_SPEC.md §17).

Queries describe the entities, interventions, comparisons and measurements in a
proposition without encoding the outcome a hypothesis would prefer. They are
generated from the proposition text alone — the model writing them is not told
which hypothesis the node came from — and frozen before retrieval, so no query
can be rewritten after seeing what it returned.

Shaping (length cap, direction-word removal, lexical backoff) is the same policy
`direct_rag` uses, in `src.literature.query_policy`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from src.common.config import AppConfig
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.query_policy import ShapedQuery, shape_query
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

LOGGER = get_logger("evidence.queries")

QUERY_PROMPT = "proposition_query_v1"


def generate_queries(
    proposition: str,
    *,
    config: AppConfig,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    event_log: Optional[EventLog] = None,
) -> Tuple[List[ShapedQuery], Dict[str, Any]]:
    log = event_log or NULL_EVENT_LOG
    policy = config.retrieval.query_policy
    n_queries = config.retrieval.queries_per_node
    template = prompts.get(QUERY_PROMPT)
    messages = [{"role": "user", "content": template.render(
        proposition=proposition, n_queries=n_queries, max_terms=policy.max_terms)}]

    def validate(parsed: Dict[str, Any]) -> None:
        queries = parsed.get("queries")
        if not isinstance(queries, list) or not queries:
            raise ValueError("missing 'queries' list")
        if not all(isinstance(q, str) and q.strip() for q in queries):
            raise ValueError("'queries' must be non-empty strings")

    response = llm.complete_json(
        messages, purpose="graph.proposition_query", prompt_version=QUERY_PROMPT, validator=validate)
    raw = [q.strip() for q in (response.parsed or {}).get("queries", [])][:n_queries]
    shaped = [
        shape_query(
            query, max_terms=policy.max_terms, direction_words=policy.direction_words,
            stopwords=policy.stopwords, strip_direction_words=policy.strip_direction_words,
            protected_phrases=policy.protected_phrases,
        )
        for query in raw
    ]
    for item in shaped:
        if item.changed:
            log.decision("query_shaped", original=item.original, query=item.query,
                         removed_direction_words=item.removed_direction_words)
    return shaped, response.record(include_messages=messages)
