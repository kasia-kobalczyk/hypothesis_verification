"""Phase 1: generate diagnostic tests on development instances. No literature.

    python3 scripts/run_phase1_generation.py --instances RBV2-0050-N04 ... --out <dir>

Generation only: no retrieval, no observation, no scoring. Produces the Phase 1
diagnostics the frozen design asks for -- how many tests are generated, how many are
empirically observable, how many discriminative, the prediction distribution, and
why tests were rejected.
"""
from __future__ import annotations

import argparse, collections, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.loader import load_pair_instances  # noqa: E402
from src.benchmark.presentation import build_presentation  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.diagnostics.generate import generate_tests  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.phase1")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="configs/mvp.yaml")
    ap.add_argument("--instances", nargs="+", required=True)
    ap.add_argument("--n-tests", type=int, default=6)
    ap.add_argument("--out", default="benchmark/diagnostic/phase1")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    configure_logging(args.log_level)

    out = Path(args.out)
    if out.exists():
        print("refusing to overwrite {}".format(out))
        return 1
    out.mkdir(parents=True)

    cfg = load_config(args.config)
    prompts = PromptLibrary(cfg.prompts.dir)
    log = EventLog(out / "events.jsonl")
    llm = build_llm_client(cfg.llm, event_log=log)

    instances = load_pair_instances(cfg, instance_ids=args.instances)
    rows, preds, rejects = [], collections.Counter(), collections.Counter()
    for inst in instances:
        presentation = build_presentation(inst, cfg.run)
        try:
            test_set, art = generate_tests(
                instance_id=inst.id, question=inst.question, presentation=presentation,
                config=cfg, llm=llm, prompts=prompts, n_tests=args.n_tests, event_log=log)
        except (LLMParseError, LLMError) as exc:
            LOGGER.error("%s: generation failed: %s", inst.id, exc)
            rows.append({"instance": inst.id, "error": str(exc)})
            continue
        write_json(out / "{}.json".format(inst.id), art)
        for t in test_set.tests:
            for v in t.predictions_by_hypothesis.values():
                preds[v] += 1
            if t.rejected_reason:
                rejects[t.rejected_reason.split(":")[0].split(" for ")[0]] += 1
        rows.append({"instance": inst.id, **test_set.stats()})
        LOGGER.info("%s done", inst.id)

    ok = [r for r in rows if "error" not in r]
    total = sum(r["n_generated"] for r in ok)
    summary = {
        "generated_at": utc_now_iso(), "phase": 1,
        "design_freeze": json.loads(
            Path("benchmark/frozen/diagnostic_design_freeze.json").read_text())["sha256_16"],
        "n_instances": len(rows), "n_failed": len(rows) - len(ok),
        "n_tests_generated": total,
        "n_empirically_observable": sum(r["n_empirically_observable"] for r in ok),
        "n_discriminative": sum(r["n_discriminative"] for r in ok),
        "n_usable": sum(r["n_usable"] for r in ok),
        "prediction_distribution": dict(preds),
        "rejection_reasons": dict(rejects),
        "per_instance": rows,
    }
    write_json(out / "summary.json", summary)

    print("\nPHASE 1 — diagnostic test generation (no literature)")
    print("  instances            %d (%d failed)" % (len(rows), len(rows) - len(ok)))
    print("  tests generated      %d" % total)
    print("  empirically observable %d (%.0f%%)" % (
        summary["n_empirically_observable"], 100 * summary["n_empirically_observable"] / max(total, 1)))
    print("  discriminative       %d (%.0f%%)" % (
        summary["n_discriminative"], 100 * summary["n_discriminative"] / max(total, 1)))
    print("  usable (both)        %d (%.0f%%)" % (
        summary["n_usable"], 100 * summary["n_usable"] / max(total, 1)))
    print("  prediction distribution:")
    for k, v in preds.most_common():
        print("    %-24s %4d (%.0f%%)" % (k, v, 100 * v / max(sum(preds.values()), 1)))
    if rejects:
        print("  rejection reasons:")
        for k, v in rejects.most_common():
            print("    %-44s %d" % (k, v))
    print("\nwrote %s" % (out / "summary.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
