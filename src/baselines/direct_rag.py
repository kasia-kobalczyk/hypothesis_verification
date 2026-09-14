"""Baseline 2: direct RAG verifier (IMPLEMENTATION_SPEC.md §11).

For each candidate hypothesis: generate outcome-neutral queries, retrieve
eligible pre-cutoff literature through the *same* service the consequence-graph
method will use, assess the retrieved set jointly, then rank.

Two rules from the spec are load-bearing here:

* a retrieval or model failure is an **error**, never `no_evidence` (§29). If any
  hypothesis cannot be assessed, the instance is reported as `error` with its
  partial artifacts kept, rather than ranked from a partial score vector.
* queries are generated from the question and the hypothesis only, and are
  frozen before any retrieval result is seen (§17) — there is no re-query loop
  conditioned on whether the returned evidence was favourable.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.common.errors import (
    CacheMissError,
    LLMError,
    LLMParseError,
    MissingCutoffError,
    ProviderError,
    TemporalLeakError,
)
from src.common.logging_utils import get_logger
from src.experiments.base import InstanceContext, InstanceResult, Method
from src.experiments.metrics import ranking_from_scores
from src.inference.parameters import EVIDENCE_LABELS, normalise_evidence_label
from src.literature.base import Paper
from src.literature.dedup import deduplicate
from src.literature.query_policy import (
    RetrievalAttempt,
    lexical_ladder,
    shape_query,
)

LOGGER = get_logger("baselines.direct_rag")

NO_LITERATURE_PLACEHOLDER = (
    "[no eligible literature was retrieved for this hypothesis]\n"
    "This means nothing relevant was found within the available record, not that "
    "the hypothesis was contradicted."
)


class DirectRag(Method):
    name = "direct_rag"
    requires_literature = True

    def prompt_versions(self) -> List[str]:
        cfg = self.config.baselines.direct_rag
        return [cfg.query_prompt_version, cfg.assess_prompt_version]

    # ------------------------------------------------------------------ #
    def run_instance(self, ctx: InstanceContext) -> InstanceResult:
        cfg = self.config.baselines.direct_rag
        policy = self.config.retrieval.query_policy
        presentation = ctx.presentation
        result = InstanceResult(instance_id=ctx.instance.id, method=self.name)
        # Token usage for this instance only (the client accumulates run totals).
        usage_at_start = dict(ctx.llm.usage_totals)

        query_template = ctx.prompts.get(cfg.query_prompt_version)
        assess_template = ctx.prompts.get(cfg.assess_prompt_version)

        queries_artifact: Dict[str, Any] = {
            "method": self.name,
            "prompt_version": cfg.query_prompt_version,
            "prompt_record": query_template.record(),
            "queries_per_hypothesis": cfg.queries_per_hypothesis,
            "query_policy": self.config.retrieval.query_policy.model_dump(mode="json"),
            "by_hypothesis": {},
        }
        retrieval_artifact: Dict[str, Any] = {"by_hypothesis": {}}
        evidence_artifact: Dict[str, Any] = {
            "method": self.name,
            "prompt_version": cfg.assess_prompt_version,
            "prompt_record": assess_template.record(),
            "ranking_signal": cfg.ranking_signal,
            "ordinal_mappings": ctx.mappings.record(),
            "by_hypothesis": {},
        }
        model_outputs: Dict[str, Any] = {"query_generation": {}, "assessment": {}}

        scores: Dict[str, float] = {}
        ordinal_scores: Dict[str, float] = {}
        llm_scores: Dict[str, float] = {}
        n_queries = 0
        n_eligible = 0
        n_excluded = 0
        n_informative = 0
        n_no_evidence = 0
        n_retrieval_errors = 0
        n_searches = 0
        n_zero_result_searches = 0
        n_queries_needing_backoff = 0
        n_queries_empty_after_backoff = 0
        failed: List[str] = []

        for item in presentation.items:
            hid = item.hypothesis_id

            # -- 1. outcome-neutral queries, frozen before retrieval -------- #
            try:
                queries, query_response = self._generate_queries(ctx, item.text, query_template)
            except (LLMParseError, LLMError) as exc:
                ctx.record_error("direct_rag.query_generation", exc, hypothesis_id=hid)
                failed.append(hid)
                queries_artifact["by_hypothesis"][hid] = {"label": item.label, "error": str(exc)}
                continue
            model_outputs["query_generation"][hid] = query_response
            queries_artifact["by_hypothesis"][hid] = {
                "label": item.label,
                "queries": [s.query for s in queries],
                "shaping": [s.record() for s in queries],
            }
            n_queries += len(queries)

            # -- 2. retrieval through the shared temporal service ----------- #
            papers: List[Paper] = []
            seen_ids = set()
            per_query: List[Dict[str, Any]] = []
            retrieval_failed = False

            for shaped_query in queries:
                # Ladder: the shaped query, then deterministic shorter variants,
                # tried only while the PROVIDER returns nothing. The trigger is
                # the absence of results, never their content, so backoff cannot
                # chase a favourable outcome.
                ladder = [shaped_query.query] + lexical_ladder(
                    shaped_query.query,
                    min_terms=policy.min_terms,
                    steps=policy.backoff_steps,
                )
                attempts: List[RetrievalAttempt] = []
                record = None
                failed_here = False

                for step, candidate in enumerate(ladder):
                    try:
                        record = ctx.literature.search_with_record(candidate, top_k=cfg.top_k)
                    except (TemporalLeakError, MissingCutoffError):
                        # A leak invalidates the experiment and a missing cutoff
                        # means this instance should never have run: both
                        # propagate. Catching their base class here would
                        # silently downgrade a leak to a failed instance.
                        raise
                    except (ProviderError, CacheMissError) as exc:
                        # Explicitly NOT `no_evidence`: the literature was never consulted.
                        ctx.record_error(
                            "direct_rag.retrieval", exc, hypothesis_id=hid, query=candidate
                        )
                        n_retrieval_errors += 1
                        retrieval_failed = True
                        failed_here = True
                        per_query.append({
                            "query": candidate, "step": step,
                            "error": str(exc), "error_type": type(exc).__name__,
                            "shaping": shaped_query.record(),
                        })
                        break

                    attempts.append(RetrievalAttempt(
                        query=candidate, step=step,
                        n_results=record.n_normalised, n_eligible=record.n_eligible,
                    ))
                    n_excluded += record.n_excluded
                    n_searches += 1
                    if record.n_normalised > 0:
                        break
                    n_zero_result_searches += 1

                if failed_here or record is None:
                    continue

                if len(attempts) > 1:
                    n_queries_needing_backoff += 1
                    ctx.event_log.decision(
                        "lexical_backoff",
                        instance_id=ctx.instance.id, hypothesis_id=hid,
                        original=shaped_query.query, steps=len(attempts) - 1,
                        final_query=attempts[-1].query, n_results=attempts[-1].n_results,
                    )
                if attempts[-1].n_results == 0:
                    n_queries_empty_after_backoff += 1

                summary = self._retrieval_summary(record)
                summary["shaping"] = shaped_query.record()
                summary["attempts"] = [a.record() for a in attempts]
                per_query.append(summary)
                for paper in record.eligible:
                    if paper.paper_id not in seen_ids:
                        seen_ids.add(paper.paper_id)
                        papers.append(paper)

            retrieval_artifact["by_hypothesis"][hid] = {
                "label": item.label,
                "queries": per_query,
                "n_unique_eligible": len(papers),
            }

            if retrieval_failed:
                failed.append(hid)
                continue

            # Collapse preprint/journal versions across queries (§6, §21).
            merged = deduplicate(papers, self.config.literature.dedup, event_log=ctx.event_log)
            papers = merged.papers[: cfg.max_papers_in_prompt]
            retrieval_artifact["by_hypothesis"][hid]["n_after_cross_query_dedup"] = len(merged.papers)
            retrieval_artifact["by_hypothesis"][hid]["duplicate_groups"] = merged.groups
            retrieval_artifact["by_hypothesis"][hid]["papers_shown"] = [
                p.model_dump(mode="json", exclude={"raw"}) for p in papers
            ]
            n_eligible += len(papers)

            # -- 3. joint evidence assessment ------------------------------- #
            try:
                assessment, assess_response = self._assess(ctx, item.text, papers, assess_template)
            except (LLMParseError, LLMError) as exc:
                ctx.record_error("direct_rag.assessment", exc, hypothesis_id=hid)
                failed.append(hid)
                evidence_artifact["by_hypothesis"][hid] = {"label": item.label, "error": str(exc)}
                continue

            model_outputs["assessment"][hid] = assess_response
            evidence_artifact["by_hypothesis"][hid] = {
                "label": item.label,
                "n_papers": len(papers),
                "assessment": assessment,
            }

            if assessment["evidence_label"] == "no_evidence":
                n_no_evidence += 1
            else:
                n_informative += 1

            # Both rules are always computed and saved; `ranking_signal` only
            # decides which one ranks. The primary rule is the ordinal evidence
            # label mapped through the centralised log-LR table.
            ordinal_scores[hid] = ctx.mappings.evidence_value(assessment["evidence_label"])
            llm_scores[hid] = float(assessment["score"])
            scores[hid] = (
                ordinal_scores[hid] if cfg.ranking_signal == "ordinal_map" else llm_scores[hid]
            )

        order = [item.hypothesis_id for item in presentation.items]
        result.artifacts["queries"] = queries_artifact
        result.artifacts["retrieval"] = retrieval_artifact
        result.artifacts["evidence"] = evidence_artifact
        result.artifacts["model_outputs"] = model_outputs
        result.usage = {
            key: ctx.llm.usage_totals.get(key, 0) - usage_at_start.get(key, 0)
            for key in ctx.llm.usage_totals
        }
        result.errors = list(ctx.errors)
        result.diagnostics = {
            "n_queries": n_queries,
            "n_searches": n_searches,
            "n_zero_result_searches": n_zero_result_searches,
            "n_queries_needing_backoff": n_queries_needing_backoff,
            "n_queries_empty_after_backoff": n_queries_empty_after_backoff,
            "query_recall": (
                (n_queries - n_queries_empty_after_backoff) / n_queries if n_queries else None
            ),
            "n_eligible_papers": n_eligible,
            "n_excluded_papers": n_excluded,
            "n_informative_assessments": n_informative,
            "n_no_evidence_assessments": n_no_evidence,
            "n_retrieval_errors": n_retrieval_errors,
            "n_failed_hypotheses": len(failed),
        }

        if failed:
            # Partial score vectors are not comparable across hypotheses.
            result.status = "error"
            result.scores = {}
            result.ranking = []
            result.artifacts["scores"] = {
                "method": self.name,
                "status": "error",
                "failed_hypotheses": failed,
                "partial_scores": scores,
                "partial_scores_ordinal_map": ordinal_scores,
                "partial_scores_llm": llm_scores,
                "gold_id": ctx.instance.gold_hypothesis.id,
            }
            LOGGER.warning(
                "%s: %d/%d hypotheses could not be assessed; instance left unscored",
                ctx.instance.id, len(failed), len(presentation.items),
            )
            return result

        result.scores = scores
        result.ranking = ranking_from_scores(scores, order=order)
        result.artifacts["scores"] = {
            "method": self.name,
            "scores": scores,
            "ranking": result.ranking,
            "ranking_signal": cfg.ranking_signal,
            "scores_ordinal_map": ordinal_scores,
            "scores_llm": llm_scores,
            "ranking_ordinal_map": ranking_from_scores(ordinal_scores, order=order),
            "ranking_llm": ranking_from_scores(llm_scores, order=order),
            "n_tied_at_top": sum(1 for v in scores.values() if v == max(scores.values())) if scores else 0,
            "evidence_labels": {
                hid: evidence_artifact["by_hypothesis"][hid]["assessment"]["evidence_label"]
                for hid in scores
            },
            "label_to_hypothesis_id": presentation.label_to_id,
            "gold_id": ctx.instance.gold_hypothesis.id,
        }
        return result

    # ------------------------------------------------------------------ #
    def _generate_queries(self, ctx: InstanceContext, hypothesis_text: str, template) -> Any:
        cfg = self.config.baselines.direct_rag
        policy = self.config.retrieval.query_policy
        render_values = {
            "question": ctx.instance.question,
            "hypothesis": hypothesis_text,  # verbatim
            "n_queries": cfg.queries_per_hypothesis,
        }
        if "$max_terms" in template.text:
            render_values["max_terms"] = policy.max_terms
        prompt = template.render(**render_values)
        messages = [{"role": "user", "content": prompt}]

        def validator(parsed: Dict[str, Any]) -> None:
            queries = parsed.get("queries")
            if not isinstance(queries, list) or not queries:
                raise ValueError("missing 'queries' list")
            if not all(isinstance(q, str) and q.strip() for q in queries):
                raise ValueError("'queries' must be non-empty strings")

        response = ctx.llm.complete_json(
            messages,
            purpose="direct_rag.query_generation",
            prompt_version=cfg.query_prompt_version,
            validator=validator,
        )
        raw_queries = [q.strip() for q in (response.parsed or {}).get("queries", [])]
        raw_queries = raw_queries[: cfg.queries_per_hypothesis]

        # The prompt asks for short, outcome-neutral queries; this enforces it.
        shaped = [
            shape_query(
                q,
                max_terms=policy.max_terms,
                direction_words=policy.direction_words,
                stopwords=policy.stopwords,
                strip_direction_words=policy.strip_direction_words,
                protected_phrases=policy.protected_phrases,
            )
            for q in raw_queries
        ]
        for item in shaped:
            if item.changed:
                ctx.event_log.decision(
                    "query_shaped",
                    instance_id=ctx.instance.id,
                    original=item.original,
                    query=item.query,
                    removed_direction_words=item.removed_direction_words,
                    truncated_from=item.truncated_from,
                )
        return shaped, response.record(include_messages=messages)

    def _assess(
        self,
        ctx: InstanceContext,
        hypothesis_text: str,
        papers: List[Paper],
        template,
    ) -> Any:
        cfg = self.config.baselines.direct_rag
        # `render` re-checks eligibility for every record before it becomes text.
        literature = (
            ctx.literature.render(papers, max_papers=cfg.max_papers_in_prompt)
            if papers
            else NO_LITERATURE_PLACEHOLDER
        )
        prompt = template.render(
            question=ctx.instance.question,
            hypothesis=hypothesis_text,  # verbatim
            literature=literature,
            labels=", ".join(EVIDENCE_LABELS),
        )
        messages = [{"role": "user", "content": prompt}]

        def validator(parsed: Dict[str, Any]) -> None:
            if normalise_evidence_label(parsed.get("evidence_label")) is None:
                raise ValueError("unknown evidence_label {!r}".format(parsed.get("evidence_label")))
            try:
                float(parsed.get("score"))
            except (TypeError, ValueError):
                raise ValueError("non-numeric score")

        response = ctx.llm.complete_json(
            messages,
            purpose="direct_rag.assessment",
            prompt_version=cfg.assess_prompt_version,
            validator=validator,
        )
        parsed = response.parsed or {}
        model_label = normalise_evidence_label(parsed.get("evidence_label"))
        label = model_label
        enforced = False
        if cfg.enforce_no_evidence_without_papers and label != "no_evidence" and not papers:
            # Guard the §29 invariant from the other side: a model must not
            # claim support when nothing was retrieved. Only the label is
            # rewritten; the model's score is left as reported, so a run using
            # `ranking_signal: llm_score` stays interpretable.
            ctx.event_log.decision(
                "assessment_label_corrected",
                instance_id=ctx.instance.id,
                original=label,
                corrected="no_evidence",
                reason="no eligible literature was retrieved",
            )
            label = "no_evidence"
            enforced = True
        assessment = {
            "evidence_label": label,
            "model_evidence_label": model_label,
            "label_enforced_by_harness": enforced,
            "score": float(parsed.get("score")),
            "rationale": parsed.get("rationale"),
            "key_papers": parsed.get("key_papers") or [],
            "independence_note": parsed.get("independence_note"),
            "n_papers_shown": len(papers),
        }
        return assessment, response.record(include_messages=messages)

    @staticmethod
    def _retrieval_summary(record: Any) -> Dict[str, Any]:
        return {
            "query": record.query,
            "cache_status": record.cache_status,
            "cutoff_date": record.cutoff_date.isoformat() if record.cutoff_date else None,
            "n_normalised": record.n_normalised,
            "n_eligible": record.n_eligible,
            "n_excluded": record.n_excluded,
            "n_duplicates_collapsed": record.n_duplicates_collapsed,
            "notes": list(record.notes),
            "eligible": [p.model_dump(mode="json", exclude={"raw"}) for p in record.eligible],
            # Post-cutoff records: retained for diagnosis, never shown to a model.
            "excluded": [
                {
                    "paper_id": p.paper_id,
                    "title": p.title,
                    "eligible_date": p.eligible_date.isoformat() if p.eligible_date else None,
                    "reason": p.exclusion_reason,
                }
                for p in record.excluded
            ],
        }
