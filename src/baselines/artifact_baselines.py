"""Artifact baselines: how much of the ranking signal is not science?

The gold hypothesis in this benchmark is a short prose summary of a paper's
conclusion; the negatives are long, elaborately specified LLM proposals. A
ranker could therefore do well by reading style and length alone, and the slice
must not be rewritten to remove that (IMPLEMENTATION_SPEC.md §2, §34). The
honest alternative is to measure the confound directly:

* `style_artifact` ranks by surface features only — no model, no question, no
  literature. Its score is the ceiling attributable to formatting.
* `question_hidden_judge` is the direct judge with the scientific question
  withheld. Whatever it scores above the style baseline is what the candidate
  texts alone reveal, without the scientific target in view.

Both are diagnostics. A method that does not beat them is not doing science.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from src.baselines.direct_judge import DirectJudge
from src.common.logging_utils import get_logger
from src.experiments.base import InstanceContext, InstanceResult, Method
from src.experiments.metrics import ranking_from_scores

LOGGER = get_logger("baselines.artifact")

_WORD_RE = re.compile(r"\b\w+\b")


def surface_features(text: str) -> Dict[str, float]:
    """Content-free descriptors of a hypothesis string."""
    words = _WORD_RE.findall(text)
    digits = sum(character.isdigit() for character in text)
    return {
        "n_chars": float(len(text)),
        "n_words": float(len(words)),
        "n_lines": float(text.count("\n") + 1),
        "n_digits": float(digits),
        "digit_ratio": digits / len(text) if text else 0.0,
        "mean_word_length": (sum(len(w) for w in words) / len(words)) if words else 0.0,
    }


class StyleArtifactBaseline(Method):
    """Rank by one surface feature. Deterministic, no model, no literature."""

    name = "style_artifact"
    requires_literature = False

    def run_instance(self, ctx: InstanceContext) -> InstanceResult:
        feature = self.config.baselines.style_artifact.feature
        sign = -1.0 if self.config.baselines.style_artifact.prefer == "shortest" else 1.0

        result = InstanceResult(instance_id=ctx.instance.id, method=self.name)
        features: Dict[str, Dict[str, float]] = {}
        scores: Dict[str, float] = {}
        for hypothesis in ctx.instance.hypotheses:
            values = surface_features(hypothesis.text)
            if feature not in values:
                raise KeyError(
                    "unknown style feature {!r}; available: {}".format(feature, sorted(values))
                )
            features[hypothesis.id] = values
            scores[hypothesis.id] = sign * values[feature]

        order = [item.hypothesis_id for item in ctx.presentation.items]
        result.scores = scores
        result.ranking = ranking_from_scores(scores, order=order)
        result.artifacts["scores"] = {
            "method": self.name,
            "feature": feature,
            "prefer": self.config.baselines.style_artifact.prefer,
            "scores": scores,
            "features": features,
            "ranking": result.ranking,
            "gold_id": ctx.instance.gold_hypothesis.id,
            "note": "surface features only; no question, no model, no literature",
        }
        result.diagnostics = {"n_queries": 0, "n_eligible_papers": 0}
        return result


class QuestionHiddenJudge(DirectJudge):
    """The direct judge with the scientific question withheld."""

    name = "question_hidden_judge"
    requires_literature = False

    def prompt_versions(self) -> List[str]:
        return [self.config.baselines.question_hidden_judge.prompt_version]

    def _render_prompt(self, ctx: InstanceContext, template: Any, labels: List[str]) -> str:
        # The template has no $question placeholder, so the question cannot be
        # rendered into the prompt even by accident.
        return template.render(hypotheses=ctx.presentation.render(), labels=", ".join(labels))

    def _config(self) -> Any:
        return self.config.baselines.question_hidden_judge
