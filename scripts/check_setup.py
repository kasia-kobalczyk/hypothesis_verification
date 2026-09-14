"""Pre-flight check: credentials, connectivity, dataset, frozen cutoffs.

    python scripts/check_setup.py            # everything except a paid LLM call
    python scripts/check_setup.py --llm      # also make one tiny Azure call

Exits non-zero if anything required for a real run is missing, so it can gate a
long experiment before it burns API budget.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.loader import load_instances  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.env import (  # noqa: E402
    AZURE_BASE_VARS,
    AZURE_KEY_VARS,
    AZURE_VERSION_VARS,
    CROSSREF_MAILTO_VARS,
    S2_KEY_VARS,
    get_env,
)
from src.common.logging_utils import configure_logging  # noqa: E402
from src.llm.client import resolve_deployment  # noqa: E402

OK, WARN, FAIL = "  ok  ", " warn ", " FAIL "


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check the environment before a run.")
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--llm", action="store_true", help="make one small Azure OpenAI call")
    parser.add_argument("--literature", action="store_true", help="issue one Semantic Scholar query")
    args = parser.parse_args(argv)
    configure_logging("WARNING")

    failures = 0
    lines = []

    def report(status, what, detail=""):
        nonlocal failures
        if status is FAIL:
            failures += 1
        lines.append("[{}] {:<34} {}".format(status, what, detail))

    config = load_config(args.config)
    report(OK, "config", config.source_path)

    # -- dataset + frozen cutoffs -------------------------------------- #
    try:
        instances = load_instances(config)
        report(OK, "dataset", "{} instances".format(len(instances)))
        without = [i.id for i in instances if not i.has_cutoff]
        ambiguous = [i.id for i in instances if i.cutoff_ambiguous]
        if without:
            report(FAIL, "frozen cutoffs", "missing for {}".format(", ".join(without)))
        else:
            report(OK, "frozen cutoffs", "all {} resolved".format(len(instances)))
        if ambiguous:
            report(WARN, "cutoffs needing review", ", ".join(ambiguous))
    except Exception as exc:
        report(FAIL, "dataset", str(exc))

    # -- credentials ---------------------------------------------------- #
    report(OK if get_env(*AZURE_KEY_VARS) else FAIL, "AZURE_API_KEY", "set" if get_env(*AZURE_KEY_VARS) else "missing")
    report(OK if get_env(*AZURE_BASE_VARS) else FAIL, "AZURE_API_BASE", get_env(*AZURE_BASE_VARS) or "missing")
    report(OK, "AZURE_API_VERSION", get_env(*AZURE_VERSION_VARS, default="2024-05-01-preview (default)"))
    deployment, source = resolve_deployment(config.llm)
    report(OK, "llm deployment", "{} (from {})".format(deployment, source))
    report(
        OK if get_env(*S2_KEY_VARS) else WARN,
        "S2_API_KEY",
        "set" if get_env(*S2_KEY_VARS) else "missing: expect HTTP 429 from Semantic Scholar",
    )
    report(OK if get_env(*CROSSREF_MAILTO_VARS) else WARN, "CROSSREF_MAILTO",
           get_env(*CROSSREF_MAILTO_VARS) or "unset (polite pool disabled)")

    # -- connectivity --------------------------------------------------- #
    from src.literature.crossref import CrossrefClient

    try:
        message = CrossrefClient(config.crossref).get_work("10.1038/s41586-024-07098-5")
        report(OK if message else FAIL, "crossref", "reachable" if message else "DOI lookup returned nothing")
    except Exception as exc:
        report(FAIL, "crossref", str(exc))

    if args.literature:
        from src.benchmark.loader import build_cutoff_registry
        from src.literature.service import build_literature_service

        try:
            instances = load_instances(config)
            service = build_literature_service(config, build_cutoff_registry(instances))
            papers = service.search_literature("protein folding kinetics", instances[0].id, top_k=3)
            report(OK, "semantic scholar", "{} eligible result(s)".format(len(papers)))
        except Exception as exc:
            report(FAIL, "semantic scholar", "{}: {}".format(type(exc).__name__, exc))

    if args.llm:
        from src.llm.client import build_llm_client

        try:
            client = build_llm_client(config.llm)
            response = client.complete_json(
                [{"role": "user", "content": 'Reply with the JSON object {"ok": true} and nothing else.'}],
                purpose="setup_check",
            )
            report(OK, "azure openai", "{} ({} tokens)".format(response.model, response.usage.get("total_tokens")))
        except Exception as exc:
            report(FAIL, "azure openai", "{}: {}".format(type(exc).__name__, exc))

    print("\n".join(lines))
    print("\n{} check(s) failed".format(failures) if failures else "\nall checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
