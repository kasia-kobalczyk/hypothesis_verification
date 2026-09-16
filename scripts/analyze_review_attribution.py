"""Score attribution of the frozen graph pilot under human review labels.

BENCH-GRAPH-ATTRIBUTION-001. Deterministic, LLM-free, verifier untouched.

Inputs:
  * the private, checksummed pilot archive (via scripts/build_review_packet.py);
  * `benchmark/review/graph_pilot_001/human_labels_D045.json`, the Research
    Director's 40 priority-node labels, transcribed exactly from D045.

Outputs, in `benchmark/review/graph_pilot_001/attribution/`:
  node_contributions.jsonl     every generated node: class, category, contributions
  case_category_attribution.json   per case x category x hypothesis sums
  counterfactual_views.json    scores/ordering under each deterministic view
  coverage.json                reviewed vs unreviewed influence, next review batch
  ATTRIBUTION_REPORT.md        human-readable report

Orientation. All log-odds here are **log-score(H2) - log-score(H1)**, positive means
support for H2. The review packet records each node's log-odds in its graph's own
hypothesis order, which differs between cases, so it is not reused directly.

Two decompositions, reported side by side:

* **Evidence zeroed (primary).** Under the configured independent aggregation a
  case's log-score is a sum of per-node terms, so removing a node's evidence removes
  exactly its term and nothing else. Category sums are exact and unique.
* **Graph deletion (sensitivity).** The removed nodes are deleted from the graph and
  the case is rescored with the verifier's own `src.inference.bayes`. Descendants
  then lose the routes through them. 58 of 78 score-moving nodes receive part of
  P(X|H) through a parent, so an erroneous parent edge can also inflate its
  children; node-local zeroing does not remove that. The difference between the two
  decompositions is the path-mediated part. It is not additive across nodes.

Node classes: `reviewed` (one of the 40 D045 nodes), `unreviewed_score_moving` (the
other 38), `non_moving` (equal contribution to both hypotheses; cannot move the
log-odds). Unreviewed nodes are never treated as valid or invalid; every view states
what it does with them.

Usage:
    python scripts/analyze_review_attribution.py
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_review_packet as bp  # noqa: E402
from src.inference.parameters import load_ordinal_mappings  # noqa: E402

PACKET = bp.OUT
LABELS = PACKET / "human_labels_D045.json"
OUT = PACKET / "attribution"

REVIEWED_CATEGORIES = [
    "genuine_discriminator",
    "silence_as_null_error",
    "generic_component_fact",
    "compatible_non_discriminative",
    "evidence_construct_mismatch",
    "invalid_or_weak_implication",
]
CONFIRMED_ERRORS = {"silence_as_null_error", "evidence_construct_mismatch", "invalid_or_weak_implication"}

# Source: .agent/PROJECT_STATE.md, "Hypothesis-comparison observations" (Research
# Director): in all four `favored` cases the later resolution favours H2. Other
# resolution types have no winner and are compared descriptively only.
FAVOURED = {
    "eukaryogenesis_mito_timing": "H2",
    "fly_wing_constraint_vs_selection": "H2",
    "glnbp_induced_fit_vs_conformational_selection": "H2",
    "pfc_storage_vs_control": "H2",
}

TIE_TOL = 1e-12

# name -> (description, predicate(node_class, category) -> keep?)
VIEWS: "OrderedDict[str, Tuple[str, Any]]" = OrderedDict([
    ("original",
     ("frozen verifier: every node kept",
      lambda cls, cat: True)),
    ("A1_genuine_reviewed_plus_unreviewed",
     ("directive views A1 and D (identical here): reviewed genuine discriminators kept, all other "
      "reviewed nodes removed, unreviewed score-moving nodes untouched",
      lambda cls, cat: cls != "reviewed" or cat == "genuine_discriminator")),
    ("A2_genuine_reviewed_only",
     ("directive views A2 and C (identical here): strict. Reviewed genuine discriminators only; "
      "unreviewed score-moving nodes set aside",
      lambda cls, cat: cls == "non_moving" or (cls == "reviewed" and cat == "genuine_discriminator"))),
    ("B1_remove_confirmed_errors",
     ("directive view B: reviewed silence errors, construct mismatches and weak implications removed; "
      "reviewed genuine, generic and compatible kept; unreviewed untouched",
      lambda cls, cat: cls != "reviewed" or cat not in CONFIRMED_ERRORS)),
    ("B2_remove_confirmed_errors_reviewed_only",
     ("view B, strict: as B1 but unreviewed score-moving nodes set aside",
      lambda cls, cat: cls == "non_moving" or (cls == "reviewed" and cat not in CONFIRMED_ERRORS))),
    ("R_unreviewed_only",
     ("reference: all reviewed nodes removed; unreviewed score-moving nodes only",
      lambda cls, cat: cls != "reviewed")),
])


# --------------------------------------------------------------------------- #
def _scores_from_log_odds(lo: float) -> Dict[str, float]:
    """Normalised scores under the uniform prior from log-odds H2:H1."""
    p2 = 1.0 / (1.0 + math.exp(-lo)) if lo >= 0 else math.exp(lo) / (1.0 + math.exp(lo))
    return OrderedDict([("H1", 1.0 - p2), ("H2", p2)])


def _top(lo: float) -> str:
    if abs(lo) <= TIE_TOL:
        return "tie"
    return "H2" if lo > 0 else "H1"


def _relation(top: str, favoured: str) -> str:
    if favoured is None:
        return "not_applicable_non_directional_resolution"
    if top == "tie":
        return "no_ordering"
    return "agrees" if top == favoured else "opposes"


# --------------------------------------------------------------------------- #
def load_labels() -> Dict[Tuple[str, str], str]:
    data = json.loads(LABELS.read_text(encoding="utf-8"))
    return {(l["case_id"], l["node_id"]): l["human_primary_category"] for l in data["labels"]}


def analyse(run: Path) -> Dict[str, Any]:
    mappings = load_ordinal_mappings(str(ROOT / "configs" / "ordinal_mappings.yaml"))
    labels = load_labels()
    packet_ids = {json.loads(line)["review_id"]
                  for line in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()}

    nodes_out: List[Dict[str, Any]] = []
    cases: Dict[str, Any] = OrderedDict()
    moving_seen: Set[str] = set()

    for inst in sorted(p for p in (run / "instances").iterdir() if p.is_dir()):
        case_id = inst.name
        graph_record = bp._load(inst / "graph.json")
        frozen = bp._load(inst / "scores.json")
        evidence = bp._load(inst / "evidence.json")["by_node"]
        if sorted(graph_record["hypothesis_ids"]) != ["H1", "H2"]:
            raise SystemExit("{}: expected hypotheses H1, H2".format(case_id))

        ev_labels = {nid: e["assessment"]["evidence_label"] for nid, e in evidence.items()}
        graph = bp.rebuild_graph(graph_record)
        result = bp.score_graph(graph, ev_labels, frozen["inference"], mappings)
        bp.verify_reproduction(case_id, frozen, result)       # aborts on any mismatch

        contrib: Dict[str, Dict[str, float]] = defaultdict(dict)
        for c in result.contributions:
            contrib[c.node_id][c.hypothesis_id] = c.contribution
        frozen_lo = result.log_scores["H2"] - result.log_scores["H1"]
        if abs(frozen_lo - math.log(frozen["scores"]["H2"] / frozen["scores"]["H1"])) > 1e-6:
            raise SystemExit("{}: log-odds do not reproduce frozen scores".format(case_id))

        children = defaultdict(list)
        for e in graph_record["edges"]:
            if not e["source"].startswith("H"):
                children[e["source"]].append(e["target"])

        node_class: Dict[str, str] = {}
        node_cat: Dict[str, Any] = {}
        for n in graph_record["nodes"]:
            nid = n["id"]
            c = contrib[nid]
            spread = abs(c["H2"] - c["H1"])
            if spread <= bp.INFLUENCE_TOL:
                cls = "non_moving"
            elif (case_id, nid) in labels:
                cls = "reviewed"
            else:
                cls = "unreviewed_score_moving"
            if cls != "non_moving":
                moving_seen.add("{}-{}-{}".format(bp.PACKET_ID, case_id, nid))
            if (case_id, nid) in labels and cls != "reviewed":
                raise SystemExit("{} {}: labelled node does not move the score".format(case_id, nid))
            node_class[nid] = cls
            node_cat[nid] = labels.get((case_id, nid))
            nodes_out.append(OrderedDict([
                ("review_id", "{}-{}-{}".format(bp.PACKET_ID, case_id, nid)),
                ("case_id", case_id), ("node_id", nid),
                ("node_class", cls),
                ("human_primary_category", node_cat[nid]),
                ("origin_hypothesis_id", n.get("generation_origin_hypothesis")),
                ("parents", [e["source"] for e in graph_record["edges"]
                             if e["target"] == nid and not e["source"].startswith("H")]),
                ("children", sorted(children[nid], key=lambda x: int(x[1:]))),
                ("evidence_label", ev_labels[nid]),
                ("p_true_given_H1", result.p_matrix[nid]["H1"]),
                ("p_true_given_H2", result.p_matrix[nid]["H2"]),
                ("contribution_H1", c["H1"]),
                ("contribution_H2", c["H2"]),
                ("log_odds_H2_over_H1", c["H2"] - c["H1"]),
                ("absolute_influence", spread),
            ]))

        # -------- category attribution (exact, additive) ---------------- #
        buckets: Dict[str, Dict[str, float]] = OrderedDict()
        for key in REVIEWED_CATEGORIES + ["unreviewed_score_moving", "non_moving"]:
            buckets[key] = OrderedDict([("n_nodes", 0), ("contribution_H1", 0.0), ("contribution_H2", 0.0),
                                        ("log_odds_H2_over_H1", 0.0), ("absolute_influence", 0.0)])
        for nid in contrib:
            key = node_cat[nid] if node_class[nid] == "reviewed" else node_class[nid]
            b = buckets[key]
            b["n_nodes"] += 1
            b["contribution_H1"] += contrib[nid]["H1"]
            b["contribution_H2"] += contrib[nid]["H2"]
            b["log_odds_H2_over_H1"] += contrib[nid]["H2"] - contrib[nid]["H1"]
            b["absolute_influence"] += abs(contrib[nid]["H2"] - contrib[nid]["H1"])
        summed = sum(b["log_odds_H2_over_H1"] for b in buckets.values())
        if abs(summed - frozen_lo) > 1e-9:
            raise SystemExit("{}: category buckets do not sum to the frozen log-odds".format(case_id))

        reviewed_abs = sum(buckets[k]["absolute_influence"] for k in REVIEWED_CATEGORIES)
        unreviewed_abs = buckets["unreviewed_score_moving"]["absolute_influence"]

        # -------- counterfactual views ---------------------------------- #
        favoured = FAVOURED.get(case_id)
        views = OrderedDict()
        for name, (description, keep) in VIEWS.items():
            kept = [nid for nid in contrib if keep(node_class[nid], node_cat[nid])]
            removed = [nid for nid in contrib if nid not in kept]
            lo_zero = sum(contrib[nid]["H2"] - contrib[nid]["H1"] for nid in kept)
            n_moving_kept = sum(1 for nid in kept if node_class[nid] != "non_moving")

            # sensitivity: delete removed nodes from the graph, rescore with bayes
            reduced = dict(graph_record)
            gone = set(removed)
            reduced["nodes"] = [n for n in graph_record["nodes"] if n["id"] not in gone]
            reduced["edges"] = [e for e in graph_record["edges"] if e["source"] not in gone and e["target"] not in gone]
            res_del = bp.score_graph(bp.rebuild_graph(reduced), {k: v for k, v in ev_labels.items() if k not in gone},
                                     frozen["inference"], mappings)
            lo_del = res_del.log_scores["H2"] - res_del.log_scores["H1"]

            top_zero, top_del = _top(lo_zero), _top(lo_del)
            views[name] = OrderedDict([
                ("description", description),
                ("n_score_moving_nodes_kept", n_moving_kept),
                ("no_score_moving_nodes_kept", n_moving_kept == 0),
                ("evidence_zeroed", OrderedDict([
                    ("log_odds_H2_over_H1", lo_zero),
                    ("scores", _scores_from_log_odds(lo_zero)),
                    ("top", top_zero),
                    ("relation_to_later_resolution", _relation(top_zero, favoured)),
                ])),
                ("graph_deleted_sensitivity", OrderedDict([
                    ("log_odds_H2_over_H1", lo_del),
                    ("scores", _scores_from_log_odds(lo_del)),
                    ("top", top_del),
                    ("relation_to_later_resolution", _relation(top_del, favoured)),
                    ("path_mediated_difference", lo_del - lo_zero),
                ])),
            ])

        cases[case_id] = OrderedDict([
            ("original", OrderedDict([
                ("scores", OrderedDict([("H1", frozen["scores"]["H1"]), ("H2", frozen["scores"]["H2"])])),
                ("log_odds_H2_over_H1", frozen_lo),
                ("top", _top(frozen_lo)),
            ])),
            ("later_resolution_favours", favoured),
            ("total_absolute_influence", reviewed_abs + unreviewed_abs),
            ("reviewed_absolute_influence", reviewed_abs),
            ("unreviewed_absolute_influence", unreviewed_abs),
            ("reviewed_log_odds_H2_over_H1", sum(buckets[k]["log_odds_H2_over_H1"] for k in REVIEWED_CATEGORIES)),
            ("unreviewed_log_odds_H2_over_H1", buckets["unreviewed_score_moving"]["log_odds_H2_over_H1"]),
            ("categories", buckets),
            ("views", views),
        ])

    if moving_seen != packet_ids:
        raise SystemExit("score-moving set differs from the review packet")
    return {"nodes": nodes_out, "cases": cases}


# --------------------------------------------------------------------------- #
def coverage(nodes: List[Dict[str, Any]], cases: Dict[str, Any]) -> Dict[str, Any]:
    moving = [n for n in nodes if n["node_class"] != "non_moving"]
    total = sum(n["absolute_influence"] for n in moving)
    reviewed = sum(n["absolute_influence"] for n in moving if n["node_class"] == "reviewed")
    design_share = reviewed / total
    per_case = OrderedDict()
    for case_id, c in cases.items():
        share = c["reviewed_absolute_influence"] / c["total_absolute_influence"]
        per_case[case_id] = OrderedDict([
            ("score_moving_nodes", sum(1 for n in moving if n["case_id"] == case_id)),
            ("reviewed_nodes", sum(1 for n in moving if n["case_id"] == case_id and n["node_class"] == "reviewed")),
            ("unreviewed_nodes", sum(1 for n in moving if n["case_id"] == case_id and n["node_class"] != "reviewed")),
            ("reviewed_absolute_influence", c["reviewed_absolute_influence"]),
            ("unreviewed_absolute_influence", c["unreviewed_absolute_influence"]),
            ("reviewed_share_of_case_influence", share),
            ("below_packet_design_coverage", share < design_share),
        ])
    batch = sorted((n for n in moving if n["node_class"] == "unreviewed_score_moving"),
                   key=lambda n: (-n["absolute_influence"], n["review_id"]))
    low_cases = {"fly_wing_constraint_vs_selection", "pfc_interhemispheric_architecture", "spider_orb_web_origin"}
    return OrderedDict([
        ("orientation", "log-odds H2 over H1"),
        ("total_absolute_influence", total),
        ("reviewed_nodes", sum(1 for n in moving if n["node_class"] == "reviewed")),
        ("reviewed_absolute_influence", reviewed),
        ("unreviewed_nodes", sum(1 for n in moving if n["node_class"] == "unreviewed_score_moving")),
        ("unreviewed_absolute_influence", total - reviewed),
        ("reviewed_share", design_share),
        ("per_case", per_case),
        ("under_covered_cases_definition",
         "case whose reviewed share of its own influence is below the packet-wide reviewed share"),
        ("under_covered_cases", [c for c, v in per_case.items() if v["below_packet_design_coverage"]]),
        ("recommended_next_review_batch", OrderedDict([
            ("first_low_coverage_cases", [n["review_id"] for n in batch if n["case_id"] in low_cases]),
            ("then_remaining_by_influence", [n["review_id"] for n in batch if n["case_id"] not in low_cases]),
            ("influence", OrderedDict((n["review_id"], n["absolute_influence"]) for n in batch)),
        ])),
    ])


def totals_across_cases(cases: Dict[str, Any]) -> Dict[str, Any]:
    out = OrderedDict()
    for key in REVIEWED_CATEGORIES + ["unreviewed_score_moving", "non_moving"]:
        out[key] = OrderedDict([
            ("n_nodes", sum(c["categories"][key]["n_nodes"] for c in cases.values())),
            ("absolute_influence", sum(c["categories"][key]["absolute_influence"] for c in cases.values())),
            ("signed_log_odds_H2_over_H1_summed_across_cases",
             sum(c["categories"][key]["log_odds_H2_over_H1"] for c in cases.values())),
        ])
    # Toward the later-favoured hypothesis, favored cases only (H2 in all four).
    out_fav = OrderedDict()
    for key in REVIEWED_CATEGORIES + ["unreviewed_score_moving"]:
        out_fav[key] = sum(c["categories"][key]["log_odds_H2_over_H1"]
                           for cid, c in cases.items() if cid in FAVOURED)
    return OrderedDict([("by_category", out),
                        ("favored_cases_log_odds_toward_later_favoured_hypothesis", out_fav)])


# --------------------------------------------------------------------------- #
def write(result: Dict[str, Any], cov: Dict[str, Any], totals: Dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "node_contributions.jsonl").write_text(
        "".join(json.dumps(n, ensure_ascii=False) + "\n" for n in result["nodes"]), encoding="utf-8")
    header = OrderedDict([
        ("orientation", "all log-odds are log-score(H2) minus log-score(H1); positive supports H2"),
        ("labels", "benchmark/review/graph_pilot_001/human_labels_D045.json (D045; model-based Research "
                   "Director review, not external expert ground truth)"),
        ("favoured_hypothesis_source", ".agent/PROJECT_STATE.md: H2 in all four `favored` cases"),
    ])
    (out / "case_category_attribution.json").write_text(json.dumps(OrderedDict([
        ("_about", header),
        ("cases", OrderedDict((cid, OrderedDict([(k, c[k]) for k in (
            "original", "later_resolution_favours", "total_absolute_influence", "reviewed_absolute_influence",
            "unreviewed_absolute_influence", "reviewed_log_odds_H2_over_H1", "unreviewed_log_odds_H2_over_H1",
            "categories")])) for cid, c in result["cases"].items())),
        ("totals", totals),
    ]), indent=1) + "\n", encoding="utf-8")
    (out / "counterfactual_views.json").write_text(json.dumps(OrderedDict([
        ("_about", header),
        ("views", OrderedDict((k, v[0]) for k, v in VIEWS.items())),
        ("cases", OrderedDict((cid, OrderedDict([("original", c["original"]),
                                                  ("later_resolution_favours", c["later_resolution_favours"]),
                                                  ("views", c["views"])]))
                              for cid, c in result["cases"].items())),
    ]), indent=1) + "\n", encoding="utf-8")
    (out / "coverage.json").write_text(json.dumps(cov, indent=1) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
SHORT = OrderedDict([
    ("genuine_discriminator", "genuine"), ("silence_as_null_error", "silence err"),
    ("generic_component_fact", "generic comp."), ("compatible_non_discriminative", "compatible"),
    ("evidence_construct_mismatch", "construct mism."), ("invalid_or_weak_implication", "weak impl."),
    ("unreviewed_score_moving", "UNREVIEWED"),
])
VIEW_SHORT = OrderedDict([
    ("original", "original"), ("A1_genuine_reviewed_plus_unreviewed", "A1 genuine + unrev."),
    ("A2_genuine_reviewed_only", "A2 genuine only"), ("B1_remove_confirmed_errors", "B1 errors removed"),
    ("B2_remove_confirmed_errors_reviewed_only", "B2 errors removed, reviewed only"),
    ("R_unreviewed_only", "R unreviewed only"),
])


def _f(x: float) -> str:
    return "{:+.2f}".format(x)


def _mech(result, packet) -> Dict[str, Any]:
    """Mechanical facts about how reviewed categories moved scores (no judgment)."""
    POS = {"strongly_implied", "implied", "weakly_implied"}
    NEG = {"unlikely", "strongly_contradicted"}
    out = defaultdict(lambda: defaultdict(int))
    for n in result["nodes"]:
        cat = n["human_primary_category"]
        if not cat:
            continue
        rec = packet[n["review_id"]]
        routes = rec["verifier_graph"]["cross_hypothesis_judgments"]
        labels = {h: v["direct_edge_label"] for h, v in routes.items()}
        origin = n["origin_hypothesis_id"]
        other = "H1" if origin == "H2" else "H2"
        out[cat]["n"] += 1
        out[cat]["sign_opposed_direct_edges"] += int(bool(set(labels.values()) & POS) and bool(set(labels.values()) & NEG))
        out[cat]["non_origin_labelled_unlikely_or_contradicted"] += int(labels[other] in NEG)
        lo_toward_origin = n["log_odds_H2_over_H1"] if origin == "H2" else -n["log_odds_H2_over_H1"]
        out[cat]["push_toward_generating_hypothesis"] += int(lo_toward_origin > 0)
        out[cat]["evidence_support"] += int(n["evidence_label"] in ("weak_support", "support", "strong_support"))
        out[cat]["evidence_contradiction"] += int("contradiction" in n["evidence_label"])
    return out


def render_report(result, cov, totals, packet) -> str:
    cases = result["cases"]
    L: List[str] = []
    add = L.append
    total = cov["total_absolute_influence"]
    tb = totals["by_category"]

    add("# BENCH-GRAPH-ATTRIBUTION-001 — score attribution under reviewed labels")
    add("")
    add("Deterministic accounting of the frozen eight-case graph pilot (`pilot_explanatory_001`) "
        "using the Research Director's labels for the 40 priority nodes (D045). No model, "
        "retrieval or verifier code was run beyond re-scoring the frozen graphs with the "
        "verifier's own scoring function; frozen scores reproduce exactly.")
    add("")
    add("**Read the four kinds of statement separately.** §1 is observed frozen verifier "
        "behaviour. §2 uses the D045 human categories, which are *model-based Research Director "
        "review, not external expert ground truth*. §3–§5 are counterfactual arithmetic and "
        "coverage. §6 is the executor's interpretation.")
    add("")
    add("Orientation throughout: **log-odds = log-score(H2) − log-score(H1)**; positive supports "
        "H2. In all four `favored` cases the later resolution favours H2 (PROJECT_STATE). "
        "Ordinal mappings are placeholders (`v0-placeholder`): signs and relative sizes carry "
        "information, absolute magnitudes do not.")
    add("")

    # ---- 1 ------------------------------------------------------------ #
    add("## 1. Observed frozen verifier output")
    add("")
    add("| case | resolution | later favours | frozen scores H1 / H2 | log-odds | top |")
    add("| --- | --- | --- | --- | --- | --- |")
    hidden = json.loads((PACKET / "hidden_case_context.json").read_text(encoding="utf-8"))
    for cid, c in cases.items():
        o = c["original"]
        add("| {} | {} | {} | {:.3f} / {:.3f} | {} | {} |".format(
            cid, hidden[cid]["resolution_type"], c["later_resolution_favours"] or "—",
            o["scores"]["H1"], o["scores"]["H2"], _f(o["log_odds_H2_over_H1"]), o["top"]))
    add("")

    # ---- 2 ------------------------------------------------------------ #
    add("## 2. Influence by reviewed category")
    add("")
    add("Total absolute score influence across all 78 score-moving nodes: **{:.2f}**. "
        "Reviewed (40 nodes): {:.2f} ({:.1%}). Unreviewed (38 nodes): {:.2f} ({:.1%}).".format(
            total, cov["reviewed_absolute_influence"], cov["reviewed_share"],
            cov["unreviewed_absolute_influence"], 1 - cov["reviewed_share"]))
    add("")
    add("| category | nodes | absolute influence | share of all influence |")
    add("| --- | --- | --- | --- |")
    for key, name in SHORT.items():
        add("| {} | {} | {:.2f} | {:.1%} |".format(name, tb[key]["n_nodes"], tb[key]["absolute_influence"],
                                                    tb[key]["absolute_influence"] / total))
    add("")
    add("Signed log-odds by case and category (node count in brackets; `·` = no node):")
    add("")
    add("| case | frozen | " + " | ".join(SHORT.values()) + " | reviewed coverage |")
    add("| --- | --- | " + " | ".join("---" for _ in SHORT) + " | --- |")
    for cid, c in cases.items():
        cells = []
        for key in SHORT:
            b = c["categories"][key]
            cells.append("{} ({})".format(_f(b["log_odds_H2_over_H1"]), b["n_nodes"]) if b["n_nodes"] else "·")
        add("| {} | {} | {} | {:.0%} |".format(cid, _f(c["original"]["log_odds_H2_over_H1"]), " | ".join(cells),
                                              cov["per_case"][cid]["reviewed_share_of_case_influence"]))
    add("")
    fav = totals["favored_cases_log_odds_toward_later_favoured_hypothesis"]
    add("Summed over the four `favored` cases, toward the later-favoured hypothesis: " + ", ".join(
        "{} {}".format(SHORT[k], _f(v)) for k, v in fav.items()) + ".")
    add("")
    mech = _mech(result, packet)
    add("How reviewed categories moved scores (mechanical counts from verifier edges and evidence):")
    add("")
    add("| category | nodes | direct edges sign-opposed | non-origin hypothesis labelled unlikely/contradicted | push toward generating hypothesis | evidence support / contradiction |")
    add("| --- | --- | --- | --- | --- | --- |")
    for key in REVIEWED_CATEGORIES:
        m = mech[key]
        add("| {} | {} | {} | {} | {} | {} / {} |".format(
            SHORT[key], m["n"], m["sign_opposed_direct_edges"], m["non_origin_labelled_unlikely_or_contradicted"],
            m["push_toward_generating_hypothesis"], m["evidence_support"], m["evidence_contradiction"]))
    add("")

    # ---- 3 ------------------------------------------------------------ #
    add("## 3. Counterfactual views")
    add("")
    for key, (desc, _) in VIEWS.items():
        add("- **{}**: {}".format(VIEW_SHORT[key], desc))
    add("")
    add("Each cell: log-odds, top, relation to the later resolution (`agrees` / `opposes` / "
        "`no ordering`; non-directional cases show the lean only). *Evidence zeroed* is exact "
        "and additive. The bracketed *graph deleted* value also removes routes to descendants "
        "and is shown only where it differs by more than 0.05.")
    add("")
    add("| case | " + " | ".join(VIEW_SHORT.values()) + " |")
    add("| --- | " + " | ".join("---" for _ in VIEW_SHORT) + " |")
    for cid, c in cases.items():
        cells = []
        for key in VIEW_SHORT:
            v = c["views"][key]
            z, d = v["evidence_zeroed"], v["graph_deleted_sensitivity"]
            rel = {"agrees": "agrees", "opposes": "**opposes**", "no_ordering": "no ordering",
                   "not_applicable_non_directional_resolution": "lean"}[z["relation_to_later_resolution"]]
            cell = "{} {} {}".format(_f(z["log_odds_H2_over_H1"]), z["top"], rel)
            if abs(d["path_mediated_difference"]) > 0.05:
                cell += " [del {} {}]".format(_f(d["log_odds_H2_over_H1"]), d["top"])
            cells.append(cell)
        add("| {} | {} |".format(cid, " | ".join(cells)))
    add("")
    no_genuine = [cid for cid, c in cases.items() if c["categories"]["genuine_discriminator"]["n_nodes"] == 0]
    add("Cases with **no reviewed genuine discriminator** (A2 has nothing to order on): {} of 8 — {}.".format(
        len(no_genuine), ", ".join("`{}`".format(c) for c in no_genuine)))
    add("")
    unstable = [cid for cid, c in cases.items()
                if c["views"]["A1_genuine_reviewed_plus_unreviewed"]["evidence_zeroed"]["top"]
                != c["views"]["A1_genuine_reviewed_plus_unreviewed"]["graph_deleted_sensitivity"]["top"]]
    if unstable:
        add("Where the two decompositions disagree on the top hypothesis (path-mediated effects "
            "large enough to change the ordering): {}.".format(", ".join("`{}` (view A1)".format(c) for c in unstable)))
        add("")

    # ---- 4 ------------------------------------------------------------ #
    add("## 4. Focus cases")
    add("")
    def cat(cid, key):
        return cases[cid]["categories"][key]["log_odds_H2_over_H1"]
    def view(cid, key):
        return cases[cid]["views"][key]["evidence_zeroed"]

    g = "glnbp_induced_fit_vs_conformational_selection"
    add("### GlnBP (later resolution: induced fit, H2)")
    add("")
    add("- frozen: {} toward induced fit. Silence errors contribute {}, generic component facts {}, "
        "genuine discriminators **{}**, compatible {}, unreviewed {}.".format(
            _f(cases[g]["original"]["log_odds_H2_over_H1"]), _f(cat(g, "silence_as_null_error")),
            _f(cat(g, "generic_component_fact")), _f(cat(g, "genuine_discriminator")),
            _f(cat(g, "compatible_non_discriminative")), _f(cat(g, "unreviewed_score_moving"))))
    add("- genuine discriminators only (A2): {} → **{}** ({}).".format(
        _f(view(g, "A2_genuine_reviewed_only")["log_odds_H2_over_H1"]), view(g, "A2_genuine_reviewed_only")["top"],
        view(g, "A2_genuine_reviewed_only")["relation_to_later_resolution"]))
    add("- confirmed errors removed (B1): {} → {} ({}), carried by generic component facts ({}) against "
        "the genuine discriminators ({}).".format(
        _f(view(g, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"]), view(g, "B1_remove_confirmed_errors")["top"],
        view(g, "B1_remove_confirmed_errors")["relation_to_later_resolution"],
        _f(cat(g, "generic_component_fact")), _f(cat(g, "genuine_discriminator"))))
    add("")
    e = "eukaryogenesis_mito_timing"
    add("### Eukaryogenesis (later resolution: complex host before mitochondria, H2)")
    add("")
    add("- frozen: {}. Generic component facts {}, weak implication {}, silence error {}, unreviewed {}; "
        "no reviewed genuine discriminator.".format(
            _f(cases[e]["original"]["log_odds_H2_over_H1"]), _f(cat(e, "generic_component_fact")),
            _f(cat(e, "invalid_or_weak_implication")), _f(cat(e, "silence_as_null_error")),
            _f(cat(e, "unreviewed_score_moving"))))
    add("- after removing reviewed invalid, generic and silence contributions, what remains is "
        "genuine ({}) plus compatible ({}) plus unreviewed ({}) = **{}**; A1 top **{}**.".format(
            _f(cat(e, "genuine_discriminator")), _f(cat(e, "compatible_non_discriminative")),
            _f(cat(e, "unreviewed_score_moving")),
            _f(cat(e, "genuine_discriminator") + cat(e, "compatible_non_discriminative") + cat(e, "unreviewed_score_moving")),
            view(e, "A1_genuine_reviewed_plus_unreviewed")["top"]))
    add("- errors removed only (B1): {} ({}), carried by generic component facts.".format(
        _f(view(e, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"]),
        view(e, "B1_remove_confirmed_errors")["relation_to_later_resolution"]))
    add("")
    fw = "fly_wing_constraint_vs_selection"
    add("### Fly-wing (later resolution: correlational selection, H2)")
    add("")
    add("- frozen: {}; the single reviewed node is a silence error ({}); the only other score-moving "
        "node is unreviewed ({}).".format(_f(cases[fw]["original"]["log_odds_H2_over_H1"]),
                                          _f(cat(fw, "silence_as_null_error")), _f(cat(fw, "unreviewed_score_moving"))))
    add("- errors removed (B1): {} {}; strict (B2): {}.".format(
        _f(view(fw, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"]), view(fw, "B1_remove_confirmed_errors")["top"],
        view(fw, "B2_remove_confirmed_errors_reviewed_only")["top"]))
    add("")
    ps = "pfc_storage_vs_control"
    add("### PFC storage vs control (later resolution: control, H2; frozen verifier favoured storage)")
    add("")
    add("- frozen: {} (toward storage). Silence error {}, construct mismatch {}, compatible {}, "
        "genuine discriminators **{}**, unreviewed {}.".format(
            _f(cases[ps]["original"]["log_odds_H2_over_H1"]), _f(cat(ps, "silence_as_null_error")),
            _f(cat(ps, "evidence_construct_mismatch")), _f(cat(ps, "compatible_non_discriminative")),
            _f(cat(ps, "genuine_discriminator")), _f(cat(ps, "unreviewed_score_moving"))))
    add("- genuine only (A2): {} {} ({}); errors removed (B1): {} {} ({}).".format(
        _f(view(ps, "A2_genuine_reviewed_only")["log_odds_H2_over_H1"]), view(ps, "A2_genuine_reviewed_only")["top"],
        view(ps, "A2_genuine_reviewed_only")["relation_to_later_resolution"],
        _f(view(ps, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"]), view(ps, "B1_remove_confirmed_errors")["top"],
        view(ps, "B1_remove_confirmed_errors")["relation_to_later_resolution"]))
    add("")

    # ---- coverage ------------------------------------------------------ #
    add("## 5. Coverage and the next review batch")
    add("")
    add("| case | score-moving | reviewed | reviewed share of case influence | unreviewed influence |")
    add("| --- | --- | --- | --- | --- |")
    for cid, v in cov["per_case"].items():
        add("| {} | {} | {} | {:.1%}{} | {:.2f} |".format(
            cid, v["score_moving_nodes"], v["reviewed_nodes"], v["reviewed_share_of_case_influence"],
            " (below packet-wide {:.1%})".format(cov["reviewed_share"]) if v["below_packet_design_coverage"] else "",
            v["unreviewed_absolute_influence"]))
    add("")
    nb = cov["recommended_next_review_batch"]
    add("Recommended next human-review batch (not labelled here): the {} unreviewed nodes in the three "
        "low-influence cases — {} — then the remaining {} by influence.".format(
            len(nb["first_low_coverage_cases"]), ", ".join("`{}`".format(x) for x in nb["first_low_coverage_cases"]),
            len(nb["then_remaining_by_influence"])))
    add("")
    L.extend(render_interpretation(result, cov, totals, mech))
    return "\n".join(L)


def render_interpretation(result, cov, totals, mech) -> List[str]:
    cases = result["cases"]
    tb = totals["by_category"]
    total = cov["total_absolute_influence"]
    share = lambda k: tb[k]["absolute_influence"] / total
    def lo(cid, key):
        return cases[cid]["categories"][key]["log_odds_H2_over_H1"]
    def v(cid, name):
        return cases[cid]["views"][name]["evidence_zeroed"]
    e, g, fw, ps = ("eukaryogenesis_mito_timing", "glnbp_induced_fit_vs_conformational_selection",
                    "fly_wing_constraint_vs_selection", "pfc_storage_vs_control")
    frozen_agrees = [c for c in FAVOURED if cases[c]["views"]["original"]["evidence_zeroed"]["relation_to_later_resolution"] == "agrees"]
    a2_agrees = [c for c in FAVOURED if v(c, "A2_genuine_reviewed_only")["relation_to_later_resolution"] == "agrees"]
    no_genuine = [c for c in cases if cases[c]["categories"]["genuine_discriminator"]["n_nodes"] == 0]
    errors = sum(share(k) for k in CONFIRMED_ERRORS)
    nondisc = share("generic_component_fact") + share("compatible_non_discriminative")
    m_sil, m_gen = mech["silence_as_null_error"], mech["generic_component_fact"]

    L = ["## 6. Interpretation (executor; for the Research Director, not a decision)", ""]
    L.append("**Every judgment below is conditional on the D045 labels being correct.** They are model-based "
             "first-pass review, and {:.1%} of score influence is still unreviewed.".format(1 - cov["reviewed_share"]))
    L.append("")
    L.append("**1. None of the frozen pilot's agreements with the later resolution rests on a reviewed genuine "
             "discriminator.** The frozen verifier agreed in {} of the 4 `favored` cases ({}). Restricted to "
             "reviewed genuine discriminators (A2), {} of those agree:".format(
                 len(frozen_agrees), ", ".join(frozen_agrees), sum(1 for c in frozen_agrees if c in a2_agrees)))
    L.append("")
    L.append("- **Eukaryogenesis** and **fly-wing** have no reviewed genuine discriminator, so A2 gives no ordering.")
    L.append("- **GlnBP's** two genuine discriminators point the other way ({}, toward conformational "
             "selection). Its frozen {} toward induced fit came from silence errors ({}) and generic component "
             "facts ({}).".format(_f(lo(g, "genuine_discriminator")), _f(cases[g]["original"]["log_odds_H2_over_H1"]),
                                  _f(lo(g, "silence_as_null_error")), _f(lo(g, "generic_component_fact"))))
    L.append("")
    L.append("**2. Removing only the confirmed errors (B1) keeps the right direction in two of those cases, but "
             "on component facts, not discrimination.** Eukaryogenesis stays at {} and GlnBP at {}; generic "
             "component facts contribute {} and {} respectively. Fly-wing collapses to {}, carried by a single "
             "unreviewed node, so its apparent success disappears.".format(
                 _f(v(e, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"]),
                 _f(v(g, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"]),
                 _f(lo(e, "generic_component_fact")), _f(lo(g, "generic_component_fact")),
                 "{:+.3f}".format(v(fw, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"])))
    L.append("")
    L.append("**3. The one failure reverses under reviewed attribution.** In PFC storage vs control, the two "
             "genuine discriminators favour the later-supported control account ({}). One silence error ({}) "
             "and three construct mismatches ({}) outweighed them. Genuine only (A2) gives {}; errors removed "
             "(B1) gives {}.".format(
                 _f(lo(ps, "genuine_discriminator")), _f(lo(ps, "silence_as_null_error")),
                 _f(lo(ps, "evidence_construct_mismatch")),
                 _f(v(ps, "A2_genuine_reviewed_only")["log_odds_H2_over_H1"]),
                 _f(v(ps, "B1_remove_confirmed_errors")["log_odds_H2_over_H1"])))
    L.append("")
    L.append("*Relation to an earlier retraction:* the pilot report withdrew a similar claim. It rested on the "
             "LLM auditor, which had miscalled X15. D045 labels X15 a construct mismatch, not genuine; the claim "
             "now rests on X6 and X24 instead.")
    L.append("")
    L.append("**4. Most cases are underdetermined once non-discriminative reviewed nodes are set aside.** {} of 8 "
             "cases have no reviewed genuine discriminator. With unreviewed nodes left in (A1), their leanings rest "
             "entirely on unreviewed nodes. Those leanings can flip (eukaryogenesis goes to {}) or depend on the "
             "decomposition (forest).".format(
                 len(no_genuine), _f(v(e, "A1_genuine_reviewed_plus_unreviewed")["log_odds_H2_over_H1"])))
    L.append("")
    L.append("**5. The dominant problem is broader than silence handling.** Shares of all score influence:")
    L.append("")
    L.append("| group | share |")
    L.append("| --- | --- |")
    L.append("| reviewed silence errors | {:.1%} |".format(share("silence_as_null_error")))
    L.append("| generic component facts + compatible non-discriminative propositions | **{:.1%}** |".format(nondisc))
    L.append("| all confirmed errors (silence, construct mismatch, weak implication) | {:.1%} |".format(errors))
    L.append("| reviewed genuine discriminators | **{:.1%}** |".format(share("genuine_discriminator")))
    L.append("")
    L.append("Mechanically, the categories share one pathway: the hypothesis that did not generate the proposition "
             "received `unlikely`/`strongly_contradicted`. This happened in {} of {} silence errors and {} of {} "
             "generic component facts. {} of the {} generic component facts carried literature support.".format(
                 m_sil["non_origin_labelled_unlikely_or_contradicted"], m_sil["n"],
                 m_gen["non_origin_labelled_unlikely_or_contradicted"], m_gen["n"],
                 m_gen["evidence_support"], m_gen["n"]))
    L.append("")
    L.append("The reviewed categories differ in *why* that opposing label is unwarranted: the competitor is silent, "
             "or the fact is not specific to the hypothesis. That supports D045's reading of a broader "
             "discrimination/relevance failure rather than a single silence bug.")
    L.append("")
    L.append("Per the directive, no fix is proposed here.")
    L.append("")
    return L


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = bp.extract_verified(Path(tmp))
        result = analyse(root / "run")
    cov = coverage(result["nodes"], result["cases"])
    totals = totals_across_cases(result["cases"])
    write(result, cov, totals, OUT)
    packet = {json.loads(line)["review_id"]: json.loads(line)
              for line in (PACKET / "review_set_full.jsonl").read_text(encoding="utf-8").splitlines()}
    (OUT / "ATTRIBUTION_REPORT.md").write_text(render_report(result, cov, totals, packet) + "\n", encoding="utf-8")
    print(json.dumps({"reviewed_share": cov["reviewed_share"], "under_covered": cov["under_covered_cases"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
