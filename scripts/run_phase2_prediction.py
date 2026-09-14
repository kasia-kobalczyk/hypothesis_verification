"""Phase 2: independent re-prediction on the FIXED Phase 1 tests.

    python3 scripts/run_phase2_prediction.py --phase1 benchmark/diagnostic/phase1

Judge B sees one (claim, measurement) pair at a time, is never shown the Phase 1
vocabulary or the Phase 1 predictions, and is walked through five steps whose
answers are mapped onto the coarse directions afterwards. That is what decorrelates
it from generation, which predicted all candidates jointly in one call.

Also runs an unrelated-test control: each claim paired with a measurement from a
DIFFERENT instance. A claim should mostly not determine the outcome of a
measurement from another field, so a low 'does not determine' rate there would mean
the predictor is inventing predictions rather than reading the claim.
"""
from __future__ import annotations

import argparse, collections, json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.loader import load_pair_instances  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.phase2")
PROMPT = "diagnostic_predict_judge_b_v2"
MAP = {"up_or_appears": "positive_or_present",
       "approximately_unchanged": "neutral_or_no_change",
       "down_or_absent": "negative_or_absent",
       "claim_does_not_determine": "indeterminate"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="configs/mvp.yaml")
    ap.add_argument("--phase1", default="benchmark/diagnostic/phase1")
    ap.add_argument("--out", default="benchmark/diagnostic/phase2")
    ap.add_argument("--controls", type=int, default=40)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    configure_logging(args.log_level)

    out = Path(args.out)
    if out.exists():
        print("refusing to overwrite {}".format(out)); return 1
    out.mkdir(parents=True)

    cfg = load_config(args.config)
    prompts = PromptLibrary(cfg.prompts.dir)
    template = prompts.get(PROMPT)
    log = EventLog(out / "events.jsonl")
    llm = build_llm_client(cfg.llm, event_log=log)

    files = sorted(p for p in Path(args.phase1).glob("*.json") if p.name != "summary.json")
    texts = {}   # instance -> hypothesis_id -> text
    for inst in load_pair_instances(cfg, instance_ids=[p.stem for p in files]):
        texts[inst.id] = {h.id: h.text for h in inst.hypotheses}

    def ask(hypothesis_text, test):
        messages = [{"role": "user", "content": template.render(
            hypothesis=hypothesis_text, system=test["system"],
            context=test.get("context") or "(not specified)",
            intervention=test["intervention_or_exposure"],
            measured_outcome=test["measured_outcome"],
            baseline=test.get("baseline_or_comparator") or "(not stated in the test)")}]

        def validate(parsed):
            if str(parsed.get("expected_direction", "")).strip() not in MAP:
                raise ValueError("bad expected_direction")

        resp = llm.complete_json(messages, purpose="diagnostic.predict_b",
                                 prompt_version=PROMPT, validator=validate)
        p = resp.parsed or {}
        return MAP[str(p.get("expected_direction")).strip()], p

    rows, pairs = [], []
    all_tests = []
    for path in files:
        art = json.loads(path.read_text())
        inst = path.stem
        for test in art["tests"]:
            all_tests.append((inst, test))
            for hyp, phase1 in test["predictions_by_hypothesis"].items():
                try:
                    b, raw = ask(texts[inst][hyp], test)
                except (LLMParseError, LLMError) as exc:
                    LOGGER.error("%s/%s/%s: %s", inst, test["test_id"], hyp, exc)
                    continue
                pairs.append({"instance": inst, "test_id": test["test_id"],
                              "hypothesis": hyp, "a": phase1, "b": b,
                              "b_bears": bool(raw.get("claim_bears_on_this_quantity"))})
        LOGGER.info("%s: done", inst)

    # unrelated-test control
    rng = random.Random(20260913)
    controls = []
    for _ in range(args.controls):
        (i1, t1), (i2, _t2) = rng.sample(all_tests, 2)
        if i1 == i2:
            continue
        hyp = rng.choice(sorted(texts[i2]))
        try:
            b, raw = ask(texts[i2][hyp], t1)
        except (LLMParseError, LLMError):
            continue
        controls.append({"claim_from": i2, "test_from": i1, "b": b,
                         "b_bears": bool(raw.get("claim_bears_on_this_quantity"))})

    agree = sum(1 for p in pairs if p["a"] == p["b"])
    conf = collections.Counter((p["a"], p["b"]) for p in pairs)
    labels = ["positive_or_present", "neutral_or_no_change", "negative_or_absent", "indeterminate"]
    write_json(out / "summary.json", {
        "generated_at": utc_now_iso(), "phase": 2, "n_pairs": len(pairs),
        "exact_direction_agreement": agree / max(len(pairs), 1),
        "confusion": {"{}|{}".format(a, b): n for (a, b), n in conf.items()},
        "controls": {"n": len(controls),
                     "indeterminate_rate": sum(1 for c in controls if c["b"] == "indeterminate") / max(len(controls), 1),
                     "bears_rate": sum(1 for c in controls if c["b_bears"]) / max(len(controls), 1)},
        "pairs": pairs, "control_rows": controls})

    print("\nPHASE 2 — prediction reproducibility")
    print("  (test, hypothesis) pairs      %d" % len(pairs))
    print("  exact direction agreement     %.3f" % (agree / max(len(pairs), 1)))
    print("\n  confusion  rows=generation, cols=judge B")
    print("  %-24s %s" % ("", " ".join("%8s" % l[:8] for l in labels)))
    for a in labels:
        print("  %-24s %s" % (a, " ".join("%8d" % conf[(a, b)] for b in labels)))
    print("\n  unrelated-test control: n=%d  'claim does not determine' %.2f  'bears on quantity' %.2f"
          % (len(controls),
             sum(1 for c in controls if c["b"] == "indeterminate") / max(len(controls), 1),
             sum(1 for c in controls if c["b_bears"]) / max(len(controls), 1)))
    print("\nwrote %s" % (out / "summary.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
