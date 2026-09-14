"""Phase 1: joint diagnostic-test generation.

Tests are generated once for ALL candidates together, never per hypothesis. The
model is shown the candidates and asked where they come apart; it is not shown any
literature, and it is asked for predictions, not for truths.

Everything is logged: the raw call, each test, and the reason any test was rejected,
so a Phase 1 failure is attributable without reconstruction.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from src.benchmark.presentation import Presentation
from src.common.config import AppConfig
from src.common.errors import LLMError, LLMParseError
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.diagnostics.schema import (
    DiagnosticTest,
    PREDICTIONS,
    TestSet,
    normalise_prediction,
)
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary

LOGGER = get_logger("diagnostics.generate")

GENERATE_PROMPT = "diagnostic_test_generate_v1"


def _render_candidates(presentation: Presentation) -> str:
    return "\n\n".join("Candidate {}:\n{}".format(item.label, item.text)
                        for item in presentation.items)


def generate_tests(
    *,
    instance_id: str,
    question: str,
    presentation: Presentation,
    config: AppConfig,
    llm: BaseLLMClient,
    prompts: PromptLibrary,
    n_tests: int = 6,
    event_log: Optional[EventLog] = None,
) -> Tuple[TestSet, Dict[str, Any]]:
    """Generate diagnostic tests jointly for every candidate."""
    log = event_log or NULL_EVENT_LOG
    template = prompts.get(GENERATE_PROMPT)
    labels = [item.label for item in presentation.items]
    messages = [{"role": "user", "content": template.render(
        question=question,
        candidates=_render_candidates(presentation),
        n_tests=n_tests,
        ids=", ".join(labels),
    )}]

    def validate(parsed: Dict[str, Any]) -> None:
        items = parsed.get("tests")
        if not isinstance(items, list) or not items:
            raise ValueError("missing 'tests' list")
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("each test must be an object")
            for field in ("system", "intervention_or_exposure", "measured_outcome"):
                if not str(item.get(field, "")).strip():
                    raise ValueError("test is missing {}".format(field))

    response = llm.complete_json(
        messages, purpose="diagnostic.generate", prompt_version=GENERATE_PROMPT,
        validator=validate)
    raw = (response.parsed or {}).get("tests", [])

    test_set = TestSet(instance_id=instance_id,
                       hypothesis_ids=[i.hypothesis_id for i in presentation.items])
    rejected: List[Dict[str, Any]] = []

    for index, item in enumerate(raw[:n_tests], start=1):
        # Map model-facing labels back to internal hypothesis ids. A label the
        # presentation does not know is dropped rather than guessed at.
        predictions: Dict[str, str] = {}
        unknown: List[str] = []
        for label, value in (item.get("predictions_by_hypothesis") or {}).items():
            hypothesis_id = presentation.resolve(label)
            if hypothesis_id is None:
                unknown.append(str(label))
                continue
            norm = normalise_prediction(value)
            if norm is None:
                unknown.append("{}={}".format(label, value))
                continue
            predictions[hypothesis_id] = norm

        test = DiagnosticTest(
            test_id="T{}".format(index),
            system=str(item.get("system", "")).strip(),
            context=str(item.get("context", "")).strip(),
            intervention_or_exposure=str(item.get("intervention_or_exposure", "")).strip(),
            measured_outcome=str(item.get("measured_outcome", "")).strip(),
            baseline_or_comparator=str(item.get("baseline_or_comparator", "")).strip(),
            rationale=str(item.get("rationale", "")).strip(),
            empirically_observable=bool(item.get("empirically_observable", True)),
            predictions_by_hypothesis=predictions,
        )

        # Rejection reasons are recorded on the test, not silently dropped: Phase 1
        # is validated on WHY tests fail as much as on how many survive.
        missing = [h for h in test_set.hypothesis_ids if h not in predictions]
        if missing:
            test.rejected_reason = "no prediction for {}".format(", ".join(missing))
        elif not test.empirically_observable:
            test.rejected_reason = "not empirically observable"
        elif not test.is_discriminative():
            test.rejected_reason = "every candidate predicts the same, or all indeterminate"
        if test.rejected_reason:
            rejected.append({"test_id": test.test_id, "reason": test.rejected_reason,
                             "unknown_labels": unknown})
        test_set.tests.append(test)

    stats = test_set.stats()
    log.decision("diagnostic_tests_generated", instance_id=instance_id, **stats)
    LOGGER.info("%s: %s", instance_id, stats)
    artifacts = {
        "prompt_version": prompts.get(GENERATE_PROMPT).record(),
        "n_requested": n_tests,
        "stats": stats,
        "rejected": rejected,
        "tests": [t.record() for t in test_set.tests],
        "call": response.record(include_messages=messages),
    }
    return test_set, artifacts
