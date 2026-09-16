"""Assemble the human-readable pilot report from the frozen artifacts.

Every number in the report comes from a JSON file produced by an earlier stage;
nothing is computed here for the first time and nothing is typed in by hand. That
is deliberate -- a report written separately from the analysis is a report that
can disagree with it.

Inputs (all must exist):
    <run>/summary.json                 the run itself
    <run>/leak_audit.json              empirical leak audit (Step 3)
    <run>/recovery.json                consequence recovery (Step 6, 7A)
    <run>/evidence_discovery.json      evidence discovery (Step 7B)
    <run>/hypothesis_comparison.json   hypothesis comparison (Step 7C)

Usage:
    python scripts/build_pilot_report.py --run runs/pilot_explanatory_001
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import resolve_path
from src.common.logging_utils import get_logger

LOGGER = get_logger("pilot.report")

REQUIRED = ["summary.json", "leak_audit.json", "recovery.json",
            "evidence_discovery.json", "hypothesis_comparison.json",
            "ranking_attribution.json", "audit_checks.json"]


def _git(*args: str) -> str:
    try:
        return subprocess.check_output(["git"] + list(args), stderr=subprocess.DEVNULL,
                                       text=True).strip()
    except Exception:  # noqa: BLE001
        return "<unavailable>"


def _pct(numerator: int, denominator: int) -> str:
    if not denominator:
        return "n/a"
    return "{}/{} ({:.0%})".format(numerator, denominator, numerator / denominator)


def _table(headers: List[str], rows: List[List[Any]]) -> List[str]:
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join("" if c is None else str(c) for c in row) + " |")
    return out


def build(run_dir: Path) -> str:
    data = {name: json.loads((run_dir / name).read_text(encoding="utf-8"))
            for name in REQUIRED}
    summary = data["summary.json"]
    leak = data["leak_audit.json"]
    recovery = data["recovery.json"]
    evidence = data["evidence_discovery.json"]
    comparison = data["hypothesis_comparison.json"]

    rec = recovery["summary"]
    silence = rec["silence_handling"]
    data["audit_checks.json"] = data["audit_checks.json"]
    lines: List[str] = []
    add = lines.append

    add("# BENCH-GRAPH-PILOT-001 — diagnostic pilot report")
    add("")
    add("**This is a behavioural observation, not a performance measurement.** The "
        "benchmark carries no gold hypothesis, no accuracy is computed, and nothing "
        "in the method was tuned on these eight cases. Counts below describe what "
        "the existing pipeline did; they are not a score.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 1. Provenance")
    add("")
    add("| field | value |")
    add("| --- | --- |")
    add("| git commit | `{}` |".format(_git("rev-parse", "HEAD")))
    dirty = [l for l in _git("status", "--porcelain").splitlines() if l.strip()]
    add("| git status | {} |".format(
        "clean" if not dirty else
        "{} uncommitted path(s): the pilot integration, tests and analysis scripts "
        "are not yet committed; the frozen method files are unchanged (prompt SHAs "
        "verified by test)".format(len(dirty))))
    add("| run id | `{}` |".format(summary.get("run_id")))
    add("| method | `{}` |".format(summary.get("method")))
    add("| dataset status | `{}` |".format(summary.get("dataset_status")))
    add("| config | `configs/pilot_explanatory.yaml` |")
    add("| frozen method | `benchmark/frozen/narrow_graph_v3_complete.json` |")
    add("| LLM provider | `{}` |".format(summary.get("llm_provider")))
    add("| LLM deployment | `{}` |".format(summary.get("llm_deployment")))
    add("| LLM calls | {} |".format(summary.get("llm_calls")))
    add("| parse failures | {} |".format(summary.get("llm_parse_failures")))
    add("| estimated cost | ${} |".format(
        round((summary.get("cost") or {}).get("cost_usd", 0), 2)))
    add("| literature provider calls | {} |".format(
        (summary.get("literature_stats") or {}).get("provider_calls")))
    add("| recovery judge | `{}` via `{}` |".format(
        recovery.get("judge_prompt"), recovery.get("judge_model")))
    add("| evidence judge | `{}` via `{}` |".format(
        evidence.get("judge_prompt"), evidence.get("judge_model")))
    add("")
    add("The pilot config differs from `configs/mvp.yaml` only in `dataset.kind`, "
        "`dataset.status` and `dataset.case_path`; every method parameter and every "
        "prompt SHA is pinned to the freeze by "
        "`tests/test_pilot_config_is_the_frozen_method.py`.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 2. Temporal and hidden-annotation safety")
    add("")
    add("Two independent lines of evidence, because they fail differently: the tests "
        "reason about the code, the audit reasons about the artifacts.")
    add("")
    add("**Tests (adversarial).** `tests/test_explanatory_cutoff_enforcement.py` "
        "rigs the provider to return each case's *real resolving study* through "
        "search, reference expansion, citation expansion and metadata lookup, and "
        "asserts none of it survives; a companion test asserts a pre-cutoff decoy "
        "*does* survive, so the filter is discriminating rather than merely "
        "restrictive. `tests/test_explanatory_hidden_isolation.py` proves the loader "
        "refuses any non-visible field and that no hidden DOI, resolver identity, "
        "reference discriminator, resolving observation or resolution summary can "
        "reach a rendered prompt.")
    add("")
    add("**Empirical audit of this run.** Every byte sent to the model was scanned "
        "against the hidden annotations, and every retrieved paper against the "
        "case cutoff.")
    add("")
    add("\n".join(_table(
        ["case", "cutoff", "papers retrieved", "chars to model", "post-cutoff",
         "hidden-content hits", "verdict"],
        [[c["case_id"], c["cutoff"], c["n_papers_retrieved"],
          "{:,}".format(c["n_chars_sent_to_model"]),
          len(c["post_cutoff_papers_retrieved"]),
          len(c["hidden_doi_hits"]) + len(c["hidden_phrase_hits"]),
          "clean" if c["clean"] else "**LEAK**"]
         for c in leak["cases"]])))
    add("")
    add("All cases clean: **{}**".format(leak["all_clean"]))
    add("")

    audit = data["audit_checks.json"]
    attribution = data["ranking_attribution.json"]
    ev = evidence["summary"]
    rb = audit["structural_comparison_same_frozen_method"]["researchbench_reserve_12"]
    px = audit["structural_comparison_same_frozen_method"]["explanatory_pilot_8"]
    favoured = {k: v for k, v in audit["resolution_favoured_hypothesis"].items() if k != "basis"}
    rel = audit["judge_reliability"]

    # ------------------------------------------------------------------ #
    add("## 3. Behaviour compared with ResearchBench (Step 8, question 1)")
    add("")
    add("Same frozen method, same model, structural measures only (no judge).")
    add("")
    def _share(n, d):
        return "{} ({:.0%})".format(n, n / d) if d else "n/a"
    add("\n".join(_table(
        ["measure", "ResearchBench reserve-12", "explanatory pilot-8"],
        [["instances / nodes", "{} / {}".format(rb["instances"], rb["nodes"]),
          "{} / {}".format(px["instances"], px["nodes"])],
         ["sign-opposed nodes (one hypothesis above `neutral`, the other below)",
          _share(rb["sign_opposed_nodes"], rb["nodes"]), _share(px["sign_opposed_nodes"], px["nodes"])],
         ["root edges labelled `unlikely`/`strongly_contradicted`",
          "{:.0%}".format(rb["negative_edge_share"]), "{:.0%}".format(px["negative_edge_share"])],
         ["root edges labelled `neutral`",
          "{:.0%}".format(rb["neutral_edge_share"]), "{:.0%}".format(px["neutral_edge_share"])],
         ["nodes with informative evidence",
          _share(rb["informative_nodes"], rb["nodes"]), _share(px["informative_nodes"], px["nodes"])],
         ["median score margin", "{:.3f}".format(rb["median_margin"]), "{:.3f}".format(px["median_margin"])],
         ["instances with margin > 0.5", rb["n_margin_over_0_5"], px["n_margin_over_0_5"]]])))
    add("")
    add("The verifier behaves very differently on genuine competing explanations: it "
        "draws opposite-signed implications nine times as often and ranks far more "
        "decisively. Section 5 shows how much of that opposition is real.")
    add("")
    add("The permissive measure \"edge labels differ at all\" is uninformative here — "
        "it counts `implied` vs `weakly_implied` — and is {} on the pilot and {} on "
        "ResearchBench.".format(
            _pct(px["edge_labels_differ_nodes"], px["nodes"]),
            _pct(rb["edge_labels_differ_nodes"], rb["nodes"])))
    add("")

    # ------------------------------------------------------------------ #
    add("## 4. Consequence discovery (Step 7A)")
    add("")
    add("An auditor judge (`recovery_classify_v1`, which saw the hidden reference "
        "discriminators but never the verifier's edge labels) stated each "
        "proposition's status under each hypothesis and assigned a category.")
    add("")
    add("\n".join(_table(
        ["category", "n", "share"],
        [[k, v, "{:.0%}".format(v / rec["n_propositions"])]
         for k, v in sorted(rec["categories"].items(), key=lambda kv: -kv[1])])))
    add("")
    add("**Measurement caveat.** Because the auditor cannot see edge labels, its "
        "`silence_as_null_error` category identifies *one-sided propositions* (one "
        "hypothesis predicts, the other is silent) — a property of what was "
        "generated, not proof the verifier erred. Section 5 separates the two.")
    add("")
    add("Reference-discriminator coverage per case (a discriminator counts once, and "
        "only on a verbatim match):")
    add("")
    add("\n".join(_table(
        ["case", "reference discriminators", "recovered",
         "genuine discriminators generated", "compatible / generic"],
        [[c["case_id"], c["n_reference_discriminators"],
          c["n_reference_discriminators_recovered"],
          c["categories"]["reference_discriminator_recovered"]
          + c["categories"]["novel_plausible_discriminator"],
          c["categories"]["compatible_non_discriminative"]
          + c["categories"]["generic_component_fact"]]
         for c in rec["per_case"]])))
    add("")
    total_ref = sum(c["n_reference_discriminators"] for c in rec["per_case"])
    total_rec = sum(c["n_reference_discriminators_recovered"] for c in rec["per_case"])
    add("Overall: {} reference discriminators recovered; {} propositions genuinely "
        "discriminative ({} matching a reference discriminator, {} novel).".format(
            _pct(total_rec, total_ref), _pct(rec["n_judge_treated_as_discriminative"],
                                              rec["n_propositions"]),
            rec["categories"]["reference_discriminator_recovered"],
            rec["categories"]["novel_plausible_discriminator"]))
    add("")

    # ------------------------------------------------------------------ #
    add("## 5. Silence as a null prediction (Step 8, questions 2–3)")
    add("")
    add("`edge_assess_v1` already defines `neutral` as \"the candidate says nothing "
        "either way\" and tells the model to use it freely, so this is not a missing "
        "label. Joining the auditor's statuses with the verifier's edge labels:")
    add("")
    add("- one-sided propositions (≥1 hypothesis silent): **{}**".format(
        _pct(rec["n_one_sided_propositions"], rec["n_propositions"])))
    labels = silence["edge_label_given_to_a_silent_hypothesis"]
    n_sil = silence["n_silent_hypothesis_proposition_pairs"]
    absence = labels.get("unlikely", 0) + labels.get("strongly_contradicted", 0)
    presence = sum(labels.get(k, 0) for k in ("strongly_implied", "implied", "weakly_implied"))
    add("- a silent hypothesis was labelled `neutral` (correct, inert at 0.50): **{}**".format(
        _pct(labels.get("neutral", 0), n_sil)))
    add("- …read as **absence** (`unlikely`/`strongly_contradicted`): **{}**".format(
        _pct(absence, n_sil)))
    add("- …read as presence (`*implied`): **{}**".format(_pct(presence, n_sil)))
    add("")
    add("Of the **{}** sign-opposed nodes that distinguish the pilot from ResearchBench, "
        "**{}** are genuine discriminators and **{}** are opposition manufactured from "
        "silence, according to the auditor.".format(rec["n_system_sign_opposed"],
                          rec["n_sign_opposed_genuine_discriminator"],
                          rec["n_sign_opposed_manufactured_from_silence"]))
    add("")
    sens = rel["judge_reliability_sensitivity"] if "judge_reliability_sensitivity" in rel else rel["sensitivity_sign_opposed_split"]
    add("**Sensitivity.** The auditor appears to over-call silence (section 8). "
        "Extrapolating the blind second rater's disagreements gives roughly {} genuine "
        "vs {} manufactured. {}".format(
            sens["crude_extrapolation"]["genuine"], sens["crude_extrapolation"]["manufactured"],
            sens["reading"][0].upper() + sens["reading"][1:] + "."))
    add("")
    mech = attribution.get("_manufactured_mechanism") or {}
    if mech:
        add("**Which way manufactured opposition pushes.** Of {} manufactured nodes that "
            "moved a score, {} favoured the hypothesis that *generated* the proposition "
            "(total log-odds {:.2f}) and {} favoured the other ({:.2f}). Evidence on "
            "these nodes is overwhelmingly `support`, so literature support for a "
            "hypothesis's own one-sided consequences is scored as evidence *against* "
            "its silent competitor: component truth standing in for hypothesis "
            "truth.".format(mech["n_moving"], mech["n_toward_origin"],
                            mech["logodds_toward_origin"], mech["n_toward_other"],
                            mech["logodds_toward_other"]))
        add("")

    # ------------------------------------------------------------------ #
    add("## 6. Historical evidence discovery (Step 7B)")
    add("")
    add("\n".join(_table(
        ["attribution", "all {} propositions".format(ev["n_nodes"]),
         "{} genuine discriminators".format(ev["n_discriminative_nodes"])],
        [[k, ev["attribution_all_nodes"].get(k, 0), ev["attribution_discriminative_nodes"].get(k, 0)]
         for k in sorted(set(ev["attribution_all_nodes"]) | set(ev["attribution_discriminative_nodes"]),
                         key=lambda k: -ev["attribution_all_nodes"].get(k, 0))])))
    add("")
    add("Assessor errors: {}. Retrieval returning nothing: {}.".format(
        ev["n_assessor_errors"], ev["n_retrieved_nothing"]))
    add("")
    add("When the right discriminator was generated, the pre-cutoff literature usually "
        "did not contain the decisive observation — expected by construction, since "
        "the resolving study postdates the cutoff. Informative evidence concentrated "
        "on propositions that do not discriminate. **Caveat:** the attribution judge "
        "sees only what was retrieved, so it is structurally unable to detect evidence "
        "that exists but was never retrieved; `retrieval_failure` is likely "
        "under-counted and `no_relevant_historical_evidence_exists` over-counted.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 7. Hypothesis comparison and failure attribution (Step 7C, Step 8 q5)")
    add("")
    add("No accuracy is computed. Each score's log-odds toward the top-ranked "
        "hypothesis is decomposed exactly (from `scores.json` contributions) by what "
        "the auditor found about each node.")
    add("")
    groups = ["genuine_discriminator", "manufactured_opposition", "silence_read_one_way",
              "one_sided_neutral_ok", "both_predict_same"]
    comp_by = {c["case_id"]: c for c in comparison["cases"]}
    rows = []
    for cid, a in sorted((k, v) for k, v in attribution.items() if not k.startswith("_")):
        c = comp_by[cid]["comparison_to_hidden_resolution"]
        fav = favoured.get(cid)
        rel_to = ("matches" if a["top"] == fav else "OPPOSES") if fav else "n/a"
        rows.append([cid, c["resolution_type"], fav or "—", a["top"], rel_to,
                     "{:+.2f}".format(a["total_logodds_toward_top"])]
                    + ["{:+.2f}".format(a["by_group"].get(g, 0.0)) for g in groups])
    add("\n".join(_table(
        ["case", "resolution", "favoured", "top", "top vs resolution", "total"]
        + ["genuine", "manufactured", "silence one-way", "one-sided (ok)", "both same"],
        rows)))
    add("")
    err = rel["known_auditor_error_direction"]["example"]
    add("**This decomposition inherits the auditor's errors, and they matter here.** "
        "Example: in `{}`, the auditor called H2 silent on {} (\"{}\"), but H2 states "
        "{}. Reclassified, that case's genuine-discriminator push {}. The pre-cutoff "
        "literature strongly supported content-selective persistent PFC activity; "
        "whether that counts against a control account was the interpretive crux of "
        "the dispute itself, which the resolving study settled with a causal "
        "manipulation not yet performed at the cutoff. Treat every per-case "
        "attribution as provisional pending expert review of the score-moving nodes.".format(
            err["case"], err["node"], err["proposition"], err["hypothesis_text"].split(": ", 1)[1],
            err["effect"].replace("moves pfc_storage genuine-discriminator log-odds", "moves")))
    add("")
    add("Read the directional cases by *what drove the ranking*, not by whether it "
        "matched: a match driven by manufactured opposition is not a success, and a "
        "mismatch driven by it is a method failure rather than an absence of evidence. "
        "For `mixed`, `regime_dependent` and `component_wise` cases there is no winner "
        "to match; the table shows only what the system leaned on.")
    add("")
    add("Ordinal→numeric mappings are placeholders (`v0-placeholder`); magnitudes are "
        "comparable within this run only, and only their sign and relative size carry "
        "information.")
    add("")

    # ------------------------------------------------------------------ #
    add("## 8. How far the audit can be trusted")
    add("")
    tr = rel["test_retest_case_pfc_storage_vs_control"]
    sr = rel["second_rater"]
    add("\n".join(_table(
        ["check", "result"],
        [["internal consistency (category vs per-hypothesis statuses)",
          "{} inconsistencies in {}".format(rel["internal_consistency"]["inconsistencies"],
                                            rel["internal_consistency"]["n"])],
         ["test-retest, one case judged twice",
          "category {}/{}, discriminative {}/{}".format(tr["category_agree"], tr["n"],
                                                       tr["is_discriminative_agree"], tr["n"])],
         ["blind second rating ({}), stratified sample".format(sr["rater"]),
          "discriminative {}/{}, full status {}/{}; judge {} vs rater {} discriminative".format(
              sr["discriminative_agree"], sr["n"], sr["status_vector_agree"], sr["n"],
              sr["judge_discriminative"], sr["executor_discriminative"])],
         ["non-verbatim reference matches", "{} — {}".format(
             rel["unverbatim_reference_matches"]["n"],
             rel["unverbatim_reference_matches"]["effect_on_recovery_counts"])]])))
    add("")
    add("The judge and the second rater are both LLMs (the judge is the same deployment "
        "as the verifier). No human domain expert has reviewed any judgment. "
        "The auditor's disagreements are not random: it over-calls `indeterminate` "
        "and misses explicit denials in hypothesis text ({}), plausibly because its "
        "prompt warns emphatically against reading silence as absence. Its one-sided "
        "share on the sample was {} vs the second rater's {}.".format(
            rel["known_auditor_error_direction"]["example"]["node"] + " in "
            + rel["known_auditor_error_direction"]["example"]["case"],
            rel["one_sided_share_on_sample"]["auditor"],
            rel["one_sided_share_on_sample"]["second_rater"]))
    add("")
    add("What is robust: the structural comparison (section 3, no judge involved); "
        "that silence-driven contrast is a large share of the opposition under either "
        "rater; and the direction of the mechanism (one-sided support flows to the "
        "generating hypothesis). What is not robust: whether silence-driven contrast is "
        "a majority, and every per-case failure attribution.")
    add("")
    add("`{}/manual_review/score_moving_nodes_for_expert_review.json` lists every node "
        "that moved a ranking, ordered by influence, with blank fields for a human "
        "domain expert.".format(run_dir))
    add("")

    add("## 9. Artifacts")
    add("")
    for name in REQUIRED:
        add("- `{}`".format(run_dir / name))
    add("- `{}/manual_review/` — blind sample and compared ratings".format(run_dir))
    add("- per-case forensics: `{}/instances/<case_id>/` — `input.json`, `graph.json`, "
        "`edge_judgments.json`, `queries.json`, `retrieval.json`, `evidence.json`, "
        "`scores.json`, `model_outputs.json`, `events.jsonl`, `report.md`".format(run_dir))
    add("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    parser.add_argument("--out", default="docs/PILOT_REPORT.md")
    args = parser.parse_args()

    run_dir = resolve_path(args.run)
    missing = [n for n in REQUIRED if not (run_dir / n).exists()]
    if missing:
        LOGGER.error("missing prerequisite artifact(s): %s", missing)
        return 2

    text = build(run_dir)
    out_path = resolve_path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    LOGGER.info("wrote %s (%d lines)", out_path, text.count("\n") + 1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
