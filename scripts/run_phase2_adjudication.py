"""Phase 2 (AMENDMENT 2): independent prediction adjudication on the fixed tests.

    python3 scripts/run_phase2_adjudication.py

Two predictors solve the SAME isolated task -- one (test, hypothesis) pair at a
time, never shown the competing candidates -- with different scaffolds. The
generator's predictions are provisional and are NOT one of the two: generator vs
predictor is not a reproducibility test, because they solve different tasks under
different information.

Discriminativeness is then recomputed from adjudicated predictions, with
`indeterminate` unable to create discrimination:

    positive vs negative   -> diagnostic
    positive vs neutral    -> diagnostic
    positive vs indeterminate -> NOT diagnostic
"""
from __future__ import annotations

import argparse, collections, itertools, json, sys
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

LOGGER = get_logger("scripts.phase2adj")
PREDICTORS = {"A": "diagnostic_predict_a_v1", "B": "diagnostic_predict_judge_b_v2"}
MAP = {"up_or_appears": "positive_or_present",
       "approximately_unchanged": "neutral_or_no_change",
       "down_or_absent": "negative_or_absent",
       "claim_does_not_determine": "indeterminate"}
LABELS = ["positive_or_present", "neutral_or_no_change", "negative_or_absent", "indeterminate"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="configs/mvp.yaml")
    ap.add_argument("--phase1", default="benchmark/diagnostic/phase1")
    ap.add_argument("--out", default="benchmark/diagnostic/phase2_adjudicated")
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

    files = sorted(p for p in Path(args.phase1).glob("*.json") if p.name != "summary.json")
    texts = {}
    for inst in load_pair_instances(cfg, instance_ids=[p.stem for p in files]):
        texts[inst.id] = {h.id: h.text for h in inst.hypotheses}

    def predict(which, hypothesis_text, test):
        tmpl = prompts.get(PREDICTORS[which])
        messages = [{"role": "user", "content": tmpl.render(
            hypothesis=hypothesis_text, system=test["system"],
            context=test.get("context") or "(not specified)",
            intervention=test["intervention_or_exposure"],
            measured_outcome=test["measured_outcome"],
            baseline=test.get("baseline_or_comparator") or "(not stated in the test)")}]

        def validate(parsed):
            if str(parsed.get("expected_direction", "")).strip() not in MAP:
                raise ValueError("bad expected_direction")

        r = llm.complete_json(messages, purpose="diagnostic.adjudicate_{}".format(which),
                              prompt_version=PREDICTORS[which], validator=validate)
        return MAP[str((r.parsed or {}).get("expected_direction")).strip()]

    rows, tests_out = [], []
    for path in files:
        art = json.loads(path.read_text())
        inst = path.stem
        for test in art["tests"]:
            adj = {}
            for hyp, gen in test["predictions_by_hypothesis"].items():
                got = {}
                for which in ("A", "B"):
                    try:
                        got[which] = predict(which, texts[inst][hyp], test)
                    except (LLMParseError, LLMError) as exc:
                        LOGGER.error("%s/%s/%s/%s: %s", inst, test["test_id"], hyp, which, exc)
                if len(got) == 2:
                    rows.append({"instance": inst, "test_id": test["test_id"],
                                 "hypothesis": hyp, "generator": gen,
                                 "A": got["A"], "B": got["B"]})
                    # adjudicated label only where the two independent predictors agree
                    adj[hyp] = got["A"] if got["A"] == got["B"] else None
            definite = {v for v in adj.values() if v in DISCRIMINATIVE_PREDICTIONS}
            tests_out.append({
                "instance": inst, "test_id": test["test_id"],
                "generator_discriminative": len({
                    v for v in test["predictions_by_hypothesis"].values()
                    if v in DISCRIMINATIVE_PREDICTIONS}) >= 2,
                "adjudicated": adj,
                "adjudicated_discriminative": len(definite) >= 2,
                "unresolved": sum(1 for v in adj.values() if v is None)})
        LOGGER.info("%s done", inst)

    agree = sum(1 for r in rows if r["A"] == r["B"])
    conf = collections.Counter((r["A"], r["B"]) for r in rows)
    gen_d = sum(1 for t in tests_out if t["generator_discriminative"])
    adj_d = sum(1 for t in tests_out if t["adjudicated_discriminative"])
    write_json(out / "summary.json", {
        "generated_at": utc_now_iso(), "phase": "2-adjudicated",
        "predictors": PREDICTORS, "n_pairs": len(rows),
        "predictor_agreement": agree / max(len(rows), 1),
        "confusion_A_vs_B": {"{}|{}".format(a, b): n for (a, b), n in conf.items()},
        "n_tests": len(tests_out),
        "generator_discriminative": gen_d, "adjudicated_discriminative": adj_d,
        "rows": rows, "tests": tests_out})

    print("\nPHASE 2 (adjudicated) — predictor A vs predictor B, isolated task")
    print("  (test, hypothesis) pairs        %d" % len(rows))
    print("  PREDICTOR-VS-PREDICTOR agreement %.3f" % (agree / max(len(rows), 1)))
    print("\n  confusion  rows=A, cols=B")
    print("  %-24s %s" % ("", " ".join("%8s" % l[:8] for l in LABELS)))
    for a in LABELS:
        print("  %-24s %s" % (a, " ".join("%8d" % conf[(a, b)] for b in LABELS)))
    print("\n  usable-test yield")
    print("    by generator predictions    %d/%d (%.0f%%)" % (
        gen_d, len(tests_out), 100 * gen_d / max(len(tests_out), 1)))
    print("    by adjudicated predictions  %d/%d (%.0f%%)" % (
        adj_d, len(tests_out), 100 * adj_d / max(len(tests_out), 1)))
    print("\nwrote %s" % (out / "summary.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
