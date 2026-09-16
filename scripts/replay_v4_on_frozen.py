"""Stage A of BENCH-GRAPH-V4-DEV-001: apply the v4 layer to the FROZEN v3 pilot.

Same propositions, same retrieved records, same evidence labels as
`pilot_explanatory_001`; only the comparative layer differs. That makes v3 and v4
directly comparable node by node, and lets the D045/D046 development labels, which
exist only for the frozen v3 propositions, be used to check v4's behaviour.

LLM calls: one prediction-state call per proposition, and one construct-match call
per proposition with informative evidence. No generation, no query writing, no
retrieval: the construct-match judge is shown the exact record text the v3 evidence
assessor saw, cut from the frozen rendered prompts and renumbered as the live renderer
would number the cited subset.

Output (gitignored, like every run):
    runs/<replay-id>/manifest.json
    runs/<replay-id>/events.jsonl
    runs/<replay-id>/instances/<case>/discrimination.json
    runs/<replay-id>/summary.json

Usage:
    python scripts/replay_v4_on_frozen.py --replay-id v4_replay_pilot_iter01 --notes "..."
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_review_packet as bp  # noqa: E402
from src.benchmark.presentation import Presentation, PresentedHypothesis  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.io import write_json  # noqa: E402
from src.common.logging_utils import EventLog, get_logger  # noqa: E402
from src.experiments.runner import _git_state  # noqa: E402
from src.inference.parameters import load_ordinal_mappings  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402
from src.evidence.construct_match import CONSTRUCT_PROMPT  # noqa: E402
from src.graph.prediction_state import STATE_PROMPT  # noqa: E402
from src.methods.consequence_graph_v4 import METHOD_VERSION, run_v4_layer  # noqa: E402

LOGGER = get_logger("v4.replay")
CONFIG = ROOT / "configs" / "v4_dev_explanatory.yaml"


def presentation_from_frozen(inst: Path) -> Presentation:
    instance = bp._load(inst / "input.json")
    pres = bp._load(inst / "presentation.json")
    texts = {h["id"]: h["text"] for h in instance["hypotheses"]}
    id_to_label = {v: k for k, v in pres["label_to_hypothesis_id"].items()}
    items = [PresentedHypothesis(id_to_label[h], h, texts[h], False) for h in pres["presentation_order"]]
    return Presentation(instance["id"], items, seed_key=pres["seed_key"], order=pres["order"])


def frozen_records(inst: Path, graph_record) -> dict:
    """node_id -> list of (paper_id, exact block text) as shown to the v3 assessor."""
    text_to_node = {n["text"]: n["id"] for n in graph_record["nodes"]}
    calls = bp.assessor_calls(bp._events(inst / "events.jsonl"), text_to_node)
    return {nid: [(b["paper_id"], b["exact_text_shown_to_assessor"])
                  for b in bp.split_literature(call["messages"][-1]["content"])]
            for nid, call in calls.items()}


def renumber(blocks) -> str:
    return bp.RECORD_SEPARATOR.join(re.sub(r"^\[\d+\] ", "[{}] ".format(i), text, count=1)
                                    for i, (_, text) in enumerate(blocks, start=1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-id", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--cases", nargs="*", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    out = ROOT / "runs" / args.replay_id
    if out.exists() and not args.force:
        LOGGER.error("%s exists; pass --force to overwrite", out)
        return 2
    out.mkdir(parents=True, exist_ok=True)

    config = load_config(str(CONFIG))
    mappings = load_ordinal_mappings(str(ROOT / "configs" / "ordinal_mappings.yaml"))
    prompts = PromptLibrary(config.prompts.dir)
    llm = build_llm_client(config.llm)
    llm.event_log = EventLog(out / "events.jsonl")

    write_json(out / "manifest.json", OrderedDict([
        ("replay_id", args.replay_id),
        ("stage", "A: v4 layer on frozen v3 pilot artifacts"),
        ("method_version", METHOD_VERSION),
        ("source_archive_sha256", (bp.PRESERVED / "pilot_explanatory_001.tar.gz.sha256").read_text().split()[0]),
        ("git", _git_state()),
        ("prompts", prompts.manifest([STATE_PROMPT, CONSTRUCT_PROMPT])),
        ("llm", {"provider": config.llm.provider, "deployment": getattr(llm, "deployment", None),
                 "temperature": config.llm.temperature, "seed": config.llm.seed}),
        ("notes", args.notes),
    ]))

    summary = OrderedDict()
    with tempfile.TemporaryDirectory() as tmp:
        run = bp.extract_verified(Path(tmp)) / "run"
        for inst in sorted(p for p in (run / "instances").iterdir() if p.is_dir()):
            if args.cases and inst.name not in args.cases:
                continue
            graph_record = bp._load(inst / "graph.json")
            evidence = bp._load(inst / "evidence.json")["by_node"]
            frozen_scores = bp._load(inst / "scores.json")
            shown = frozen_records(inst, graph_record)

            def records_for(node_id, cited, shown=shown):
                blocks = shown.get(node_id) or []
                chosen = [b for b in blocks if b[0] in set(cited)] if cited else blocks
                return renumber(chosen) if chosen else None

            layer = run_v4_layer(
                instance_id=inst.name, presentation=presentation_from_frozen(inst), graph_record=graph_record,
                evidence_by_node=evidence, records_for=records_for, llm=llm, prompts=prompts, mappings=mappings,
                multi_parent_rule=frozen_scores["inference"]["multi_parent_rule"],
                parent_false_baseline=frozen_scores["inference"]["parent_false_baseline"],
                max_workers=args.workers)
            layer["v3_frozen_scores"] = frozen_scores["scores"]
            write_json(out / "instances" / inst.name / "discrimination.json", layer)
            summary[inst.name] = OrderedDict([
                ("v3_frozen_scores", frozen_scores["scores"]), ("v4_scores", layer["scores"]),
                ("summary", layer["summary"]), ("n_errors", len(layer["errors"]))])
            LOGGER.info("%s: v3 %s -> v4 %s | %s", inst.name,
                        {k: round(v, 3) for k, v in frozen_scores["scores"].items()},
                        {k: round(v, 3) for k, v in layer["scores"].items()},
                        {k: v for k, v in layer["summary"].items() if v})
    write_json(out / "summary.json", OrderedDict([
        ("cases", summary), ("llm_calls", getattr(llm, "n_calls", None)),
        ("llm_usage", dict(getattr(llm, "usage_totals", {}))), ("llm_parse_failures", getattr(llm, "n_parse_failures", None))]))
    print(json.dumps({c: {"v3": v["v3_frozen_scores"], "v4": v["v4_scores"], "errors": v["n_errors"]}
                      for c, v in summary.items()}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
