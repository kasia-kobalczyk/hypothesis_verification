"""Proposition-level evidence assessment (IMPLEMENTATION_SPEC.md §19).

`D_v` is the retrieved set for proposition `X_v`. The assessor reads it jointly
and returns one ordinal label — it is not counting papers, and it is not told
which hypothesis the proposition came from, so it cannot tilt a judgment toward
a candidate.

`no_evidence` and `mixed` stay distinct (§19), and a retrieval failure is never
either of them: it is an error recorded by the caller (§29).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.inference.parameters import EVIDENCE_LABELS, normalise_evidence_label
from src.literature.base import Paper
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

LOGGER = get_logger("evidence.assess")

ASSESS_PROMPT = "evidence_assess_v1"

NO_LITERATURE_PLACEHOLDER = (
    "[no eligible literature was retrieved for this proposition]\n"
    "This means nothing relevant was found within the available record, not that "
    "the proposition was contradicted."
)


def assess_proposition(
    proposition: str,
    papers: List[Paper],
    *,
    literature_tool: Any,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    max_papers: int,
    enforce_no_evidence_without_papers: bool = True,
    event_log: Optional[EventLog] = None,
    assess_prompt: str = ASSESS_PROMPT,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    log = event_log or NULL_EVENT_LOG
    template = prompts.get(assess_prompt)
    # `render` re-checks eligibility for every record before it becomes text.
    literature = (
        literature_tool.render(papers, max_papers=max_papers) if papers else NO_LITERATURE_PLACEHOLDER
    )
    messages = [{"role": "user", "content": template.render(
        proposition=proposition, literature=literature, labels=", ".join(EVIDENCE_LABELS))}]

    def validate(parsed: Dict[str, Any]) -> None:
        if normalise_evidence_label(parsed.get("evidence_label")) is None:
            raise ValueError("unknown evidence_label {!r}".format(parsed.get("evidence_label")))

    response = llm.complete_json(
        messages, purpose="graph.evidence_assess", prompt_version=assess_prompt,
        validator=validate)
    parsed = response.parsed or {}
    model_label = normalise_evidence_label(parsed.get("evidence_label"))
    label, enforced = model_label, False
    if enforce_no_evidence_without_papers and label != "no_evidence" and not papers:
        log.decision("assessment_label_corrected", original=label, corrected="no_evidence",
                     reason="no eligible literature was retrieved")
        label, enforced = "no_evidence", True

    assessment = {
        "evidence_label": label,
        # v2 only; absent under v1. Recorded so a run's provenance shows whether a
        # bridge was refused rather than silently taken.
        "supporting_spans": parsed.get("supporting_spans"),
        "requires_external_bridge": parsed.get("requires_external_bridge"),
        "proposition_unassessable": parsed.get("proposition_unassessable"),
        "model_evidence_label": model_label,
        "label_enforced_by_harness": enforced,
        "rationale": parsed.get("rationale"),
        "key_papers": parsed.get("key_papers") or [],
        "independence_note": parsed.get("independence_note"),
        "n_papers_shown": len(papers),
    }
    return assessment, response.record(include_messages=messages)
