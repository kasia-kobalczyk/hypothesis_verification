"""Replay labelled assessment cases through an assessor prompt and report agreement.

    python3 scripts/assessor_agreement.py --prompt evidence_assess_v1
    python3 scripts/assessor_agreement.py --prompt evidence_assess_v2 --dry-run

Uses the retrieved papers stored with each case, so retrieval is NOT re-run: the only
thing varying is the assessor prompt. That makes this the right instrument for asking
whether a prompt change altered judgment rather than luck of the draw.

Reports, in order of how much they matter:

1. **Direction agreement** — support / none / contradict. This is what moves the
   ranking; an exact-label mismatch between `support` and `weak_support` does not.
2. **Exact-label agreement.**
3. **The informative-vs-`no_evidence` confusion matrix**, which is where the
   construct question lives.
4. For indirect judgments, whether an inferential link was actually stated. A prompt
   that claims indirect evidence without stating the link has failed the rubric's
   one safeguard.

A prompt that raises the informative rate **without** raising direction agreement is
manufacturing signal. That combination is called out explicitly rather than buried.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.assessor_agreement")

LABELSET = "benchmark/assessor/labelset_candidates.jsonl"

SUPPORTING = {"strong_support", "support", "weak_support"}
CONTRADICTING = {"strong_contradiction", "contradiction", "weak_contradiction"}


def direction(label: Optional[str]) -> str:
    if label in SUPPORTING:
        return "support"
    if label in CONTRADICTING:
        return "contradict"
    if label == "mixed":
        return "mixed"
    return "none"


def render_literature(papers: List[Dict[str, Any]]) -> str:
    blocks = []
    for paper in papers:
        if not (paper.get("abstract") or "").strip():
            continue
        blocks.append("id: {}\ntitle: {}\nyear: {}\nvenue: {}\nabstract: {}".format(
            paper.get("id"), paper.get("title"), paper.get("year"),
            paper.get("venue"), paper.get("abstract")))
    return "\n\n".join(blocks)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--prompt", default="evidence_assess_v1")
    parser.add_argument("--labelset", default=LABELSET)
    parser.add_argument("--out", default=None)
    parser.add_argument("--gate", action="store_true",
                        help="evaluate the pre-registered acceptance gate "
                             "(benchmark/assessor/acceptance_gate.json)")
    parser.add_argument("--compare-to", default=None,
                        help="an earlier agreement_<prompt>.json to measure improvement against")
    parser.add_argument("--dry-run", action="store_true",
                        help="render prompts and report coverage; make no model calls")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    config = load_config(args.config)
    prompts = PromptLibrary(config.prompts.dir)
    template = prompts.get(args.prompt)

    cases = [json.loads(line) for line in Path(args.labelset).read_text().splitlines()
             if line.strip()]
    labelled = [c for c in cases if c.get("gold_label")]
    if not labelled:
        print("no adjudicated cases in {} -- nothing to measure.".format(args.labelset))
        print("Label some cases first; see benchmark/assessor/README.md.")
        return 1

    unreviewed = [c for c in labelled if c.get("labelled_by") == "proposed-unreviewed"]
    if unreviewed:
        print("WARNING: {} of {} labels are marked 'proposed-unreviewed'. Agreement "
              "against them measures consistency with a proposal, not with ground "
              "truth.\n".format(len(unreviewed), len(labelled)))

    if args.dry_run:
        print("{} adjudicated case(s); {} would be sent to the model.".format(
            len(labelled), sum(1 for c in labelled if render_literature(c["papers"]))))
        for case in labelled:
            print("  {:<24} gold={:<20} current={}".format(
                case["case_id"], case["gold_label"], case["current_label"]))
        return 0

    event_log = EventLog(Path("benchmark/assessor") / "agreement_events.jsonl")
    llm = build_llm_client(config.llm, event_log=event_log)
    from src.evidence.assess import EVIDENCE_LABELS

    labels = ", ".join(EVIDENCE_LABELS)

    rows: List[Dict[str, Any]] = []
    for case in labelled:
        literature = render_literature(case["papers"])
        if not literature:
            continue
        messages = [{"role": "user", "content": template.render(
            proposition=case["proposition"], literature=literature, labels=labels)}]

        def validate(parsed: Dict[str, Any]) -> None:
            if not str(parsed.get("evidence_label", "")).strip():
                raise ValueError("missing evidence_label")

        try:
            response = llm.complete_json(
                messages, purpose="assessor.agreement", prompt_version=args.prompt,
                validator=validate)
            parsed = response.parsed or {}
        except (LLMParseError, LLMError) as exc:
            LOGGER.error("%s: %s", case["case_id"], exc)
            rows.append({"case_id": case["case_id"], "error": str(exc)})
            continue

        predicted = str(parsed.get("evidence_label", "")).strip()
        rows.append({
            "case_id": case["case_id"],
            "gold_label": case["gold_label"],
            "gold_directness": case.get("gold_directness"),
            "predicted_label": predicted,
            "predicted_directness": parsed.get("evidence_directness"),
            "predicted_link": parsed.get("inference_link"),
            "predicted_chain": parsed.get("chain"),
            "requires_unsupported_facts": parsed.get("requires_unsupported_facts"),
            "proposition_unassessable": parsed.get("proposition_unassessable"),
            "rationale": parsed.get("rationale"),
            "exact_match": predicted == case["gold_label"],
            "direction_match": direction(predicted) == direction(case["gold_label"]),
            "gold_informative": case["gold_label"] != "no_evidence",
            "predicted_informative": predicted != "no_evidence",
        })

    scored = [r for r in rows if "error" not in r]
    if not scored:
        print("every case errored; nothing to report")
        return 1

    exact = sum(r["exact_match"] for r in scored) / len(scored)
    direction_agreement = sum(r["direction_match"] for r in scored) / len(scored)
    confusion = Counter(
        (r["gold_informative"], r["predicted_informative"]) for r in scored)
    gold_rate = sum(r["gold_informative"] for r in scored) / len(scored)
    pred_rate = sum(r["predicted_informative"] for r in scored) / len(scored)
    unlinked = [r for r in scored
                if r.get("predicted_directness") == "indirect" and not r.get("predicted_link")]

    print("\nprompt: {}   cases: {}   errors: {}".format(
        args.prompt, len(scored), len(rows) - len(scored)))
    print("  direction agreement (support/none/contradict) : {:.3f}".format(direction_agreement))
    print("  exact-label agreement                          : {:.3f}".format(exact))
    print("  informative rate  gold {:.3f}  predicted {:.3f}".format(gold_rate, pred_rate))
    print("  confusion (gold informative -> predicted informative):")
    for gold in (True, False):
        for pred in (True, False):
            print("    gold={:<5} pred={:<5} {}".format(
                gold, pred, confusion[(gold, pred)]))
    if unlinked:
        print("  RUBRIC VIOLATION: {} indirect judgment(s) stated no inference_link".format(
            len(unlinked)))
    if pred_rate > gold_rate and direction_agreement <= 0.5:
        print("\n  WARNING: this prompt calls more cases informative than the labels do "
              "while agreeing on direction no better than chance. That is the signature "
              "of manufacturing evidence from topical adjacency.")

    # Chain audit: an indirect judgment whose chain is missing, truncated, or admits
    # it needed unsupported facts has failed the rubric's own test.
    indirect = [r for r in scored if r.get("predicted_directness") == "indirect"]
    bad_chain = [r for r in indirect
                 if not isinstance(r.get("predicted_chain"), list)
                 or len(r.get("predicted_chain") or []) != 3
                 or any(not str(step).strip() for step in (r.get("predicted_chain") or []))]
    admits_unsupported = [r for r in indirect if r.get("requires_unsupported_facts")]
    if indirect:
        print("  indirect judgments: {}   without a complete 3-step chain: {}   "
              "admitting unsupported facts: {}".format(
                  len(indirect), len(bad_chain), len(admits_unsupported)))
        if admits_unsupported:
            print("    RUBRIC VIOLATION: these should have returned no_evidence")

    if args.gate:
        gate = json.loads(Path("benchmark/assessor/acceptance_gate.json").read_text())
        print("\n=== pre-registered acceptance gate ===")
        thresholds = {
            "criterion_2_direction_agreement_improves":
                gate["criterion_2_direction_agreement_improves"]["threshold"],
            "criterion_3_promotions_are_not_merely_related":
                gate["criterion_3_promotions_are_not_merely_related"]["threshold"],
        }
        if any(v is None for v in thresholds.values()):
            print("  CANNOT EVALUATE: thresholds are unset in acceptance_gate.json.")
            print("  They must be set by the research owner BEFORE adjudication, not now.")
            print("  (This refusal is the point; see docs/DECISIONS.md #16.)")
        else:
            print("  thresholds present; evaluation requires an adjudicated label set "
                  "and a --compare-to baseline.")

    out = Path(args.out or "benchmark/assessor/agreement_{}.json".format(args.prompt))
    write_json(out, {
        "generated_at": utc_now_iso(),
        "prompt": args.prompt,
        "prompt_record": template.record(),
        "n_cases": len(scored),
        "labels_unreviewed": len(unreviewed),
        "direction_agreement": round(direction_agreement, 4),
        "exact_agreement": round(exact, 4),
        "gold_informative_rate": round(gold_rate, 4),
        "predicted_informative_rate": round(pred_rate, 4),
        "rubric_violations_unlinked_indirect": len(unlinked),
        "rows": rows,
    })
    print("\nwrote {}".format(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
