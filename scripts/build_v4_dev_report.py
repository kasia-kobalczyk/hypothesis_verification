"""Generate docs/V4_DEV_REPORT.md from the development metrics (deterministic).

Numbers come from:
  benchmark/v4_dev/iter0{1,2,3}/development_metrics.json   stage A replays (2 replicates each)
  benchmark/v4_dev/stage_b/run_comparison.json              end-to-end runs + noise floor

The iteration log (what changed, why, which commit) is authored below as data, because
it records decisions, not measurements.

Usage:
    python scripts/build_v4_dev_report.py
"""
from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "benchmark" / "v4_dev"
OUT = ROOT / "docs" / "V4_DEV_REPORT.md"

CATS = ["genuine_discriminator", "silence_as_null_error", "generic_component_fact",
        "compatible_non_discriminative", "evidence_construct_mismatch", "invalid_or_weak_implication"]
SHORT = {"genuine_discriminator": "genuine", "silence_as_null_error": "silence err",
         "generic_component_fact": "generic fact", "compatible_non_discriminative": "compatible",
         "evidence_construct_mismatch": "construct mism.", "invalid_or_weak_implication": "weak impl.",
         "unreviewed": "unreviewed"}

ITERATIONS = [
    OrderedDict([
        ("id", "iter01"), ("commit", "83b707f"),
        ("state_prompt", "prediction_state_v1"), ("construct_prompt", "construct_match_v1"),
        ("change", "Initial v4: prediction states with strength only for determinate states; deterministic "
                   "discrimination gate; holistic construct match; direct-only; gated scoring without chain routes."),
        ("why", "Directive design."),
    ]),
    OrderedDict([
        ("id", "iter02"), ("commit", "7f4718b"),
        ("state_prompt", "prediction_state_v2"), ("construct_prompt", "construct_match_v2"),
        ("change", "State prompt: general scope rule (a candidate about one system does not determine claims "
                   "about a broader class or another member). Construct match: element-wise; the gating label "
                   "is derived in code ('direct' only if every asserted element is established); the holistic "
                   "impression is recorded, never used."),
        ("why", "Iteration 1: reviewed generic component facts scored through contrasting states on "
                "class-level propositions; a reviewed construct mismatch (PFC storage X15, 'store and "
                "represent') was judged 'direct'; single construct flips swung case outcomes between replicates."),
    ]),
    OrderedDict([
        ("id", "iter03"), ("commit", "6817782"),
        ("state_prompt", "prediction_state_v3"), ("construct_prompt", "construct_match_v2"),
        ("change", "State prompt: explicit, required proposition scope (within / broader than candidates / "
                   "possibility only); the gate classifies out-of-scope propositions as "
                   "generic_or_possibility_claim regardless of states."),
        ("why", "Iteration 2: 5 of 14 reviewed generic facts stayed comparatively eligible despite the advisory "
                "scope rule (family-level and 'can / is possible' claims). Human decision after iteration 2: fix "
                "the state side only, keep direct-only, do not freeze, escalate the evidence policy."),
    ]),
    OrderedDict([
        ("id", "head"), ("commit", "a770f94"),
        ("state_prompt", "prediction_state_v2"), ("construct_prompt", "construct_match_v2"),
        ("change", "Development head reverted to iteration 2's state prompt; the v3 prompt and scope gate remain "
                   "implemented and tested but inactive. No new replay needed: iteration 2 already has two replicates."),
        ("why", "Iteration 3 regressed on both replicates (more manufactured contrasts, lower stability, only "
                "failure-category nodes scored). Further state-side tuning stopped per the human decision."),
    ]),
]


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _pct(x):
    return "—" if x is None else "{:.0%}".format(x)


def build() -> str:
    iters = OrderedDict((it["id"], _load(DEV / it["id"] / "development_metrics.json"))
                        for it in ITERATIONS if (DEV / it["id"] / "development_metrics.json").exists())
    stage_b_path = DEV / "stage_b" / "run_comparison.json"
    stage_b = _load(stage_b_path) if stage_b_path.exists() else None
    L = []
    add = L.append

    add("# v4 development report — BENCH-GRAPH-V4-DEV-001")
    add("")
    add("**Status: NOT FROZEN — evidence-directness policy escalated to the Research Director.** The eight cases "
        "are a spent development set; nothing here is held-out evidence. D045/D046 are model-based Research "
        "Director development labels, used to diagnose behaviour, not as ground truth or an optimisation target.")
    add("")
    add("Design: `docs/V4_DESIGN.md`. Metrics: `benchmark/v4_dev/`. Every stage-A iteration was replayed twice "
        "on the frozen v3 pilot (same propositions, same retrieved records, same evidence labels), so v3 and v4 "
        "are compared node by node.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 1. Iteration log")
    add("")
    add("| iteration | commit | state prompt | construct prompt | change | why |")
    add("| --- | --- | --- | --- | --- | --- |")
    for it in ITERATIONS:
        add("| {id} | `{commit}` | `{state_prompt}` | `{construct_prompt}` | {change} | {why} |".format(**it))
    add("")
    add("No case-specific rule, no benchmark answer in any prompt, no change to numeric mappings, and no change "
        "to the construct policy (direct only, human decision) in any iteration.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 2. Structural metrics per iteration (stage A, both replicates)")
    add("")
    add("| iteration · replicate | pairs indeterminate | comparative | one-sided | shared | out-of-scope | eligible | scored | construct direct / partial / mismatch (informative evidence) |")
    add("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for iid, m in iters.items():
        for rep, R in m["replicates"].items():
            a = R["A_prediction_states"]["v4_all_192_nodes"]
            b = R["B_eligibility"]
            pr = a["profiles"]
            cm = b["construct_match_on_informative_evidence"]
            add("| {} · {} | {} | {} | {} | {} | {} | {} | {} | {} / {} / {} |".format(
                iid, "rep2" if rep.endswith("rep2") else "rep1", _pct(a["fraction_pairs_indeterminate"]),
                pr.get("comparative_discriminator", 0), pr.get("one_sided_prediction", 0),
                pr.get("shared_prediction", 0), pr.get("generic_or_possibility_claim", 0),
                round(b["fraction_comparatively_eligible"] * 192), round(b["fraction_used_in_score"] * 192),
                cm.get("direct", 0), cm.get("partial", 0), cm.get("mismatch", 0)))
    first = next(iter(iters.values()))["replicates"]
    v3a = next(iter(first.values()))["A_prediction_states"]["v3_score_moving_78_nodes_edges_read_as_states"]
    add("")
    add("v3 reference (its direct edge labels read as states, on the 78 score-moving nodes): {:.0%} of pairs "
        "`neutral`; profiles {}. v3 scored every node with an evidence label.".format(
            v3a["fraction_pairs_indeterminate"], v3a["profiles"]))
    add("")
    add("**Stability between replicates**")
    add("")
    add("| iteration | state pairs | profile class | scored / not | construct label |")
    add("| --- | --- | --- | --- | --- |")
    for iid, m in iters.items():
        s = m["stability"]
        add("| {} | {} | {} | {} | {} |".format(iid, s["state_pair_agreement"], s["profile_agreement"],
                                                s["used_in_score_agreement"], s["construct_agreement"]))
    add("")

    # ------------------------------------------------------------------ #
    add("## 3. Alignment with D045/D046 development labels")
    add("")
    add("Per reviewed category: comparatively eligible (before construct gating) / scored, over the two replicates.")
    add("")
    add("| category (n) | " + " | ".join(iters) + " |")
    add("| --- | " + " | ".join("---" for _ in iters) + " |")
    any_rep = next(iter(next(iter(iters.values()))["replicates"].values()))
    for cat in CATS:
        n = any_rep["C_human_alignment"]["by_human_category"][cat]["n"]
        cells = []
        for m in iters.values():
            reps = list(m["replicates"].values())
            cells.append(" · ".join("{}/{}".format(r["C_human_alignment"]["by_human_category"][cat]["v4_eligible"],
                                                    r["C_human_alignment"]["by_human_category"][cat]["v4_used_in_score"])
                                     for r in reps))
        add("| {} ({}) | {} |".format(SHORT[cat], n, " | ".join(cells)))
    add("")
    add("D046 per-hypothesis state agreement (12 nodes × 2 hypotheses; 4 states were qualified by the reviewer):")
    add("")
    for iid, m in iters.items():
        reps = list(m["replicates"].values())
        add("- {}: unqualified {} · all {}".format(iid, " / ".join(r["C_human_alignment"]["d046_state_confusion"]["agreement_unqualified"] for r in reps),
                                                   " / ".join(r["C_human_alignment"]["d046_state_confusion"]["agreement_all"] for r in reps)))
    add("")
    add("**Fate of the four D045 genuine discriminators**")
    add("")
    add("| node | " + " | ".join(iters) + " |")
    add("| --- | " + " | ".join("---" for _ in iters) + " |")
    names = [g["review_id"] for g in any_rep["C_human_alignment"]["genuine_discriminators"]]
    for rid in names:
        cells = []
        for m in iters.values():
            parts = []
            for r in m["replicates"].values():
                g = next(x for x in r["C_human_alignment"]["genuine_discriminators"] if x["review_id"] == rid)
                parts.append(g["v4_gate_reason"])
            cells.append(" · ".join(parts))
        add("| `{}` | {} |".format(rid[4:], " | ".join(cells)))
    add("")

    # ------------------------------------------------------------------ #
    add("## 4. Score-influence composition (|log-odds|, by reviewed category)")
    add("")
    add("| category | v3 (frozen) | " + " | ".join("{} rep1 · rep2".format(i) for i in iters) + " |")
    add("| --- | --- | " + " | ".join("---" for _ in iters) + " |")
    v3d = any_rep["D_influence_composition"]["v3"]
    for cat in CATS + ["unreviewed"]:
        cells = []
        for m in iters.values():
            cells.append(" · ".join("{:.2f}".format(r["D_influence_composition"]["v4"][cat]["absolute_influence"])
                                     for r in m["replicates"].values()))
        add("| {} | {:.2f} ({}) | {} |".format(SHORT[cat], v3d[cat]["absolute_influence"], _pct(v3d[cat]["share"]),
                                               " | ".join(cells)))
    tot = []
    for m in iters.values():
        tot.append(" · ".join("{:.2f}".format(r["D_influence_composition"]["v4"]["total_absolute_influence"])
                               for r in m["replicates"].values()))
    add("| **total** | {:.2f} | {} |".format(v3d["total_absolute_influence"], " | ".join(tot)))
    add("")

    # ------------------------------------------------------------------ #
    add("## 5. The evidence-policy question (for the Research Director)")
    add("")
    add("Under the human-decided direct-only policy with element-wise construct matching (iteration 2 = development "
        "head), **no proposition scores on any development case in either replicate**: every eligible proposition's "
        "cited records establish only part of what it asserts. All four reviewed genuine discriminators are "
        "eligible but blocked as `construct_partial`.")
    add("")
    add("Sensitivity only (recomputed from the recorded judgments, no model call; NOT the policy): case scores "
        "P(H2) if `partial` evidence were also allowed.")
    add("")
    add("| case | " + " | ".join("{} rep1 · rep2".format(i) for i in iters) + " |")
    add("| --- | " + " | ".join("---" for _ in iters) + " |")
    case_ids = list(any_rep["per_case"])
    for cid in case_ids:
        cells = []
        for m in iters.values():
            cells.append(" · ".join("{:.2f}".format(ps[cid]["direct_or_partial_scores"]["H2"])
                                     for ps in m["partial_sensitivity"].values()))
        add("| {} | {} |".format(cid, " | ".join(cells)))
    add("")
    add("Nodes that would score if partial were allowed, by reviewed category (all eight cases):")
    add("")
    add("| iteration · replicate | total | genuine | silence err | generic fact | compatible | construct mism. | weak impl. | unreviewed |")
    add("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    minority = []
    for iid, m in iters.items():
        for rep, cases_ps in m["partial_sensitivity"].items():
            by = {}
            for v in cases_ps.values():
                for k, n in v["scored_direct_or_partial_by_reviewed_category"].items():
                    by[k] = by.get(k, 0) + n
            total = sum(by.values())
            minority.append(by.get("genuine_discriminator", 0) * 2 < total)
            add("| {} · {} | {} | {} |".format(iid, "rep2" if rep.endswith("rep2") else "rep1", total, " | ".join(
                str(by.get(k, 0)) for k in CATS + ["unreviewed"])))
    add("")
    add("Genuine discriminators would be a minority of the scored nodes in {} of {} replicates, so relaxing the "
        "evidence policy alone would {}meet the directive's success criteria: the state side still gives "
        "determinate contrasts to reviewed silence errors and generic facts.".format(
            sum(minority), len(minority), "not " if all(minority) else "not reliably "))
    add("")

    # ------------------------------------------------------------------ #
    add("## 6. End-to-end runs (stage B)")
    add("")
    if not stage_b:
        add("_Not yet available._")
    else:
        add("| run | calls | cost $ | ok/err | nodes | unique | abstraction specific/mechanistic/class | mean chars | content TTR | v3 sign-opposed nodes |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for name, r in stage_b.items():
            if not r.get("generation_and_structure"):
                add("| {} | — | — | — | — | — | — | — | — | — |".format(name))
                continue
            g = r["generation_and_structure"]
            lv = g["abstraction_levels"]
            add("| {} | {} | {} | {}/{} | {} | {} | {}/{}/{} | {:.0f} | {:.3f} | {} |".format(
                name, r["llm_calls"], round(r["cost_usd"] or 0, 2), r["n_ok"], r["n_error"], g["n_nodes"],
                g["unique_proposition_texts"], lv.get("specific"), lv.get("mechanistic"), lv.get("class"),
                g["mean_proposition_chars"], g["content_type_token_ratio"], g["sign_opposed_v3_edge_nodes"]))
        add("")
        add("Case scores P(H2) — frozen v3 · v3 re-run · v4 run (v3 on the v4 run's own graph → v4):")
        add("")
        add("| case | frozen v3 | v3 re-run | v4 run: v3 scoring on same graph | v4 run: v4 |")
        add("| --- | --- | --- | --- | --- |")
        names_b = list(stage_b)
        for cid in case_ids:
            vals = []
            for name in names_b:
                g = (stage_b[name].get("generation_and_structure") or {}).get("cases", {}).get(cid)
                vals.append(g)
            fz, rr, v4 = vals
            add("| {} | {} | {} | {} | {} |".format(
                cid, "{:.2f}".format(fz["scores"]["H2"]) if fz else "—", "{:.2f}".format(rr["scores"]["H2"]) if rr else "—",
                "{:.2f}".format(v4["v3_reference_scores_same_graph"]["H2"]) if v4 and v4.get("v3_reference_scores_same_graph") else "—",
                "{:.2f}".format(v4["scores"]["H2"]) if v4 else "—"))
        add("")
        v4run = stage_b.get("v4_dev_explanatory_001", {}).get("generation_and_structure", {})
        scored = [(cid, n) for cid, c in v4run.get("cases", {}).items() for n in c.get("v4_scored_nodes", [])]
        add("**What v4 scored in the live run** ({} proposition(s); all other cases tie). These propositions were "
            "regenerated and are unreviewed; an exact-text match to a reviewed pilot proposition is shown where one "
            "exists.".format(len(scored)))
        add("")
        add("| case | node | proposition | states (H1 · H2) | evidence | construct elements | log-odds H2:H1 | identical reviewed pilot proposition |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for cid, n in scored:
            m = n["identical_text_reviewed_in_pilot"]
            add("| {} | {} | {} | {} · {} | {} | {} | {:+.2f} | {} |".format(
                cid, n["node_id"], n["text"], n["states"].get("H1"), n["states"].get("H2"), n["evidence_label"],
                "; ".join("{}: {}".format(s, e) for s, e in n["construct_elements"]), n["log_odds_H2_over_H1"],
                "`{}` — {}".format(m["review_id"][4:], m["category"]) if m else "none"))
        add("")
        add("**Consequence discovery** (post-hoc recovery auditor, identical for every run; known bias toward "
            "calling hypotheses silent):")
        add("")
        add("| run | reference discriminators recovered | cases with any recovery | novel plausible |")
        add("| --- | --- | --- | --- |")
        for name, r in stage_b.items():
            d = r.get("consequence_discovery") or {}
            if not d.get("available"):
                add("| {} | — | — | — |".format(name))
                continue
            add("| {} | {}/{} | {}/8 | {} |".format(name, d["reference_discriminators_recovered"],
                                                   d["reference_discriminators_total"], d["cases_with_any_recovery"],
                                                   d["novel_plausible_discriminators"]))
    add("")

    # ------------------------------------------------------------------ #
    add("## 7. Freeze readiness")
    add("")
    add("**Not ready to freeze.** Acceptance criteria 1–7 and 9 are met: states are separate from strength; "
        "`indeterminate` never scores; gating precedes aggregation; one-sided propositions are retained "
        "descriptively; construct mismatch cannot score; v3 is untouched and reproducible; v4 has been run on the "
        "eight development cases; generation is unchanged. Criterion 8 is not met in a usable form: in the "
        "stage-A replays failure categories lose relative influence only because nothing scores at all, the "
        "reviewed genuine discriminators are not usable, and in the live run the only propositions that score "
        "belong to the generic/possibility failure class (below). Criterion 10 (freeze) is withheld pending the Director's decision on the "
        "evidence policy.")
    add("")
    if stage_b:
        v4run = stage_b.get("v4_dev_explanatory_001", {}).get("generation_and_structure", {})
        scored = [n for c in v4run.get("cases", {}).values() for n in c.get("v4_scored_nodes", [])]
        generic_match = sum(1 for n in scored if (n["identical_text_reviewed_in_pilot"] or {}).get("category")
                            == "generic_component_fact")
        modal = sum(1 for n in scored if " can " in " {} ".format(n["text"].lower()))
        add("**The two gates interact in the wrong direction.** In the live v4 run, {} proposition(s) scored; {} "
            "of them assert only that something *can* occur, and {} is text-identical to a pilot proposition "
            "labelled `generic_component_fact`. General claims are exactly what abstracts state outright, so they "
            "pass element-wise construct matching as `direct`, while specific discriminators rarely have every "
            "element established. Under direct-only, construct gating therefore selects FOR the generic-fact "
            "failure class that the state side has not removed. Relaxing construct strictness would re-admit "
            "reviewed failures (section 5); tightening it leaves generic facts as the only thing that scores. "
            "Both routes need the state-side problem (contrast assigned to class-level and possibility claims) "
            "solved first.".format(len(scored), modal, generic_match))
        add("")
    return "\n".join(L)


def main() -> int:
    OUT.write_text(build() + "\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
