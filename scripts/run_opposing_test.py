"""The one targeted experiment: can ANY measurement make these claims disagree?

    python3 scripts/run_opposing_test.py

Same 10 development pairs, no retrieval. A narrowed generator is asked only for
measurements where BOTH claims determine an outcome and the outcomes conflict, and
is explicitly told that returning zero is correct. It does NOT assign the direction
labels -- the two independent predictors do that, exactly as in Phase 2.

Interpretation, fixed before running:
  many validated opposing tests  -> Phase 1 was badly formulated; revise generation
  essentially zero               -> these candidate pairs are not competing
                                    predictive hypotheses, and the problem is the
                                    benchmark's candidate construction
"""
from __future__ import annotations

import argparse, collections, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.loader import load_pair_instances  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.diagnostics.schema import DISCRIMINATIVE_PREDICTIONS  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.opposing")
GEN = "diagnostic_test_opposing_v1"
PREDICTORS = {"A": "diagnostic_predict_a_v1", "B": "diagnostic_predict_judge_b_v2"}
MAP = {"up_or_appears": "positive_or_present",
       "approximately_unchanged": "neutral_or_no_change",
       "down_or_absent": "negative_or_absent",
       "claim_does_not_determine": "indeterminate"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="configs/mvp.yaml")
    ap.add_argument("--phase1", default="benchmark/diagnostic/phase1")
    ap.add_argument("--n-tests", type=int, default=5)
    ap.add_argument("--out", default="benchmark/diagnostic/opposing")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    configure_logging(args.log_level)
    out = Path(args.out)
    if out.exists():
        print("refusing to overwrite {}".format(out)); return 1
    out.mkdir(parents=True)

    cfg = load_config(args.config)
    prompts = PromptLibrary(cfg.prompts.dir)
    llm = build_llm_client(cfg.llm, event_log=EventLog(out / "events.jsonl"))
    ids = [p.stem for p in sorted(Path(args.phase1).glob("*.json")) if p.name != "summary.json"]
    instances = load_pair_instances(cfg, instance_ids=ids)

    gen_t = prompts.get(GEN)
    rows, per_inst = [], []
    for inst in instances:
        gold = [h for h in inst.hypotheses if h.gold][0]
        neg = [h for h in inst.hypotheses if not h.gold][0]
        messages = [{"role": "user", "content": gen_t.render(
            question=inst.question, claim_1=gold.text, claim_2=neg.text,
            n_tests=args.n_tests)}]

        def validate(parsed):
            if "tests" not in parsed:
                raise ValueError("missing 'tests'")

        try:
            r = llm.complete_json(messages, purpose="opposing.generate",
                                  prompt_version=GEN, validator=validate)
        except (LLMParseError, LLMError) as exc:
            LOGGER.error("%s: %s", inst.id, exc); continue
        parsed = r.parsed or {}
        tests = parsed.get("tests") or []
        LOGGER.info("%s: generator proposed %d (no_conflict_found=%s)",
                    inst.id, len(tests), parsed.get("no_conflict_found"))

        adjudicated = []
        for i, t in enumerate(tests, start=1):
            preds = {}
            for hyp, text in ((gold.id, gold.text), (neg.id, neg.text)):
                got = {}
                for which, pname in PREDICTORS.items():
                    tmpl = prompts.get(pname)
                    m = [{"role": "user", "content": tmpl.render(
                        hypothesis=text, system=t.get("system", ""),
                        context=t.get("context") or "(not specified)",
                        intervention=t.get("intervention_or_exposure", ""),
                        measured_outcome=t.get("measured_outcome", ""),
                        baseline=t.get("baseline_or_comparator") or "(not stated)")}]

                    def v(parsed2):
                        if str(parsed2.get("expected_direction", "")).strip() not in MAP:
                            raise ValueError("bad direction")
                    try:
                        rr = llm.complete_json(m, purpose="opposing.predict_" + which,
                                               prompt_version=pname, validator=v)
                        got[which] = MAP[str((rr.parsed or {}).get("expected_direction")).strip()]
                    except (LLMParseError, LLMError) as exc:
                        LOGGER.error("%s T%d %s %s: %s", inst.id, i, hyp, which, exc)
                if len(got) == 2:
                    preds[hyp] = got["A"] if got["A"] == got["B"] else None
                    rows.append({"instance": inst.id, "test": i, "hypothesis": hyp,
                                 "A": got["A"], "B": got["B"]})
            definite = {v for v in preds.values() if v in DISCRIMINATIVE_PREDICTIONS}
            adjudicated.append({"test": i, "preds": preds,
                                "opposing": len(definite) >= 2,
                                "measured_outcome": t.get("measured_outcome", "")})
        write_json(out / "{}.json".format(inst.id),
                   {"proposed": tests, "no_conflict_found": parsed.get("no_conflict_found"),
                    "reason_if_none": parsed.get("reason_if_none"),
                    "adjudicated": adjudicated, "call": r.record(include_messages=messages)})
        per_inst.append({"instance": inst.id, "n_proposed": len(tests),
                         "n_opposing": sum(1 for a in adjudicated if a["opposing"]),
                         "declared_no_conflict": bool(parsed.get("no_conflict_found"))})

    tot_p = sum(p["n_proposed"] for p in per_inst)
    tot_o = sum(p["n_opposing"] for p in per_inst)
    shapes = collections.Counter()
    for p in per_inst:
        art = json.loads((out / "{}.json".format(p["instance"])).read_text())
        for a in art["adjudicated"]:
            shapes[" vs ".join(sorted(
                (v or "unresolved").split("_")[0] for v in a["preds"].values()))] += 1
    write_json(out / "summary.json", {
        "generated_at": utc_now_iso(), "experiment": "targeted opposing-prediction generation",
        "n_instances": len(per_inst), "n_proposed": tot_p, "n_validated_opposing": tot_o,
        "shapes": dict(shapes), "per_instance": per_inst, "rows": rows})

    print("\nTARGETED OPPOSING-PREDICTION TEST (no retrieval)")
    print("  instances                       %d" % len(per_inst))
    print("  measurements proposed           %d" % tot_p)
    print("  instances declaring no conflict %d" % sum(1 for p in per_inst if p["declared_no_conflict"]))
    print("  VALIDATED opposing tests        %d  (%.2f per pair)" % (
        tot_o, tot_o / max(len(per_inst), 1)))
    print("\n  adjudicated shapes:")
    for k, v in shapes.most_common():
        print("    %-44s %d" % (k, v))
    print("\n  per instance:")
    for p in per_inst:
        print("    %-14s proposed %d -> validated opposing %d%s" % (
            p["instance"][-8:], p["n_proposed"], p["n_opposing"],
            "  (declared no conflict)" if p["declared_no_conflict"] else ""))
    print("\nwrote %s" % (out / "summary.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
