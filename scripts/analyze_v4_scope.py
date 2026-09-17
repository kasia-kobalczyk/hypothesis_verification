"""BENCH-GRAPH-V4-SCOPE-001 development metrics for replicated stage-A v4-scope replays.

Deterministic, no LLM. Inputs: >= 3 replicate replays of ONE v4-scope iteration (on the
frozen v3 pilot), the prior-v4 head replays (`v4_replay_pilot_iter02{,_rep2}`), the frozen
v3 node contributions, and the D045/D046 development labels. Sections follow directive §13:

  consistency           every recorded gate re-derived from the recorded judgments with
                        the current gate code, and the scores re-computed;
  A_state_preservation  prior v4 vs v4-scope prediction states (same prompt; measures noise
                        and D046 agreement, so a regression would be visible);
  B_scope               scope counts, reviewed category x scope, generic facts gated,
                        genuine discriminators retained;
  C_contrast_evidence   contrast-relevance distribution; genuine discriminators' evidence;
                        generic/compatible facts with context-only support that v3 scored;
  D_scope_x_evidence    the specificity-assessability table (§10), quantified;
  E_influence           |log-odds| influence composition by reviewed category, v3 / prior v4
                        / v4-scope / v4-scope with contrast_partial allowed;
  F_partial_sensitivity §9, reporting only;
  G_scored_nodes        every scored node with scope, label, evidence, contribution;
  H_stability           pairwise replicate agreement, v4-scope vs prior v4;
  per_case              scores per replicate (later-resolution relation is descriptive only).

The D045/D046 labels are model-based DEVELOPMENT annotations; this script reports agreement
with them, it does not optimise it.

Usage:
    python scripts/analyze_v4_scope.py --replay runs/v4scope_replay_iter01{,_rep2,_rep3} --name iter01
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_v4_development as dev  # noqa: E402
from src.inference import discrimination as d  # noqa: E402
from src.inference.parameters import load_ordinal_mappings  # noqa: E402

OUT_ROOT = ROOT / "benchmark" / "v4_scope"
PRIOR_V4 = [ROOT / "runs" / "v4_replay_pilot_iter02", ROOT / "runs" / "v4_replay_pilot_iter02_rep2"]
CATEGORIES = dev.CATEGORIES
UNREVIEWED = "unreviewed"
EVIDENCE_COLUMNS = ["no_evidence_assessment", "no_evidence", "mixed", "element_unavailable",
                    "relevance_unavailable", "contrast_direct", "contrast_partial", "context_only",
                    "construct_mismatch", "relevance_no_evidence"]


def _frac(a, b):
    return None if not b else a / b


def load_replay(replay: Path):
    """review_id -> node record (v4-scope), plus per-case layers."""
    nodes, cases = OrderedDict(), OrderedDict()
    for path in sorted((replay / "instances").glob("*/discrimination.json")):
        layer = json.loads(path.read_text(encoding="utf-8"))
        cases[path.parent.name] = layer
        for nid, rec in layer["nodes"].items():
            nodes["GP1-{}-{}".format(path.parent.name, nid)] = dict(rec, case_id=path.parent.name, node_id=nid)
    return nodes, cases


def scope_of(rec):
    return (rec.get("scope") or {}).get("scope") or "scope_unavailable"


def relevance_of(rec):
    return (rec.get("contrast_relevance") or {}).get("contrast_relevance")


def evidence_column(rec) -> str:
    """Evidence availability / contrast relevance, whatever the node's eligibility.

    Relevance is judged for every node with informative evidence and an element, including
    nodes whose element carries no contrast, so the assessability table can show it; the
    `has_contrast` outcome is counted separately (`n_has_contrast_false`).
    """
    label = rec.get("evidence_label")
    if label is None:
        return "no_evidence_assessment"
    if label in d.UNINFORMATIVE_EVIDENCE:
        return label
    if not rec.get("contrast_element"):
        return "element_unavailable"
    rel = relevance_of(rec)
    if rel is None:
        return "relevance_unavailable"
    return "relevance_no_evidence" if rel == "no_evidence" else rel


def influence(contribution: Dict[str, float]) -> float:
    return abs(contribution["H2"] - contribution["H1"])


# --------------------------------------------------------------------------- #
def regate(cases, mappings, allowed):
    """Re-derive gates and scores from recorded judgments. Returns per-case (gates, result)."""
    out = OrderedDict()
    for case, layer in cases.items():
        hyps = layer["hypothesis_ids"]
        gates, states, labels, texts = OrderedDict(), {}, {}, {}
        for nid, rec in layer["nodes"].items():
            gates[nid] = d.gate_node_scope(
                node_id=nid, hypothesis_ids=hyps, states=rec["states"], scope=(rec["scope"] or {}).get("scope"),
                evidence_label=rec["evidence_label"], has_contrast=(rec["contrast_element"] or {}).get("has_contrast"),
                contrast_relevance=relevance_of(rec), allowed_relevance=allowed)
            if rec["states"]:
                states[nid] = rec["states"]
            labels[nid], texts[nid] = rec["evidence_label"], rec["text"]
        res = d.score_gated(hypothesis_ids=hyps, nodes=texts, states=states, gates=gates, evidence_labels=labels,
                            mappings=mappings, multi_parent_rule="noisy_or", parent_false_baseline=0.5,
                            instance_id=case)
        contrib: Dict[str, Dict[str, float]] = {}
        for c in res.contributions:
            contrib.setdefault(c.node_id, {"H1": 0.0, "H2": 0.0})[c.hypothesis_id] = c.contribution
        out[case] = (gates, res, contrib)
    return out


def consistency(cases, main) -> Dict[str, Any]:
    gate_mismatch, score_mismatch = [], []
    for case, layer in cases.items():
        gates, res, _ = main[case]
        for nid, rec in layer["nodes"].items():
            if (rec["gate_reason"], rec["used_in_score"]) != (gates[nid]["gate_reason"], gates[nid]["used_in_score"]):
                gate_mismatch.append("{}-{}".format(case, nid))
        if any(abs(res.scores[h] - layer["scores"][h]) > 1e-12 for h in layer["scores"]):
            score_mismatch.append(case)
    return OrderedDict([("gate_mismatches", gate_mismatch), ("score_mismatches", score_mismatch),
                        ("ok", not gate_mismatch and not score_mismatch)])


# --------------------------------------------------------------------------- #
def state_block(nodes, labels) -> Dict[str, Any]:
    pairs, profiles = Counter(), Counter()
    unavailable = 0
    for rec in nodes.values():
        if not rec["states"]:
            unavailable += 1
            continue
        for s in rec["states"].values():
            pairs[s["state"]] += 1
        profiles[rec["profile_class"]] += 1
    n, n_pairs = len(nodes), sum(pairs.values())
    rows = []
    for rid, lab in labels.items():
        for h, human in (lab.get("human_prediction_for_each_hypothesis") or {}).items():
            got = ((nodes[rid]["states"] or {}).get(h) or {}).get("state")
            rows.append((human, got, lab["human_prediction_qualifiers"][h]["qualified"]))
    unq = [r for r in rows if not r[2]]
    silence = [rid for rid, lab in labels.items() if lab["human_primary_category"] == "silence_as_null_error"]
    return OrderedDict([
        ("pair_states", dict(pairs)), ("indeterminate_rate", _frac(pairs["indeterminate"], n_pairs)),
        ("profiles", dict(profiles)),
        ("fraction_one_sided", _frac(profiles["one_sided_prediction"], n)),
        ("fraction_comparative_contrast", _frac(profiles["comparative_discriminator"], n)),
        ("nodes_states_unavailable", unavailable),
        ("d046_state_agreement_unqualified", "{}/{}".format(sum(h == g for h, g, _ in unq), len(unq))),
        ("d046_state_agreement_all", "{}/{}".format(sum(h == g for h, g, _ in rows), len(rows))),
        ("reviewed_silence_errors_with_comparative_profile", "{}/{}".format(
            sum(1 for r in silence if nodes[r]["profile_class"] == "comparative_discriminator"), len(silence))),
        ("reviewed_silence_errors_used_in_score", "{}/{}".format(
            sum(1 for r in silence if nodes[r]["used_in_score"]), len(silence))),
    ])


def scope_block(nodes, labels) -> Dict[str, Any]:
    cat = lambda rid: (labels.get(rid) or {}).get("human_primary_category") or UNREVIEWED  # noqa: E731
    by_scope = Counter(scope_of(r) for r in nodes.values())
    comparative = Counter(scope_of(r) for r in nodes.values() if r["comparatively_eligible"])
    cross = OrderedDict()
    for c in CATEGORIES + [UNREVIEWED]:
        cross[c] = dict(Counter(scope_of(nodes[rid]) for rid in nodes if cat(rid) == c))
    generic = [rid for rid in labels if cat(rid) == "generic_component_fact"]
    genuine = [rid for rid in labels if cat(rid) == "genuine_discriminator"]
    return OrderedDict([
        ("scope_counts_all_nodes", dict(by_scope)),
        ("scope_counts_comparative_profile_nodes", dict(comparative)),
        ("human_category_x_scope", cross),
        ("generic_component_facts", OrderedDict([
            ("n", len(generic)),
            ("rejected_from_scoring", sum(1 for r in generic if not nodes[r]["used_in_score"])),
            ("scope_non_comparative", sum(1 for r in generic
                                          if scope_of(nodes[r]) not in d.COMPARATIVE_SCOPE_CLASSES)),
            ("nodes", OrderedDict((r, OrderedDict([("scope", scope_of(nodes[r])), ("profile", nodes[r]["profile_class"]),
                                                    ("gate_reason", nodes[r]["gate_reason"])])) for r in generic)),
        ])),
        ("genuine_discriminators", OrderedDict([
            ("n", len(genuine)),
            ("scope_eligible", sum(1 for r in genuine if nodes[r]["scope_eligible"])),
            ("comparative_and_scope_eligible", sum(1 for r in genuine if nodes[r]["comparatively_eligible"]
                                                   and nodes[r]["scope_eligible"])),
            ("used_in_score", sum(1 for r in genuine if nodes[r]["used_in_score"])),
            ("nodes", OrderedDict((r, OrderedDict([
                ("scope", scope_of(nodes[r])), ("profile", nodes[r]["profile_class"]),
                ("evidence_label", nodes[r]["evidence_label"]), ("contrast_relevance", relevance_of(nodes[r])),
                ("gate_reason", nodes[r]["gate_reason"])])) for r in genuine)),
        ])),
    ])


def contrast_block(nodes, labels, v3) -> Dict[str, Any]:
    cat = lambda rid: (labels.get(rid) or {}).get("human_primary_category") or UNREVIEWED  # noqa: E731
    informative = [r for r in nodes if nodes[r]["evidence_label"] not in (None, "no_evidence", "mixed")]
    eligible = [r for r in informative if nodes[r]["comparatively_eligible"] and nodes[r]["scope_eligible"]]
    raw_conflicts = [r for r in informative if (nodes[r].get("contrast_relevance") or {}).get("contrast_variable_reported") == "yes"
                     and nodes[r]["contrast_relevance"].get("different_construct") == "yes"]
    context_generic = [r for r in informative if cat(r) in ("generic_component_fact", "compatible_non_discriminative")
                       and relevance_of(nodes[r]) in ("context_only", "construct_mismatch", "no_evidence")]
    eligible_with_contrast = [r for r in eligible if (nodes[r].get("contrast_element") or {}).get("has_contrast")]
    return OrderedDict([
        ("n_informative_evidence_nodes", len(informative)),
        ("relevance_comparative_scope_eligible_and_has_contrast",
         dict(Counter(evidence_column(nodes[r]) for r in eligible_with_contrast))),
        ("relevance_all_informative", dict(Counter(evidence_column(nodes[r]) for r in informative))),
        ("relevance_comparative_and_scope_eligible", dict(Counter(evidence_column(nodes[r]) for r in eligible))),
        ("relevance_by_human_category", OrderedDict(
            (c, dict(Counter(evidence_column(nodes[r]) for r in informative if cat(r) == c)))
            for c in CATEGORIES)),
        ("genuine_discriminators_contrast_direct", "{}/{}".format(
            sum(1 for r in labels if cat(r) == "genuine_discriminator" and relevance_of(nodes[r]) == "contrast_direct"),
            sum(1 for r in labels if cat(r) == "genuine_discriminator"))),
        ("generic_or_compatible_with_only_context_mismatch_or_none_that_v3_scored", OrderedDict([
            ("n", sum(1 for r in context_generic if v3[r]["absolute_influence"] > 0)),
            ("of_generic_or_compatible_with_that_relevance", len(context_generic)),
            ("nodes", [r for r in context_generic if v3[r]["absolute_influence"] > 0])])),
        ("answers_yes_reported_and_yes_different_construct", raw_conflicts),
        ("has_contrast_false_on_informative", sum(1 for r in informative if nodes[r].get("contrast_element")
                                                  and not nodes[r]["contrast_element"]["has_contrast"])),
    ])


def scope_x_evidence(nodes, restrict=None) -> Dict[str, Any]:
    rows = OrderedDict()
    scopes = list(d.SCOPE_CLASSES) + ["scope_unavailable"]
    for s in scopes:
        recs = [r for r in nodes.values() if scope_of(r) == s and (restrict is None or restrict(r))]
        counts = Counter(evidence_column(r) for r in recs)
        n_inf = sum(counts[c] for c in EVIDENCE_COLUMNS if c not in ("no_evidence_assessment", "no_evidence", "mixed"))
        rows[s] = OrderedDict([("n", len(recs))] + [(c, counts[c]) for c in EVIDENCE_COLUMNS] + [
            ("n_has_contrast_false", sum(1 for r in recs if r.get("contrast_element")
                                         and not r["contrast_element"]["has_contrast"])),
            ("p_informative_evidence", _frac(n_inf, len(recs))),
            ("p_contrast_direct", _frac(counts["contrast_direct"], len(recs))),
            ("p_contrast_direct_or_partial", _frac(counts["contrast_direct"] + counts["contrast_partial"], len(recs))),
            ("p_contrast_direct_given_informative", _frac(counts["contrast_direct"], n_inf)),
        ])
    spec = [r for r in nodes.values() if scope_of(r) in d.COMPARATIVE_SCOPE_CLASSES and (restrict is None or restrict(r))]
    broad = [r for r in nodes.values() if scope_of(r) in ("broader_class_fact", "possibility_claim")
             and (restrict is None or restrict(r))]

    def grp(recs):
        inf = [r for r in recs if evidence_column(r) not in ("no_evidence_assessment", "no_evidence", "mixed")]
        return OrderedDict([("n", len(recs)), ("p_informative_evidence", _frac(len(inf), len(recs))),
                            ("p_contrast_direct", _frac(sum(evidence_column(r) == "contrast_direct" for r in recs), len(recs))),
                            ("p_contrast_direct_given_informative",
                             _frac(sum(evidence_column(r) == "contrast_direct" for r in recs), len(inf)))])
    return OrderedDict([("rows", rows), ("specific_(hypothesis_or_mechanism)", grp(spec)),
                        ("broad_(class_fact_or_possibility)", grp(broad))])


def composition(influence_by_rid, labels) -> Dict[str, Any]:
    total = sum(influence_by_rid.values())
    out = OrderedDict([("total_absolute_influence", total)])
    for c in CATEGORIES + [UNREVIEWED]:
        val = sum(v for rid, v in influence_by_rid.items()
                  if ((labels.get(rid) or {}).get("human_primary_category") or UNREVIEWED) == c)
        out[c] = OrderedDict([("absolute_influence", val), ("share", _frac(val, total))])
    return out


def pairwise(replicates: List[Dict[str, Any]], key) -> List[str]:
    out = []
    for a, b in itertools.combinations(replicates, 2):
        common = [rid for rid in a if rid in b]
        vals = [(key(a[rid]), key(b[rid])) for rid in common]
        vals = [(x, y) for x, y in vals if x is not None or y is not None]
        out.append("{}/{}".format(sum(x == y for x, y in vals), len(vals)))
    return out


def state_pairs_agreement(replicates) -> List[str]:
    out = []
    for a, b in itertools.combinations(replicates, 2):
        pairs = [(a[r]["states"][h]["state"], b[r]["states"][h]["state"]) for r in a
                 if a[r]["states"] and b[r]["states"] for h in a[r]["states"]]
        out.append("{}/{}".format(sum(x == y for x, y in pairs), len(pairs)))
    return out


# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", nargs="+", required=True, help="replicate replays of ONE v4-scope iteration")
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    replays = [(ROOT / r).resolve() for r in args.replay]
    mappings = load_ordinal_mappings(str(ROOT / "configs" / "ordinal_mappings.yaml"))
    labels, _, v3, _, _ = dev.load(PRIOR_V4[0])

    prior = [dev.load(p)[3] for p in PRIOR_V4]
    loaded = [load_replay(r) for r in replays]
    for nodes, _ in loaded:
        if set(nodes) != set(v3):
            raise SystemExit("replay nodes differ from the frozen v3 nodes")

    out = OrderedDict([("iteration", args.name), ("replays", [r.name for r in replays]),
                       ("prior_v4_replays", [p.name for p in PRIOR_V4])])
    out["consistency"] = OrderedDict()
    reps = OrderedDict()
    for replay, (nodes, cases) in zip(replays, loaded):
        main_g = regate(cases, mappings, d.COMPARATIVE_RELEVANCE)
        sens_g = regate(cases, mappings, d.SENSITIVITY_RELEVANCE)
        out["consistency"][replay.name] = consistency(cases, main_g)
        manifest = json.loads((replay / "manifest.json").read_text(encoding="utf-8"))
        summary = json.loads((replay / "summary.json").read_text(encoding="utf-8"))
        infl = {"GP1-{}-{}".format(c, n): influence(r["contribution"]) for c, layer in cases.items()
                for n, r in layer["nodes"].items()}
        sens_infl = {"GP1-{}-{}".format(c, n): influence(contrib.get(n, {"H1": 0.0, "H2": 0.0}))
                     for c, (_, _, contrib) in sens_g.items() for n in cases[c]["nodes"]}
        sens_scored = {"GP1-{}-{}".format(c, n) for c, (gates, _, _) in sens_g.items()
                       for n, g in gates.items() if g["used_in_score"]}
        main_scored = {rid for rid, r in nodes.items() if r["used_in_score"]}
        cat = lambda rid: (labels.get(rid) or {}).get("human_primary_category") or UNREVIEWED  # noqa: E731
        reps[replay.name] = OrderedDict([
            ("git", manifest["git"]), ("prompts", {k: v.get("sha256_16") if isinstance(v, dict) else v
                                                   for k, v in manifest["prompts"].items()}),
            ("llm_calls", summary.get("llm_calls")), ("llm_usage", summary.get("llm_usage")),
            ("n_errors", sum(len(l["errors"]) for l in cases.values())),
            ("A_state_preservation", state_block(nodes, labels)),
            ("B_scope", scope_block(nodes, labels)),
            ("C_contrast_evidence", contrast_block(nodes, labels, v3)),
            ("D_scope_x_evidence", OrderedDict([
                ("all_nodes", scope_x_evidence(nodes)),
                ("comparative_profile_nodes", scope_x_evidence(nodes, lambda r: r["comparatively_eligible"]))])),
            ("E_influence", composition(infl, labels)),
            ("F_partial_sensitivity", OrderedDict([
                ("REPORTING_ONLY", "contrast_partial admitted; not the method (directive §9)"),
                ("n_scored_main", len(main_scored)), ("n_scored_sensitivity", len(sens_scored)),
                ("additional_nodes", sorted(sens_scored - main_scored)),
                ("additional_by_category", dict(Counter(cat(r) for r in sens_scored - main_scored))),
                ("generic_component_facts_reentering", sorted(r for r in sens_scored - main_scored
                                                              if cat(r) == "generic_component_fact")),
                ("influence", composition(sens_infl, labels)),
                ("case_scores", OrderedDict((c, dict(res.scores)) for c, (_, res, _) in sens_g.items())),
            ])),
            ("G_scored_nodes", [OrderedDict([
                ("review_id", rid), ("human_category", cat(rid)), ("scope", scope_of(nodes[rid])),
                ("states", {h: s["state"] for h, s in nodes[rid]["states"].items()}),
                ("evidence_label", nodes[rid]["evidence_label"]),
                ("contrast_variable", nodes[rid]["contrast_element"]["contrast_variable"]),
                ("log_odds_H2_over_H1", nodes[rid]["contribution"]["H2"] - nodes[rid]["contribution"]["H1"]),
                ("text", nodes[rid]["text"])]) for rid in sorted(main_scored)]),
            ("G_scored_scope_counts", dict(Counter(scope_of(nodes[r]) for r in main_scored))),
            ("per_case", OrderedDict((c, OrderedDict([
                ("v3_frozen_scores", layer["v3_frozen_scores"]), ("scores", layer["scores"]),
                ("n_scored", layer["summary"]["n_used_in_score"]),
                ("later_resolution_favours_(descriptive_only)", dev.FAVOURED.get(c))])) for c, layer in cases.items())),
        ])
    out["replicates"] = reps
    out["prior_v4"] = OrderedDict((p.name, OrderedDict([
        ("A_state_preservation", state_block(nodes, labels)),
        ("n_used_in_score", sum(1 for r in nodes.values() if r["used_in_score"]))]))
        for p, nodes in zip(PRIOR_V4, prior))

    scope_nodes = [n for n, _ in loaded]
    out["H_stability"] = OrderedDict([
        ("v4_scope_state_pairs", state_pairs_agreement(scope_nodes)),
        ("prior_v4_state_pairs", state_pairs_agreement(prior)),
        ("v4_scope_vs_prior_v4_state_pairs", state_pairs_agreement([scope_nodes[0], prior[0]])),
        ("v4_scope_profile", pairwise(scope_nodes, lambda r: r["profile_class"])),
        ("prior_v4_profile", pairwise(prior, lambda r: r["profile_class"])),
        ("scope_class", pairwise(scope_nodes, scope_of)),
        ("scope_eligible", pairwise(scope_nodes, lambda r: r["scope_eligible"])),
        ("has_contrast", pairwise(scope_nodes, lambda r: (r.get("contrast_element") or {}).get("has_contrast"))),
        ("contrast_relevance", pairwise(scope_nodes, relevance_of)),
        ("used_in_score", pairwise(scope_nodes, lambda r: r["used_in_score"])),
        ("scored_in_all_replicates", sorted(set.intersection(*[{k for k, r in n.items() if r["used_in_score"]}
                                                               for n in scope_nodes]))),
        ("scored_in_any_replicate", sorted(set.union(*[{k for k, r in n.items() if r["used_in_score"]}
                                                       for n in scope_nodes]))),
        ("case_scores_by_replicate", OrderedDict((c, [reps[r.name]["per_case"][c]["scores"] for r in replays])
                                                 for c in loaded[0][1])),
    ])

    dest = OUT_ROOT / args.name
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "development_metrics.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("wrote", (dest / "development_metrics.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
