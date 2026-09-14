"""Pin the exact system a comparison runs against.

    python3 scripts/freeze_system.py --name narrow_v1 --note "..."

Records the resolved config plus the sha of every prompt the method uses, so a
later run can be checked against it rather than assumed identical. Prompts have
changed under this project several times mid-experiment; a hash is cheaper than
remembering.

Writes `benchmark/frozen/<name>.json`. Re-freezing under an existing name is
refused: a freeze that can be silently rewritten is not a freeze.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

METHOD_PROMPTS = [
    "generate_prompt", "edge_assess_v1", "edge_assess_chain_v1",
    "proposition_query_v1",
]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--name", required=True)
    parser.add_argument("--assess-prompt", default=None,
                        help="override evidence.assess_prompt for this frozen arm")
    parser.add_argument("--note", default="")
    parser.add_argument("--out-dir", default="benchmark/frozen")
    args = parser.parse_args(argv)

    out = Path(args.out_dir) / "{}.json".format(args.name)
    if out.exists():
        print("refusing to overwrite {} -- a freeze that can be rewritten is not a freeze"
              .format(out))
        return 1

    config = load_config(args.config)
    prompts = PromptLibrary(config.prompts.dir)
    assess = args.assess_prompt or config.evidence.assess_prompt

    names = [config.graph.generate_prompt, "edge_assess_v1", "edge_assess_chain_v1",
             "proposition_query_v1", assess]
    shas: Dict[str, Any] = {}
    for name in names:
        shas[name] = prompts.get(name).record()

    payload = {
        "name": args.name,
        "frozen_at": utc_now_iso(),
        "note": args.note,
        "evidence_assess_prompt": assess,
        "prompt_shas": shas,
        "config": {
            "graph": config.graph.model_dump(mode="json"),
            "retrieval_query_policy": config.retrieval.query_policy.model_dump(mode="json"),
            "inference": config.inference.model_dump(mode="json"),
            "ordinal_mappings_path": config.ordinal_mappings_path,
            "dedup": config.literature.dedup.model_dump(mode="json"),
            "max_papers_in_prompt": config.baselines.direct_rag.max_papers_in_prompt,
        },
        "ordinal_mappings": json.loads(Path(config.ordinal_mappings_path).read_text())
        if config.ordinal_mappings_path.endswith(".json") else
        {"note": "see {} -- YAML, hashed below".format(config.ordinal_mappings_path)},
        "uncalibrated": ("ordinal mappings are placeholders; absolute posteriors are "
                         "meaningless and only the ordering carries information"),
    }
    write_json(out, payload)
    print("froze {} -> {}".format(args.name, out))
    for name, record in shas.items():
        print("  {:<28} {}".format(name, record["sha256_16"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
