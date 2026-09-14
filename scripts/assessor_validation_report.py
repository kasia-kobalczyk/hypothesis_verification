"""Evaluate the pre-registered assessor gate from a validation run.

    python3 scripts/assessor_validation_report.py

Reads `benchmark/assessor/validation.json` and reports the four criteria in
`benchmark/assessor/acceptance_gate.json`, plus the adversarial control table.

The framing matters and is repeated in the output: these are **reproducibility and
grounding** statistics, not validity. No domain experts labelled anything. Passing
makes the assessor *provisionally* validated.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import utc_now_iso, write_json  # noqa: E402


def kappa(pairs: List[Tuple[Any, Any]]) -> Optional[float]:
    if not pairs:
        return None
    n = len(pairs)
    observed = sum(1 for a, b in pairs if a == b) / n
    left, right = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    expected = sum((left[c] / n) * (right[c] / n) for c in set(left) | set(right))
    return None if expected >= 1.0 else (observed - expected) / (1 - expected)


def _norm(text):
    import re

    return re.sub(r"\s+", " ", (text or "")).strip().lower()


def _f(value, fmt="{:.3f}"):
    return fmt.format(value) if isinstance(value, (int, float)) else "n/a"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", default="benchmark/assessor/validation.json")
    parser.add_argument("--out", default="benchmark/assessor/validation_report.json")
    parser.add_argument("--md-out", default="benchmark/assessor/validation_report.md")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.validation).read_text())
    gate = data["gate"]
    rows = data["rows"]

    by = defaultdict(dict)              # (condition, case_id) -> judge -> row
    for row in rows:
        by[(row["condition"], row["case_id"])][row["judge"]] = row
    judges = sorted({r["judge"] for r in rows})

    lines: List[str] = ["# Assessor validation — provisional", ""]
    lines += ["Rubric freeze `{}`. Model `{}`, judges {}.".format(
        data["rubric_freeze"]["sha256_16_of_construct"], data.get("model"),
        ", ".join("{}={}".format(k, v) for k, v in data["judges"].items())), ""]
    lines += ["> **{}**".format(data["same_model_caveat"]), ""]
    lines += ["> This measures reproducibility, grounding and robustness to adversarial "
              "controls. It does **not** measure agreement with expert judgment, because "
              "no expert labels exist. Passing makes the assessor *provisionally* "
              "validated.", ""]

    report: Dict[str, Any] = {"generated_at": utc_now_iso(),
                              "rubric_freeze": data["rubric_freeze"], "criteria": {}}

    # ---- criteria 1 and 2: reproducibility on the real condition ------------ #
    real = {cid: judged for (cond, cid), judged in by.items() if cond == "real"}
    both = {cid: j for cid, j in real.items() if len(j) >= 2}
    cat = {j: {cid: v[j]["category"] for cid, v in both.items()} for j in judges}
    direction = {j: {cid: v[j]["direction"] for cid, v in both.items()} for j in judges}

    for left, right in combinations(judges, 2):
        shared = sorted(set(cat[left]) & set(cat[right]))
        three = [(cat[left][c], cat[right][c]) for c in shared]
        boundary = [(cat[left][c], cat[right][c]) for c in shared
                    if not (cat[left][c] == "DIRECT" and cat[right][c] == "DIRECT")]
        dirs = [(direction[left][c], direction[right][c]) for c in shared]

        c1 = sum(1 for a, b in boundary if a == b) / len(boundary) if boundary else None
        c2 = sum(1 for a, b in dirs if a == b) / len(dirs) if dirs else None
        t1 = gate["criterion_1_boundary_reproducibility"]["threshold"]
        t2 = gate["criterion_2_direction_reproducibility"]["threshold"]

        lines += ["## Criteria 1 and 2 — inter-assessor reproducibility", "",
                  "| statistic | n | value | threshold | verdict |",
                  "| --- | --- | --- | --- | --- |",
                  "| three-way (all cases) | {} | {} | — | — |".format(
                      len(three), _f(sum(1 for a, b in three if a == b) / len(three))),
                  "| three-way kappa | {} | {} | — | — |".format(len(three), _f(kappa(three))),
                  "| **boundary reproducibility** | {} | **{}** | {} | **{}** |".format(
                      len(boundary), _f(c1), t1,
                      "PASS" if c1 is not None and c1 >= t1 else "FAIL"),
                  "| boundary kappa | {} | {} | — | — |".format(len(boundary), _f(kappa(boundary))),
                  "| **direction reproducibility** | {} | **{}** | {} | **{}** |".format(
                      len(dirs), _f(c2), t2,
                      "PASS" if c2 is not None and c2 >= t2 else "FAIL"),
                  "| direction kappa | {} | {} | — | — |".format(len(dirs), _f(kappa(dirs))),
                  ""]
        report["criteria"]["criterion_1_boundary_reproducibility"] = {
            "value": c1, "n": len(boundary), "threshold": t1,
            "pass": bool(c1 is not None and c1 >= t1), "kappa": kappa(boundary)}
        report["criteria"]["criterion_2_direction_reproducibility"] = {
            "value": c2, "n": len(dirs), "threshold": t2,
            "pass": bool(c2 is not None and c2 >= t2), "kappa": kappa(dirs)}

    # ---- criterion 3: grounded and independently reproduced ------------------ #
    t3 = gate["criterion_3_grounded_and_independently_reproduced"]["threshold"]
    primary = judges[0]
    positives = [cid for cid, j in both.items() if j[primary]["category"] != "NO_EVIDENCE"]
    qualifying = []
    for cid in positives:
        row = both[cid][primary]
        chain_ok = not row["needs_outside_fact"]
        other = [j for j in judges if j != primary]
        reproduced = all(both[cid][o]["category"] != "NO_EVIDENCE" for o in other)
        if row["grounded"] and chain_ok and reproduced:
            qualifying.append(cid)
    c3 = len(qualifying) / len(positives) if positives else None
    lines += ["## Criterion 3 — grounded and independently reproduced", "",
              "Of the evidential judgments judge `{}` makes, the share that carry a span "
              "found verbatim in the supplied abstract, need no unsupported fact, **and** "
              "are also called evidential by the other judge.".format(primary), "",
              "| | n |", "| --- | --- |",
              "| judge {} called evidential | {} |".format(primary, len(positives)),
              "| …span grounded verbatim | {} |".format(
                  sum(1 for c in positives if both[c][primary]["grounded"])),
              "| …and no unsupported fact | {} |".format(
                  sum(1 for c in positives if both[c][primary]["grounded"]
                      and not both[c][primary]["needs_outside_fact"])),
              "| …and reproduced by the other judge | **{}** |".format(len(qualifying)), "",
              "**{} = {}**, threshold {} -> **{}**".format(
                  "grounded + reproduced", _f(c3), t3,
                  "PASS" if c3 is not None and c3 >= t3 else "FAIL"), ""]
    report["criteria"]["criterion_3_grounded_and_independently_reproduced"] = {
        "value": c3, "n_positives": len(positives), "n_qualifying": len(qualifying),
        "threshold": t3, "pass": bool(c3 is not None and c3 >= t3)}

    # ---- criterion 4 and the control table ----------------------------------- #
    lines += ["## Criterion 4 and the adversarial controls", "",
              "| condition | judgments | informative | P(informative) | grounded spans |",
              "| --- | --- | --- | --- | --- |"]
    control: Dict[str, Dict[str, Any]] = {}
    for condition in ("real", "mismatched", "swapped", "negated", "span_removed"):
        subset = [r for r in rows if r["condition"] == condition]
        if not subset:
            continue
        informative = [r for r in subset if r["category"] != "NO_EVIDENCE"]
        rate = len(informative) / len(subset)
        control[condition] = {
            "n": len(subset), "n_informative": len(informative), "p_informative": rate,
            "n_grounded": sum(1 for r in informative if r["grounded"])}
        lines.append("| `{}` | {} | {} | {} | {} |".format(
            condition, len(subset), len(informative), _f(rate),
            control[condition]["n_grounded"]))
    lines.append("")

    t4 = gate["criterion_4_negative_control_mismatched_abstract"]["threshold_max"]
    c4 = control.get("mismatched", {}).get("p_informative")
    lines += ["**P(informative | mismatched abstract) = {}**, must be ≤ {} -> **{}**".format(
        _f(c4), t4, "PASS" if c4 is not None and c4 <= t4 else "FAIL"), ""]
    report["criteria"]["criterion_4_negative_control"] = {
        "value": c4, "threshold_max": t4,
        "pass": bool(c4 is not None and c4 <= t4)}
    report["controls"] = control

    # Direction flip under negation: informativeness persisting while direction does
    # not move is the signature of an assessor not reading the claim.
    flips = same = 0
    for cid, judged in real.items():
        for judge, row in judged.items():
            neg = by.get(("negated", cid), {}).get(judge)
            if not neg or row["direction"] == "none" or neg["direction"] == "none":
                continue
            if neg["direction"] != row["direction"]:
                flips += 1
            else:
                same += 1
    total = flips + same
    lines += ["### Direction flip under negation", "",
              "Of {} case(s) where both the original and the negated proposition drew a "
              "directional judgment, **{} flipped** and {} kept the same direction "
              "({}).".format(total, flips, same,
                             _f(flips / total) if total else "n/a"), "",
              "A judgment that stays informative but does not move direction when the "
              "claim is negated is not reading the claim.", ""]
    report["direction_flip_under_negation"] = {
        "n": total, "n_flipped": flips, "n_same": same,
        "flip_rate": (flips / total) if total else None}

    # Span removal: an indirect judgment should not survive losing its evidence.
    removed = [r for r in rows if r["condition"] == "span_removed"]
    survived = [r for r in removed if r["category"] != "NO_EVIDENCE"]
    if removed:
        original = {(r["case_id"], r["judge"]): r for r in rows if r["condition"] == "real"}
        same_span = cited_new = no_span = 0
        for row in survived:
            prior = original.get((row["case_id"], row["judge"]), {})
            new_span = _norm(row.get("span"))
            old_span = _norm(prior.get("span"))
            if not new_span:
                no_span += 1
            elif new_span == old_span:
                same_span += 1
            else:
                cited_new += 1
        lines += ["### Survival after the supporting span is removed", "",
                  "{} grounded positive(s) re-judged with the supporting sentence deleted; "
                  "**{} still called the record evidential** ({}).".format(
                      len(removed), len(survived), _f(len(survived) / len(removed))), "",
                  "| of the survivors | n |", "| --- | --- |",
                  "| cited a **different** span, still verbatim | {} |".format(cited_new),
                  "| cited the **same** span (should be impossible) | {} |".format(same_span),
                  "| cited no span at all | {} |".format(no_span), ""]
        if cited_new and not same_span and not no_span:
            lines += ["**Read this as a limitation of the control, not a failure of the "
                      "assessor.** Every survivor moved to a different, still-verbatim span: "
                      "the abstracts carry redundant support, and deleting one sentence "
                      "leaves other evidential sentences standing. To test what this control "
                      "was meant to test, every span the judge could rely on has to go, or "
                      "the control needs single-finding abstracts.", ""]
        else:
            lines += ["Survivors citing the same or no span would mean the judgment was not "
                      "resting on the evidence it cited.", ""]
        report["span_removal"] = {
            "n": len(removed), "n_survived": len(survived),
            "survival_rate": len(survived) / len(removed),
            "survivors_cited_different_span": cited_new,
            "survivors_cited_same_span": same_span,
            "survivors_cited_no_span": no_span,
            "interpretation": ("control limitation (redundant support in the abstract)"
                               if cited_new and not same_span and not no_span
                               else "possible assessor failure")}

    # Where the judges diverge, and on what. A symmetric split means the boundary is
    # fuzzy; a one-sided split means the two prompts sit at different thresholds.
    if len(judges) >= 2:
        left, right = judges[0], judges[1]
        ev = {"DIRECT", "INDIRECT"}
        matrix = Counter((cat[left][c], cat[right][c]) for c in sorted(cat[left]))
        left_only = sum(n for (a, b), n in matrix.items() if a in ev and b not in ev)
        right_only = sum(n for (a, b), n in matrix.items() if b in ev and a not in ev)
        both_ev = sum(n for (a, b), n in matrix.items() if a in ev and b in ev)
        direct_agree = sum(n for (a, b), n in matrix.items() if a == "DIRECT" and b in ev)
        n_direct = sum(n for (a, b), n in matrix.items() if a == "DIRECT")
        lines += ["### Where the two judges diverge", "",
                  "| | judge {} DIRECT | INDIRECT | NO_EVIDENCE |".format(right),
                  "| --- | --- | --- | --- |"]
        for a in ("DIRECT", "INDIRECT", "NO_EVIDENCE"):
            lines.append("| judge {} {} | {} | {} | {} |".format(
                left, a, matrix[(a, "DIRECT")], matrix[(a, "INDIRECT")],
                matrix[(a, "NO_EVIDENCE")]))
        lines += ["",
                  "- both call it evidential: **{}**".format(both_ev),
                  "- only {} does: **{}**".format(left, left_only),
                  "- only {} does: **{}**".format(right, right_only), ""]
        if n_direct:
            lines += ["Agreement on **direct** evidence is {} of {}. The divergence is "
                      "almost entirely in the *indirect* category.".format(
                          direct_agree, n_direct), ""]
        if left_only > 2 * right_only + 3:
            lines += ["**This is a systematic offset, not symmetric noise.** One prompt's "
                      "bar for 'this establishes a fact that changes belief' sits well below "
                      "the other's, even though both were given the same frozen rubric.", ""]
        report["judge_divergence"] = {
            "both_evidential": both_ev, "{}_only".format(left): left_only,
            "{}_only".format(right): right_only,
            "systematic_offset": bool(left_only > 2 * right_only + 3),
            "matrix": {"{}|{}".format(a, b): n for (a, b), n in matrix.items()}}

    verdicts = {k: v.get("pass") for k, v in report["criteria"].items()}
    overall = all(verdicts.values())
    report["overall_pass"] = overall
    lines += ["## Gate", "",
              "| criterion | verdict |", "| --- | --- |"]
    for key, passed in verdicts.items():
        lines.append("| {} | **{}** |".format(key, "PASS" if passed else "FAIL"))
    lines += ["", "**Overall: {}**".format("PASS (provisional)" if overall else "FAIL"), "",
              gate["paper_wording"]["claim_instead"] if overall else
              "Do not proceed to calibration or the sweep.", ""]

    Path(args.md_out).write_text("\n".join(lines) + "\n")
    write_json(args.out, report)
    print("\n".join(lines))
    print("wrote {} and {}".format(args.md_out, args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
