"""Empirical leak audit of a finished pilot run (BENCH-GRAPH-PILOT-001, Step 3).

The tests in `tests/test_explanatory_hidden_isolation.py` and
`tests/test_explanatory_cutoff_enforcement.py` prove that leakage *cannot* happen,
by construction and against an adversarial provider. This script is the other half:
it checks what actually *did* happen, by reading every byte the run sent to the
model and every paper it retrieved.

The two are not redundant. The tests reason about the code; this reasons about the
artifacts. A route nobody modelled -- a cached record from an earlier run, a
provider returning a paper with a wrong date, a prompt assembled somewhere
unexpected -- shows up here and nowhere else.

Three things are checked, per case, against the run's own logs:

1. no hidden annotation (resolver DOI, resolver identity, reference discriminator,
   resolving observation, resolution summary) appears in any message sent to the
   model;
2. no retrieved paper postdates the case's cutoff;
3. the resolver's DOIs appear nowhere in the retrieval record.

Usage:
    python scripts/audit_pilot_leakage.py --run runs/pilot_explanatory_001
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import resolve_path, write_json
from src.common.logging_utils import get_logger

LOGGER = get_logger("pilot.leak_audit")

HIDDEN_PATH = Path("benchmark/explanatory/cases_hidden.json")
VISIBLE_PATH = Path("benchmark/explanatory/cases_visible.jsonl")

# A phrase this long, reproduced exactly, is not coincidence.
WINDOW_WORDS = 8


def _walk_strings(node: Any) -> List[str]:
    out: List[str] = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for key, value in node.items():
            out.append(str(key))
            out.extend(_walk_strings(value))
    elif isinstance(node, (list, tuple)):
        for item in node:
            out.extend(_walk_strings(item))
    return out


def _dois(case: Dict[str, Any]) -> Set[str]:
    found: Set[str] = set()
    for text in _walk_strings(case):
        found.update(m.lower() for m in re.findall(r"10\.\d{4,9}/[^\s\"'),;]+", text))
    return found


def _windows(text: str) -> Set[str]:
    words = text.lower().split()
    if len(words) <= WINDOW_WORDS:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + WINDOW_WORDS])
            for i in range(len(words) - WINDOW_WORDS + 1)}


def _hidden_phrases(case: Dict[str, Any]) -> Set[str]:
    """Distinctive multi-word phrases from the answer key."""
    phrases: Set[str] = set()
    for item in case.get("reference_discriminators") or []:
        phrases |= _windows(item)
    for item in case.get("resolving_observations") or []:
        phrases |= _windows(item)
    summary = ((case.get("resolution") or {}).get("summary") or "")
    phrases |= _windows(summary)
    return {p for p in phrases if p}


def _model_text(events_path: Path) -> str:
    """Every byte the run sent to or received from the model, as one blob."""
    chunks: List[str] = []
    if not events_path.exists():
        return ""
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        for message in event.get("messages") or []:
            chunks.append(str(message.get("content") or ""))
        if event.get("response_text"):
            chunks.append(str(event["response_text"]))
    return "\n".join(chunks).lower()


def _retrieved_papers(instance_dir: Path) -> Iterable[Dict[str, Any]]:
    path = instance_dir / "retrieval.json"
    if not path.exists():
        return []
    retrieval = json.loads(path.read_text(encoding="utf-8"))
    for node in (retrieval.get("by_node") or {}).values():
        for query in node.get("queries") or []:
            for paper in query.get("eligible") or []:
                yield paper


def audit_case(instance_dir: Path, case: Dict[str, Any], cutoff: date) -> Dict[str, Any]:
    blob = _model_text(instance_dir / "events.jsonl")

    doi_hits = sorted(d for d in _dois(case) if d in blob)
    phrase_hits = sorted(p for p in _hidden_phrases(case) if p in blob)

    post_cutoff: List[Dict[str, Any]] = []
    resolver_dois = _dois(case)
    resolver_in_retrieval: List[Dict[str, Any]] = []
    n_papers = 0
    for paper in _retrieved_papers(instance_dir):
        n_papers += 1
        raw = paper.get("publication_date") or ""
        when = None
        try:
            when = date.fromisoformat(raw[:10]) if len(raw) >= 10 else None
        except ValueError:
            when = None
        if when is not None and when > cutoff:
            post_cutoff.append({"doi": paper.get("doi"), "title": paper.get("title"),
                                "publication_date": raw})
        if (paper.get("doi") or "").lower() in resolver_dois:
            resolver_in_retrieval.append({"doi": paper.get("doi"),
                                          "title": paper.get("title")})

    clean = not (doi_hits or phrase_hits or post_cutoff or resolver_in_retrieval)
    return {
        "case_id": instance_dir.name,
        "cutoff": cutoff.isoformat(),
        "n_chars_sent_to_model": len(blob),
        "n_papers_retrieved": n_papers,
        "hidden_doi_hits": doi_hits,
        "hidden_phrase_hits": phrase_hits,
        "post_cutoff_papers_retrieved": post_cutoff,
        "resolver_papers_in_retrieval": resolver_in_retrieval,
        "clean": clean,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    run_dir = resolve_path(args.run)
    hidden = json.loads(resolve_path(HIDDEN_PATH).read_text(encoding="utf-8"))["cases"]
    cutoffs = {}
    for line in resolve_path(VISIBLE_PATH).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            cutoffs[row["case_id"]] = date.fromisoformat(row["cutoff"])

    results = []
    for instance_dir in sorted((run_dir / "instances").iterdir()):
        if not instance_dir.is_dir():
            continue
        results.append(audit_case(instance_dir, hidden[instance_dir.name],
                                  cutoffs[instance_dir.name]))
        status = "CLEAN" if results[-1]["clean"] else "LEAK"
        LOGGER.info("%s: %s (%d papers, %d chars to model)", instance_dir.name, status,
                    results[-1]["n_papers_retrieved"], results[-1]["n_chars_sent_to_model"])

    payload = {
        "run_dir": str(run_dir),
        "audit": "BENCH-GRAPH-PILOT-001 empirical leak audit of the frozen run",
        "n_cases": len(results),
        "n_clean": sum(1 for r in results if r["clean"]),
        "all_clean": all(r["clean"] for r in results) if results else False,
        "cases": results,
    }
    out_path = Path(args.out) if args.out else run_dir / "leak_audit.json"
    write_json(out_path, payload)
    print(json.dumps({k: v for k, v in payload.items() if k != "cases"}, indent=2))
    if not payload["all_clean"]:
        LOGGER.error("LEAK DETECTED -- see %s", out_path)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
