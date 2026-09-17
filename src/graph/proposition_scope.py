"""v4-scope judgments about a proposition itself: its scope, and its contrast-bearing element.

Both are separate LLM calls from prediction-state assessment (BENCH-GRAPH-V4-SCOPE-001
§3: scope must not be folded into the state prompt). Responses are validated strictly;
anything malformed raises, and callers leave the proposition unscored.

Scope sees the research question: scope is relative to the system under dispute, which
the question names. (The prediction-state prompt deliberately does not see the question,
to avoid "A or B?" framing; scope assigns no contrast, so that concern does not apply.)
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Mapping, Tuple

from src.benchmark.presentation import Presentation
from src.graph.generate import _render_candidates
from src.inference.discrimination import StateError, normalise_scope_class

SCOPE_PROMPT = "proposition_scope_v1"
ELEMENT_PROMPT = "contrast_element_v1"
ELEMENT_FIELDS = ("shared_context", "contrast_variable", "contrast_direction_or_state",
                  "system_or_population", "measurement_or_observable")


def parse_scope_class(parsed: Dict[str, Any]) -> "OrderedDict[str, Any]":
    occurs = parsed.get("asserts_actual_occurrence_in_system_under_dispute")
    if not isinstance(occurs, bool):
        raise StateError("asserts_actual_occurrence_in_system_under_dispute must be true or false")
    return OrderedDict([
        ("scope", normalise_scope_class(parsed.get("scope"))),
        ("system_under_dispute", parsed.get("system_under_dispute")),
        ("proposition_is_about", parsed.get("proposition_is_about")),
        ("asserts_actual_occurrence_in_system_under_dispute", occurs),
        ("rationale", parsed.get("rationale")),
    ])


def parse_contrast_element(parsed: Dict[str, Any]) -> "OrderedDict[str, Any]":
    has = parsed.get("has_contrast")
    if not isinstance(has, bool):
        raise ValueError("has_contrast must be true or false")
    out: "OrderedDict[str, Any]" = OrderedDict([("has_contrast", has)])
    for field in ELEMENT_FIELDS:
        value = parsed.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("contrast element field {!r} must be a non-empty string".format(field))
        out[field] = value.strip()
    return out


def render_element(element: Mapping[str, Any]) -> str:
    return "\n".join("- {}: {}".format(f, element[f]) for f in ELEMENT_FIELDS)


def render_states(states: Mapping[str, Mapping[str, Any]], presentation: Presentation) -> str:
    lines = []
    for item in presentation.items:
        s = states[item.hypothesis_id]
        lines.append("- Candidate {}: {}{}".format(
            item.label, s["state"], " ({})".format(s["strength"]) if s.get("strength") else ""))
    return "\n".join(lines)


def assess_scope(llm, prompts, *, question: str, proposition: str,
                 presentation: Presentation) -> Tuple["OrderedDict[str, Any]", Dict[str, Any]]:
    template = prompts.get(SCOPE_PROMPT)
    messages = [{"role": "user", "content": template.render(
        question=question, candidates=_render_candidates(presentation), proposition=proposition)}]
    response = llm.complete_json(messages, purpose="graph_v4s.scope", prompt_version=SCOPE_PROMPT,
                                 validator=parse_scope_class)
    return parse_scope_class(response.parsed or {}), response.record()


def extract_contrast_element(llm, prompts, *, proposition: str, presentation: Presentation,
                             states: Mapping[str, Mapping[str, Any]]) -> Tuple["OrderedDict[str, Any]", Dict[str, Any]]:
    template = prompts.get(ELEMENT_PROMPT)
    messages = [{"role": "user", "content": template.render(
        candidates=_render_candidates(presentation), states=render_states(states, presentation),
        proposition=proposition)}]
    response = llm.complete_json(messages, purpose="graph_v4s.contrast_element", prompt_version=ELEMENT_PROMPT,
                                 validator=parse_contrast_element)
    return parse_contrast_element(response.parsed or {}), response.record()
