"""Human review packet for the frozen graph pilot (BENCH-GRAPH-REVIEW-001).

Deterministic and LLM-free. Builds, from the *preserved* pilot archive:

  benchmark/review/graph_pilot_001/
    review_set_full.jsonl        one record per score-moving node
    review_set_priority.jsonl    the high-influence subset (~80% of influence)
    review_full.md               every score-moving node, grouped by case
    review_priority.md           the priority subset, by descending influence
    hidden_case_context.md/.json post-hoc benchmark annotations, kept apart
    stats.json                   review-set statistics for the executor report

Design rules this script enforces rather than documents:

* **Selection is structural.** Nodes are chosen from verifier score contributions
  alone. The post-hoc auditor files are not even loaded until selection is done,
  so no auditor label can decide what a human reviews.
* **The verifier's own scoring code reproduces the frozen scores.** Each case graph
  is rebuilt from `graph.json` and re-scored with `src.inference.bayes`; the build
  aborts if any score, node probability or contribution disagrees with the frozen
  `scores.json`.
* **Evidence text is what the assessor saw, verbatim.** It is cut out of the
  rendered `evidence_assess_v2` prompt in `events.jsonl`, not re-rendered from
  metadata, and cross-checked against `retrieval.json`.
* **Verifier output and hidden benchmark context never share a field.** Anything
  derived from the hidden annotations lives under `posthoc_automated_audit` or in
  the separate hidden appendix, both labelled.
* **Human fields are emitted blank.**

Usage:
    python scripts/build_review_packet.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import tarfile
import tempfile
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode  # noqa: E402
from src.inference.bayes import score_hypotheses  # noqa: E402
from src.inference.parameters import load_ordinal_mappings  # noqa: E402

PRESERVED = ROOT / "benchmark" / "frozen_runs" / "pilot_explanatory_001"
ARCHIVE = PRESERVED / "pilot_explanatory_001.tar.gz"
SUMS = PRESERVED / "SHA256SUMS"
HIDDEN = ROOT / "benchmark" / "explanatory" / "cases_hidden.json"
OUT = ROOT / "benchmark" / "review" / "graph_pilot_001"

PACKET_ID = "GP1"
INFLUENCE_TOL = 1e-9          # below this a node did not move any log-odds
PRIORITY_SHARE = 0.80         # directive: ~80% of total absolute influence
REPRO_TOL = 1e-6              # normalised scores are stored at full float precision
CONTRIBUTION_ROUNDING = 5e-7 + 1e-12   # contributions are stored rounded to 6 dp


# --------------------------------------------------------------------------- #
# Archive
# --------------------------------------------------------------------------- #
def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def extract_verified(dest: Path) -> Path:
    """Extract the preserved archive and verify every file against SHA256SUMS."""
    if not ARCHIVE.exists():
        raise SystemExit(
            "private archive not found at {}. It is kept out of the public repository; "
            "see {} for its checksum and where it is stored.".format(ARCHIVE, PRESERVED / "PROVENANCE.md"))
    with tarfile.open(ARCHIVE, "r:gz") as tar:
        tar.extractall(dest)
    expected = {}
    for line in SUMS.read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        expected[rel] = digest
    for rel, digest in expected.items():
        got = _sha256(dest / rel)
        if got != digest:
            raise SystemExit("checksum mismatch for {}: archive is not the preserved run".format(rel))
    return dest


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _events(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# --------------------------------------------------------------------------- #
# Verifier reconstruction
# --------------------------------------------------------------------------- #
def rebuild_graph(graph_record: Dict[str, Any]) -> ConsequenceGraph:
    graph = ConsequenceGraph(instance_id=graph_record["instance_id"],
                             hypothesis_ids=list(graph_record["hypothesis_ids"]))
    for node in graph_record["nodes"]:
        graph.add_node(PropositionNode(**node))
    for edge in graph_record["edges"]:
        graph.add_edge(GraphEdge(**edge))
    graph.freeze()
    return graph


def score_graph(graph: ConsequenceGraph, evidence: Dict[str, str], inference: Dict[str, Any],
                mappings) -> Any:
    return score_hypotheses(
        graph, evidence, mappings=mappings,
        multi_parent_rule=inference["multi_parent_rule"],
        parent_false_baseline=inference["parent_false_baseline"],
        aggregation="independent",
    )


def verify_reproduction(case_id: str, frozen: Dict[str, Any], result: Any) -> None:
    for h, value in frozen["scores"].items():
        if abs(result.scores[h] - value) > REPRO_TOL:
            raise SystemExit("{}: score for {} not reproduced ({} vs {})".format(
                case_id, h, result.scores[h], value))
    frozen_rows = {(c["node_id"], c["hypothesis_id"]): c for c in frozen["contributions"]}
    got_rows = {(c.node_id, c.hypothesis_id): c for c in result.contributions}
    if set(frozen_rows) != set(got_rows):
        raise SystemExit("{}: contribution rows differ from frozen scores.json".format(case_id))
    # scores.json serialises p_true_given_h to 4 dp and contributions to 6 dp
    # (src/inference/bayes.py NodeContribution.record). Compare at exactly that
    # precision: stricter than a loose float tolerance, and it cannot pass by accident.
    for key, row in frozen_rows.items():
        got = got_rows[key]
        if (round(got.p_true_given_h, 4) != row["p_true_given_h"]
                or abs(got.contribution - row["contribution"]) > CONTRIBUTION_ROUNDING
                or got.evidence_label != row["evidence_label"]):
            raise SystemExit("{}: contribution {} not reproduced".format(case_id, key))


def _log_odds(totals: Dict[str, float], hyps: List[str]) -> float:
    """log-score of the first hypothesis minus the second (k=2)."""
    return totals[hyps[0]] - totals[hyps[1]]


# --------------------------------------------------------------------------- #
# Evidence text exactly as shown to the assessor
# --------------------------------------------------------------------------- #
_PROP_RE = re.compile(r"PROPOSITION:\n(.*?)\n\nRETRIEVED LITERATURE:\n", re.S)
_LIT_RE = re.compile(r"RETRIEVED LITERATURE:\n(.*?)\n\nReturn a single JSON object", re.S)
_RECORD_START = re.compile(r"^\[(\d+)\] ", re.M)
# LiteratureSearchService.render_for_prompt joins records with a blank line;
# joining the packet's blocks with this reproduces the assessor's block exactly.
RECORD_SEPARATOR = "\n\n"


def assessor_calls(events: List[Dict[str, Any]], text_to_node: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """node_id -> the evidence_assess call made for it, located by the proposition
    text embedded in the rendered prompt (events carry no node id)."""
    calls: Dict[str, Dict[str, Any]] = {}
    for event in events:
        if event.get("purpose") != "graph.evidence_assess":
            continue
        prompt = event["messages"][-1]["content"]
        match = _PROP_RE.search(prompt)
        if not match:
            raise SystemExit("evidence_assess prompt without a PROPOSITION block")
        node_id = text_to_node.get(match.group(1).strip())
        if node_id is None or node_id in calls:
            raise SystemExit("evidence_assess call does not map to exactly one node")
        calls[node_id] = event
    return calls


def split_literature(prompt: str) -> List[Dict[str, Any]]:
    """The literature block, cut into per-record text blocks, character-exact."""
    match = _LIT_RE.search(prompt)
    if not match:
        raise SystemExit("rendered prompt has no RETRIEVED LITERATURE block")
    block = match.group(1)
    starts = [m.start() for m in _RECORD_START.finditer(block)]
    records = []
    for i, start in enumerate(starts):
        if i + 1 < len(starts):
            # Remove ONLY the separator the renderer inserted. An abstract may itself
            # end in newlines, and those are part of what the assessor read.
            end = starts[i + 1] - len(RECORD_SEPARATOR)
            if block[end:starts[i + 1]] != RECORD_SEPARATOR:
                raise SystemExit("record boundary without the renderer's separator")
        else:
            end = len(block)
        text = block[start:end]
        pid = re.search(r"^    id: (.+)$", text, re.M)
        records.append({"position": int(_RECORD_START.match(text).group(1)),
                        "paper_id": pid.group(1).strip() if pid else None,
                        "exact_text_shown_to_assessor": text})
    if not starts:
        records = []
    return records


# --------------------------------------------------------------------------- #
# Graph context
# --------------------------------------------------------------------------- #
def graph_context(node: Dict[str, Any], graph: ConsequenceGraph, root_edges: Dict[Tuple[str, str], Dict[str, Any]],
                  chain_edges: Dict[Tuple[str, str], Dict[str, Any]], p_matrix: Dict[str, Dict[str, float]],
                  nodes_by_id: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    node_id = node["id"]
    origin = node.get("generation_origin_hypothesis")
    parents = [e.source for e in graph.parents(node_id) if not e.source.startswith("H")]
    routes = OrderedDict()
    for h in graph.hypothesis_ids:
        root = root_edges.get((h, node_id))
        chain_routes = []
        for parent in parents:
            chain = chain_edges.get((parent, node_id))
            parent_root = root_edges.get((h, parent))
            chain_routes.append({
                "parent_node_id": parent,
                "parent_text": nodes_by_id[parent]["text"],
                "hypothesis_to_parent_edge_label": parent_root["ordinal_strength"] if parent_root else None,
                "hypothesis_to_parent_edge_rationale": parent_root["rationale"] if parent_root else None,
                "parent_p_true_given_hypothesis": p_matrix[parent][h],
                "parent_to_node_edge_label": chain["ordinal_strength"] if chain else None,
                "parent_to_node_edge_rationale": chain["rationale"] if chain else None,
            })
        routes[h] = {
            "is_origin_of_proposition": h == origin,
            "direct_edge_label": root["ordinal_strength"] if root else None,
            "direct_edge_rationale": root["rationale"] if root else None,
            "routes_via_parent": chain_routes,
            "p_true_given_hypothesis": p_matrix[node_id][h],
        }
    path = [origin] + ([node.get("generation_parent")] if node.get("generation_parent") else []) + [node_id]
    return {
        "depth": node.get("depth"),
        "generation_parent": node.get("generation_parent"),
        "parent_node_ids": parents,
        "generation_path": path,
        "cross_hypothesis_judgments": routes,
        "combination_rule": "P(X|H) = noisy_or over the direct H->X edge and every "
                            "H->parent->X route; unrouted = 0.5",
    }


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(run: Path, supplementary: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    mappings = load_ordinal_mappings(str(ROOT / "configs" / "ordinal_mappings.yaml"))
    instances = sorted(p for p in (run / "instances").iterdir() if p.is_dir())

    # ---------------- phase 1: verifier artifacts only ------------------ #
    records: List[Dict[str, Any]] = []
    case_summary: Dict[str, Any] = OrderedDict()
    zero_spread_nonzero = []
    for inst in instances:
        case_id = inst.name
        graph_record = _load(inst / "graph.json")
        edges = _load(inst / "edge_judgments.json")
        frozen = _load(inst / "scores.json")
        evidence = _load(inst / "evidence.json")["by_node"]
        retrieval = _load(inst / "retrieval.json")["by_node"]
        instance = _load(inst / "input.json")
        presentation = _load(inst / "presentation.json")
        events = _events(inst / "events.jsonl")

        hyps = list(graph_record["hypothesis_ids"])
        if len(hyps) != 2:
            raise SystemExit("{}: packet assumes k=2".format(case_id))
        graph = rebuild_graph(graph_record)
        labels = {nid: entry["assessment"]["evidence_label"] for nid, entry in evidence.items()}
        result = score_graph(graph, labels, frozen["inference"], mappings)
        verify_reproduction(case_id, frozen, result)

        per_node: Dict[str, Dict[str, float]] = defaultdict(dict)
        for row in frozen["contributions"]:
            per_node[row["node_id"]][row["hypothesis_id"]] = row["contribution"]
        totals = {h: sum(per_node[n][h] for n in per_node) for h in hyps}
        case_log_odds = _log_odds(totals, hyps)
        top = max(frozen["scores"], key=frozen["scores"].get)

        nodes_by_id = {n["id"]: n for n in graph_record["nodes"]}
        text_to_node = {n["text"]: n["id"] for n in graph_record["nodes"]}
        calls = assessor_calls(events, text_to_node)
        root_edges = {(e["source"], e["target"]): e for e in edges["root_edges"]}
        chain_edges = {(e["source"], e["target"]): e for e in edges["chain_edges"]}
        display = {h: "Candidate {}".format(lbl) for lbl, h in presentation["label_to_hypothesis_id"].items()}
        hypotheses_shown = OrderedDict((h["id"], h["text"]) for h in instance["hypotheses"])

        case_records = []
        for node_id in sorted(per_node, key=lambda n: int(n[1:])):
            contribs = per_node[node_id]
            spread = max(contribs.values()) - min(contribs.values())
            if spread <= INFLUENCE_TOL:
                if any(abs(v) > INFLUENCE_TOL for v in contribs.values()):
                    zero_spread_nonzero.append((case_id, node_id))
                continue
            node = nodes_by_id[node_id]
            assessment = evidence[node_id]["assessment"]
            call = calls[node_id]
            prompt = call["messages"][-1]["content"]
            shown_blocks = split_literature(prompt)
            meta_by_id = {p["paper_id"]: p for p in retrieval[node_id]["papers_shown"]}
            if [b["paper_id"] for b in shown_blocks] != [p["paper_id"] for p in retrieval[node_id]["papers_shown"]]:
                raise SystemExit("{} {}: prompt records differ from retrieval.json papers_shown".format(case_id, node_id))
            key_papers = set(assessment.get("key_papers") or [])
            shown_text = RECORD_SEPARATOR.join(b["exact_text_shown_to_assessor"] for b in shown_blocks)
            papers = []
            for block in shown_blocks:
                meta = meta_by_id[block["paper_id"]]
                papers.append(OrderedDict([
                    ("position", block["position"]),
                    ("paper_id", meta["paper_id"]),
                    ("title", meta.get("title")),
                    ("authors", [a.get("name") if isinstance(a, dict) else a for a in meta.get("authors") or []]),
                    ("year", meta.get("year")),
                    ("venue", meta.get("venue")),
                    ("doi", meta.get("doi")),
                    ("semantic_scholar_id", meta.get("provider_id")),
                    ("url", meta.get("url")),
                    ("publication_date_reported", meta.get("publication_date")),
                    ("eligible_date_used_by_cutoff_filter", meta.get("eligible_date")),
                    ("date_source", meta.get("date_source")),
                    ("retrieval_query", meta.get("retrieval_query")),
                    ("is_key_paper_cited_by_assessor", meta["paper_id"] in key_papers),
                    ("exact_text_shown_to_assessor", block["exact_text_shown_to_assessor"]),
                ]))

            others = {h: sum(per_node[n][h] for n in per_node if n != node_id) for h in hyps}
            withheld = _log_odds(others, hyps)
            deleted = deleted_counterfactual(graph_record, labels, node_id, frozen["inference"], mappings)

            record = OrderedDict([
                ("review_id", "{}-{}-{}".format(PACKET_ID, case_id, node_id)),
                ("case_id", case_id),
                ("node_id", node_id),
                ("proposition", OrderedDict([
                    ("text", node["text"]),
                    ("origin_hypothesis_id", node.get("generation_origin_hypothesis")),
                    ("abstraction_level", (node.get("metadata") or {}).get("abstraction_level")),
                    ("generator_why_implied", (node.get("metadata") or {}).get("why_implied")),
                    ("generator_why_discriminative", (node.get("metadata") or {}).get("why_discriminative")),
                    ("empirically_assessable", node.get("empirically_assessable")),
                ])),
                ("case_context", OrderedDict([
                    ("phenomenon", instance["question"]),
                    ("historical_cutoff", instance["cutoff_date"]),
                    ("hypotheses_as_shown_to_verifier", hypotheses_shown),
                    ("verifier_display_labels", display),
                ])),
                ("verifier_graph", graph_context(node, graph, root_edges, chain_edges,
                                                 result.p_matrix, nodes_by_id)),
                ("verifier_evidence", OrderedDict([
                    ("queries", [q.get("query") for q in retrieval[node_id].get("queries") or []]),
                    ("n_unique_eligible_papers", retrieval[node_id].get("n_unique_eligible")),
                    ("n_papers_shown_to_assessor", len(papers)),
                    ("evidence_label_used_in_score", assessment["evidence_label"]),
                    ("model_evidence_label", assessment.get("model_evidence_label")),
                    ("label_enforced_by_harness", assessment.get("label_enforced_by_harness")),
                    ("evidence_log_likelihood_ratio", mappings.evidence_value(assessment["evidence_label"])),
                    ("supporting_spans", [OrderedDict([
                        ("text", s),
                        ("found_verbatim_in_shown_records", s in shown_text),
                        ("longest_verbatim_run_chars", _longest_run(s, shown_text)),
                        ("span_chars", len(s)),
                    ]) for s in assessment.get("supporting_spans") or []]),
                    ("key_papers", sorted(key_papers)),
                    ("assessor_rationale", assessment.get("rationale")),
                    ("requires_external_bridge", assessment.get("requires_external_bridge")),
                    ("proposition_unassessable", assessment.get("proposition_unassessable")),
                    ("independence_note", assessment.get("independence_note")),
                    ("assessor_call_id", call.get("call_id")),
                    ("assessor_raw_response", call.get("response_text")),
                    ("per_paper_contribution_note",
                     "The evidence assessor returns ONE label for the node from all papers shown; "
                     "the method has no per-paper contribution. Key papers and spans are those the "
                     "assessor cited."),
                    ("papers_shown_separator", RECORD_SEPARATOR),
                    ("papers_shown", papers),
                ])),
                ("score_influence", OrderedDict([
                    ("log_likelihood_contribution_by_hypothesis", OrderedDict((h, contribs[h]) for h in hyps)),
                    ("log_odds_contribution", OrderedDict([
                        ("definition", "{} minus {}".format(hyps[0], hyps[1])),
                        ("value", contribs[hyps[0]] - contribs[hyps[1]]),
                    ])),
                    ("favours", hyps[0] if contribs[hyps[0]] > contribs[hyps[1]] else hyps[1]),
                    ("absolute_influence", spread),
                    ("case_total_log_odds", OrderedDict([("definition", "{} minus {}".format(hyps[0], hyps[1])),
                                                         ("value", case_log_odds)])),
                    ("case_top_ranked_hypothesis", top),
                    ("counterfactual_evidence_withheld", OrderedDict([
                        ("definition", "node treated as unobserved; graph unchanged (exact: contributions are additive)"),
                        ("case_log_odds", withheld),
                        ("top_ranked_hypothesis", _top_from_log_odds(withheld, hyps)),
                        ("ranking_changes", _top_from_log_odds(withheld, hyps) != top),
                    ])),
                    ("counterfactual_node_deleted", OrderedDict([
                        ("definition", "node and its edges removed; descendants lose the route through it; "
                                       "rescored with src.inference.bayes"),
                        ("case_log_odds", deleted),
                        ("top_ranked_hypothesis", _top_from_log_odds(deleted, hyps)),
                        ("ranking_changes", _top_from_log_odds(deleted, hyps) != top),
                    ])),
                ])),
            ])
            case_records.append(record)

        case_records.sort(key=lambda r: -r["score_influence"]["absolute_influence"])
        for rank, record in enumerate(case_records, start=1):
            record["score_influence"]["rank_in_case"] = rank
        records.extend(case_records)
        case_summary[case_id] = {"n_nodes": len(graph_record["nodes"]),
                                 "n_score_moving": len(case_records),
                                 "total_log_odds": case_log_odds, "top": top,
                                 "scores": frozen["scores"]}

    # global ranking and the priority subset, from influence only
    records.sort(key=lambda r: (-r["score_influence"]["absolute_influence"], r["review_id"]))
    total = sum(r["score_influence"]["absolute_influence"] for r in records)
    cumulative = 0.0
    priority_cut = None
    for rank, record in enumerate(records, start=1):
        cumulative += record["score_influence"]["absolute_influence"]
        record["score_influence"]["rank_global"] = rank
        record["score_influence"]["cumulative_share_of_total_influence"] = cumulative / total
        if priority_cut is None and cumulative / total >= PRIORITY_SHARE - 1e-12:
            priority_cut = rank
    for record in records:
        record["score_influence"]["in_priority_set"] = record["score_influence"]["rank_global"] <= priority_cut
    selected_ids = [r["review_id"] for r in records]

    # ---------------- phase 2: post-hoc metadata, after selection ------- #
    attach_audit_metadata(records, run, supplementary)
    assert [r["review_id"] for r in records] == selected_ids, "audit metadata altered selection"

    for record in records:
        record["human_review"] = blank_human_fields(list(record["case_context"]["hypotheses_as_shown_to_verifier"]))

    stats = review_statistics(records, case_summary, priority_cut, total, zero_spread_nonzero)
    stats["automated_audit_instability_all_rerated_nodes"] = audit_instability(run, supplementary)
    hidden = hidden_context(case_summary)
    return records, stats, hidden


def deleted_counterfactual(graph_record, labels, node_id, inference, mappings) -> float:
    reduced = dict(graph_record)
    reduced["nodes"] = [n for n in graph_record["nodes"] if n["id"] != node_id]
    reduced["edges"] = [e for e in graph_record["edges"] if node_id not in (e["source"], e["target"])]
    graph = rebuild_graph(reduced)
    remaining = {k: v for k, v in labels.items() if k != node_id}
    result = score_graph(graph, remaining, inference, mappings)
    hyps = graph_record["hypothesis_ids"]
    return result.log_scores[hyps[0]] - result.log_scores[hyps[1]]


def _longest_run(span: str, shown: str) -> int:
    """Length of the longest exact substring of `span` found in the shown text.
    Mechanical grounding check only; says nothing about relevance."""
    if span in shown:
        return len(span)
    import difflib
    matcher = difflib.SequenceMatcher(None, span, shown, autojunk=False)
    return matcher.find_longest_match(0, len(span), 0, len(shown)).size


def _top_from_log_odds(value: float, hyps: List[str]) -> str:
    if abs(value) <= 1e-12:
        return "tie"
    return hyps[0] if value > 0 else hyps[1]


# --------------------------------------------------------------------------- #
# Post-hoc metadata (non-authoritative)
# --------------------------------------------------------------------------- #
def attach_audit_metadata(records: List[Dict[str, Any]], run: Path, supplementary: Path) -> None:
    recovery = _load(run / "recovery.json")
    primary = {(c["case_id"], r["node_id"]): r for c in recovery["cases"] for r in c["propositions"]}
    attribution = {(c["case_id"], n["node_id"]): n for c in _load(run / "evidence_discovery.json")["cases"]
                   for n in c["nodes"]}
    second = {(r["case"], r["node"]): r for r in _load(run / "manual_review" / "ratings_compared.json")}
    retest_path = supplementary / "dryrun" / "recovery.json"
    retest = {(c["case_id"], r["node_id"]): r for c in _load(retest_path)["cases"] for r in c["propositions"]}

    for record in records:
        key = (record["case_id"], record["node_id"])
        p = primary.get(key)
        a = attribution.get(key)
        s = second.get(key)
        t = retest.get(key)
        judge = (p or {}).get("judge") or {}
        rec = (p or {}).get("reconciliation") or {}
        primary_disc = judge.get("is_discriminative")
        record["posthoc_automated_audit"] = OrderedDict([
            ("NON_AUTHORITATIVE", "LLM post-hoc audit. Not ground truth. The recovery auditor was "
                                  "shown hidden benchmark annotations (reference discriminators)."),
            ("primary_recovery_auditor", None if p is None else OrderedDict([
                ("prompt", "recovery_classify_v1"),
                ("category", judge.get("category")),
                ("status_under_each_hypothesis", judge.get("status_under_each")),
                ("is_discriminative", primary_disc),
                ("matched_reference_discriminator_HIDDEN_CONTEXT", judge.get("matched_reference_discriminator")),
                ("status_reasoning", judge.get("status_reasoning")),
                ("category_reasoning", judge.get("category_reasoning")),
                ("confidence", judge.get("confidence")),
            ])),
            ("derived_from_primary_and_edges", None if p is None else OrderedDict([
                ("opposition_call", "genuine" if primary_disc else
                    ("manufactured_from_silence" if rec.get("manufactured_opposition") else
                     ("silence_given_directional_label" if rec.get("silence_inflation") else
                      ("one_sided_silence_labelled_neutral" if rec.get("one_sided_proposition") else
                       "both_predict_same")))),
                ("silent_hypotheses_read_as_absence", rec.get("silent_hypotheses_read_as_absence")),
                ("silent_hypotheses_read_as_presence", rec.get("silent_hypotheses_read_as_presence")),
                ("silent_hypotheses_handled_as_neutral", rec.get("silent_hypotheses_handled_as_neutral")),
            ])),
            ("evidence_attribution_auditor", None if a is None else OrderedDict([
                ("prompt", "evidence_attribution_v1"),
                ("attribution", a.get("attribution")),
                ("reasoning", (a.get("judge") or {}).get("reasoning")),
            ])),
            ("second_rater_blind_executor", None if s is None else OrderedDict([
                ("rater", "executor (Claude, an LLM), not a human expert; blind to primary labels"),
                ("status_under_each_hypothesis", s.get("executor_status")),
                ("is_discriminative", s.get("executor_discriminative")),
                ("confidence", s.get("executor_confidence")),
                ("note", s.get("executor_note")),
            ])),
            ("primary_auditor_retest", None if t is None else OrderedDict([
                ("description", "same auditor prompt run on an earlier copy of this case"),
                ("category", (t.get("judge") or {}).get("category")),
                ("is_discriminative", (t.get("judge") or {}).get("is_discriminative")),
                ("status_under_each_hypothesis", (t.get("judge") or {}).get("status_under_each")),
            ])),
            ("disagreement", OrderedDict([
                ("second_rater_vs_primary_discriminative",
                 None if s is None else s.get("executor_discriminative") != primary_disc),
                ("second_rater_vs_primary_status",
                 None if s is None or not judge else s.get("executor_status") != judge.get("status_under_each")),
                ("retest_vs_primary_category",
                 None if t is None else (t.get("judge") or {}).get("category") != judge.get("category")),
                ("any", any(x for x in [
                    None if s is None else s.get("executor_discriminative") != primary_disc,
                    None if s is None or not judge else s.get("executor_status") != judge.get("status_under_each"),
                    None if t is None else (t.get("judge") or {}).get("category") != judge.get("category"),
                ] if x is not None)),
            ])),
        ])


def audit_instability(run: Path, supplementary: Path) -> Dict[str, Any]:
    """Disagreement over EVERY node that was re-rated, whether or not it moves a score.

    Only two re-ratings exist: a blind second rating of 3 nodes per case (24) and one
    re-run of the primary auditor on one case (24). Coverage is therefore thin and
    uneven, and that is reported rather than extrapolated.
    """
    recovery = _load(run / "recovery.json")
    primary = {(c["case_id"], r["node_id"]): r["judge"] for c in recovery["cases"] for r in c["propositions"]}
    second = _load(run / "manual_review" / "ratings_compared.json")
    retest = _load(supplementary / "dryrun" / "recovery.json")
    by_case: Dict[str, Dict[str, int]] = OrderedDict()
    for row in second:
        c = by_case.setdefault(row["case"], OrderedDict([
            ("second_rater_n", 0), ("second_rater_discriminative_disagree", 0),
            ("second_rater_status_disagree", 0), ("retest_n", 0),
            ("retest_category_disagree", 0), ("retest_discriminative_disagree", 0)]))
        judge = primary[(row["case"], row["node"])]
        c["second_rater_n"] += 1
        c["second_rater_discriminative_disagree"] += int(row["executor_discriminative"] != judge["is_discriminative"])
        c["second_rater_status_disagree"] += int(row["executor_status"] != judge["status_under_each"])
    for case in retest["cases"]:
        c = by_case[case["case_id"]]
        for r in case["propositions"]:
            judge = primary[(case["case_id"], r["node_id"])]
            c["retest_n"] += 1
            c["retest_category_disagree"] += int(r["judge"]["category"] != judge["category"])
            c["retest_discriminative_disagree"] += int(r["judge"]["is_discriminative"] != judge["is_discriminative"])
    totals = OrderedDict((k, sum(c[k] for c in by_case.values())) for k in next(iter(by_case.values())))
    return OrderedDict([("coverage_note", "second rater: 3 random nodes per case; retest: one case only"),
                        ("by_case", by_case), ("totals", totals)])


def blank_human_fields(hypothesis_ids: List[str]) -> Dict[str, Any]:
    return OrderedDict([
        ("human_primary_category", None),
        ("human_secondary_flags", []),
        ("human_prediction_for_each_hypothesis", OrderedDict((h, None) for h in hypothesis_ids)),
        ("human_is_genuinely_discriminative", None),
        ("human_silence_as_null_error", None),
        ("human_implication_validity", None),
        ("human_evidence_relevance", None),
        ("human_notes", None),
        ("human_confidence", None),
        ("reviewer", None),
    ])


# --------------------------------------------------------------------------- #
# Statistics and hidden appendix
# --------------------------------------------------------------------------- #
def review_statistics(records, case_summary, priority_cut, total, zero_spread_nonzero) -> Dict[str, Any]:
    by_case = OrderedDict()
    for case_id, summ in case_summary.items():
        case_recs = [r for r in records if r["case_id"] == case_id]
        by_case[case_id] = OrderedDict([
            ("generated_nodes", summ["n_nodes"]),
            ("score_moving_nodes", len(case_recs)),
            ("priority_nodes", sum(1 for r in case_recs if r["score_influence"]["in_priority_set"])),
            ("share_of_total_influence", sum(r["score_influence"]["absolute_influence"] for r in case_recs) / total),
            ("single_node_removals_changing_ranking_evidence_withheld",
             sum(1 for r in case_recs if r["score_influence"]["counterfactual_evidence_withheld"]["ranking_changes"])),
            ("single_node_removals_changing_ranking_node_deleted",
             sum(1 for r in case_recs if r["score_influence"]["counterfactual_node_deleted"]["ranking_changes"])),
        ])

    def edge_pattern(record):
        routes = record["verifier_graph"]["cross_hypothesis_judgments"]
        origin = [v["direct_edge_label"] for v in routes.values() if v["is_origin_of_proposition"]]
        non = [v["direct_edge_label"] for v in routes.values() if not v["is_origin_of_proposition"]]
        return "origin={} | non_origin={}".format(",".join(origin) or "-", ",".join(non) or "-")

    def non_origin_non_neutral(record):
        return any(not v["is_origin_of_proposition"] and v["direct_edge_label"] != "neutral"
                   for v in record["verifier_graph"]["cross_hypothesis_judgments"].values())

    def audit_counts(recs):
        audits = [r["posthoc_automated_audit"] for r in recs]
        primary = Counter((a["primary_recovery_auditor"] or {}).get("category") for a in audits)
        calls = Counter((a["derived_from_primary_and_edges"] or {}).get("opposition_call") for a in audits)
        rated = [a for a in audits if a["second_rater_blind_executor"]]
        retested = [a for a in audits if a["primary_auditor_retest"]]
        return OrderedDict([
            ("primary_categories", dict(primary)),
            ("primary_opposition_calls", dict(calls)),
            ("second_rater_overlap", len(rated)),
            ("second_rater_discriminative_disagreements",
             sum(1 for a in rated if a["disagreement"]["second_rater_vs_primary_discriminative"])),
            ("second_rater_status_disagreements",
             sum(1 for a in rated if a["disagreement"]["second_rater_vs_primary_status"])),
            ("retest_overlap", len(retested)),
            ("retest_category_disagreements",
             sum(1 for a in retested if a["disagreement"]["retest_vs_primary_category"])),
        ])

    priority = [r for r in records if r["score_influence"]["in_priority_set"]]
    return OrderedDict([
        ("total_generated_nodes", sum(s["n_nodes"] for s in case_summary.values())),
        ("score_moving_nodes", len(records)),
        ("score_moving_definition", "nodes whose log-likelihood contributions differ between the "
                                    "hypotheses by more than {} (i.e. they move the log-odds)".format(INFLUENCE_TOL)),
        ("nodes_with_equal_nonzero_contributions_excluded", [list(x) for x in zero_spread_nonzero]),
        ("total_absolute_influence", total),
        ("priority_nodes", priority_cut),
        ("priority_share_of_influence", records[priority_cut - 1]["score_influence"]["cumulative_share_of_total_influence"]),
        ("by_case", by_case),
        ("edge_label_patterns_full", dict(Counter(edge_pattern(r) for r in records).most_common())),
        ("edge_label_patterns_priority", dict(Counter(edge_pattern(r) for r in priority).most_common())),
        ("nodes_with_non_origin_hypothesis_non_neutral_full", sum(1 for r in records if non_origin_non_neutral(r))),
        ("nodes_with_non_origin_hypothesis_non_neutral_priority", sum(1 for r in priority if non_origin_non_neutral(r))),
        ("supporting_spans_not_found_verbatim",
         sum(1 for r in records for s in r["verifier_evidence"]["supporting_spans"]
             if not s["found_verbatim_in_shown_records"])),
        ("supporting_spans_total", sum(len(r["verifier_evidence"]["supporting_spans"]) for r in records)),
        ("automated_audit_full", audit_counts(records)),
        ("automated_audit_priority", audit_counts(priority)),
    ])


def hidden_context(case_summary) -> Dict[str, Any]:
    hidden = _load(HIDDEN)["cases"]
    return OrderedDict((case_id, OrderedDict([
        ("resolution_type", hidden[case_id]["resolution"]["type"]),
        ("resolution_summary", hidden[case_id]["resolution"]["summary"]),
        ("reference_discriminators", hidden[case_id]["reference_discriminators"]),
        ("resolving_observations", hidden[case_id]["resolving_observations"]),
        ("resolver", hidden[case_id]["resolver"]),
    ])) for case_id in case_summary)


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #
def _fmt(x: float) -> str:
    return "{:+.3f}".format(x)


def render_node(r: Dict[str, Any], heading: str) -> List[str]:
    si = r["score_influence"]
    prop = r["proposition"]
    ctx = r["case_context"]
    L: List[str] = []
    add = L.append
    add(heading)
    add("")
    add("**{}** — case `{}`, node `{}`".format(r["review_id"], r["case_id"], r["node_id"]))
    add("")
    add("> {}".format(prop["text"]))
    add("")
    add("- generated from **{}** ({}); abstraction: `{}`".format(
        prop["origin_hypothesis_id"], ctx["verifier_display_labels"].get(prop["origin_hypothesis_id"]),
        prop["abstraction_level"]))
    if prop["generator_why_implied"]:
        add("- generator's stated reason: {}".format(prop["generator_why_implied"]))
    add("- influence: **{:.3f}** (rank {} in case, {} overall; cumulative {:.0%}) — favours **{}**".format(
        si["absolute_influence"], si["rank_in_case"], si["rank_global"],
        si["cumulative_share_of_total_influence"], si["favours"]))
    add("- log-likelihood contribution: {}".format(", ".join(
        "{} {}".format(h, _fmt(v)) for h, v in si["log_likelihood_contribution_by_hypothesis"].items())))
    add("- removing it alone: evidence withheld → case log-odds {} (ranking {}); node deleted → {} (ranking {})".format(
        _fmt(si["counterfactual_evidence_withheld"]["case_log_odds"]),
        "CHANGES" if si["counterfactual_evidence_withheld"]["ranking_changes"] else "unchanged",
        _fmt(si["counterfactual_node_deleted"]["case_log_odds"]),
        "CHANGES" if si["counterfactual_node_deleted"]["ranking_changes"] else "unchanged"))
    add("")
    add("**Hypotheses (as shown to the verifier)**")
    add("")
    for h, text in ctx["hypotheses_as_shown_to_verifier"].items():
        add("- **{}** ({}): {}".format(h, ctx["verifier_display_labels"].get(h), text))
    add("")
    add("**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR")
    add("")
    add("| hypothesis | origin? | direct edge | route via parent | P(X\\|H) |")
    add("| --- | --- | --- | --- | --- |")
    for h, v in r["verifier_graph"]["cross_hypothesis_judgments"].items():
        via = "; ".join("{} [H→parent `{}`, P={:.2f}] → `{}`".format(
            c["parent_node_id"], c["hypothesis_to_parent_edge_label"], c["parent_p_true_given_hypothesis"],
            c["parent_to_node_edge_label"]) for c in v["routes_via_parent"]) or "—"
        add("| {} | {} | `{}` | {} | {:.3f} |".format(
            h, "yes" if v["is_origin_of_proposition"] else "no", v["direct_edge_label"], via,
            v["p_true_given_hypothesis"]))
    add("")
    for h, v in r["verifier_graph"]["cross_hypothesis_judgments"].items():
        add("- edge rationale, **{}** → node: {}".format(h, v["direct_edge_rationale"]))
    for c in (list(r["verifier_graph"]["cross_hypothesis_judgments"].values())[0]["routes_via_parent"]):
        add("- parent `{}`: {}".format(c["parent_node_id"], c["parent_text"]))
        add("- chain rationale, `{}` → node: {}".format(c["parent_node_id"], c["parent_to_node_edge_rationale"]))
    add("")
    ev = r["verifier_evidence"]
    add("**Verifier evidence** — label used in score: `{}` (log-LR {:+.1f}){}".format(
        ev["evidence_label_used_in_score"], ev["evidence_log_likelihood_ratio"],
        " — harness-enforced (model said `{}`)".format(ev["model_evidence_label"]) if ev["label_enforced_by_harness"] else ""))
    add("")
    add("- queries: {}".format("; ".join("`{}`".format(q) for q in ev["queries"])))
    add("- assessor rationale: {}".format(ev["assessor_rationale"]))
    if ev["supporting_spans"]:
        add("- supporting spans cited by the assessor:")
        for s in ev["supporting_spans"]:
            add("  - \"{}\"{}".format(s["text"], "" if s["found_verbatim_in_shown_records"]
                                     else " **(not verbatim in the records shown: longest exact run {} of {} chars)**".format(
                                         s["longest_verbatim_run_chars"], s["span_chars"])))
    add("- {} papers shown; key papers: {}".format(
        ev["n_papers_shown_to_assessor"], ", ".join("`{}`".format(k) for k in ev["key_papers"]) or "none"))
    add("- _{}_".format(ev["per_paper_contribution_note"]))
    add("")
    for p in ev["papers_shown"]:
        authors = ", ".join(p["authors"][:4]) + (" et al." if len(p["authors"]) > 4 else "")
        ident = p["doi"] and "doi:{}".format(p["doi"]) or p["url"] or p["paper_id"]
        add("<details><summary>[{}]{} {} — {} ({}); cutoff-filter date {}; {}</summary>".format(
            p["position"], " **KEY**" if p["is_key_paper_cited_by_assessor"] else "",
            p["title"], authors or "authors n/a", p["year"], p["eligible_date_used_by_cutoff_filter"], ident))
        add("")
        add("```text")
        add(p["exact_text_shown_to_assessor"])
        add("```")
        add("</details>")
        add("")
    audit = r["posthoc_automated_audit"]
    pa = audit["primary_recovery_auditor"] or {}
    add("<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>")
    add("")
    add("- primary auditor: `{}`; statuses {}; discriminative={}".format(
        pa.get("category"), pa.get("status_under_each_hypothesis"), pa.get("is_discriminative")))
    add("- primary reasoning: {}".format(pa.get("status_reasoning")))
    if pa.get("matched_reference_discriminator_HIDDEN_CONTEXT"):
        add("- matched hidden reference discriminator: {}".format(pa["matched_reference_discriminator_HIDDEN_CONTEXT"]))
    add("- derived opposition call: `{}`".format((audit["derived_from_primary_and_edges"] or {}).get("opposition_call")))
    ea = audit["evidence_attribution_auditor"] or {}
    add("- evidence attribution: `{}` — {}".format(ea.get("attribution"), ea.get("reasoning")))
    if audit["second_rater_blind_executor"]:
        s = audit["second_rater_blind_executor"]
        add("- second rater (LLM, blind): statuses {}; discriminative={} ({} confidence) — {}".format(
            s["status_under_each_hypothesis"], s["is_discriminative"], s["confidence"], s["note"]))
    if audit["primary_auditor_retest"]:
        t = audit["primary_auditor_retest"]
        add("- auditor retest: `{}`; discriminative={}".format(t["category"], t["is_discriminative"]))
    add("- disagreement flags: {}".format(dict(audit["disagreement"])))
    add("</details>")
    add("")
    add("**Human review** (blank) — `human_primary_category`: ☐ genuine_discriminator ☐ compatible_non_discriminative "
        "☐ generic_component_fact ☐ silence_as_null_error ☐ invalid_or_weak_implication "
        "☐ evidence_construct_mismatch ☐ valid_but_historically_uninformative · prediction per hypothesis: {} · "
        "genuinely discriminative: ☐ · silence-as-null error: ☐ · implication validity: ☐ · evidence relevance: ☐ · "
        "confidence: ☐ · notes: ☐".format(", ".join("{} ☐".format(h) for h in ctx["hypotheses_as_shown_to_verifier"])))
    add("")
    add("---")
    add("")
    return L


def render_full(records, stats) -> str:
    L = ["# Graph pilot review — full score-moving set", "",
         "Packet `{}` · {} score-moving nodes of {} generated · rubric: `RUBRIC.md` · "
         "machine-readable: `review_set_full.jsonl`".format(
             PACKET_ID, stats["score_moving_nodes"], stats["total_generated_nodes"]), "",
         "Grouped by case; within a case, by descending influence. Verifier output comes first in "
         "every entry; the post-hoc automated audit is collapsed at the end and is not authoritative. "
         "Hidden benchmark resolutions are in `hidden_case_context.md` and are not shown here.", ""]
    for case_id in stats["by_case"]:
        case_recs = sorted((r for r in records if r["case_id"] == case_id),
                           key=lambda r: r["score_influence"]["rank_in_case"])
        c = stats["by_case"][case_id]
        L += ["## {}".format(case_id), "",
              "{} score-moving of {} generated nodes; {} in the priority set; {:.0%} of total influence".format(
                  c["score_moving_nodes"], c["generated_nodes"], c["priority_nodes"], c["share_of_total_influence"]),
              ""]
        if case_recs:
            r0 = case_recs[0]
            L += ["- phenomenon: {}".format(r0["case_context"]["phenomenon"]),
                  "- cutoff: {}".format(r0["case_context"]["historical_cutoff"]),
                  "- case total log-odds ({}): {}; top-ranked: {}".format(
                      r0["score_influence"]["case_total_log_odds"]["definition"],
                      _fmt(r0["score_influence"]["case_total_log_odds"]["value"]),
                      r0["score_influence"]["case_top_ranked_hypothesis"]), ""]
        for r in case_recs:
            L += render_node(r, "### {} · rank {} in case".format(r["node_id"], r["score_influence"]["rank_in_case"]))
    return "\n".join(L)


def render_priority(records, stats) -> str:
    pr = [r for r in records if r["score_influence"]["in_priority_set"]]
    L = ["# Graph pilot review — priority packet", "",
         "The {} nodes that together account for {:.1%} of all absolute score influence across the eight "
         "cases, ordered by descending influence. Selected from verifier score contributions only. "
         "Rubric: `RUBRIC.md` · machine-readable: `review_set_priority.jsonl`.".format(
             len(pr), stats["priority_share_of_influence"]), "",
         "| rank | review id | influence | cumulative | favours | case ranking changes if withheld |",
         "| --- | --- | --- | --- | --- | --- |"]
    for r in pr:
        si = r["score_influence"]
        L.append("| {} | `{}` | {:.3f} | {:.0%} | {} | {} |".format(
            si["rank_global"], r["review_id"], si["absolute_influence"],
            si["cumulative_share_of_total_influence"], si["favours"],
            "**yes**" if si["counterfactual_evidence_withheld"]["ranking_changes"] else "no"))
    L.append("")
    for r in pr:
        L += render_node(r, "## #{} · `{}`".format(r["score_influence"]["rank_global"], r["review_id"]))
    return "\n".join(L)


def render_hidden(hidden) -> str:
    L = ["# Hidden benchmark context — POST-HOC ONLY", "",
         "**Not verifier evidence.** These annotations were hidden from the verifier and postdate each "
         "case's cutoff. They are provided so a reviewer can, *after* forming an independent judgment of a "
         "proposition, compare it with how the dispute was later resolved. Reviewing implication validity "
         "blind to this file is recommended.", ""]
    for case_id, h in hidden.items():
        L += ["## {}".format(case_id), "",
              "- resolution type: `{}`".format(h["resolution_type"]),
              "- resolution summary: {}".format(h["resolution_summary"]),
              "- reference discriminators:"] + ["  - {}".format(d) for d in h["reference_discriminators"]] + \
             ["- resolving observations:"] + ["  - {}".format(o) for o in h["resolving_observations"]] + \
             ["- resolver: `{}`".format(json.dumps(h["resolver"], sort_keys=True)), ""]
    return "\n".join(L)


# --------------------------------------------------------------------------- #
def write_outputs(records, stats, hidden, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)

    def jsonl(path, rows):
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    jsonl(out / "review_set_full.jsonl", records)
    jsonl(out / "review_set_priority.jsonl", [r for r in records if r["score_influence"]["in_priority_set"]])
    (out / "stats.json").write_text(json.dumps(stats, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "hidden_case_context.json").write_text(json.dumps(hidden, indent=1, ensure_ascii=False) + "\n",
                                                  encoding="utf-8")
    (out / "review_full.md").write_text(render_full(records, stats) + "\n", encoding="utf-8")
    (out / "review_priority.md").write_text(render_priority(records, stats) + "\n", encoding="utf-8")
    (out / "hidden_case_context.md").write_text(render_hidden(hidden) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        root = extract_verified(Path(tmp))
        records, stats, hidden = build(root / "run", root / "supplementary_scratch")
    write_outputs(records, stats, hidden, Path(args.out))
    print(json.dumps({k: stats[k] for k in ("total_generated_nodes", "score_moving_nodes", "priority_nodes",
                                            "priority_share_of_influence")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
