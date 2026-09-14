"""CLI entry point (IMPLEMENTATION_SPEC.md §24).

    python -m src.experiments.run --method direct_judge \\
        --dataset data/researchbench_dev20.jsonl --config configs/mvp.yaml

    python -m src.experiments.run --method direct_rag \\
        --dataset data/researchbench_dev20.jsonl --config configs/mvp.yaml \\
        --instances RBV-01 RBV-02

The language-model deployment comes from `--model`, else `llm.deployment` in the
config, else `$LLM_MODEL` in `.env`, else the built-in default `gpt-4.1-kasia`.

Any configuration key can be overridden from the command line with
`--set a.b.c=value`, e.g. `--set literature.top_k=5`.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from src.common.config import load_config
from src.common.io import dumps
from src.common.logging_utils import configure_logging, get_logger
from src.experiments.runner import METHODS, ExperimentRunner

LOGGER = get_logger("experiments.run")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.experiments.run",
        description="Run a hypothesis-verification method over the development slice.",
    )
    parser.add_argument(
        "--method",
        required=True,
        choices=sorted(METHODS),
        help="verification method to run",
    )
    parser.add_argument("--config", default="configs/mvp.yaml", help="YAML configuration file")
    parser.add_argument("--dataset", default=None, help="override dataset.path")
    parser.add_argument("--pairs", action="store_true",
                        help="run over the frozen pair slice (k=2 instances) instead of dev20")
    parser.add_argument("--instances", nargs="*", default=None, help="subset of instance ids (debugging)")
    parser.add_argument("--limit", type=int, default=None, help="run only the first N instances")
    parser.add_argument("--run-id", default=None, help="explicit run id (default: method_timestamp_hash)")
    parser.add_argument("--label", default=None, help="free-text label stored in the manifest")
    parser.add_argument("--refresh-cache", action="store_true", help="ignore cached provider responses")
    parser.add_argument(
        "--offline", action="store_true",
        help="serve literature from cache only; a cache miss is an error, not an empty result",
    )
    parser.add_argument("--llm", default=None, choices=["azure", "mock"], help="override llm.provider")
    parser.add_argument(
        "--model", default=None,
        help="Azure deployment to use (e.g. gpt-4.1-kasia). Overrides $LLM_MODEL; "
             "an `azure/` prefix is accepted and stripped.",
    )
    parser.add_argument("--set", dest="overrides", action="append", default=[],
                        help="config override, e.g. --set literature.top_k=5")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.log_level)

    overrides = list(args.overrides)
    if args.dataset:
        overrides.append("dataset.path={}".format(args.dataset))
    if args.pairs:
        overrides.append("dataset.kind=pairs")
    if args.refresh_cache:
        overrides.append("literature.cache.refresh=true")
    if args.offline:
        overrides.append("literature.cache.offline=true")
    if args.llm:
        overrides.append("llm.provider={}".format(args.llm))
    if args.model:
        overrides.append("llm.deployment={}".format(args.model))

    config = load_config(args.config, overrides=overrides)
    runner = ExperimentRunner(
        config,
        args.method,
        instance_ids=args.instances,
        run_id=args.run_id,
        label=args.label,
        limit=args.limit,
    )
    summary = runner.run()

    print("\nrun: {}".format(runner.run_dir))
    print(dumps(summary.get("metrics", {})))
    if summary.get("n_error") or summary.get("n_skipped"):
        print(
            "instances: ok={} error={} skipped={}".format(
                summary.get("n_ok"), summary.get("n_error"), summary.get("n_skipped")
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
