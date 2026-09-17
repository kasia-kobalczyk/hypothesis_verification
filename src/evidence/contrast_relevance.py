"""v4-scope evidence relevance, judged against a proposition's contrast-bearing element.

Replaces v4's whole-proposition construct match for gating (BENCH-GRAPH-V4-SCOPE-001
§8). The judge answers three structured questions about the cited records (does it
report the contrast variable; does it support the shared context; does it concern a
different construct), and the category is derived in code by
`src.inference.discrimination.derive_contrast_relevance`. The judge never sees the
evidence label or the assessor's rationale.
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Mapping, Sequence, Tuple

from src.graph.proposition_scope import render_element
from src.inference.discrimination import derive_contrast_relevance

RELEVANCE_PROMPT = "contrast_relevance_v1"
NO_SPANS = "(the assessor quoted no spans)"


def parse_contrast_relevance(parsed: Dict[str, Any]) -> "OrderedDict[str, Any]":
    category = derive_contrast_relevance(parsed.get("contrast_variable_reported"),
                                         parsed.get("shared_context_supported"),
                                         parsed.get("different_construct"))
    return OrderedDict([
        ("contrast_relevance", category),
        ("contrast_variable_reported", str(parsed.get("contrast_variable_reported")).strip().lower()),
        ("shared_context_supported", str(parsed.get("shared_context_supported")).strip().lower()),
        ("different_construct", str(parsed.get("different_construct")).strip().lower()),
        ("what_the_records_report", parsed.get("what_the_records_report")),
        ("rationale", parsed.get("rationale")),
    ])


def assess_contrast_relevance(llm, prompts, *, proposition: str, element: Mapping[str, Any],
                              spans: Sequence[str], records_text: str) -> Tuple["OrderedDict[str, Any]", Dict[str, Any]]:
    template = prompts.get(RELEVANCE_PROMPT)
    messages = [{"role": "user", "content": template.render(
        proposition=proposition, element=render_element(element),
        spans="\n".join("- \"{}\"".format(s) for s in spans) if spans else NO_SPANS,
        records=records_text)}]
    response = llm.complete_json(messages, purpose="graph_v4s.contrast_relevance", prompt_version=RELEVANCE_PROMPT,
                                 validator=parse_contrast_relevance)
    return parse_contrast_relevance(response.parsed or {}), response.record()
