"""Post-hoc consequence-recovery analysis for BENCH-GRAPH-PILOT-001 (Step 6).

Runs ONLY against a frozen run. The hidden annotations enter here and nowhere
else: this script reads the run's artifacts after the fact and never writes back
into anything the verifier can see.

Two independent readings of every generated proposition are produced and kept
separate, because they answer different questions:

* **The system's own claim.** Computed structurally from `edge_judgments.json`.
  The verifier judged each proposition against *every* hypothesis, so a
  proposition is one the system itself treated as discriminating exactly when
  those per-hypothesis edge labels differ. No model call, no interpretation.

* **An independent adjudication.** An LLM judge that sees the hidden reference
  discriminators and classifies the proposition into the six directive
  categories. Its raw output is preserved verbatim for manual review.

Where the two disagree is the interesting part, and the directive's central
worry -- `silence_as_null_error` -- lives precisely there: a proposition the
system scored as discriminating because one hypothesis is silent about it.

Usage:
    python scripts/analyze_pilot_recovery.py --run runs/pilot_explanatory_001
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config
from src.common.io import resolve_path, write_json
from src.common.logging_utils import EventLog, get_logger
from src.llm.client import build_llm_client
from src.llm.prompts import PromptLibrary

# Post-hoc audit prompts live OUTSIDE the verifier's prompt directory. They are
# allowed to state the cutoff date and to show hidden annotations, both of which
# are forbidden in verifier prompts -- see src/llm/prompts_audit/README.md. The
# separation is a directory, not a flag, so a verifier run cannot reach them.
AUDIT_PROMPTS = Path(__file__).resolve().parents[1] / "src" / "llm" / "prompts_audit"

LOGGER = get_logger("pilot.recovery")

HIDDEN_PATH = Path("benchmark/explanatory/cases_hidden.json")

CATEGORIES = [
    "reference_discriminator_recovered",
    "novel_plausible_discriminator",
    "compatible_non_discriminative",
    "generic_component_fact",
    "invalid_or_unsupported",
    "silence_as_null_error",
]

STATUSES = [
    "positive_or_present",
    "negative_or_absent",
    "neutral_or_no_change",
    "indeterminate",
]


# --------------------------------------------------------------------------- #
# The system's own claim, read structurally out of the run
# --------------------------------------------------------------------------- #
def system_discrimination(
    node_id: str, root_edges: List[Dict[str, Any]], hypothesis_ids: List[str]
) -> Dict[str, Any]:
    """What the verifier itself concluded about this proposition.

    The verifier emits one root edge per (hypothesis, proposition) pair with an
    ordinal implication label. If every hypothesis got the same label, the
    verifier did not treat the proposition as telling them apart -- whatever the
    proposition was generated from. That last clause is the directive's point:
    "A proposition is not discriminative merely because it was generated from
    only one hypothesis."
    """
    labels: Dict[str, Optional[str]] = {}
    for edge in root_edges:
        if edge.get("target") == node_id:
            labels[edge.get("source")] = edge.get("ordinal_strength")
    missing = [h for h in hypothesis_ids if h not in labels]
    distinct = {v for v in labels.values() if v is not None}
    return {
        "edge_label_by_hypothesis": labels,
        "hypotheses_without_an_edge": missing,
        "n_distinct_labels": len(distinct),
        # The verifier's own verdict: did it separate the hypotheses here?
        "system_treated_as_discriminative": len(distinct) > 1 and not missing,
        "cross_evaluated_against_all_hypotheses": not missing,
    }


# --------------------------------------------------------------------------- #
# Independent adjudication
# --------------------------------------------------------------------------- #
def _validator(payload: Dict[str, Any]) -> None:
    for key in ("status_under_each", "is_discriminative", "category"):
        if key not in payload:
            raise ValueError("missing {!r}".format(key))
    if payload["category"] not in CATEGORIES:
        raise ValueError("unknown category {!r}".format(payload["category"]))
    statuses = payload["status_under_each"]
    if not isinstance(statuses, dict) or not statuses:
        raise ValueError("status_under_each must be a non-empty object")
    for label, status in statuses.items():
        if status not in STATUSES:
            raise ValueError("unknown status {!r} for {!r}".format(status, label))


def judge_proposition(
    llm,
    library: PromptLibrary,
    *,
    phenomenon: str,
    hypotheses_block: str,
    discriminators_block: str,
    proposition_block: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    prompt = library.render(
        "recovery_classify_v1",
        phenomenon=phenomenon,
        hypotheses=hypotheses_block,
        reference_discriminators=discriminators_block,
        proposition=proposition_block,
    )
    try:
        response = llm.complete_json(
            [{"role": "user", "content": prompt}],
            purpose="pilot.recovery_classify",
            prompt_version="recovery_classify_v1",
            validator=_validator,
        )
    except Exception as exc:  # noqa: BLE001 -- recorded, never silently dropped
        return None, "{}: {}".format(type(exc).__name__, exc)
    return response.parsed, None


# --------------------------------------------------------------------------- #
# Cross-checking the two readings
# --------------------------------------------------------------------------- #
_POSITIVE_EDGES = {"strongly_implied", "implied", "weakly_implied"}
_NEGATIVE_EDGES = {"unlikely", "strongly_contradicted"}


def reconcile(system: Dict[str, Any], judged: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Where the verifier and the auditor disagree, and what kind of disagreement.

    The auditor never sees the verifier's edge labels, so on its own it can only
    say that a hypothesis is *silent* about a proposition -- a property of the
    proposition (it is one-sided), not an error by anyone. Whether the VERIFIER
    then committed the silence-as-null error is only visible by joining the two:

    * silent hypothesis labelled `neutral`   -> handled correctly. 0.50 is inert;
      a proposition one hypothesis predicts and the other is silent about can
      legitimately shift support toward the predicting one.
    * silent hypothesis labelled `unlikely` / `strongly_contradicted`
                                             -> silence read as ABSENCE: the
      null-prediction error the directive names.
    * silent hypothesis labelled `*implied`  -> silence read as PRESENCE: an
      invented implication in the other direction.

    An earlier version flagged every one-sided proposition whose edge labels
    differed, which counted correct `implied`/`neutral` handling as an error.
    Measured on the frozen pilot run, that conflated 57 correctly-handled silences
    with the real errors.
    """
    if judged is None:
        return {"comparable": False, "reason": "judge_error"}
    statuses = judged.get("status_under_each") or {}
    labels = system.get("edge_label_by_hypothesis") or {}
    silent = [h for h, s in statuses.items() if s == "indeterminate"]
    silence_labels = {h: labels.get(h) for h in silent}

    read_as_absence = [h for h, l in silence_labels.items() if l in _NEGATIVE_EDGES]
    read_as_presence = [h for h, l in silence_labels.items() if l in _POSITIVE_EDGES]
    handled_as_neutral = [h for h, l in silence_labels.items() if l == "neutral"]

    present = set(labels.values())
    sign_opposed = bool(present & _POSITIVE_EDGES) and bool(present & _NEGATIVE_EDGES)

    system_says = bool(system.get("system_treated_as_discriminative"))
    judge_says = bool(judged.get("is_discriminative"))
    return {
        "comparable": True,
        "system_treated_as_discriminative": system_says,
        "system_sign_opposed": sign_opposed,
        "judge_treated_as_discriminative": judge_says,
        "agree": system_says == judge_says,
        "n_hypotheses_indeterminate": len(silent),
        "one_sided_proposition": bool(silent),
        "silent_hypotheses_handled_as_neutral": handled_as_neutral,
        "silent_hypotheses_read_as_absence": read_as_absence,
        "silent_hypotheses_read_as_presence": read_as_presence,
        # The verifier invented a directional prediction for a silent hypothesis.
        "silence_inflation": bool(read_as_absence or read_as_presence),
        # ...and that invention produced opposite-signed edges: contrast out of
        # nothing. This is the part that moves the ranking hardest.
        "manufactured_opposition": sign_opposed and bool(silent) and not judge_says,
        # The verifier missed a distinction the auditor says is real.
        "missed_discrimination": judge_says and not system_says,
    }


# --------------------------------------------------------------------------- #
# Per-case driver
# --------------------------------------------------------------------------- #
def analyse_case(
    llm, library: PromptLibrary, *, instance_dir: Path, hidden_case: Dict[str, Any],
    visible_case: Dict[str, Any], workers: int = 1,
) -> Dict[str, Any]:
    graph = json.loads((instance_dir / "graph.json").read_text(encoding="utf-8"))
    edges = json.loads((instance_dir / "edge_judgments.json").read_text(encoding="utf-8"))
    root_edges = edges.get("root_edges") or []
    hypothesis_ids = graph.get("hypothesis_ids") or []

    id_to_text = {h["hypothesis_id"]: h["text"] for h in visible_case["hypotheses"]}
    # The judge sees the hypotheses under their real ids, not the run's anonymised
    # display labels, so its output can be joined back to the benchmark.
    hypotheses_block = "\n\n".join(
        "[{}] {}".format(hid, id_to_text.get(hid, "<unknown>")) for hid in hypothesis_ids
    )
    discriminators = hidden_case.get("reference_discriminators") or []
    discriminators_block = "\n".join(
        "- {}".format(d) for d in discriminators) or "- (none recorded)"

    def one(node: Dict[str, Any]) -> Dict[str, Any]:
        meta = node.get("metadata") or {}
        proposition_block = node["text"]
        if meta.get("why_implied"):
            proposition_block += "\n\n(The system's stated reason for deriving it: {})".format(
                meta["why_implied"])

        system = system_discrimination(node["id"], root_edges, hypothesis_ids)
        judged, error = judge_proposition(
            llm, library,
            phenomenon=visible_case["phenomenon"],
            hypotheses_block=hypotheses_block,
            discriminators_block=discriminators_block,
            proposition_block=proposition_block,
        )
        LOGGER.info("%s %s -> %s", instance_dir.name, node["id"],
                    (judged or {}).get("category", "ERROR"))
        return {
            "node_id": node["id"],
            "text": node["text"],
            "abstraction_level": meta.get("abstraction_level"),
            "generation_origin_hypothesis": node.get("generation_origin_hypothesis"),
            "depth": node.get("depth"),
            "system": system,
            "judge": judged,          # raw, verbatim, for manual review
            "judge_error": error,
            "reconciliation": reconcile(system, judged),
        }

    # Each judgment is an independent call that sees one proposition, so running
    # them concurrently changes nothing about what is judged. `map` keeps rows in
    # graph order.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows: List[Dict[str, Any]] = list(pool.map(one, graph.get("nodes") or []))

    return {
        "case_id": instance_dir.name,
        "n_nodes": len(rows),
        "n_reference_discriminators": len(discriminators),
        "reference_discriminators": discriminators,
        "propositions": rows,
    }


# configs/ordinal_mappings.yaml. Duplicated here ONLY to measure how far a
# mislabelled edge moves the posterior; nothing in the method reads this copy.
_EDGE_PROBABILITY = {
    "strongly_implied": 0.95, "implied": 0.80, "weakly_implied": 0.65,
    "neutral": 0.50, "unlikely": 0.30, "strongly_contradicted": 0.10,
}


def silence_handling(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """How the verifier labelled edges the auditor says are silences.

    `edge_assess_v1` defines "neutral" as "the candidate says nothing either way
    about the proposition" and tells the model to use it freely. So the vocabulary
    is not missing -- the question is whether the edge assessor reaches for it.

    Every non-neutral label on a silent pair moves that hypothesis's posterior
    away from the prior on a proposition it does not actually speak to. The mean
    |P - 0.5| below is how much implication is being invented per silence, in the
    method's own units.
    """
    by_label: Dict[str, int] = {}
    deviations: List[float] = []
    for case in cases:
        for row in case["propositions"]:
            judged = row.get("judge") or {}
            labels = row["system"].get("edge_label_by_hypothesis") or {}
            for hid, status in (judged.get("status_under_each") or {}).items():
                if status != "indeterminate":
                    continue
                label = labels.get(hid)
                by_label[label] = by_label.get(label, 0) + 1
                if label in _EDGE_PROBABILITY:
                    deviations.append(abs(_EDGE_PROBABILITY[label] - 0.5))

    total = sum(by_label.values())
    n_neutral = by_label.get("neutral", 0)
    return {
        "n_silent_hypothesis_proposition_pairs": total,
        "edge_label_given_to_a_silent_hypothesis": by_label,
        "n_labelled_neutral": n_neutral,
        "share_labelled_neutral": (n_neutral / total) if total else None,
        "mean_abs_probability_deviation_from_half": (
            sum(deviations) / len(deviations)) if deviations else None,
        "note": (
            "A silence labelled anything but `neutral` injects implication the "
            "hypothesis does not carry. `neutral` maps to 0.50, which is inert "
            "under the configured aggregation; every other label is not."
        ),
    }


def summarise(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {c: 0 for c in CATEGORIES}
    errors = 0
    system_disc = 0
    judge_disc = 0
    silence_inflation = 0
    missed = 0
    one_sided = 0
    sign_opposed = 0
    sign_opposed_genuine = 0
    sign_opposed_manufactured = 0
    total = 0
    per_case = []

    unverbatim_matches: List[Dict[str, str]] = []

    for case in cases:
        case_counts = {c: 0 for c in CATEGORIES}
        recovered = set()
        # Only a match that is a verbatim member of this case's reference list is
        # counted. The judge is asked for the discriminator verbatim; if it ever
        # paraphrases instead, a set of paraphrases would quietly inflate coverage
        # -- two wordings of one discriminator would read as two recoveries. Such
        # matches are recorded below rather than counted or silently dropped.
        reference_set = set(case.get("reference_discriminators") or [])
        for row in case["propositions"]:
            total += 1
            judged = row.get("judge")
            if judged is None:
                errors += 1
            else:
                counts[judged["category"]] += 1
                case_counts[judged["category"]] += 1
                if judged.get("is_discriminative"):
                    judge_disc += 1
                matched = judged.get("matched_reference_discriminator")
                if judged["category"] == "reference_discriminator_recovered" and matched:
                    if matched in reference_set:
                        recovered.add(matched)
                    else:
                        unverbatim_matches.append({
                            "case_id": case["case_id"],
                            "node_id": row["node_id"],
                            "returned": matched,
                        })
            if row["system"].get("system_treated_as_discriminative"):
                system_disc += 1
            rec = row.get("reconciliation") or {}
            silence_inflation += 1 if rec.get("silence_inflation") else 0
            missed += 1 if rec.get("missed_discrimination") else 0
            one_sided += 1 if rec.get("one_sided_proposition") else 0
            if rec.get("system_sign_opposed"):
                sign_opposed += 1
                if rec.get("judge_treated_as_discriminative"):
                    sign_opposed_genuine += 1
                if rec.get("manufactured_opposition"):
                    sign_opposed_manufactured += 1

        n_ref = case["n_reference_discriminators"]
        per_case.append({
            "case_id": case["case_id"],
            "n_nodes": case["n_nodes"],
            "categories": case_counts,
            # Coverage of the reference list: how many of the observable contrasts
            # the resolving science actually used did the system independently
            # arrive at? Reported per case; never averaged into a headline number,
            # because the reference lists differ in length and in difficulty.
            "n_reference_discriminators": n_ref,
            "n_reference_discriminators_recovered": len(recovered),
            "reference_discriminators_recovered": sorted(recovered),
        })

    return {
        "n_propositions": total,
        "n_judge_errors": errors,
        "categories": counts,
        # Permissive: ANY label difference, e.g. implied vs weakly_implied. Saturates
        # (94% on both ResearchBench reserve-12 and this pilot); see sign-opposed.
        "n_system_treated_as_discriminative": system_disc,
        "n_judge_treated_as_discriminative": judge_disc,
        "n_silence_inflation": silence_inflation,
        "n_missed_discrimination": missed,
        # The auditor's `silence_as_null_error` category cannot see edge labels, so
        # it identifies ONE-SIDED propositions. These fields separate that
        # generation property from the verifier's actual error.
        "n_one_sided_propositions": one_sided,
        "n_system_sign_opposed": sign_opposed,
        "n_sign_opposed_genuine_discriminator": sign_opposed_genuine,
        "n_sign_opposed_manufactured_from_silence": sign_opposed_manufactured,
        # Non-empty means the recovery counts need manual checking: the judge named
        # a discriminator that is not verbatim in the reference list.
        "unverbatim_reference_matches": unverbatim_matches,
        "silence_handling": silence_handling(cases),
        "per_case": per_case,
        "interpretation": (
            "Descriptive only. These counts characterise WHAT THE SYSTEM GENERATED "
            "on eight cases; they are not a score, and no part of the method may be "
            "tuned on them."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, help="frozen run directory")
    parser.add_argument("--config", default="configs/pilot_explanatory.yaml")
    parser.add_argument("--out", default=None, help="output path (default: <run>/recovery.json)")
    parser.add_argument("--cases", nargs="*", default=None)
    parser.add_argument("--workers", type=int, default=6,
                        help="concurrent judge calls (independent; order preserved)")
    parser.add_argument(
        "--resummarise", action="store_true",
        help="recompute reconciliation and summary from the raw judge output already "
             "preserved in recovery.json. Makes NO model calls, so it cannot change "
             "any judgment -- only how the preserved judgments are counted.")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing recovery.json")
    args = parser.parse_args()

    run_dir = resolve_path(args.run)
    if not (run_dir / "summary.json").exists():
        LOGGER.error(
            "%s has no summary.json: the run is not finished, so it is not frozen. "
            "Step 6 runs only against a frozen run.", run_dir)
        return 2

    out_path = Path(args.out) if args.out else run_dir / "recovery.json"
    if args.resummarise:
        payload = json.loads(out_path.read_text(encoding="utf-8"))
        for case in payload["cases"]:
            for row in case["propositions"]:
                row["reconciliation"] = reconcile(row["system"], row.get("judge"))
        payload["summary"] = summarise(payload["cases"])
        payload.setdefault("resummarised", []).append({
            "reason": (
                "reconcile() revised: silence inflation now requires the silent "
                "hypothesis to have received a directional edge label; `neutral` on a "
                "silence is correct handling. Raw judgments unchanged."),
        })
        write_json(out_path, payload)
        print(json.dumps(payload["summary"], indent=2))
        return 0
    if out_path.exists() and not args.force:
        LOGGER.error("%s exists; pass --force to overwrite", out_path)
        return 2

    hidden = json.loads(resolve_path(HIDDEN_PATH).read_text(encoding="utf-8"))["cases"]
    config = load_config(args.config)
    visible = {}
    for line in resolve_path(config.dataset.case_path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            visible[row["case_id"]] = row

    llm = build_llm_client(config.llm)
    event_log = EventLog(run_dir / "recovery_events.jsonl")
    llm.event_log = event_log
    library = PromptLibrary(AUDIT_PROMPTS)

    instance_root = run_dir / "instances"
    wanted = set(args.cases) if args.cases else None
    cases = []
    for instance_dir in sorted(instance_root.iterdir()):
        if not instance_dir.is_dir():
            continue
        if wanted and instance_dir.name not in wanted:
            continue
        if not (instance_dir / "graph.json").exists():
            LOGGER.warning("%s: no graph.json (run errored); skipped", instance_dir.name)
            continue
        cases.append(analyse_case(
            llm, library,
            instance_dir=instance_dir,
            hidden_case=hidden[instance_dir.name],
            visible_case=visible[instance_dir.name],
            workers=args.workers,
        ))

    payload = {
        "run_dir": str(run_dir),
        "analysis": "BENCH-GRAPH-PILOT-001 Step 6 consequence recovery",
        "judge_prompt": "recovery_classify_v1",
        "judge_model": getattr(llm, "deployment", None),
        "judge_note": (
            "The judge was not tuned on these eight cases. Its raw output is "
            "preserved per proposition for manual review."
        ),
        "cases": cases,
        "summary": summarise(cases),
    }
    write_json(out_path, payload)
    LOGGER.info("wrote %s", out_path)
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
