"""Consequence-based hypothesis verification (IMPLEMENTATION_SPEC.md §33).

Four stages, in a fixed order that the code enforces:

  1. build and FREEZE the consequence graph — no literature has been touched;
  2. generate outcome-neutral queries per assessable proposition and retrieve
     eligible pre-cutoff literature through the same service the baselines use;
  3. assess each proposition's retrieved set jointly, as an ordinal label;
  4. propagate the evidence through the graph to a posterior over hypotheses.

The ordering is the scientific point. Steps 2-4 can only observe a graph that is
already closed, so no consequence can be added, dropped or re-worded after its
literature outcome is known (§13, §35.6). Stage 1 never sees a paper; stage 3
never sees a hypothesis.

A retrieval or model failure is an error, never `no_evidence` (§29). Unlike
`direct_rag`, a failure on one proposition does not sink the instance: the node
is left unobserved and marginalises out exactly, which is the honest treatment —
but the count is reported, because many silent drop-outs would hollow out a
result.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.common.errors import (
    CacheMissError,
    LLMError,
    LLMParseError,
    MissingCutoffError,
    ProviderError,
    TemporalLeakError,
)
from src.common.logging_utils import get_logger
from src.evidence.assess import assess_proposition
from src.evidence.queries import generate_queries
from src.experiments.base import InstanceContext, InstanceResult, Method
from src.experiments.metrics import ranking_from_scores
from src.graph.generate import (
    CHAIN_EDGE_PROMPT,
    ROOT_EDGE_PROMPT,
    build_graph,
)
from src.inference.bayes import discriminativeness, score_hypotheses
from src.literature.base import Paper
from src.literature.dedup import deduplicate
from src.literature.query_policy import RetrievalAttempt, lexical_ladder

LOGGER = get_logger("methods.consequence_graph")


class ConsequenceGraphVerifier(Method):
    name = "consequence_graph"
    requires_literature = True

    def prompt_versions(self) -> List[str]:
        from src.evidence.assess import ASSESS_PROMPT
        from src.evidence.queries import QUERY_PROMPT

        return [self.config.graph.generate_prompt, ROOT_EDGE_PROMPT, CHAIN_EDGE_PROMPT,
                QUERY_PROMPT, self.config.evidence.assess_prompt]

    # ------------------------------------------------------------------ #
    def run_instance(self, ctx: InstanceContext) -> InstanceResult:
        config = self.config
        policy = config.retrieval.query_policy
        result = InstanceResult(instance_id=ctx.instance.id, method=self.name)

        # -- 1. graph, frozen before anything looks at the literature ----- #
        try:
            graph, graph_artifacts = build_graph(
                instance_id=ctx.instance.id, question=ctx.instance.question,
                presentation=ctx.presentation, config=config, llm=ctx.llm,
                prompts=ctx.prompts, event_log=ctx.event_log)
        except (LLMParseError, LLMError) as exc:
            ctx.record_error("consequence_graph.build", exc)
            result.status = "error"
            result.errors = list(ctx.errors)
            return result

        result.artifacts["graph"] = graph_artifacts["graph"]
        result.artifacts["edge_judgments"] = {
            "root_edges": [e.model_dump(mode="json") for e in graph.edges if e.kind == "root"],
            "chain_edges": [e.model_dump(mode="json") for e in graph.edges if e.kind == "chain"],
            "prompt_versions": graph_artifacts["prompt_versions"],
            "merge": graph_artifacts.get("merge"),
            "generation_errors": graph_artifacts.get("errors", []),
        }
        for problem in graph.validate():
            ctx.event_log.decision("graph_problem", instance_id=ctx.instance.id, problem=problem)

        assessable = graph.assessable_nodes()
        LOGGER.info("%s: graph %s, %d assessable node(s)",
                    ctx.instance.id, graph.stats(), len(assessable))

        # -- 2/3. retrieve and assess each proposition -------------------- #
        queries_artifact: Dict[str, Any] = {"by_node": {}, "queries_per_node": config.retrieval.queries_per_node}
        retrieval_artifact: Dict[str, Any] = {"by_node": {}}
        evidence_artifact: Dict[str, Any] = {"by_node": {}}
        model_outputs: Dict[str, Any] = {"query_generation": {}, "assessment": {}}

        evidence: Dict[str, str] = {}
        counters = dict(n_queries=0, n_searches=0, n_zero_result_searches=0,
                        n_queries_needing_backoff=0, n_eligible_papers=0, n_excluded_papers=0,
                        n_retrieval_errors=0, n_assessment_errors=0,
                        n_informative_assessments=0, n_no_evidence_assessments=0,
                        n_nodes_unobserved=0)

        for node in assessable:
            try:
                shaped, call = generate_queries(
                    node.text, config=config, llm=ctx.llm, prompts=ctx.prompts,
                    event_log=ctx.event_log)
            except (LLMParseError, LLMError) as exc:
                ctx.record_error("consequence_graph.query_generation", exc, node_id=node.id)
                counters["n_nodes_unobserved"] += 1
                queries_artifact["by_node"][node.id] = {"error": str(exc)}
                continue
            model_outputs["query_generation"][node.id] = call
            queries_artifact["by_node"][node.id] = {
                "text": node.text, "queries": [s.query for s in shaped],
                "shaping": [s.record() for s in shaped],
            }
            counters["n_queries"] += len(shaped)

            papers: List[Paper] = []
            seen: set = set()
            per_query: List[Dict[str, Any]] = []
            failed = False

            for shaped_query in shaped:
                ladder = [shaped_query.query] + lexical_ladder(
                    shaped_query.query, min_terms=policy.min_terms, steps=policy.backoff_steps)
                attempts: List[RetrievalAttempt] = []
                record = None
                for step, candidate in enumerate(ladder):
                    try:
                        record = ctx.literature.search_with_record(
                            candidate, top_k=config.literature.top_k)
                    except (TemporalLeakError, MissingCutoffError):
                        raise  # a leak invalidates the experiment; never downgraded
                    except (ProviderError, CacheMissError) as exc:
                        ctx.record_error("consequence_graph.retrieval", exc,
                                         node_id=node.id, query=candidate)
                        counters["n_retrieval_errors"] += 1
                        failed = True
                        per_query.append({"query": candidate, "step": step, "error": str(exc)})
                        break
                    attempts.append(RetrievalAttempt(
                        query=candidate, step=step, n_results=record.n_normalised,
                        n_eligible=record.n_eligible))
                    counters["n_searches"] += 1
                    counters["n_excluded_papers"] += record.n_excluded
                    if record.n_normalised > 0:
                        break
                    counters["n_zero_result_searches"] += 1

                if record is None:
                    continue
                if len(attempts) > 1:
                    counters["n_queries_needing_backoff"] += 1
                summary = {
                    "query": shaped_query.query,
                    "attempts": [a.record() for a in attempts],
                    "n_eligible": record.n_eligible,
                    "eligible": [p.model_dump(mode="json", exclude={"raw"}) for p in record.eligible],
                    "excluded": [
                        {"paper_id": p.paper_id, "title": p.title, "reason": p.exclusion_reason}
                        for p in record.excluded
                    ],
                }
                per_query.append(summary)
                for paper in record.eligible:
                    if paper.paper_id not in seen:
                        seen.add(paper.paper_id)
                        papers.append(paper)

            merged = deduplicate(papers, config.literature.dedup, event_log=ctx.event_log)
            papers = merged.papers[: config.baselines.direct_rag.max_papers_in_prompt]
            counters["n_eligible_papers"] += len(papers)
            retrieval_artifact["by_node"][node.id] = {
                "queries": per_query, "n_unique_eligible": len(merged.papers),
                "duplicate_groups": merged.groups,
                "papers_shown": [p.model_dump(mode="json", exclude={"raw"}) for p in papers],
            }

            if failed and not papers:
                # Retrieval never succeeded: leave the node unobserved rather
                # than call it `no_evidence` (§29).
                counters["n_nodes_unobserved"] += 1
                evidence_artifact["by_node"][node.id] = {
                    "text": node.text, "error": "retrieval failed; node left unobserved"}
                continue

            try:
                assessment, call = assess_proposition(
                    node.text, papers, literature_tool=ctx.literature, llm=ctx.llm,
                    prompts=ctx.prompts, max_papers=config.baselines.direct_rag.max_papers_in_prompt,
                    enforce_no_evidence_without_papers=(
                        config.baselines.direct_rag.enforce_no_evidence_without_papers),
                    event_log=ctx.event_log,
                    assess_prompt=config.evidence.assess_prompt)
            except (LLMParseError, LLMError) as exc:
                ctx.record_error("consequence_graph.assessment", exc, node_id=node.id)
                counters["n_assessment_errors"] += 1
                counters["n_nodes_unobserved"] += 1
                evidence_artifact["by_node"][node.id] = {"text": node.text, "error": str(exc)}
                continue

            model_outputs["assessment"][node.id] = call
            evidence_artifact["by_node"][node.id] = {"text": node.text, "assessment": assessment}
            evidence[node.id] = assessment["evidence_label"]
            if assessment["evidence_label"] == "no_evidence":
                counters["n_no_evidence_assessments"] += 1
            else:
                counters["n_informative_assessments"] += 1

        # -- 4. propagate -------------------------------------------------- #
        propagation = score_hypotheses(
            graph, evidence, mappings=ctx.mappings,
            multi_parent_rule=config.inference.multi_parent_rule,
            parent_false_baseline=config.inference.parent_false_baseline)

        order = [item.hypothesis_id for item in ctx.presentation.items]
        result.scores = dict(propagation.scores)
        result.ranking = ranking_from_scores(propagation.scores, order=order)
        result.artifacts["queries"] = queries_artifact
        result.artifacts["retrieval"] = retrieval_artifact
        result.artifacts["evidence"] = evidence_artifact
        result.artifacts["model_outputs"] = model_outputs
        result.artifacts["scores"] = {
            "method": self.name,
            "scores": result.scores,
            "ranking": result.ranking,
            "log_scores": propagation.log_scores,
            "evidence_labels": evidence,
            "p_matrix": propagation.record()["p_matrix"],
            "discriminativeness": discriminativeness(propagation.p_matrix),
            "contributions": propagation.record()["contributions"],
            "inference": {
                "prior": config.inference.prior,
                "multi_parent_rule": config.inference.multi_parent_rule,
                "parent_false_baseline": config.inference.parent_false_baseline,
                "ordinal_mappings": ctx.mappings.record(),
                "notes": propagation.notes,
            },
            "label_to_hypothesis_id": ctx.presentation.label_to_id,
            "gold_id": ctx.instance.gold_hypothesis.id,
        }
        # Standing diagnostic (DECISIONS #33): evidence yield and contradiction rate
        # split by the hypothesis a node was generated from. The broad assessor made
        # negative-origin nodes informative 27% of the time against 17% for
        # gold-origin -- implicit bridging favours generic fabricated claims -- so
        # this asymmetry is tracked on every run rather than rediscovered.
        gold_id = ctx.instance.gold_hypothesis.id
        CONTRA = {"strong_contradiction", "contradiction", "weak_contradiction"}
        by_origin: Dict[str, Dict[str, int]] = {
            "gold": {"nodes": 0, "informative": 0, "contradiction": 0},
            "negative": {"nodes": 0, "informative": 0, "contradiction": 0},
        }
        for node in graph.nodes.values():
            scope = "gold" if node.generation_origin_hypothesis == gold_id else "negative"
            by_origin[scope]["nodes"] += 1
            label = (evidence_artifact["by_node"].get(node.id, {})
                     .get("assessment", {}) or {}).get("evidence_label")
            if label and label != "no_evidence":
                by_origin[scope]["informative"] += 1
                if label in CONTRA:
                    by_origin[scope]["contradiction"] += 1
        for scope, tally in by_origin.items():
            denom = max(tally["nodes"], 1)
            tally["informative_rate"] = round(tally["informative"] / denom, 4)
            tally["contradiction_rate"] = round(tally["contradiction"] / denom, 4)

        stats = graph.stats()
        result.diagnostics = dict(counters)
        result.artifacts["yield_by_origin"] = by_origin
        result.diagnostics.update({
            "n_graph_nodes": stats["n_nodes"],
            "n_searchable_nodes": stats["n_assessable"],
            "n_shared_nodes": stats["n_shared"],
            "n_merged_nodes": stats["n_merged"],
            "n_graph_edges": stats["n_edges"],
            "n_nodes_with_evidence": len(evidence),
            "n_nodes_with_informative_evidence": counters["n_informative_assessments"],
        })
        result.errors = list(ctx.errors)
        if not evidence:
            result.status = "error"
            result.scores = {}
            result.ranking = []
            result.artifacts["scores"]["status"] = "no proposition could be assessed"
            LOGGER.warning("%s: no proposition assessed; instance left unscored", ctx.instance.id)
        return result
