"""v4 construct-match check: do the cited records address the proposition's construct?

A narrow, proposition-focused judgment made AFTER the unchanged v3 evidence assessor
has labelled the evidence. It sees the proposition, the spans the assessor quoted and
the text of the records it cited, rendered through the cutoff-enforcing literature
renderer. It does not see the evidence label or the assessor's rationale, so it cannot
simply agree with them.

Only `direct` may move v4 comparative scores (human decision, BENCH-GRAPH-V4-DEV-001);
see `src.inference.discrimination.COMPARATIVE_CONSTRUCT_MATCHES`.
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Sequence, Tuple

from src.inference.discrimination import CONSTRUCT_MATCHES
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

CONSTRUCT_PROMPT = "construct_match_v2"
ELEMENT_STATUSES = ("established", "partly", "not_established")
NO_SPANS = "(the assessor quoted no spans)"


def derive_construct_match(statuses) -> str:
    """The label used for gating, derived from per-element statuses, never from the
    judge's holistic impression (development iteration 2, see docs/V4_DESIGN.md):

    * `direct`   -- every asserted element is established by the records;
    * `mismatch` -- no element is established even partly;
    * `partial`  -- anything in between.

    A compound proposition with one unestablished part therefore cannot be `direct`.
    """
    statuses = list(statuses)
    if statuses and all(s == "established" for s in statuses):
        return "direct"
    if not statuses or all(s == "not_established" for s in statuses):
        return "mismatch"
    return "partial"


def parse_construct_match(parsed: Dict[str, Any]) -> "OrderedDict[str, Any]":
    elements = parsed.get("elements")
    if not isinstance(elements, list) or not elements:
        raise ValueError("construct match needs a non-empty 'elements' list")
    clean = []
    for element in elements:
        status = str((element or {}).get("status") or "").strip().lower()
        if status not in ELEMENT_STATUSES:
            raise ValueError("element status must be one of {}, got {!r}".format(ELEMENT_STATUSES, status))
        clean.append(OrderedDict([("element", element.get("element")), ("status", status),
                                  ("note", element.get("note"))]))
    impression = str(parsed.get("overall_impression") or "").strip().lower() or None
    if impression is not None and impression not in CONSTRUCT_MATCHES:
        raise ValueError("overall_impression must be one of {}, got {!r}".format(CONSTRUCT_MATCHES, impression))
    return OrderedDict([
        ("construct_match", derive_construct_match(e["status"] for e in clean)),
        ("elements", clean),
        ("model_overall_impression", impression),
        ("rationale", parsed.get("rationale")),
    ])


def assess_construct_match(
    llm: BaseLLMClient, prompts: PromptLibrary, *, proposition: str, spans: Sequence[str], records_text: str,
) -> Tuple["OrderedDict[str, Any]", Dict[str, Any]]:
    template = prompts.get(CONSTRUCT_PROMPT)
    messages = [{"role": "user", "content": template.render(
        proposition=proposition,
        spans="\n".join("- \"{}\"".format(s) for s in spans) if spans else NO_SPANS,
        records=records_text,
    )}]
    response = llm.complete_json(messages, purpose="graph_v4.construct_match", prompt_version=CONSTRUCT_PROMPT,
                                 validator=parse_construct_match)
    return parse_construct_match(response.parsed or {}), response.record()
