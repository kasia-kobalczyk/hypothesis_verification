"""Human-readable per-instance diagnostic reports (IMPLEMENTATION_SPEC.md §26).

A failed case must be inspectable without rerunning the model, so the report is
rendered from the saved artifacts only. The consequence-graph sections (graph,
edge judgments) appear once milestone 2 populates those artifacts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.benchmark.loader import BenchmarkInstance
from src.benchmark.presentation import Presentation
from src.experiments.base import InstanceResult

_MAX_TEXT = 1200


def _truncate(text: Optional[str], limit: int = _MAX_TEXT) -> str:
    if not text:
        return ""
    text = str(text)
    return text if len(text) <= limit else text[:limit].rstrip() + " [...]"


def render_instance_report(
    instance: BenchmarkInstance,
    result: InstanceResult,
    presentation: Presentation,
    *,
    metrics: Optional[Dict[str, Any]] = None,
    dataset_status: str = "development",
) -> str:
    lines: List[str] = []
    add = lines.append

    add("# {} — {}".format(instance.id, result.method))
    add("")
    if dataset_status != "evaluation":
        add("> **Development set.** This case is for building and debugging the method. "
            "Whether the graph is sensible, the retrieved evidence relevant and the "
            "propagation correct are all fair questions here; aggregate accuracy is not "
            "evidence for the method.")
        add("")
    add("- status: **{}**".format(result.status))
    add("- discipline: {}".format(instance.discipline))
    add("- source DOI: `{}`".format(instance.source_doi))
    add(
        "- literature cutoff: **{}** (basis: {}{})".format(
            instance.cutoff_date.isoformat() if instance.cutoff_date else "UNRESOLVED",
            instance.cutoff_basis or "n/a",
            ", ambiguous" if instance.cutoff_ambiguous else "",
        )
    )
    if instance.cutoff_notes:
        add("- cutoff notes: {}".format(instance.cutoff_notes))
    if result.skip_reason:
        add("- skipped: {}".format(result.skip_reason))
    add("")

    add("## Question")
    add("")
    add(instance.question)
    add("")

    add("## Hypotheses (presentation order)")
    add("")
    for item in presentation.items:
        add("### {} — `{}`{}".format(item.label, item.hypothesis_id, "  **[GOLD]**" if item.gold else ""))
        add("")
        add(_truncate(item.text))
        add("")

    # ---- consequence graph (milestone 2, §26) --------------------------- #
    graph = result.artifacts.get("graph")
    if graph:
        stats = graph.get("stats", {})
        nodes = {n["id"]: n for n in graph.get("nodes", [])}
        edges = graph.get("edges", [])
        scores_block = result.artifacts.get("scores") or {}
        p_matrix = scores_block.get("p_matrix") or {}
        discrim = scores_block.get("discriminativeness") or {}
        evidence_by_node = (result.artifacts.get("evidence") or {}).get("by_node") or {}
        label_of = presentation.id_to_label

        add("## Consequence graph")
        add("")
        add("- {} node(s), {} edge(s) ({} hypothesis->proposition, {} proposition->proposition)".format(
            stats.get("n_nodes"), stats.get("n_edges"),
            stats.get("n_root_edges"), stats.get("n_chain_edges")))
        add("- {} empirically assessable, {} shared across hypotheses, {} merged, max depth {}".format(
            stats.get("n_assessable"), stats.get("n_shared"),
            stats.get("n_merged"), stats.get("max_depth")))
        for problem in graph.get("problems") or []:
            add("- **problem**: {}".format(problem))
        add("")

        for node_id in sorted(nodes, key=lambda k: (nodes[k].get("depth", 1), k)):
            node = nodes[node_id]
            add("### {} (depth {}{})".format(
                node_id, node.get("depth"),
                ", from {}".format(label_of.get(node.get("generation_origin_hypothesis"), "?"))
                if node.get("generation_origin_hypothesis") else ""))
            add("")
            add("> {}".format(_truncate(node.get("text"), 500)))
            add("")
            if node.get("merged_from"):
                add("- merged with: {} (shared consequence)".format(", ".join(node["merged_from"])))
            add("- empirically assessable: {}".format(node.get("empirically_assessable")))
            if node_id in discrim:
                add("- discriminativeness (spread of P(X|H) across candidates): **{}**".format(
                    discrim[node_id]))
            row = p_matrix.get(node_id) or {}
            if row:
                add("- P(X={} | H): {}".format(
                    node_id,
                    ", ".join("{}={}".format(label_of.get(h, h), v) for h, v in sorted(row.items()))))
            add("")
            incoming = [e for e in edges if e["target"] == node_id]
            if incoming:
                add("| from | kind | implication | rationale |")
                add("| --- | --- | --- | --- |")
                for edge in incoming:
                    source = edge["source"]
                    add("| {} | {} | `{}` | {} |".format(
                        label_of.get(source, source), edge.get("kind"),
                        edge.get("ordinal_strength"), _truncate(edge.get("rationale"), 160)))
                add("")
            assessment = (evidence_by_node.get(node_id) or {}).get("assessment")
            if assessment:
                add("**Evidence `{}`** ({} paper(s) shown){}".format(
                    assessment.get("evidence_label"), assessment.get("n_papers_shown"),
                    " — label enforced by the harness" if assessment.get("label_enforced_by_harness") else ""))
                add("")
                add("> {}".format(_truncate(assessment.get("rationale"), 600)))
                add("")
            elif (evidence_by_node.get(node_id) or {}).get("error"):
                add("**Not assessed**: {} (node left unobserved, marginalised out)".format(
                    evidence_by_node[node_id]["error"]))
                add("")

        contributions = scores_block.get("contributions") or []
        if contributions:
            add("### Per-hypothesis evidence contributions")
            add("")
            add("Each observed node contributes `log(P(X|H)*LR + 1 - P(X|H))` to its "
                "hypothesis. A contribution of 0 moved nothing.")
            add("")
            add("| node | hypothesis | P(X&#124;H) | evidence | log LR | contribution |")
            add("| --- | --- | --- | --- | --- | --- |")
            for item in sorted(contributions, key=lambda c: -abs(c.get("contribution", 0)))[:40]:
                add("| {} | {} | {} | `{}` | {} | {} |".format(
                    item.get("node_id"), label_of.get(item.get("hypothesis_id"), item.get("hypothesis_id")),
                    item.get("p_true_given_h"), item.get("evidence_label"),
                    item.get("log_likelihood_ratio"), item.get("contribution")))
            add("")
        for note in (scores_block.get("inference") or {}).get("notes") or []:
            add("- _{}_".format(note))
        add("")

    # ---- retrieval + evidence ------------------------------------------ #
    queries = (result.artifacts.get("queries") or {}).get("by_hypothesis") or {}
    retrieval = (result.artifacts.get("retrieval") or {}).get("by_hypothesis") or {}
    evidence = (result.artifacts.get("evidence") or {}).get("by_hypothesis") or {}
    # The consequence verifier keys these by node; its detail is rendered above.

    if queries or retrieval or evidence:
        add("## Retrieval and evidence")
        add("")
        for item in presentation.items:
            hid = item.hypothesis_id
            add("### {} — `{}`{}".format(item.label, hid, "  **[GOLD]**" if item.gold else ""))
            add("")
            entry = queries.get(hid) or {}
            if entry.get("error"):
                add("- query generation failed: `{}`".format(entry["error"]))
            for query in entry.get("queries", []):
                add("- query: `{}`".format(query))
            add("")

            for query_record in (retrieval.get(hid) or {}).get("queries", []):
                if query_record.get("error"):
                    add(
                        "- **retrieval error** for `{}`: {} ({})".format(
                            query_record.get("query"),
                            query_record.get("error"),
                            query_record.get("error_type"),
                        )
                    )
                    continue
                add(
                    "- `{}` -> {} eligible / {} excluded (cache: {})".format(
                        query_record.get("query"),
                        query_record.get("n_eligible"),
                        query_record.get("n_excluded"),
                        query_record.get("cache_status"),
                    )
                )
                for paper in query_record.get("eligible", [])[:10]:
                    add(
                        "    - {} ({}) — `{}`".format(
                            _truncate(paper.get("title"), 160),
                            paper.get("publication_date") or paper.get("year"),
                            paper.get("paper_id"),
                        )
                    )
            add("")

            assessment = (evidence.get(hid) or {}).get("assessment")
            if assessment:
                add("**Evidence judgment:** `{}`".format(assessment.get("evidence_label")))
                add("")
                add("- score: {}".format(assessment.get("score")))
                add("- papers shown: {}".format(assessment.get("n_papers_shown")))
                add("- key papers: {}".format(", ".join(assessment.get("key_papers") or []) or "none"))
                add("- independence: {}".format(assessment.get("independence_note")))
                add("")
                add("> {}".format(_truncate(assessment.get("rationale"), 800)))
                add("")
            elif (evidence.get(hid) or {}).get("error"):
                add("**Evidence judgment failed:** {}".format(evidence[hid]["error"]))
                add("")

    # ---- scores --------------------------------------------------------- #
    scores_artifact = result.artifacts.get("scores") or {}
    rationales = scores_artifact.get("rationales") or {}
    add("## Scores")
    add("")
    if result.scores:
        # A benchmark without gold (the explanatory-hypothesis pilot) gets no gold
        # column at all rather than an empty one, so a reader cannot mistake the
        # blanks for "every candidate was judged wrong".
        gold_id = instance.gold_hypothesis.id if instance.has_gold else None
        add("| rank | label | hypothesis | score |{}".format(" gold |" if gold_id else ""))
        add("| --- | --- | --- | --- |{}".format(" --- |" if gold_id else ""))
        for position, hid in enumerate(result.ranking, start=1):
            add(
                "| {} | {} | `{}` | {:.4g} |{}".format(
                    position,
                    presentation.id_to_label.get(hid, "?"),
                    hid,
                    result.scores.get(hid, float("nan")),
                    (" {} |".format("**yes**" if hid == gold_id else "")) if gold_id else "",
                )
            )
        add("")
        if rationales:
            add("### Rationales")
            add("")
            for hid in result.ranking:
                if rationales.get(hid):
                    add("- `{}`: {}".format(hid, _truncate(rationales[hid], 600)))
            add("")
    else:
        add("_No scores were produced._")
        add("")
        if scores_artifact.get("partial_scores"):
            add("Partial scores (not used for ranking): `{}`".format(scores_artifact["partial_scores"]))
            add("")

    if not instance.has_gold:
        add(
            "- no gold hypothesis: this benchmark carries no labelled winner, so "
            "ranking-accuracy metrics are **not computed**. The ranking above is a "
            "record of what the method did, not a score."
        )
    else:
        add("- gold hypothesis: `{}` (label {})".format(
            instance.gold_hypothesis.id,
            presentation.id_to_label.get(instance.gold_hypothesis.id, "?"),
        ))
    if metrics and instance.has_gold:
        if metrics.get("pair_accuracy") is not None:
            add(
                "- **pair accuracy (primary, frozen pairs): {:.3f}** "
                "({} win, {} tie, of {} scored pairs)".format(
                    metrics["pair_accuracy"], metrics.get("pair_wins"),
                    metrics.get("pair_ties"), metrics.get("n_pairs_scored"),
                )
            )
        elif metrics.get("pair_status") == "no_evaluable_pair":
            add(
                "- **pair accuracy (primary): excluded** — no negative passed R2 "
                "screening, so this instance has no evaluable pair. It is reported "
                "in the secondary listwise metrics only."
            )
        elif metrics.get("n_pairs_frozen") is not None:
            add("- pair accuracy (primary): not available ({} frozen pair(s))".format(
                metrics.get("n_pairs_frozen")))
        add("- gold rank (secondary, listwise): {}".format(metrics.get("gold_rank")))
        add("- top-1 strict (secondary): {}".format(metrics.get("top1_strict")))
        add("- pairwise accuracy over all negatives (secondary): {}".format(
            metrics.get("pairwise_accuracy_all_negatives")))
    add("")

    if result.errors:
        add("## Errors")
        add("")
        for error in result.errors:
            add("- `{}` in {}: {}".format(error.get("type"), error.get("where"), error.get("message")))
        add("")

    if result.diagnostics:
        add("## Diagnostics")
        add("")
        for key in sorted(result.diagnostics):
            add("- {}: {}".format(key, result.diagnostics[key]))
        add("")

    return "\n".join(lines)


def render_run_summary(summary: Dict[str, Any]) -> str:
    lines = ["# Run summary: {}".format(summary.get("run_id")), ""]
    lines.append("- method: {}".format(summary.get("method")))
    if summary.get("interpretation_warning"):
        lines.append("- **{}**".format(summary["interpretation_warning"]))
    lines.append("- dataset: {}".format(summary.get("dataset")))
    lines.append("- llm: {} / {}".format(summary.get("llm_provider"), summary.get("llm_deployment")))
    lines.append("- instances: {}".format(summary.get("n_instances")))
    lines.append("")
    pairs = summary.get("pairs") or {}
    if pairs.get("present"):
        lines.append("- frozen pairs: {} retained of {} screened".format(
            pairs.get("n_pairs_retained"), pairs.get("n_pairs_screened")))
        excluded = (summary.get("metrics") or {}).get("instances_no_evaluable_pair") or []
        if excluded:
            lines.append(
                "- excluded from the primary metric (no evaluable pair): {}".format(
                    ", ".join(excluded)
                )
            )
    else:
        lines.append("- frozen pairs: none (primary metric unavailable)")
    lines.append("")

    metrics = summary.get("metrics") or {}
    primary_keys = ("pair_accuracy", "pair_accuracy_macro", "n_pairs_evaluated", "n_instances_with_pairs")
    lines.append("## Primary metrics (frozen gold-vs-negative pairs)")
    lines.append("")
    for key in primary_keys:
        lines.append("- {}: {}".format(key, metrics.get(key)))
    lines.append("")
    lines.append("## Secondary metrics (listwise over all candidates)")
    lines.append("")
    for key, value in metrics.items():
        if key in primary_keys or key == "primary_metric":
            continue
        lines.append("- {}: {}".format(key, value))
    lines.append("")
    return "\n".join(lines)
