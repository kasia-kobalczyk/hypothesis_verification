"""Freeze the gold-vs-negative pair subset (screening criterion R2).

    python scripts/build_pair_subset.py                     # all 20 instances
    python scripts/build_pair_subset.py --instances RBV-01  # one instance
    python scripts/build_pair_subset.py --dry-run           # show the workload

Writes `benchmark/dev/pairs_v1.jsonl` (one row per screened pair, PASS and FAIL
alike) plus `benchmark/dev/pairs_manifest_v1.json`.

Resumable: decisions already in the output file are reused, so a re-run only
judges pairs that are missing or previously errored. Pass `--refresh` to rejudge
everything — that changes the frozen benchmark, so it prompts for confirmation.

The judgment sees only (question, gold, negative). It never sees literature,
method outputs, or which pairs any method gets right.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.loader import load_instances  # noqa: E402
from src.benchmark.pairs import (  # noqa: E402
    PAIR_PROMPT_VERSION,
    build_pair_subset,
    load_pair_subset,
    write_pair_subset,
)
from src.common.config import load_config  # noqa: E402
from src.common.io import append_jsonl, resolve_path, utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.build_pair_subset")

DEFAULT_OUT = "benchmark/dev/pairs_v1.jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Freeze the evaluable gold-negative pairs.")
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--instances", nargs="*", default=None)
    parser.add_argument("--prompt-version", default=PAIR_PROMPT_VERSION)
    parser.add_argument("--llm", default=None, choices=["azure", "mock"])
    parser.add_argument("--model", default=None, help="Azure deployment override")
    parser.add_argument("--refresh", action="store_true", help="rejudge pairs already frozen")
    parser.add_argument("--dry-run", action="store_true", help="report the workload and exit")
    parser.add_argument("--yes", action="store_true", help="skip the --refresh confirmation")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.log_level)

    overrides = []
    if args.llm:
        overrides.append("llm.provider={}".format(args.llm))
    if args.model:
        overrides.append("llm.deployment={}".format(args.model))
    config = load_config(args.config, overrides=overrides)

    instances = load_instances(config, instance_ids=args.instances)
    out_path = resolve_path(args.out)
    existing = load_pair_subset(out_path) if out_path.exists() else None

    n_pairs = sum(len(i.hypotheses) - 1 for i in instances)
    frozen = 0 if existing is None or args.refresh else sum(
        1 for d in existing.decisions if d.decision in ("PASS", "FAIL")
    )
    LOGGER.info("%d pair(s) across %d instance(s); %d already frozen", n_pairs, len(instances), frozen)
    if args.dry_run:
        print("would judge {} pair(s) ({} reused)".format(max(0, n_pairs - frozen), frozen))
        return 0

    if args.refresh and existing is not None and not args.yes:
        answer = input(
            "--refresh rejudges {} frozen decision(s) and rewrites the benchmark "
            "subset. Type 'yes' to proceed: ".format(frozen)
        )
        if answer.strip().lower() != "yes":
            print("aborted")
            return 1

    event_log = EventLog(out_path.parent / "pairs_events.jsonl")
    llm = build_llm_client(config.llm, event_log=event_log)
    prompts = PromptLibrary(config.prompts.dir)

    # Stream decisions to a side file as they are made, so a crash mid-run does
    # not lose work even before the frozen file is rewritten.
    progress_path = out_path.parent / "pairs_progress.jsonl"
    seen = {"n": 0}

    def on_decision(decision):
        seen["n"] += 1
        append_jsonl(progress_path, decision.model_dump(mode="json"))
        LOGGER.info(
            "[%d/%d] %s/%s -> %s (%s)",
            seen["n"], n_pairs - frozen, decision.instance_id, decision.negative_id,
            decision.decision, (decision.rationale or "")[:90],
        )

    decisions = build_pair_subset(
        instances,
        llm=llm,
        prompts=prompts,
        existing=None if args.refresh else existing,
        prompt_version=args.prompt_version,
        on_decision=on_decision,
    )

    # Keep decisions for instances this run did not cover.
    if existing is not None:
        covered = {(d.instance_id, d.negative_id) for d in decisions}
        decisions = decisions + [d for d in existing.decisions if d.key not in covered]

    write_pair_subset(out_path, decisions)

    passed = [d for d in decisions if d.passed]
    errors = [d for d in decisions if d.decision == "ERROR"]
    by_instance = {}
    for decision in decisions:
        bucket = by_instance.setdefault(decision.instance_id, {"screened": 0, "retained": 0})
        bucket["screened"] += 1
        bucket["retained"] += int(decision.passed)

    manifest = {
        "name": "ResearchBench verification pair subset",
        "version": Path(args.out).stem,
        "frozen_at": utc_now_iso(),
        "criterion": (
            "R2 applied per pair: the raw negative addresses the same scientific target "
            "as the gold and disagrees with a substantive part of it."
        ),
        "policy": [
            "Every raw gold-negative pair is screened; all passing pairs are retained.",
            "Hypothesis text is never rewritten.",
            "The judgment sees only (question, gold, negative): no literature, no method output.",
        ],
        "prompt": prompts.get(args.prompt_version).record(),
        "llm": {"provider": config.llm.provider, "deployment": getattr(llm, "deployment", None)},
        "n_pairs_screened": len(decisions),
        "n_pairs_retained": len(passed),
        "n_pairs_rejected": sum(1 for d in decisions if d.decision == "FAIL"),
        "n_pairs_error": len(errors),
        "instances_without_any_pair": sorted(
            iid for iid, counts in by_instance.items() if counts["retained"] == 0
        ),
        "per_instance": by_instance,
        "llm_usage": dict(getattr(llm, "usage_totals", {})),
    }
    write_json(out_path.parent / "{}_manifest.json".format(Path(args.out).stem), manifest)

    print(
        "\nscreened {} pair(s): {} retained, {} rejected, {} error(s) -> {}".format(
            len(decisions), len(passed), manifest["n_pairs_rejected"], len(errors), out_path
        )
    )
    if manifest["instances_without_any_pair"]:
        print(
            "instances with no evaluable pair: {}".format(
                ", ".join(manifest["instances_without_any_pair"])
            )
        )
    if errors:
        print("{} pair(s) errored; re-run to retry just those.".format(len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
