"""Baseline 1: direct LLM judge (IMPLEMENTATION_SPEC.md §10).

Question + candidate hypotheses in, listwise scores out. No literature.

Isolation is structural: `requires_literature = False` makes the runner hand
this method a `ForbiddenLiteratureService`, so any retrieval attempt raises
instead of silently contaminating the baseline.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.common.errors import LLMError, LLMParseError
from src.experiments.base import InstanceContext, InstanceResult, Method
from src.experiments.metrics import ranking_from_scores
from src.common.logging_utils import get_logger

LOGGER = get_logger("baselines.direct_judge")


class DirectJudge(Method):
    name = "direct_judge"
    requires_literature = False

    def prompt_versions(self) -> List[str]:
        return [self._config().prompt_version]

    # -- overridable by variants (e.g. the question-hidden baseline) ------ #
    def _config(self) -> Any:
        return self.config.baselines.direct_judge

    def _render_prompt(self, ctx: InstanceContext, template: Any, labels: List[str]) -> str:
        return template.render(
            question=ctx.instance.question,
            hypotheses=ctx.presentation.render(),
            labels=", ".join(labels),
        )

    # ------------------------------------------------------------------ #
    def run_instance(self, ctx: InstanceContext) -> InstanceResult:
        cfg = self._config()
        presentation = ctx.presentation
        template = ctx.prompts.get(cfg.prompt_version)
        labels = presentation.labels

        messages = [{"role": "user", "content": self._render_prompt(ctx, template, labels)}]

        result = InstanceResult(instance_id=ctx.instance.id, method=self.name)
        # Token usage for this instance only, including parse-repair turns.
        usage_at_start = dict(ctx.llm.usage_totals)
        result.artifacts["prompts"] = {
            "method": self.name,
            "prompt_version": cfg.prompt_version,
            "prompt_record": template.record(),
            "mode": cfg.mode,
            "presentation": presentation.to_record(),
            "messages": messages,
        }

        def validator(parsed: Dict[str, Any]) -> None:
            entries = parsed.get("scores")
            if not isinstance(entries, list) or not entries:
                raise ValueError("missing 'scores' list")
            seen = set()
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError("'scores' entries must be objects")
                resolved = presentation.resolve(entry.get("id"))
                if resolved is None:
                    raise ValueError("unknown hypothesis label {!r}".format(entry.get("id")))
                if resolved in seen:
                    raise ValueError("duplicate score for {!r}".format(entry.get("id")))
                try:
                    float(entry.get("score"))
                except (TypeError, ValueError):
                    raise ValueError("non-numeric score for {!r}".format(entry.get("id")))
                seen.add(resolved)
            missing = [h for h in presentation.id_to_label if h not in seen]
            if missing:
                raise ValueError(
                    "missing scores for {}".format(
                        ", ".join(presentation.id_to_label[h] for h in missing)
                    )
                )

        try:
            response = ctx.llm.complete_json(
                messages,
                purpose=self.name,
                prompt_version=cfg.prompt_version,
                validator=validator,
            )
        except (LLMParseError, LLMError) as exc:
            ctx.record_error("{}.llm".format(self.name), exc)
            result.status = "error"
            result.errors = list(ctx.errors)
            result.artifacts["model_outputs"] = {
                "error": str(exc),
                "error_type": type(exc).__name__,
                "raw_text": getattr(exc, "raw_text", None),
            }
            return result

        parsed = response.parsed or {}
        scores: Dict[str, float] = {}
        rationales: Dict[str, str] = {}
        for entry in parsed.get("scores", []):
            hypothesis_id = presentation.resolve(entry.get("id"))
            if hypothesis_id is None:
                continue
            scores[hypothesis_id] = float(entry.get("score"))
            rationales[hypothesis_id] = str(entry.get("rationale") or "")

        order = [item.hypothesis_id for item in presentation.items]
        result.scores = scores
        result.ranking = ranking_from_scores(scores, order=order)
        result.usage = {
            key: ctx.llm.usage_totals.get(key, 0) - usage_at_start.get(key, 0)
            for key in ctx.llm.usage_totals
        }
        result.artifacts["model_outputs"] = response.record(include_messages=messages)
        result.artifacts["scores"] = {
            "method": self.name,
            "scores": scores,
            "rationales": rationales,
            "ranking": result.ranking,
            "model_ranking": parsed.get("ranking"),
            "label_to_hypothesis_id": presentation.label_to_id,
            "gold_id": ctx.instance.gold_hypothesis.id,
        }
        result.diagnostics = {"n_queries": 0, "n_eligible_papers": 0}
        result.errors = list(ctx.errors)
        return result
