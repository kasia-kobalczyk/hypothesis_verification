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
from src.inference.discrimination import DETERMINATE, StateError, normalise_scope_class, normalise_state

# Iteration 2 (V4-SCOPE): scope v2 adds "only weakly implied" to invalid_or_underspecified
# (the directive's own definition); element v2 judges each candidate's position on the
# contrast variable without seeing the recorded states. v1 prompts stay for provenance.
SCOPE_PROMPT = "proposition_scope_v2"
ELEMENT_PROMPT = "contrast_element_v2"
ELEMENT_FIELDS = ("shared_context", "contrast_variable", "contrast_direction_or_state",
                  "system_or_population", "measurement_or_observable")
POSITIONS = ("requires_asserted", "requires_other", "not_required")
_POSITION_FOR_STATE = {"positive_or_present": "requires_asserted", "negative_or_absent": "requires_other",
                       "substantive_null": "requires_other"}


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


def derive_positions_contrastive(positions: Mapping[str, str]) -> bool:
    """A contrast-bearing element: every candidate takes a position, and they differ."""
    values = set(positions.values())
    return "not_required" not in values and values == {"requires_asserted", "requires_other"}


def positions_agree_with_states(positions: Mapping[str, str], states: Mapping[str, Mapping[str, Any]]) -> bool:
    """The element-level positions point the same way as the recorded prediction states."""
    for h, position in positions.items():
        state = normalise_state(states[h]["state"])
        if state not in DETERMINATE or _POSITION_FOR_STATE[state] != position:
            return False
    return True


def parse_contrast_element_v2(parsed: Dict[str, Any], presentation: Presentation) -> "OrderedDict[str, Any]":
    out: "OrderedDict[str, Any]" = OrderedDict()
    for field in ELEMENT_FIELDS:
        value = parsed.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("contrast element field {!r} must be a non-empty string".format(field))
        out[field] = value.strip()
    entries = parsed.get("candidate_positions")
    if not isinstance(entries, list):
        raise ValueError("candidate_positions must be a list")
    label_to_id = presentation.label_to_id
    positions: "OrderedDict[str, Any]" = OrderedDict()
    for entry in entries:
        label = str((entry or {}).get("id", "")).strip()
        position = str((entry or {}).get("position", "")).strip().lower()
        if label not in label_to_id or label_to_id[label] in positions:
            raise ValueError("unknown or duplicate candidate id {!r}".format(label))
        if position not in POSITIONS:
            raise ValueError("unknown position {!r}".format(position))
        positions[label_to_id[label]] = OrderedDict([("position", position), ("reason", entry.get("reason"))])
    if set(positions) != set(label_to_id.values()):
        raise ValueError("candidate_positions must cover every candidate exactly once")
    out["candidate_positions"] = OrderedDict((item.hypothesis_id, positions[item.hypothesis_id])
                                             for item in presentation.items)
    out["positions_contrastive"] = derive_positions_contrastive({h: p["position"] for h, p in positions.items()})
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
                             states: Mapping[str, Mapping[str, Any]],
                             prompt_name: str = None) -> Tuple["OrderedDict[str, Any]", Dict[str, Any]]:
    """v1: the extractor sees the states and returns `has_contrast` itself.

    v2: the extractor does NOT see the states; it states each candidate's position on the
    contrast variable. `has_contrast` is derived in code: the positions must form a contrast
    AND point the same way as the recorded prediction states (two independent judgments).
    """
    name = prompt_name or ELEMENT_PROMPT
    template = prompts.get(name)
    if name == "contrast_element_v1":
        messages = [{"role": "user", "content": template.render(
            candidates=_render_candidates(presentation), states=render_states(states, presentation),
            proposition=proposition)}]
        response = llm.complete_json(messages, purpose="graph_v4s.contrast_element", prompt_version=name,
                                     validator=parse_contrast_element)
        return parse_contrast_element(response.parsed or {}), response.record()

    def validate(parsed):
        parse_contrast_element_v2(parsed, presentation)

    messages = [{"role": "user", "content": template.render(
        candidates=_render_candidates(presentation), proposition=proposition)}]
    response = llm.complete_json(messages, purpose="graph_v4s.contrast_element", prompt_version=name,
                                 validator=validate)
    element = parse_contrast_element_v2(response.parsed or {}, presentation)
    element["positions_agree_with_states"] = positions_agree_with_states(
        {h: p["position"] for h, p in element["candidate_positions"].items()}, states)
    element["has_contrast"] = element["positions_contrastive"] and element["positions_agree_with_states"]
    return element, response.record()
