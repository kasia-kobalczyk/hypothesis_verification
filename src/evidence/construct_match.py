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

CONSTRUCT_PROMPT = "construct_match_v1"
NO_SPANS = "(the assessor quoted no spans)"


def parse_construct_match(parsed: Dict[str, Any]) -> "OrderedDict[str, Any]":
    value = str(parsed.get("construct_match") or "").strip().lower()
    if value not in CONSTRUCT_MATCHES:
        raise ValueError("construct_match must be one of {}, got {!r}".format(CONSTRUCT_MATCHES, value))
    return OrderedDict([
        ("construct_match", value),
        ("proposition_construct", parsed.get("proposition_construct")),
        ("evidence_construct", parsed.get("evidence_construct")),
        ("gap", parsed.get("gap")),
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
