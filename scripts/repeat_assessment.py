"""Repeated evidence assessment under nuisance variation.

    python3 scripts/repeat_assessment.py --run <run> --repeats 3

Re-runs the FROZEN narrow assessor on the saved node/paper bundles, changing only
the order records are presented in. Order is a nuisance factor: it must not change
the scientific answer. No retrieval, no graph regeneration, no prompt change.

Produces, per node, repeated labels s_v^(1..R). Two questions:

  1. node instability            P(s_v^(r) != s_v^(r'))
  2. do changes CO-MOVE within a row -- if one repeat is more supportive on X1, is
     it also more supportive on X2, X3 from the same row?

Within-row covariance materially above cross-row covariance is direct evidence for
evidence-channel dependence, which is currently only a hypothesis (the family
ablation ruled out proposition-structure dependence, and driving-paper overlap is
only 12-19%).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.inference.parameters import EVIDENCE_LABELS, normalise_evidence_label  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.repeat_assessment")


def render(papers, max_papers):
    blocks = []
    for p in papers[:max_papers]:
        if not (p.get("abstract") or "").strip():
            continue
        blocks.append("id: {}\ntitle: {}\nyear: {}\nvenue: {}\nabstract: {}".format(
            p.get("paper_id") or p.get("id"), p.get("title"), p.get("year"),
            p.get("venue"), p.get("abstract")))
    return "\n\n".join(blocks)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--run", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", required=True)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    out_path = Path(args.out)
    if out_path.exists():
        print("refusing to overwrite {}".format(out_path))
        return 1

    cfg = load_config(args.config)
    prompts = PromptLibrary(cfg.prompts.dir)
    template = prompts.get(cfg.evidence.assess_prompt)
    llm = build_llm_client(cfg.llm, event_log=EventLog(
        Path(args.run) / "repeat_assessment_events.jsonl"))
    max_papers = cfg.baselines.direct_rag.max_papers_in_prompt

    rows: List[Dict[str, Any]] = []
    for inst in sorted((Path(args.run) / "instances").glob("*")):
        if not (inst / "retrieval.json").exists():
            continue
        retrieval = json.loads((inst / "retrieval.json").read_text())["by_node"]
        evidence = json.loads((inst / "evidence.json").read_text())["by_node"]
        node_labels: Dict[str, List[Optional[str]]] = {}
        for node_id, rec in sorted(evidence.items()):
            papers = (retrieval.get(node_id) or {}).get("papers_shown", [])
            labels: List[Optional[str]] = []
            for r in range(args.repeats):
                shuffled = list(papers)
                # nuisance variation ONLY: the order records are presented in
                random.Random("{}:{}:{}".format(inst.name, node_id, r)).shuffle(shuffled)
                lit = render(shuffled, max_papers)
                if not lit:
                    labels.append("no_evidence")
                    continue
                messages = [{"role": "user", "content": template.render(
                    proposition=rec.get("text", ""), literature=lit,
                    labels=", ".join(EVIDENCE_LABELS))}]

                def validate(parsed):
                    if normalise_evidence_label(parsed.get("evidence_label")) is None:
                        raise ValueError("bad evidence_label")

                try:
                    resp = llm.complete_json(
                        messages, purpose="repeat.evidence_assess",
                        prompt_version=cfg.evidence.assess_prompt, validator=validate)
                    labels.append(normalise_evidence_label(
                        (resp.parsed or {}).get("evidence_label")))
                except (LLMParseError, LLMError) as exc:
                    LOGGER.error("%s/%s r%d: %s", inst.name, node_id, r, exc)
                    labels.append(None)
            node_labels[node_id] = labels
        rows.append({"instance": inst.name, "labels": node_labels,
                     "original": {k: (v.get("assessment") or {}).get("evidence_label")
                                  for k, v in evidence.items()}})
        LOGGER.info("%s: %d node(s) x %d repeat(s)", inst.name, len(node_labels), args.repeats)

    write_json(out_path, {"generated_at": utc_now_iso(), "run": args.run,
                          "repeats": args.repeats,
                          "assess_prompt": cfg.evidence.assess_prompt,
                          "nuisance_varied": "record presentation order only",
                          "rows": rows})
    print("wrote {}".format(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
