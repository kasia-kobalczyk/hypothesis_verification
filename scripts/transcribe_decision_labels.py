"""Transcribe Research Director review decisions into packet label files.

Labels are parsed from `.agent/DECISIONS.md`, never retyped, so a label file can be
regenerated and diffed against the decision at any time. Nothing is inferred:
a field the decision does not state is left out, and the packet builder leaves it
blank.

  D045 -> benchmark/review/graph_pilot_001/human_labels_D045.json  (primary categories)
  D046 -> benchmark/review/graph_pilot_001/human_labels_D046.json  (adds per-hypothesis
          prediction states, secondary flags, evidence relevance, confidence, notes)

D046 states are recorded as the first backticked state token on each hypothesis line.
Where the Director qualified a state ("... if `convergent` is interpreted as ...",
"at most weakly ...", "`indeterminate` / compatible"), the full line is kept verbatim
in `human_prediction_qualifiers` and the state is flagged as qualified, so agreement
statistics can report qualified states separately rather than as unconditional.

Usage:
    python scripts/transcribe_decision_labels.py
"""
from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / ".agent" / "DECISIONS.md"
PACKET = ROOT / "benchmark" / "review" / "graph_pilot_001"

STATES = ("positive_or_present", "negative_or_absent", "substantive_null", "indeterminate")


def _section(text: str, decision: str) -> str:
    start = text.index("## {} ".format(decision))
    nxt = text.find("\n## D", start + 1)
    return text[start: nxt if nxt != -1 else len(text)]


def _cases() -> List[str]:
    full = PACKET / "review_set_full.jsonl"
    return sorted({json.loads(line)["case_id"] for line in full.read_text(encoding="utf-8").splitlines()})


def _resolve(key: str, cases: List[str]) -> Dict[str, str]:
    prefix, node = key.rsplit("-", 1)
    hits = [c for c in cases if c == prefix or c.startswith(prefix + "_")]
    if len(hits) != 1:
        raise SystemExit("cannot resolve {!r} to exactly one case: {}".format(key, hits))
    return {"case_id": hits[0], "node_id": node, "review_id": "GP1-{}-{}".format(hits[0], node)}


def parse_d045(text: str) -> List[Dict[str, Any]]:
    sec = _section(text, "D045")
    body = sec[sec.index("NODE-LEVEL PRIMARY LABELS"):sec.index("KEY INTERPRETATION")]
    cases = _cases()
    out = []
    for n, key, cat in re.findall(r"^(\d+)\.?\s+`?([A-Za-z0-9_]+-X\d+)`?\s+—\s+`?([a-z_]+)`?\s*$", body, re.M):
        out.append(OrderedDict([("d045_number", int(n)), ("d045_key", key)] + list(_resolve(key, cases).items())
                               + [("human_primary_category", cat)]))
    return out


def parse_d046(text: str) -> List[Dict[str, Any]]:
    sec = _section(text, "D046")
    body = sec[sec.index("ADJUDICATION:"):sec.index("KEY NEW METHOD DIAGNOSIS")]
    cases = _cases()
    out = []
    for block in re.split(r"\n(?=\d+\. `)", body)[1:]:
        head = re.match(r"(\d+)\. `([^`]+)`", block)
        number, key = int(head.group(1)), head.group(2)
        entry: "OrderedDict[str, Any]" = OrderedDict([("d046_number", number), ("d046_key", key)])
        entry.update(_resolve(key, cases))

        proposition = re.search(r"^Proposition:\s*(.+)$", block, re.M)
        entry["director_proposition_paraphrase"] = proposition.group(1).strip() if proposition else None

        states, qualifiers = OrderedDict(), OrderedDict()
        for hyp, line in re.findall(r"^- (H\d)[^:\n]*:\s*(.+)$", block, re.M):
            tokens = [t for t in re.findall(r"`([a-z_]+)`", line) if t in STATES]
            if not tokens:
                raise SystemExit("D046 #{} {}: no state token in {!r}".format(number, hyp, line))
            states[hyp] = tokens[0]
            stripped = line.strip()
            plain = stripped.rstrip(".") == "`{}`".format(tokens[0]) or re.match(
                r"^`{}`(;|\.|$)".format(tokens[0]), stripped)
            conditional = any(s in stripped for s in (" if ", "at most", " / "))
            qualifiers[hyp] = OrderedDict([("line_verbatim", stripped),
                                           ("qualified", bool(conditional or not plain))])
        entry["human_prediction_for_each_hypothesis"] = states
        entry["human_prediction_qualifiers"] = qualifiers

        primary = re.search(r"^Primary category[^:\n]*:\s*`([a-z_]+)`(.*)$", block, re.M)
        entry["human_primary_category"] = primary.group(1)
        entry["human_secondary_flags"] = re.findall(r"secondary `([a-z_]+)`", primary.group(2))
        entry["primary_category_note_verbatim"] = primary.group(2).strip(" .") or None

        relevance = re.search(r"^Evidence relevance:\s*(.+)$", block, re.M)
        entry["human_evidence_relevance"] = relevance.group(1).strip() if relevance else None
        confidence = re.search(r"^Confidence:\s*(.+?)\.?\s*$", block, re.M)
        entry["human_confidence"] = confidence.group(1).strip() if confidence else None
        notes = [m.strip() for m in re.findall(r"^(?:Reason|Important|The proposition is therefore)[^\n]*$",
                                                 block, re.M)]
        entry["human_notes"] = " ".join(notes) or None
        out.append(entry)
    return out


def _write(path: Path, source: str, labels: List[Dict[str, Any]], extra: Dict[str, Any]) -> None:
    payload = OrderedDict([
        ("source", source),
        ("human_reviewer", "Research Director"),
        ("human_review_source", extra["review_source"]),
        ("human_review_status", "first_pass_model_based_review"),
        ("caveat", "Model-based Research Director adjudication, not external domain-expert ground truth ({}).".format(
            extra["review_source"])),
    ])
    payload.update((k, v) for k, v in extra.items() if k != "review_source")
    payload["labels"] = labels
    path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    text = DECISIONS.read_text(encoding="utf-8")
    d045 = parse_d045(text)
    d046 = parse_d046(text)
    _write(PACKET / "human_labels_D045.json",
           "D045 in .agent/DECISIONS.md (relay-decision a256aef537b9f060bf942325), transcribed mechanically; "
           "tests/test_review_packet.py re-parses D045 and requires exact equality",
           d045, {"review_source": "D045",
                  "fields_not_recorded_in_D045": "per-hypothesis predictions, implication validity, evidence "
                                                 "relevance, notes and confidence are left blank; they were not "
                                                 "recorded and are not inferred"})
    _write(PACKET / "human_labels_D046.json",
           "D046 in .agent/DECISIONS.md (relay-decision 245e6f31cd1447bf00e42a21), transcribed mechanically by "
           "scripts/transcribe_decision_labels.py",
           d046, {"review_source": "D046",
                  "state_vocabulary": "positive_or_present | negative_or_absent | substantive_null | indeterminate "
                                      "(D046; `substantive_null` = a positive prediction of no effect/baseline)",
                  "qualified_states": "where the Director attached a condition or hedge to a state, the line is "
                                      "kept verbatim and `qualified` is true"})
    print("D045: {} labels, D046: {} labels".format(len(d045), len(d046)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
