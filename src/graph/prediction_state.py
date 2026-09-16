"""v4 prediction-state assessment: what each hypothesis commits to about a proposition.

One call per proposition covering every hypothesis, rendered with the same anonymised
candidate labels as v3's root-edge assessment. The response is validated strictly:
every candidate must appear exactly once, with a known state and, for a determinate
state, a strength. Anything else raises, and callers treat the proposition as
unscorable. A missing hypothesis is never defaulted to `indeterminate`, because
defaulting is exactly how v3 turned missing judgments into P = 0.5.
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Optional, Tuple

from src.benchmark.presentation import Presentation
from src.graph.generate import _render_candidates
from src.inference.discrimination import StateError, normalise_scope, normalise_state, normalise_strength
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

# Development head. Iteration 3 (prediction_state_v3, explicit scope) regressed on both
# replicates -- more manufactured contrasts, lower stability -- so the head reverted to
# iteration 2's prompt (BENCH-GRAPH-V4-DEV-001, docs/V4_DEV_REPORT.md). The scope field
# and its deterministic gate remain implemented and tested for prompts that emit it.
STATE_PROMPT = "prediction_state_v2"
SCOPE_PROMPTS = frozenset({"prediction_state_v3"})


def parse_states(parsed: Dict[str, Any], presentation: Presentation) -> "OrderedDict[str, Dict[str, Any]]":
    entries = parsed.get("states")
    if not isinstance(entries, list) or not entries:
        raise StateError("missing 'states'")
    out: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for entry in entries:
        hypothesis_id = presentation.resolve(entry.get("id"))
        if hypothesis_id is None:
            raise StateError("unknown candidate id {!r}".format(entry.get("id")))
        if hypothesis_id in out:
            raise StateError("candidate {!r} judged twice".format(entry.get("id")))
        state = normalise_state(entry.get("state"))
        out[hypothesis_id] = OrderedDict([
            ("state", state),
            ("strength", normalise_strength(state, entry.get("strength"))),
            ("basis", entry.get("basis")),
            ("rationale", entry.get("rationale")),
            ("display_label", presentation.id_to_label[hypothesis_id]),
        ])
    missing = [item.hypothesis_id for item in presentation.items if item.hypothesis_id not in out]
    if missing:
        raise StateError("no state for candidate(s) {}".format(
            [presentation.id_to_label[h] for h in missing]))
    return OrderedDict((item.hypothesis_id, out[item.hypothesis_id]) for item in presentation.items)


def parse_scope(parsed: Dict[str, Any]) -> "OrderedDict[str, Any]":
    """Required from prediction_state_v3 on; a missing or unknown scope fails closed."""
    return OrderedDict([("proposition_scope", normalise_scope(parsed.get("proposition_scope"))),
                        ("scope_basis", parsed.get("scope_basis"))])


def assess_prediction_states(
    llm: BaseLLMClient, prompts: PromptLibrary, *, proposition: str, presentation: Presentation,
    prompt_name: str = None,
) -> Tuple["OrderedDict[str, Dict[str, Any]]", "Optional[OrderedDict[str, Any]]", Dict[str, Any]]:
    prompt_name = prompt_name or STATE_PROMPT
    scoped = prompt_name in SCOPE_PROMPTS
    template = prompts.get(prompt_name)
    messages = [{"role": "user", "content": template.render(
        proposition=proposition,
        candidates=_render_candidates(presentation),
        ids=", ".join(presentation.labels),
    )}]

    def validate(parsed: Dict[str, Any]) -> None:
        parse_states(parsed, presentation)   # raises StateError (a ValueError) -> repair retry
        if scoped:
            parse_scope(parsed)

    response = llm.complete_json(messages, purpose="graph_v4.prediction_state", prompt_version=prompt_name,
                                 validator=validate)
    parsed = response.parsed or {}
    return parse_states(parsed, presentation), (parse_scope(parsed) if scoped else None), response.record()
