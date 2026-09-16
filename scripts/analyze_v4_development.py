"""BENCH-GRAPH-V4-DEV-001 development metrics for a stage-A replay (v4 on frozen v3).

Deterministic, no LLM. Compares, node by node on identical propositions and evidence:

  A. prediction-state behaviour: v4 states vs v3 direct edge labels read as states
     (implied* -> positive, unlikely/contradicted -> negative, neutral -> indeterminate);
  B. comparative eligibility and the reasons propositions are gated;
  C. alignment with the D045/D046 development labels (and the D046 state confusion);
  D. score-influence composition by reviewed category, v3 vs v4.

v3 contributions come from `attribution_d045_d046/node_contributions.jsonl`, which was
reproduced exactly from the frozen run. Influence is |log-odds contribution| between the
two hypotheses. The D045/D046 labels are DEVELOPMENT annotations: this script reports
agreement, it does not optimise it.

Usage:
    python scripts/analyze_v4_development.py --replay runs/v4_replay_pilot_iter01
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "benchmark" / "review" / "graph_pilot_001"
V3_NODES = PACKET / "attribution_d045_d046" / "node_contributions.jsonl"
OUT_ROOT = ROOT / "benchmark" / "v4_dev"

CATEGORIES = ["genuine_discriminator", "silence_as_null_error", "generic_component_fact",
              "compatible_non_discriminative", "evidence_construct_mismatch", "invalid_or_weak_implication"]
FAILURE_CATEGORIES = ["silence_as_null_error", "generic_component_fact", "compatible_non_discriminative",
                      "evidence_construct_mismatch", "invalid_or_weak_implication"]
V3_EDGE_AS_STATE = {"strongly_implied": "positive_or_present", "implied": "positive_or_present",
                    "weakly_implied": "positive_or_present", "neutral": "indeterminate",
                    "unlikely": "negative_or_absent", "strongly_contradicted": "negative_or_absent"}
FAVOURED = {"eukaryogenesis_mito_timing": "H2", "fly_wing_constraint_vs_selection": "H2",
            "glnbp_induced_fit_vs_conformational_selection": "H2", "pfc_storage_vs_control": "H2"}


def _jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _profile(states: Dict[str, str]) -> str:
    det = [s for s in states.values() if s != "indeterminate"]
    if not det:
        return "all_indeterminate"
    if len(det) == len(states):
        return "comparative_discriminator" if len(set(det)) > 1 else "shared_prediction"
    return "one_sided_prediction"


def load(replay: Path):
    labels: Dict[str, Dict[str, Any]] = {}
    for name in ("human_labels_D045.json", "human_labels_D046.json"):
        data = json.loads((PACKET / name).read_text(encoding="utf-8"))
        for l in data["labels"]:
            labels[l["review_id"]] = dict(l, source=data["human_review_source"])
    packet = {r["review_id"]: r for r in _jsonl(PACKET / "review_set_full.jsonl")}
    v3 = {n["review_id"]: n for n in _jsonl(V3_NODES)}
    v4: Dict[str, Dict[str, Any]] = {}
    cases: Dict[str, Any] = OrderedDict()
    for path in sorted((replay / "instances").glob("*/discrimination.json")):
        layer = json.loads(path.read_text(encoding="utf-8"))
        case = path.parent.name
        cases[case] = layer
        for nid, rec in layer["nodes"].items():
            v4["GP1-{}-{}".format(case, nid)] = dict(rec, case_id=case, node_id=nid)
    return labels, packet, v3, v4, cases


def analyse(replay: Path) -> Dict[str, Any]:
    labels, packet, v3, v4, cases = load(replay)
    if set(v4) != set(v3):
        raise SystemExit("replay nodes differ from the frozen v3 nodes")

    # ---------------- A. prediction states --------------------------------------
    v4_pairs, v3_pairs, v4_profiles, v3_profiles = Counter(), Counter(), Counter(), Counter()
    unavailable = 0
    for rid, rec in v4.items():
        if not rec["states"]:
            unavailable += 1
        else:
            for s in rec["states"].values():
                v4_pairs[s["state"]] += 1
            v4_profiles[rec["profile_class"]] += 1
        if rid in packet:          # score-moving: v3 edges available in the packet
            edges = packet[rid]["verifier_graph"]["cross_hypothesis_judgments"]
            st = {h: V3_EDGE_AS_STATE[v["direct_edge_label"]] for h, v in edges.items()}
            for s in st.values():
                v3_pairs[s] += 1
            v3_profiles[_profile(st)] += 1
    # v3 edges for non-moving nodes are not in the packet; read them from the replay's
    # graph-independent source: every node has direct edges in the frozen run, but the
    # packet only holds score-moving ones, so v3 profile counts cover score-moving nodes.
    n_pairs_v4 = sum(v4_pairs.values())
    section_a = OrderedDict([
        ("v4_all_192_nodes", OrderedDict([
            ("pair_states", dict(v4_pairs)),
            ("fraction_pairs_indeterminate", v4_pairs["indeterminate"] / n_pairs_v4 if n_pairs_v4 else None),
            ("profiles", dict(v4_profiles)), ("nodes_states_unavailable", unavailable)])),
        ("v3_score_moving_78_nodes_edges_read_as_states", OrderedDict([
            ("mapping", V3_EDGE_AS_STATE), ("pair_states", dict(v3_pairs)),
            ("fraction_pairs_indeterminate", v3_pairs["indeterminate"] / sum(v3_pairs.values())),
            ("profiles", dict(v3_profiles))])),
        ("v4_on_the_same_78_score_moving_nodes", OrderedDict([
            ("profiles", dict(Counter(v4[r]["profile_class"] for r in packet if v4[r]["states"]))),
            ("pair_states", dict(Counter(s["state"] for r in packet if v4[r]["states"]
                                         for s in v4[r]["states"].values())))])),
    ])

    # ---------------- B. eligibility -------------------------------------------
    n = len(v4)
    reasons = Counter(r["gate_reason"] for r in v4.values())
    construct = Counter((r.get("construct") or {}).get("construct_match") for r in v4.values()
                        if r.get("evidence_label") not in (None, "no_evidence", "mixed"))
    section_b = OrderedDict([
        ("n_nodes", n),
        ("fraction_comparatively_eligible", sum(1 for r in v4.values() if r["comparatively_eligible"]) / n),
        ("fraction_used_in_score", sum(1 for r in v4.values() if r["used_in_score"]) / n),
        ("fraction_one_sided", v4_profiles["one_sided_prediction"] / n),
        ("fraction_shared", v4_profiles["shared_prediction"] / n),
        ("fraction_all_indeterminate", v4_profiles["all_indeterminate"] / n),
        ("gate_reasons", dict(reasons)),
        ("construct_match_on_informative_evidence", {str(k): v for k, v in construct.items()}),
        ("eligible_blocked_by_construct", sum(1 for r in v4.values()
                                              if r["comparatively_eligible"] and
                                              str(r["gate_reason"]).startswith("construct_"))),
        ("generic_component_fact_note",
         "v4 has no separate generic-fact classifier: generic facts are gated when their state profile is "
         "shared or one-sided; section C reports what happened to the reviewed generic facts"),
    ])

    # ---------------- C. alignment with development labels ----------------------
    per_node = []
    for rid, lab in sorted(labels.items(), key=lambda kv: kv[0]):
        rec = v4[rid]
        spread = abs(rec["contribution"]["H2"] - rec["contribution"]["H1"])
        per_node.append(OrderedDict([
            ("review_id", rid), ("source", lab["source"]), ("human_primary_category", lab["human_primary_category"]),
            ("human_secondary_flags", lab.get("human_secondary_flags") or []),
            ("v4_states", {h: s["state"] for h, s in (rec["states"] or {}).items()}),
            ("v4_profile", rec["profile_class"]), ("v4_eligible", rec["comparatively_eligible"]),
            ("evidence_label", rec["evidence_label"]),
            ("v4_construct", (rec.get("construct") or {}).get("construct_match")),
            ("v4_used_in_score", rec["used_in_score"]), ("v4_gate_reason", rec["gate_reason"]),
            ("v3_influence", v3[rid]["absolute_influence"]), ("v4_influence", spread),
        ]))
    by_cat = OrderedDict()
    for cat in CATEGORIES:
        rows = [r for r in per_node if r["human_primary_category"] == cat]
        by_cat[cat] = OrderedDict([
            ("n", len(rows)),
            ("v4_eligible", sum(r["v4_eligible"] for r in rows)),
            ("v4_used_in_score", sum(r["v4_used_in_score"] for r in rows)),
            ("v4_any_hypothesis_indeterminate", sum(1 for r in rows if "indeterminate" in r["v4_states"].values())),
            ("v4_gate_reasons", dict(Counter(r["v4_gate_reason"] for r in rows))),
            ("v3_influence", sum(r["v3_influence"] for r in rows)),
            ("v4_influence", sum(r["v4_influence"] for r in rows)),
        ])
    # D046 per-hypothesis state confusion
    confusion, rows_conf = Counter(), []
    for rid, lab in labels.items():
        states = lab.get("human_prediction_for_each_hypothesis")
        if not states:
            continue
        for h, human in states.items():
            qualified = lab["human_prediction_qualifiers"][h]["qualified"]
            got = (v4[rid]["states"] or {}).get(h, {}).get("state")
            confusion[(human, got, qualified)] += 1
            rows_conf.append(OrderedDict([("review_id", rid), ("hypothesis", h), ("human", human),
                                          ("v4", got), ("qualified", qualified)]))
    unq = [r for r in rows_conf if not r["qualified"]]
    section_c = OrderedDict([
        ("by_human_category", by_cat),
        ("silence_errors_now_gated", "{}/{}".format(
            sum(1 for r in per_node if r["human_primary_category"] == "silence_as_null_error"
                and not r["v4_used_in_score"]),
            by_cat["silence_as_null_error"]["n"])),
        ("genuine_discriminators", [r for r in per_node if r["human_primary_category"] == "genuine_discriminator"]),
        ("d046_state_confusion", OrderedDict([
            ("pairs", rows_conf),
            ("agreement_unqualified", "{}/{}".format(sum(1 for r in unq if r["human"] == r["v4"]), len(unq))),
            ("agreement_all", "{}/{}".format(sum(1 for r in rows_conf if r["human"] == r["v4"]), len(rows_conf))),
            ("matrix", [OrderedDict([("human", h), ("v4", g), ("qualified", q), ("n", c)])
                        for (h, g, q), c in sorted(confusion.items(), key=lambda kv: str(kv[0]))]),
        ])),
        ("per_node", per_node),
    ])

    # ---------------- D. influence composition ---------------------------------
    def composition(influence_of):
        total = sum(influence_of(r) for r in v4)
        out = OrderedDict([("total_absolute_influence", total)])
        for cat in CATEGORIES + ["unreviewed"]:
            val = sum(influence_of(r) for r in v4
                      if (labels.get(r, {}).get("human_primary_category") or "unreviewed") == cat)
            out[cat] = OrderedDict([("absolute_influence", val), ("share", val / total if total else None)])
        return out

    v3_comp = composition(lambda r: v3[r]["absolute_influence"])
    v4_comp = composition(lambda r: abs(v4[r]["contribution"]["H2"] - v4[r]["contribution"]["H1"]))
    section_d = OrderedDict([
        ("v3", v3_comp), ("v4", v4_comp),
        ("failure_categories_influence", OrderedDict([
            ("v3", sum(v3_comp[c]["absolute_influence"] for c in FAILURE_CATEGORIES)),
            ("v4", sum(v4_comp[c]["absolute_influence"] for c in FAILURE_CATEGORIES))])),
        ("confirmed_errors_influence (silence + mismatch + weak)", OrderedDict([
            ("v3", sum(v3_comp[c]["absolute_influence"] for c in
                       ("silence_as_null_error", "evidence_construct_mismatch", "invalid_or_weak_implication"))),
            ("v4", sum(v4_comp[c]["absolute_influence"] for c in
                       ("silence_as_null_error", "evidence_construct_mismatch", "invalid_or_weak_implication")))])),
    ])

    # ---------------- per case --------------------------------------------------
    per_case = OrderedDict()
    for case, layer in cases.items():
        v3s, v4s = layer["v3_frozen_scores"], layer["scores"]
        lo3 = v3s["H2"] - v3s["H1"]
        top3 = "H2" if v3s["H2"] > v3s["H1"] else "H1"
        top4 = "tie" if abs(v4s["H2"] - v4s["H1"]) < 1e-12 else ("H2" if v4s["H2"] > v4s["H1"] else "H1")
        fav = FAVOURED.get(case)
        scored = [nid for nid, r in layer["nodes"].items() if r["used_in_score"]]
        per_case[case] = OrderedDict([
            ("v3_scores", v3s), ("v4_scores", v4s), ("v3_top", top3), ("v4_top", top4),
            ("later_resolution_favours", fav),
            ("v4_relation", None if fav is None else ("no_ordering" if top4 == "tie" else
                                                     ("agrees" if top4 == fav else "opposes"))),
            ("v4_scored_nodes", OrderedDict((nid, OrderedDict([
                ("human_label", labels.get("GP1-{}-{}".format(case, nid), {}).get("human_primary_category")),
                ("states", {h: s["state"] for h, s in layer["nodes"][nid]["states"].items()}),
                ("evidence_label", layer["nodes"][nid]["evidence_label"]),
                ("contribution_log_odds_H2_over_H1",
                 layer["nodes"][nid]["contribution"]["H2"] - layer["nodes"][nid]["contribution"]["H1"]),
            ])) for nid in scored)),
            ("summary", layer["summary"]),
        ])

    return OrderedDict([("replay", str(replay.relative_to(ROOT))), ("A_prediction_states", section_a),
                        ("B_eligibility", section_b), ("C_human_alignment", section_c),
                        ("D_influence_composition", section_d), ("per_case", per_case)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", required=True)
    args = parser.parse_args()
    replay = (ROOT / args.replay).resolve()
    result = analyse(replay)
    out = OUT_ROOT / replay.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "development_metrics.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print("wrote", (out / "development_metrics.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
