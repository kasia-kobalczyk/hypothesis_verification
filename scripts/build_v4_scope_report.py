"""Generate docs/V4_SCOPE_REPORT.md from the v4-scope development metrics (deterministic).

Numbers come from:
  benchmark/v4_scope/iter0{1,2}/development_metrics.json   stage A replays (3 replicates each)
  benchmark/v4_scope/stage_b/run_comparison.json            fresh end-to-end runs
  benchmark/review/graph_pilot_001/attribution_d045_d046/   frozen v3 node contributions

The iteration log and the criteria judgements are authored below as data, because they
record decisions, not measurements.

Usage:
    python scripts/build_v4_scope_report.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_v4_development as dev  # noqa: E402

SCOPE = ROOT / "benchmark" / "v4_scope"
OUT = ROOT / "docs" / "V4_SCOPE_REPORT.md"
CATS = dev.CATEGORIES
SHORT = {"genuine_discriminator": "genuine", "silence_as_null_error": "silence error",
         "generic_component_fact": "generic fact", "compatible_non_discriminative": "compatible",
         "evidence_construct_mismatch": "construct mismatch", "invalid_or_weak_implication": "weak implication",
         "unreviewed": "unreviewed"}
SCOPES = ["hypothesis_specific", "mechanism_specific", "broader_class_fact", "possibility_claim",
          "invalid_or_underspecified"]
EVCOLS = ["no_evidence", "mixed", "contrast_direct", "contrast_partial", "context_only", "construct_mismatch",
          "relevance_no_evidence"]

ITERATIONS = [
    OrderedDict([
        ("id", "iter01"),
        ("prompts", "prediction_state_v2 · proposition_scope_v1 · contrast_element_v1 · contrast_relevance_v1"),
        ("change", "Initial v4-scope layer: separate scope classifier over all propositions; contrast element "
                   "(extractor sees the recorded states and returns `has_contrast`); three-question contrast "
                   "relevance with the category derived in code; deterministic gate (profile → scope → evidence "
                   "→ element with a contrast → relevance) with `contrast_direct` only."),
        ("why", "Directive design. `has_contrast` was added to the gate before any replicate was run (a first "
                "launch was stopped after ~1 minute, before any case finished, and deleted), so that no "
                "proposition can score without a contrast-bearing element."),
    ]),
    OrderedDict([
        ("id", "iter02"),
        ("prompts", "prediction_state_v2 · proposition_scope_v2 · contrast_element_v2 · contrast_relevance_v2"),
        ("change", "Scope: `invalid_or_underspecified` also covers propositions only weakly implied (the "
                   "directive's own definition, omitted in v1). Element: the extractor no longer sees the "
                   "recorded states; it states each candidate's position on the contrast variable "
                   "(requires_asserted / requires_other / not_required), and `has_contrast` is derived in code "
                   "(positions form a contrast AND point the same way as the states). Relevance: capability "
                   "shown in another setting is `partly`, not `yes`."),
        ("why", "Iteration 1 (all 3 replicates): every scored node was a reviewed failure. Five were "
                "implication errors (silence / weak implication) with strong determinate states, one a "
                "possibility shown in a model setting read as occurrence (generic fact), one or two construct "
                "mismatches. The element positions were meant as a second, state-blind implication check."),
    ]),
]

# Authored after stage A iteration 2 and stage B; see section 11.
STOP_REASON = (
    "Iteration was stopped after iteration 2. The nodes that still score wrongly are the same in both "
    "iterations and in every replicate, and each is a strong determinate reading of the candidate texts that "
    "the same model reproduced in three separate calls (prediction states, scope, and the state-blind element "
    "positions). A further same-model prompt change aimed at five contested, model-labelled nodes would be "
    "label-fitting rather than method development. Iteration 2 is the final development version run in stage B.")


STAGE_B_VERDICT = "largely preserved"   # authored after stage B

STAGE_B_NOTES = [
    "**Consequence discovery.** Recovery in the three v4-scope runs is 9, 10 and 10 of 23 reference "
    "discriminators, against 11 in each of the three earlier runs (frozen pilot, v3 rerun, prior v4). Per-case "
    "recovery already moved by ±1 between those earlier runs. The v4-scope layer runs after generation and "
    "cannot influence it, and generation code, prompts and configuration are unchanged, so the difference is "
    "run-to-run variation in generation and in the post-hoc auditor, not an effect of the method. It is still "
    "lower in all three runs, which is noted rather than explained away.",
    "**Scored propositions.** 4–6 per run (15 in total), all hypothesis- or mechanism-specific. Six are text-identical "
    "to reviewed pilot propositions, and all six are reviewed failures: `glnbp-X4` (silence error) in all three runs, "
    "`glnbp-X11` (silence error) once, and `eukaryogenesis-X6` (generic component fact, classified "
    "`hypothesis_specific`) twice. The executor's own reading of the other nine, which are NOT labels: four are "
    "close paraphrases of reviewed genuine discriminators (PFC control-vs-storage in all three runs; GlnBP "
    "\"transition triggered by glutamine\" once), two are close paraphrases of reviewed silence errors "
    "(`pfc_storage-X2`, `glnbp-X11`), two are looser relatives of reviewed failures, and one has no reviewed "
    "counterpart. Fresh retrieval therefore lets genuine-like discriminators score more often than in stage A, "
    "alongside the same recurring implication errors.",
    "**Case outcomes are not stable across runs.** `eukaryogenesis_mito_timing` favours H1 in run 1 and H2 in runs 2 "
    "and 3; `glnbp` ranges from 0.66 to 0.99 for H2; `spider_orb_web_origin` is a tie in two runs and favours H1 "
    "in one; four cases tie in every run. With 4–6 scored propositions per run, a single proposition's presence "
    "or absence decides a case.",
]

RECOMMENDATION = [
    "**Recommendation: do not freeze v4-scope for held-out evaluation; continue development.** The scope layer does "
    "what it was built for: broad-class facts and possibility claims no longer score, and generic-fact and "
    "construct-mismatch influence is gone in stage A (in stage B, one text-identical reviewed generic fact, classified "
    "`hypothesis_specific`, scored in two of three runs). But the few propositions that still score are dominated by reviewed "
    "implication errors (silence errors and weak implications), the reviewed genuine discriminators almost never "
    "score because the pre-cutoff literature addresses their contrast only partly, and in 4 of 8 cases the method "
    "abstains (tie) in every replicate. Freezing now would evaluate, on held-out cases, a verifier whose decisions "
    "rest on 4–6 propositions per 192, most of them wrong for reasons the gate cannot see.",
    "**The residual failure is on the implication side, not scope or evidence.** For the recurring scored errors "
    "(`glnbp-X4`, `glnbp-X11`, `pfc_storage-X2`, `eukaryogenesis-X7`, and `forest-X15` in 2 of 3 replicates), "
    "gpt-4.1 gives determinate, opposed states (strong for the three silence errors) whenever they score, and "
    "reproduces the same contrast when asked separately, "
    "without seeing the states, for each candidate's position on the contrast variable. Example: `glnbp-X4` "
    "(\"Apo-GlnBP *adopts* a closed or semi-closed conformation\") is read as required by a candidate that "
    "says apo-GlnBP *samples* a closed conformation, and as ruled out by the induced-fit candidate; the records "
    "(no major apo closed population) are then `contrast_direct`. The proposition overstates the candidate "
    "(dominant vs sampled state), and neither the state judge nor the element judge separates the two.",
    "Options for the Research Director (recommendations only, none implemented): (a) require agreement from an "
    "independent judge (a different model family) on determinate contrasts before a proposition may score, since "
    "same-model re-asking does not decorrelate these errors; (b) re-adjudicate the five recurring scored nodes with "
    "per-hypothesis states, ideally by a domain expert, because D045 recorded only primary categories for them and "
    "at least `glnbp-X4` is a subtle reading; (c) decide the `contrast_partial` policy explicitly (section 8 shows "
    "it is the only route by which genuine discriminators carry influence, but it re-admits generic facts and never "
    "removes silence errors); (d) accept abstention as a legitimate outcome and evaluate the verifier on coverage "
    "as well as direction.",
]

LIMITATIONS = [
    "D045/D046 are model-based Research Director development labels on 52 of 192 frozen-pilot propositions, with "
    "only 4 genuine discriminators; every composition share rests on these few nodes, and stage-B runs regenerate "
    "propositions, so labels transfer only through identical text.",
    "Stage A replays reuse the frozen v3 evidence labels; the relevance judge sees only the records the v3 assessor "
    "cited (or all shown records when none were cited).",
    "All judgments use one model (gpt-4.1) at temperature 0; replicate variation is sampling nondeterminism, not "
    "model diversity.",
    "Two iterations only; iteration 2 changed three prompts at once, so their separate effects are not identified.",
    "Ordinal mappings are the unchanged `v0-placeholder` values; log-odds magnitudes are not calibrated.",
    "Costs are list-price estimates with unverified rates.",
]


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _pct(x):
    return "—" if x is None else "{:.0%}".format(x)


def _reps(m):
    return list(m["replicates"].values())


def v3_composition():
    labels, _, v3, _, _ = dev.load(ROOT / "runs" / "v4_replay_pilot_iter02")
    total = sum(v["absolute_influence"] for v in v3.values())
    out = OrderedDict()
    for cat in CATS + ["unreviewed"]:
        val = sum(v["absolute_influence"] for rid, v in v3.items()
                  if ((labels.get(rid) or {}).get("human_primary_category") or "unreviewed") == cat)
        out[cat] = (val, val / total)
    return out, total


def build() -> str:
    iters = OrderedDict((it["id"], _load(SCOPE / it["id"] / "development_metrics.json")) for it in ITERATIONS)
    stage_b_path = SCOPE / "stage_b" / "run_comparison.json"
    stage_b = _load(stage_b_path) if stage_b_path.exists() else None
    final = iters["iter02"]
    L = []
    add = L.append

    add("# v4-scope development report — BENCH-GRAPH-V4-SCOPE-001")
    add("")
    add("**Status: NOT FROZEN. Recommendation: do not freeze; continue development (section 11).** The eight cases "
        "are a spent development set; nothing here is held-out evidence. D045/D046 are model-based Research "
        "Director development labels, used to diagnose behaviour, not as ground truth or an optimisation target.")
    add("")
    add("Design: `docs/V4_SCOPE_DESIGN.md`. Metrics: `benchmark/v4_scope/`. Stage A replays the v4-scope layer on "
        "the frozen v3 pilot (192 propositions, identical retrieved records and evidence labels), three independent "
        "replicates per iteration, so behaviour is compared node by node with v3, prior v4 and the labels. Stage B "
        "runs the final version end to end three times.")
    add("")
    add("Model and configuration: Azure OpenAI `gpt-4.1-kasia` (api 2024-05-01-preview), temperature 0, seed "
        "20260911, JSON mode, for every verifier call; Semantic Scholar + Crossref literature with the frozen "
        "per-case cutoffs; ordinal mappings `v0-placeholder` (unchanged); config `configs/v4_dev_explanatory.yaml` "
        "(identical to the pilot except `dataset.status: development`).")
    add("")

    # ------------------------------------------------------------------ #
    add("## 1. Iteration log")
    add("")
    add("| iteration | replay commit | prompts | change | why |")
    add("| --- | --- | --- | --- | --- |")
    for it in ITERATIONS:
        commits = sorted({r["git"]["commit"][:7] for r in _reps(iters[it["id"]])})
        add("| {} | `{}` | {} | {} | {} |".format(it["id"], "`, `".join(commits), it["prompts"], it["change"], it["why"]))
    add("")
    add(STOP_REASON)
    add("")
    add("No case-specific rule, no development-case content in any prompt (checked by a test against the "
        "visible phenomenon text of all eight cases), no hidden annotation in verifier context, no change to "
        "numeric mappings, and `indeterminate` contributes nothing in every iteration.")
    add("")
    add("Replays: " + "; ".join("{}: `{}`".format(i, "`, `".join("runs/" + r for r in m["replays"]))
                                for i, m in iters.items()) + " (gitignored). Every recorded gate and score was "
        "re-derived from the recorded judgments with the committed gate code: " +
        ", ".join("{} {}".format(i, "all consistent" if all(c["ok"] for c in m["consistency"].values())
                                 else "INCONSISTENT") for i, m in iters.items()) + ". LLM errors: " +
        ", ".join("{} {}".format(i, "/".join(str(r["n_errors"]) for r in _reps(m))) for i, m in iters.items()) + ".")
    add("")

    # ------------------------------------------------------------------ #
    add("## 2. Prediction-state preservation")
    add("")
    add("All v4-scope iterations use `prediction_state_v2`, the prior v4 head, unchanged. Differences from prior v4 "
        "are therefore run-to-run noise, which this table measures.")
    add("")
    add("| run | pairs indeterminate | comparative profiles | one-sided | D046 unqualified / all | reviewed silence errors with a comparative profile |")
    add("| --- | --- | --- | --- | --- | --- |")
    for name, p in final["prior_v4"].items():
        a = p["A_state_preservation"]
        add("| prior v4 `{}` | {} | {} | {} | {} / {} | {} |".format(
            name, _pct(a["indeterminate_rate"]), a["profiles"].get("comparative_discriminator", 0),
            a["profiles"].get("one_sided_prediction", 0), a["d046_state_agreement_unqualified"],
            a["d046_state_agreement_all"], a["reviewed_silence_errors_with_comparative_profile"]))
    for iid, m in iters.items():
        for rep, r in m["replicates"].items():
            a = r["A_state_preservation"]
            add("| {} `{}` | {} | {} | {} | {} / {} | {} |".format(
                iid, rep, _pct(a["indeterminate_rate"]), a["profiles"].get("comparative_discriminator", 0),
                a["profiles"].get("one_sided_prediction", 0), a["d046_state_agreement_unqualified"],
                a["d046_state_agreement_all"], a["reviewed_silence_errors_with_comparative_profile"]))
    add("")
    add("State-pair agreement between replicates (of 384 hypothesis × proposition pairs): prior v4 {}; "
        "iteration 1 {}; iteration 2 {}; iteration-2 replicate 1 vs prior v4 {}. Profile-class agreement: prior v4 {}; "
        "iteration 1 {}; iteration 2 {}.".format(
            final["H_stability"]["prior_v4_state_pairs"][0], ", ".join(iters["iter01"]["H_stability"]["v4_scope_state_pairs"]),
            ", ".join(final["H_stability"]["v4_scope_state_pairs"]), final["H_stability"]["v4_scope_vs_prior_v4_state_pairs"][0],
            final["H_stability"]["prior_v4_profile"][0], ", ".join(iters["iter01"]["H_stability"]["v4_scope_profile"]),
            ", ".join(final["H_stability"]["v4_scope_profile"])))
    add("")
    add("**No regression.** The same four of the ten reviewed silence errors (`pfc_storage_vs_control-X2`, "
        "`glnbp_induced_fit_vs_conformational_selection-X4`, `-X11`, `eukaryogenesis_mito_timing-X2`) have a "
        "comparative profile in every run, prior v4 included. Prior v4 did not score them only because its "
        "whole-proposition construct match rated their evidence `partial` or `mismatch` (both prior-v4 replicates); "
        "v4-scope's contrast relevance rates three of them `contrast_direct`, which exposes the state error "
        "(section 6).")
    add("")

    # ------------------------------------------------------------------ #
    add("## 3. Scope behaviour")
    add("")
    add("| iteration · replicate | hypothesis-specific | mechanism-specific | broader class | possibility | invalid | "
        "on comparative profiles: specific / broad+possibility |")
    add("| --- | --- | --- | --- | --- | --- | --- |")
    for iid, m in iters.items():
        for rep, r in m["replicates"].items():
            s, c = r["B_scope"]["scope_counts_all_nodes"], r["B_scope"]["scope_counts_comparative_profile_nodes"]
            add("| {} · {} | {} | {} | {} | {} | {} | {} / {} |".format(
                iid, rep[-4:] if rep.endswith(("rep2", "rep3")) else "rep1", *[s.get(k, 0) for k in SCOPES],
                c.get("hypothesis_specific", 0) + c.get("mechanism_specific", 0),
                c.get("broader_class_fact", 0) + c.get("possibility_claim", 0)))
    add("")
    add("**Reviewed category × scope** (iteration 2, summed over 3 replicates; each node counted once per replicate)")
    add("")
    add("| category (n nodes) | " + " | ".join(SCOPES) + " |")
    add("| --- | " + " | ".join("---" for _ in SCOPES) + " |")
    for cat in CATS:
        tot = Counter()
        for r in _reps(final):
            tot.update(r["B_scope"]["human_category_x_scope"].get(cat, {}))
        n = sum(tot.values()) // len(_reps(final))
        add("| {} ({}) | {} |".format(SHORT[cat], n, " | ".join(str(tot.get(s, 0)) for s in SCOPES)))
    add("")
    for iid, m in iters.items():
        g = [r["B_scope"]["generic_component_facts"] for r in _reps(m)]
        gd = [r["B_scope"]["genuine_discriminators"] for r in _reps(m)]
        add("- {}: reviewed generic component facts not scored {} (scope non-comparative {}); reviewed genuine "
            "discriminators scope-eligible {}, comparative and scope-eligible {}, scored {}.".format(
                iid, " · ".join("{}/{}".format(x["rejected_from_scoring"], x["n"]) for x in g),
                " · ".join("{}/{}".format(x["scope_non_comparative"], x["n"]) for x in g),
                " · ".join("{}/{}".format(x["scope_eligible"], x["n"]) for x in gd),
                " · ".join("{}/{}".format(x["comparative_and_scope_eligible"], x["n"]) for x in gd),
                " · ".join("{}/{}".format(x["used_in_score"], x["n"]) for x in gd)))
    add("")
    add("**The 14 reviewed generic component facts, iteration 2** (scope · gate reason, per replicate)")
    add("")
    add("| node | replicate 1 | replicate 2 | replicate 3 |")
    add("| --- | --- | --- | --- |")
    rids = list(_reps(final)[0]["B_scope"]["generic_component_facts"]["nodes"])
    for rid in rids:
        add("| `{}` | {} |".format(rid[4:], " | ".join(
            "{} · {}".format(r["B_scope"]["generic_component_facts"]["nodes"][rid]["scope"],
                             r["B_scope"]["generic_component_facts"]["nodes"][rid]["gate_reason"]) for r in _reps(final))))
    add("")
    add("**The 4 reviewed genuine discriminators** (scope · profile · contrast relevance · gate reason)")
    add("")
    add("| node | " + " | ".join("{} rep{}".format(i, k + 1) for i in iters for k in range(3)) + " |")
    add("| --- | " + " | ".join("---" for _ in iters for _ in range(3)) + " |")
    rids = list(_reps(final)[0]["B_scope"]["genuine_discriminators"]["nodes"])
    for rid in rids:
        cells = []
        for m in iters.values():
            for r in _reps(m):
                g = r["B_scope"]["genuine_discriminators"]["nodes"][rid]
                cells.append("{} · {} · {} · {}".format(g["scope"], g["profile"], g["contrast_relevance"], g["gate_reason"]))
        add("| `{}` | {} |".format(rid[4:], " | ".join(cells)))
    add("")

    # ------------------------------------------------------------------ #
    add("## 4. Contrast-bearing evidence")
    add("")
    add("| iteration · replicate | informative-evidence nodes | direct | partial | context only | construct mismatch | "
        "no evidence | element without contrast | on eligible nodes with a contrast: direct / partial | genuine discriminators direct |")
    add("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for iid, m in iters.items():
        for k, r in enumerate(_reps(m)):
            c = r["C_contrast_evidence"]
            rel, el = c["relevance_all_informative"], c["relevance_comparative_scope_eligible_and_has_contrast"]
            add("| {} · rep{} | {} | {} | {} | {} | {} | {} | {} | {} / {} | {} |".format(
                iid, k + 1, c["n_informative_evidence_nodes"], rel.get("contrast_direct", 0), rel.get("contrast_partial", 0),
                rel.get("context_only", 0), rel.get("construct_mismatch", 0), rel.get("relevance_no_evidence", 0),
                c["has_contrast_false_on_informative"], el.get("contrast_direct", 0), el.get("contrast_partial", 0),
                c["genuine_discriminators_contrast_direct"]))
    add("")
    add("Relevance by reviewed category, iteration 2 (summed over replicates):")
    add("")
    add("| category | " + " | ".join(EVCOLS[2:]) + " |")
    add("| --- | " + " | ".join("---" for _ in EVCOLS[2:]) + " |")
    for cat in CATS:
        tot = Counter()
        for r in _reps(final):
            tot.update(r["C_contrast_evidence"]["relevance_by_human_category"].get(cat, {}))
        add("| {} | {} |".format(SHORT[cat], " | ".join(str(tot.get(col, 0)) for col in EVCOLS[2:])))
    add("")
    add("`context_only` and `construct_mismatch` are almost never assigned: the cited records had already been "
        "judged informative by the v3 assessor, and the relevance judge almost always finds that they report the "
        "contrast variable at least partly. The separation the directive asked for therefore happens between "
        "`contrast_direct` and `contrast_partial`, not between direct and context-only.")
    add("")
    gen = [r["C_contrast_evidence"]["generic_or_compatible_with_only_context_mismatch_or_none_that_v3_scored"]
           for r in _reps(final)]
    add("Reviewed generic/compatible facts that v3 scored and that now receive only context-only, mismatch or "
        "no-evidence relevance: {} per iteration-2 replicate. Generic facts are not excluded by the evidence "
        "judgment; they are excluded by scope and state profile (section 3), and when they reach the relevance "
        "judge they are usually rated `contrast_direct` or `contrast_partial`.".format(
            " · ".join(str(g["n"]) for g in gen)))
    add("")

    # ------------------------------------------------------------------ #
    add("## 5. Specificity–assessability trade-off")
    add("")
    add("Is historical evidence less able to test hypothesis/mechanism-specific propositions than broad ones? "
        "Rates over all 192 propositions per replicate: P(informative evidence), P(contrast-direct evidence), and "
        "P(contrast-direct | informative).")
    add("")
    add("| iteration · replicate | specific: n · informative · direct · direct given informative | broad class + possibility: n · informative · direct · direct given informative |")
    add("| --- | --- | --- |")
    for iid, m in iters.items():
        for k, r in enumerate(_reps(m)):
            t = r["D_scope_x_evidence"]["all_nodes"]
            s, b = t["specific_(hypothesis_or_mechanism)"], t["broad_(class_fact_or_possibility)"]
            add("| {} · rep{} | {} · {} · {} · {} | {} · {} · {} · {} |".format(
                iid, k + 1, s["n"], _pct(s["p_informative_evidence"]), _pct(s["p_contrast_direct"]),
                _pct(s["p_contrast_direct_given_informative"]), b["n"], _pct(b["p_informative_evidence"]),
                _pct(b["p_contrast_direct"]), _pct(b["p_contrast_direct_given_informative"])))
    add("")
    add("**Scope × evidence availability / contrast relevance**, iteration 2, counts summed over 3 replicates "
        "(so each row totals 3 × its mean node count):")
    add("")
    add("| scope | n | " + " | ".join(EVCOLS) + " | element without contrast | P(informative) | P(direct) |")
    add("| --- | --- | " + " | ".join("---" for _ in EVCOLS) + " | --- | --- | --- |")
    for s in SCOPES:
        tot = Counter()
        for r in _reps(final):
            row = r["D_scope_x_evidence"]["all_nodes"]["rows"][s]
            tot.update({k: v for k, v in row.items() if isinstance(v, int)})
        n = tot["n"]
        inf = n - tot["no_evidence"] - tot["mixed"] - tot["no_evidence_assessment"]
        add("| {} | {} | {} | {} | {} | {} |".format(s, n, " | ".join(str(tot[c]) for c in EVCOLS),
                                                    tot["n_has_contrast_false"], _pct(inf / n if n else None),
                                                    _pct(tot["contrast_direct"] / n if n else None)))
    add("")
    add("Findings, stable across replicates:")
    add("")
    add("1. **Availability.** Specific propositions (about two thirds of all) are less often reached by any "
        "informative evidence than broad ones: 37–38% vs 48–50% in every replicate of both iterations. The most "
        "case-specific class is the least assessable: in iteration 2, `hypothesis_specific` has informative evidence "
        "for 30% and contrast-direct evidence for 6% of propositions, against 46% / 17% for `mechanism_specific`.")
    add("2. **Directness depends on the relevance prompt.** Under relevance v1, broad propositions received "
        "contrast-direct evidence about twice as often as specific ones (17–21% vs 9–10%). Under v2, which "
        "downgrades capability shown in another setting, the rates are similar (10–13% vs 11–12%). The directness "
        "gap is therefore not robust; the availability gap is.")
    add("3. **Genuine discriminators.** The four reviewed genuine discriminators received contrast-direct evidence "
        "in 1 of 24 node-replicates; their records address the contrast variable only partly (for example, "
        "apo and holo structures that do not show binding order).")
    add("")
    add("`invalid_or_underspecified` was never assigned, in either scope prompt version.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 6. What scores")
    add("")
    for iid, m in iters.items():
        occurrences = Counter()
        meta = {}
        for r in _reps(m):
            for s in r["G_scored_nodes"]:
                occurrences[s["review_id"]] += 1
                meta[s["review_id"]] = s
        add("**{}** — scored nodes per replicate: {}; by scope {}.".format(
            iid, " · ".join(str(len(r["G_scored_nodes"])) for r in _reps(m)),
            " · ".join(str(r["G_scored_scope_counts"]) for r in _reps(m))))
        add("")
        add("| node | reviewed category | scope | evidence | replicates scored | log-odds H2−H1 | proposition |")
        add("| --- | --- | --- | --- | --- | --- | --- |")
        for rid, k in sorted(occurrences.items(), key=lambda kv: (-kv[1], kv[0])):
            s = meta[rid]
            add("| `{}` | {} | {} | {} | {}/3 | {:+.2f} | {} |".format(rid[4:], SHORT.get(s["human_category"], s["human_category"]),
                                                                  s["scope"], s["evidence_label"], k,
                                                                  s["log_odds_H2_over_H1"], s["text"]))
        add("")
    add("Every scored node is hypothesis- or mechanism-specific by construction; no broader-class fact or "
        "possibility claim scored in any replicate.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 7. Score-influence composition (|log-odds H2−H1| by reviewed category)")
    add("")
    v3c, v3t = v3_composition()
    header = ["v3 frozen pilot"] + ["{} rep{}".format(i, k + 1) for i in iters for k in range(3)]
    add("| category | " + " | ".join(header) + " |")
    add("| --- | " + " | ".join("---" for _ in header) + " |")
    for cat in CATS + ["unreviewed"]:
        cells = ["{:.2f} ({})".format(*v3c[cat][:1], _pct(v3c[cat][1]))]
        for m in iters.values():
            for r in _reps(m):
                e = r["E_influence"][cat]
                cells.append("{:.2f} ({})".format(e["absolute_influence"], _pct(e["share"])))
        add("| {} | {} |".format(SHORT[cat], " | ".join(cells)))
    add("| total | {} |".format(" | ".join(["{:.2f}".format(v3t)] + ["{:.2f}".format(r["E_influence"]["total_absolute_influence"])
                                                                    for m in iters.values() for r in _reps(m)])))
    add("")
    add("Prior v4 (stage A, direct-only construct policy) scored no node on the frozen pilot, so its composition is "
        "empty. v3's total covers all 192 nodes, with many unreviewed contributors; the v4-scope totals come from "
        "4–6 nodes, all reviewed.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 8. `contrast_partial` sensitivity analysis (reporting only; not the method)")
    add("")
    add("| iteration · replicate | scored: main → with partial | added nodes by category | generic facts re-entering | genuine share with partial | silence share with partial |")
    add("| --- | --- | --- | --- | --- | --- |")
    for iid, m in iters.items():
        for k, r in enumerate(_reps(m)):
            f = r["F_partial_sensitivity"]
            add("| {} · rep{} | {} → {} | {} | {} | {} | {} |".format(
                iid, k + 1, f["n_scored_main"], f["n_scored_sensitivity"],
                ", ".join("{} {}".format(SHORT.get(c, c), v) for c, v in sorted(f["additional_by_category"].items())),
                ", ".join("`{}`".format(x[4:]) for x in f["generic_component_facts_reentering"]) or "none",
                _pct(f["influence"]["genuine_discriminator"]["share"]), _pct(f["influence"]["silence_as_null_error"]["share"])))
    add("")
    add("Allowing partial evidence is the only configuration in which the reviewed genuine discriminators carry "
        "material influence, but it also re-admits generic facts (iteration 2) and never removes the silence errors, "
        "which remain the largest single category. It is not stable or clean enough to define the method (directive §9).")
    add("")

    # ------------------------------------------------------------------ #
    add("## 9. Replicate stability and case scores (stage A)")
    add("")
    add("| agreement between replicate pairs | iteration 1 | iteration 2 |")
    add("| --- | --- | --- |")
    for key in ("scope_class", "scope_eligible", "has_contrast", "contrast_relevance", "used_in_score"):
        add("| {} | {} | {} |".format(key, ", ".join(iters["iter01"]["H_stability"][key]), ", ".join(final["H_stability"][key])))
    add("")
    add("Case scores (H1 / H2) per replicate. The later-resolution column is descriptive only and was not used "
        "for any decision.")
    add("")
    add("| case | v3 frozen | iteration 1 | iteration 2 | later resolution favours |")
    add("| --- | --- | --- | --- | --- |")
    for case in final["H_stability"]["case_scores_by_replicate"]:
        pc = _reps(final)[0]["per_case"][case]
        fmt = lambda s: "{:.2f}/{:.2f}".format(s["H1"], s["H2"])  # noqa: E731
        add("| {} | {} | {} | {} | {} |".format(
            case, fmt(pc["v3_frozen_scores"]), " · ".join(fmt(s) for s in iters["iter01"]["H_stability"]["case_scores_by_replicate"][case]),
            " · ".join(fmt(s) for s in final["H_stability"]["case_scores_by_replicate"][case]),
            pc["later_resolution_favours_(descriptive_only)"] or "mixed / regime-dependent"))
    add("")

    # ------------------------------------------------------------------ #
    add("## 10. Stage B — fresh end-to-end runs of the final version")
    add("")
    if not stage_b:
        add("Not yet available.")
    else:
        add("| run | ok / error | LLM calls | cost (USD, list price, unverified) | nodes | unique texts | reference discriminators recovered | cases with any recovery | novel plausible discriminators |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for name, r in stage_b.items():
            if not r.get("run"):
                add("| {} | not available | | | | | | | |".format(name))
                continue
            g, dsc = r["generation_and_structure"], r["consequence_discovery"]
            add("| {} | {} / {} | {} | {} | {} | {} | {} | {} | {} |".format(
                name, r["n_ok"], r["n_error"], r["llm_calls"], "—" if r["cost_usd"] is None else "{:.2f}".format(r["cost_usd"]),
                g["n_nodes"], g["unique_proposition_texts"],
                "{}/{}".format(dsc["reference_discriminators_recovered"], dsc["reference_discriminators_total"]) if dsc.get("available") else "—",
                dsc.get("cases_with_any_recovery", "—"), dsc.get("novel_plausible_discriminators", "—")))
        add("")
        scope_runs = [(n, r) for n, r in stage_b.items() if r.get("v4_scope_layer")]
        if scope_runs:
            add("| run | scored nodes | scored by scope | scored nodes whose text is identical to a reviewed pilot node | relevance counts |")
            add("| --- | --- | --- | --- | --- |")
            for name, r in scope_runs:
                v = r["v4_scope_layer"]
                add("| {} | {} | {} | {} | {} |".format(name, v["n_scored"], v["scored_by_scope"],
                                                        v["scored_by_identical_reviewed_text"], v["relevance_counts"]))
            add("")
            add("| case | " + " | ".join(n for n, _ in scope_runs) + " |")
            add("| --- | " + " | ".join("---" for _ in scope_runs) + " |")
            for case in scope_runs[0][1]["v4_scope_layer"]["cases"]:
                cells = []
                for _, r in scope_runs:
                    c = r["v4_scope_layer"]["cases"][case]
                    cells.append("{:.2f}/{:.2f} ({} scored)".format(c["scores"]["H1"], c["scores"]["H2"], c["summary"]["n_used_in_score"]))
                add("| {} | {} |".format(case, " | ".join(cells)))
            add("")
            add("Scored propositions in the fresh runs:")
            add("")
            add("| run · case | node | scope | evidence | log-odds H2−H1 | reviewed identical text | proposition |")
            add("| --- | --- | --- | --- | --- | --- | --- |")
            for name, r in scope_runs:
                for case, c in r["v4_scope_layer"]["cases"].items():
                    for s in c["scored_nodes"]:
                        match = s["identical_text_reviewed_in_pilot"]
                        add("| {} · {} | {} | {} | {} | {:+.2f} | {} | {} |".format(
                            name[-3:], case, s["node_id"], s["scope"], s["evidence_label"], s["log_odds_H2_over_H1"],
                            "{} ({})".format(match["category"], match["review_id"][4:]) if match else "—", s["text"]))
            add("")
            for para in STAGE_B_NOTES:
                add(para)
                add("")
    # ------------------------------------------------------------------ #
    add("## 11. Development success criteria (directive §14) and recommendation")
    add("")
    disc = None
    if stage_b:
        disc = OrderedDict((n, r["consequence_discovery"]) for n, r in stage_b.items()
                           if r.get("run") and r["consequence_discovery"].get("available"))
    genuine_final = " · ".join(_pct(r["E_influence"]["genuine_discriminator"]["share"]) for r in _reps(final))
    silence_final = " · ".join(_pct(r["E_influence"]["silence_as_null_error"]["share"]) for r in _reps(final))
    add("| # | criterion | verdict | evidence |")
    add("| --- | --- | --- | --- |")
    add("| 1 | prediction-state performance from prior v4 intact | met | same state prompt; D046 unqualified 20/20 in all "
        "6 replicates; indeterminate rate and state-pair agreement within prior-v4 run-to-run noise (section 2) |")
    add("| 2 | broad class / possibility claims largely excluded | met | no broader-class or possibility proposition "
        "scored in any replicate; reviewed generic facts not scored 14/14 in all iteration-2 replicates (section 3) |")
    add("| 3 | reviewed genuine discriminators retained when specific | partly | all 4 scope-eligible with a contrast-bearing "
        "element in every replicate, but scored in 1 of 12 iteration-2 node-replicates: their pre-cutoff evidence is "
        "`contrast_partial` (sections 3, 4) |")
    add("| 4 | evidence must bear on the contrast-bearing element | met structurally, weak in practice | only "
        "`contrast_direct` scores; but `context_only` / `construct_mismatch` are almost never assigned, and "
        "`contrast_direct` is given to records that measure the stated variable even when the proposition overstates "
        "a candidate's commitment (section 6) |")
    add("| 5 | generic-fact and construct-mismatch influence drops materially | met (iteration 2) | v3 26% + 7% → 0% in "
        "all 3 iteration-2 replicates (iteration 1: 18–20% + 11–19%) (section 7) |")
    add("| 6 | genuine-discriminator share of influence increases | not met | v3 8% → {} (iteration 2); silence errors "
        "rise from 22% to {} of a much smaller total (section 7) |".format(genuine_final, silence_final))
    if disc:
        cells = "; ".join("{} {}/{}".format(n.split(" ")[0], d["reference_discriminators_recovered"],
                                            d["reference_discriminators_total"]) for n, d in disc.items())
        add("| 7 | consequence discovery preserved | {} | generation is unchanged; reference discriminators "
            "recovered: {} (section 10) |".format(STAGE_B_VERDICT, cells))
    else:
        add("| 7 | consequence discovery preserved | pending | stage B not available |")
    def identical(m):
        return sum(1 for v in m["H_stability"]["case_scores_by_replicate"].values()
                   if all(abs(s["H1"] - v[0]["H1"]) < 1e-9 for s in v))

    def ties(m):
        return sum(1 for v in m["H_stability"]["case_scores_by_replicate"].values()
                   if all(abs(s["H1"] - 0.5) < 1e-12 for s in v))
    add("| 8 | replicate behaviour no less stable | met | scored/not agreement 190–192/192 between replicate pairs; "
        "case scores identical across the 3 replicates in {} (iteration 1) and {} (iteration 2) of 8 cases; ties in "
        "every replicate: {} and {} cases (section 9) |".format(identical(iters["iter01"]), identical(final),
                                                                ties(iters["iter01"]), ties(final)))
    add("")
    for para in RECOMMENDATION:
        add(para)
        add("")

    add("## 12. Limitations")
    add("")
    for item in LIMITATIONS:
        add("- " + item)
    add("")
    return "\n".join(L) + "\n"


def main() -> int:
    OUT.write_text(build(), encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
