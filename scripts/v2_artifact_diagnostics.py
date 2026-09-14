"""Artifact diagnostics for a frozen pair slice.

    python scripts/v2_artifact_diagnostics.py                     # v2
    python scripts/v2_artifact_diagnostics.py --also-v1           # v1 too, for contrast

Three diagnostics, run AFTER the slice is frozen and used only to characterise
it. They never feed back into selection, and the length band is not adjusted on
what they show.

  1. shortest-text-first   gold wins iff the gold is the shorter text
  2. longest-text-first    gold wins iff the gold is the longer text
  3. question-hidden judge a model sees the two hypotheses, shuffled and
                           anonymised, with the question withheld

A tie scores 0.5. A model parse failure is an error, not a wrong answer: it is
excluded and reported separately.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.v2_slice import count_tokens  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import read_jsonl, resolve_path, stable_hash, utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.v2_diagnostics")
JUDGE_PROMPT = "pair_judge_no_question_v1"


def length_heuristic(pairs: List[Dict[str, Any]], *, prefer: str) -> Dict[str, Any]:
    """`prefer='shortest'` picks the shorter text as the gold."""
    wins = ties = 0
    for pair in pairs:
        gold, negative = pair["gold_token_count"], pair["negative_token_count"]
        if gold == negative:
            ties += 1
        elif (gold < negative) == (prefer == "shortest"):
            wins += 1
    total = len(pairs)
    return {
        "prefer": prefer,
        "n_pairs": total,
        "wins": wins,
        "ties": ties,
        "accuracy": round((wins + 0.5 * ties) / total, 4) if total else None,
    }


def question_hidden_judge(
    pairs: List[Dict[str, Any]], *, llm, prompts, seed: int, counterbalance: bool = True
) -> Dict[str, Any]:
    """The no-science floor: can a judge pick the gold from the two texts alone?

    **Every pair is scored in both orders** (gold as option A, then gold as option
    B) and the two outcomes averaged. Without that, the measurement is confounded
    by the judge's position preference, which is large and not constant across
    slices: measured on the single-order runs, this judge chose option A on 61% of
    v2 pairs and **85%** of canonical pairs, and its accuracy split
    0.983 / 0.319 by gold position on canonical. A per-pair shuffle spreads that
    bias around but does not remove it -- it leaves the accuracy depending on how
    the coin happened to land.

    Counterbalanced scoring gives each pair credit 1.0 (right both ways), 0.5
    (order-dependent) or 0.0 (wrong both ways), so position preference cancels
    exactly rather than approximately. `position_preference` and `consistency`
    report what it would have contributed.
    """
    template = prompts.get(JUDGE_PROMPT)
    errors = 0
    rows: List[Dict[str, Any]] = []
    credit = 0.0
    n_chose_a = n_calls = 0
    n_consistent = 0

    def ask(option_a: str, option_b: str) -> Optional[str]:
        messages = [{"role": "user", "content": template.render(
            option_a=option_a, option_b=option_b)}]

        def validate(parsed: Dict[str, Any]) -> None:
            if str(parsed.get("choice", "")).strip().upper() not in ("A", "B"):
                raise ValueError("choice must be A or B")

        response = llm.complete_json(
            messages, purpose="v2.question_hidden_pair_judge",
            prompt_version=JUDGE_PROMPT, validator=validate)
        return str((response.parsed or {}).get("choice", "")).strip().upper()

    for pair in pairs:
        gold = pair["gold_hypothesis"]
        negative = pair["negative_hypothesis"]
        # Which order is presented FIRST is still seeded, so the transcript order
        # is reproducible; with counterbalancing it no longer affects the score.
        rng = random.Random(int(stable_hash("{}:{}".format(seed, pair["pair_id"])), 16))
        gold_first = rng.random() < 0.5
        orders = [(gold, negative, True), (negative, gold, False)]
        if not gold_first:
            orders.reverse()
        if not counterbalance:
            orders = orders[:1]

        outcomes: List[Dict[str, Any]] = []
        failed = False
        for option_a, option_b, gold_is_a in orders:
            try:
                choice = ask(option_a, option_b)
            except (LLMParseError, LLMError) as exc:
                errors += 1
                rows.append({"pair_id": pair["pair_id"], "error": str(exc),
                             "gold_was": "A" if gold_is_a else "B"})
                failed = True
                break
            n_calls += 1
            n_chose_a += int(choice == "A")
            outcomes.append({
                "gold_was": "A" if gold_is_a else "B",
                "choice": choice,
                "chose_gold": (choice == "A") == gold_is_a,
            })
        if failed:
            continue

        pair_credit = sum(o["chose_gold"] for o in outcomes) / len(outcomes)
        credit += pair_credit
        consistent = len({o["chose_gold"] for o in outcomes}) == 1
        n_consistent += int(consistent)
        rows.append({
            "pair_id": pair["pair_id"],
            "orders": outcomes,
            "credit": pair_credit,
            "order_consistent": consistent,
            # Kept for continuity with the single-order runs.
            "gold_was": outcomes[0]["gold_was"],
            "choice": outcomes[0]["choice"],
            "chose_gold": outcomes[0]["chose_gold"],
        })

    scored = len(pairs) - errors
    return {
        "prompt_version": JUDGE_PROMPT,
        "counterbalanced": counterbalance,
        "n_pairs": len(pairs),
        "n_scored": scored,
        "n_errors": errors,
        "n_judge_calls": n_calls,
        "accuracy": round(credit / scored, 4) if scored else None,
        # What the order confound was worth. 0.5 means no position preference.
        "position_preference_chose_a": round(n_chose_a / n_calls, 4) if n_calls else None,
        # Fraction of pairs the judge answered the same way in both orders. A low
        # number means the judge is largely reading position, not content.
        "order_consistency": round(n_consistent / scored, 4) if scored and counterbalance else None,
        # Accuracy restricted to the pairs the judge answered the same way both
        # ways. Separates "reads the text" from "reads the position": the
        # order-flipped pairs each score 0.5 by construction.
        "accuracy_when_consistent": (
            round(sum(r["credit"] for r in rows if r.get("order_consistent"))
                  / max(sum(1 for r in rows if r.get("order_consistent")), 1), 4)
            if counterbalance else None),
        "single_order_accuracy": (
            round(sum(r.get("chose_gold", False) for r in rows if "orders" in r) / scored, 4)
            if scored else None),
        "rows": rows,
    }


def v1_pairs_as_records(config) -> List[Dict[str, Any]]:
    """v1's retained pairs in the same shape, for contrast."""
    from src.benchmark.loader import load_instances
    from src.benchmark.pairs import load_pair_subset

    subset = load_pair_subset(resolve_path(config.dataset.pairs_path))
    instances = {i.id: i for i in load_instances(config)}
    out: List[Dict[str, Any]] = []
    for decision in subset.decisions:
        if not decision.passed:
            continue
        instance = instances.get(decision.instance_id)
        if instance is None:
            continue
        gold = instance.gold_hypothesis.text
        negative = instance.hypothesis(decision.negative_id).text
        out.append({
            "pair_id": "{}::{}".format(decision.instance_id, decision.negative_id),
            "gold_hypothesis": gold, "negative_hypothesis": negative,
            "gold_token_count": count_tokens(gold),
            "negative_token_count": count_tokens(negative),
            "length_ratio": round(count_tokens(negative) / max(1, count_tokens(gold)), 4),
        })
    return out


def summarise_lengths(pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
    import statistics

    ratios = [p["length_ratio"] for p in pairs]
    return {
        "n_pairs": len(pairs),
        "ratio_min": round(min(ratios), 3) if ratios else None,
        "ratio_median": round(statistics.median(ratios), 3) if ratios else None,
        "ratio_max": round(max(ratios), 3) if ratios else None,
        "share_gold_shorter": round(
            sum(1 for p in pairs if p["gold_token_count"] < p["negative_token_count"]) / len(pairs), 4
        ) if pairs else None,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Artifact diagnostics for a frozen pair slice.")
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--pairs", default="benchmark/v2/researchbench_v2_pairs.jsonl")
    parser.add_argument("--out", default="benchmark/v2/v2_artifact_diagnostics.json")
    parser.add_argument("--label", default="v2", help="name for the slice being diagnosed")
    parser.add_argument("--also-v1", action="store_true", help="run the same diagnostics on v1")
    parser.add_argument("--also-v2", action="store_true", help="run the same diagnostics on v2")
    parser.add_argument("--no-judge", action="store_true", help="skip the model diagnostic")
    parser.add_argument("--seed", type=int, default=20260911)
    parser.add_argument("--single-order", action="store_true",
                        help="score each pair in one order only (reproduces the "
                             "position-confounded earlier runs; not recommended)")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    config = load_config(args.config)
    pairs = list(read_jsonl(resolve_path(args.pairs)))
    if not pairs:
        print("no pairs in {}".format(args.pairs))
        return 1

    out_path = resolve_path(args.out)
    event_log = EventLog(out_path.parent / "v2_diagnostics_events.jsonl")
    prompts = PromptLibrary(config.prompts.dir)
    llm = None if args.no_judge else build_llm_client(config.llm, event_log=event_log)

    def diagnose(records: List[Dict[str, Any]], label: str) -> Dict[str, Any]:
        LOGGER.info("%s: %d pairs", label, len(records))
        block = {
            "slice": label,
            "length_profile": summarise_lengths(records),
            "shortest_text_first": length_heuristic(records, prefer="shortest"),
            "longest_text_first": length_heuristic(records, prefer="longest"),
        }
        if llm is not None:
            block["question_hidden_judge"] = question_hidden_judge(
                records, llm=llm, prompts=prompts, seed=args.seed,
                counterbalance=not args.single_order)
        return block

    report = {
        "generated_at": utc_now_iso(),
        "note": (
            "Characterisation only. These results did not influence selection and the "
            "length band was not adjusted on them."
        ),
        "tie_rule": "a tie scores 0.5; a model parse failure is an error, not a wrong answer",
        "llm": {"provider": config.llm.provider,
                "deployment": getattr(llm, "deployment", None) if llm else None},
        args.label: diagnose(pairs, args.label),
    }
    if args.also_v1:
        report["v1"] = diagnose(v1_pairs_as_records(config), "v1")
    if args.also_v2:
        v2_path = resolve_path("benchmark/v2/researchbench_v2_pairs.jsonl")
        report["v2"] = diagnose(list(read_jsonl(v2_path)), "v2")

    write_json(out_path, report)

    for key in (args.label, "v2", "v1"):
        block = report.get(key)
        if not block:
            continue
        print("\n{} — {} pairs".format(key, block["length_profile"]["n_pairs"]))
        print("  gold shorter in            {:.1%}".format(block["length_profile"]["share_gold_shorter"]))
        print("  ratio min/median/max       {}/{}/{}".format(
            block["length_profile"]["ratio_min"], block["length_profile"]["ratio_median"],
            block["length_profile"]["ratio_max"]))
        print("  shortest-text-first        {:.3f}".format(block["shortest_text_first"]["accuracy"]))
        print("  longest-text-first         {:.3f}".format(block["longest_text_first"]["accuracy"]))
        judge = block.get("question_hidden_judge")
        if judge and judge["accuracy"] is not None:
            print("  question-hidden judge      {:.3f}  ({} scored, {} errors)".format(
                judge["accuracy"], judge["n_scored"], judge["n_errors"]))
    print("\nwrote {}\n".format(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
