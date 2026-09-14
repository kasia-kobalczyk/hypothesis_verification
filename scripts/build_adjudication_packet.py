"""Build a BLIND adjudication packet: cases stripped of the current assessor's output.

    python3 scripts/build_adjudication_packet.py --judges A B

Writes one markdown worksheet per judge plus a JSONL answer file they fill in. The
current label and rationale are removed, so a judge cannot anchor on them, and the
key linking cases back to run artifacts is written to a separate file that judges do
not open.

No LLM calls. Deterministic.

Why blind, and why two judges: the adjudication is not really about getting 37
labels right. It is about measuring whether two people can reliably tell *indirect
but evidential* from *merely related*. If they cannot, the `indirect` category is
too subjective to calibrate and the method cannot use indirect evidence in a
principled way. Anchoring on v1's output, or having one judge, would destroy exactly
that measurement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.io import utc_now_iso, write_json  # noqa: E402

STRIPPED = (
    "current_label", "current_rationale", "rationale_invokes_directness",
    "rationale_concedes_related_work", "stratum",
    "gold_label", "gold_directness", "gold_link", "gold_link_type",
    "disagrees_with_current", "note", "labelled_by", "proposition_unassessable",
)

INSTRUCTIONS = """# Assessor adjudication — judge {judge}

Read `docs/ASSESSOR_RUBRIC.md` first. You are deciding, for each case, what the
retrieved literature says about the proposition.

**Do not look at** `benchmark/assessor/labelset_candidates.jsonl`, the run
artifacts, or another judge's worksheet. They contain the answer you are being asked
to produce independently.

For each case fill in one line of `{answers}`:

```json
{{"case_id": "...", "direction": "supports|contradicts|none",
 "strength": "strong|moderate|weak|null",
 "directness": "direct|indirect|null",
 "intermediate_fact": "the specific fact the record establishes, or null",
 "link": "one sentence naming the record id, or null",
 "merely_related": false,
 "proposition_unassessable": false,
 "confidence": "high|medium|low",
 "notes": ""}}
```

The three definitions, in full:

* **DIRECT** — the record explicitly tests, measures, reports, or states the
  proposition or its negation.
* **INDIRECT** — the record does not test the proposition itself, but establishes a
  **specific intermediate fact** that changes belief in the proposition through a
  named mechanistic, causal, logical, or quantitative link. You must be able to name
  that fact in `intermediate_fact`. If you cannot, it is not indirect.
* **NO EVIDENCE** — no such proposition-specific link can be stated.

**`merely_related` is the field this whole exercise turns on.** Set it true when the
record shares entities, a disease, an instrument or a field with the proposition but
you cannot state a link. That is different from a record that is simply off-topic,
and the difference is what we are measuring.

Set `proposition_unassessable` when the proposition cannot be checked *as written* —
for example it refers to "specific genetic alterations" without naming them. That is
a defect in the proposition, not a fact about the literature, and it is recorded on a
separate channel.

---

"""


def render_case(case: Dict[str, Any], index: int, total: int) -> str:
    lines = ["## Case {}/{} — `{}`".format(index, total, case["case_id"]), ""]
    lines += ["**Proposition**", "", "> {}".format(case["proposition"]), ""]
    papers = [p for p in case["papers"] if (p.get("abstract") or "").strip()]
    lines.append("**Retrieved records ({} with abstracts)**".format(len(papers)))
    lines.append("")
    for paper in papers:
        lines.append("- **`{}`** — {} ({}, {})".format(
            paper.get("id"), paper.get("title"), paper.get("year") or "n.d.",
            paper.get("venue") or "—"))
        lines.append("")
        lines.append("  {}".format((paper.get("abstract") or "").replace("\n", " ")))
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labelset", default="benchmark/assessor/labelset_candidates.jsonl")
    parser.add_argument("--judges", nargs="+", default=["A", "B"])
    parser.add_argument("--out-dir", default="benchmark/assessor/adjudication")
    args = parser.parse_args(argv)

    cases = [json.loads(line) for line in Path(args.labelset).read_text().splitlines()
             if line.strip()]
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    blind = []
    key = {}
    for case in cases:
        stripped = {k: v for k, v in case.items() if k not in STRIPPED}
        blind.append(stripped)
        key[case["case_id"]] = {
            "run": case.get("run"), "instance": case.get("instance"),
            "node": case.get("node"), "current_label": case.get("current_label"),
            "stratum": case.get("stratum"),
        }

    # The key is what makes the packet blind: it lives apart from the worksheets.
    write_json(out_dir / "_key_do_not_open_before_judging.json", {
        "generated_at": utc_now_iso(),
        "warning": "Contains the current assessor's labels. Opening this before you "
                   "have submitted your judgments invalidates your contribution to "
                   "the inter-judge agreement statistic.",
        "cases": key,
    })

    for judge in args.judges:
        answers = "answers_judge_{}.jsonl".format(judge)
        text = INSTRUCTIONS.format(judge=judge, answers=answers)
        for index, case in enumerate(blind, start=1):
            text += render_case(case, index, len(blind))
        (out_dir / "worksheet_judge_{}.md".format(judge)).write_text(text)
        # Re-sync the answer stub with the current case set, preserving anything the
        # judge has already filled in. Writing it only when absent left judges
        # answering case ids that no longer existed after the set changed.
        stub = out_dir / answers
        prior = {}
        if stub.exists():
            for line in stub.read_text().splitlines():
                if line.strip():
                    row = json.loads(line)
                    prior[row["case_id"]] = row
        answered = {cid: row for cid, row in prior.items()
                    if row.get("direction") is not None or row.get("directness") is not None}
        dropped = [cid for cid in answered if cid not in {c["case_id"] for c in blind}]
        if dropped:
            print("  WARNING: {} answered case(s) are no longer in the set: {}".format(
                len(dropped), ", ".join(sorted(dropped)[:5])))
        with stub.open("w", encoding="utf-8") as handle:
            for case in blind:
                row = prior.get(case["case_id"], {
                    "case_id": case["case_id"], "direction": None, "strength": None,
                    "directness": None, "intermediate_fact": None, "link": None,
                    "merely_related": None, "proposition_unassessable": None,
                    "confidence": None, "notes": "",
                })
                handle.write(json.dumps(row, sort_keys=True) + "\n")
        if answered:
            print("  preserved {} existing judgment(s)".format(len(answered)))
        print("judge {}: {} / {}".format(judge, out_dir / "worksheet_judge_{}.md".format(judge),
                                         stub))

    print("\n{} case(s), blinded. The key is in {}".format(
        len(blind), out_dir / "_key_do_not_open_before_judging.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
