"""Semantic merging of pooled propositions (IMPLEMENTATION_SPEC.md §13.4).

The graph is shared across hypotheses, not k independent trees: propositions
generated from different candidates are pooled and equivalent ones collapsed, so
inferential pathways can collide. A shared node is the point — it records that
several candidates predict the same thing, and that several downstream
observations reflect one mechanism (§35.9).

`merge_threshold` is marked TODO in the spec, so the mode is configuration:

* `none`    — pool without merging (every node keeps its own identity);
* `lexical` — deterministic normalised-title similarity, the default here;
* `llm`     — a semantic judge; NOT implemented, and the honest reason is that
              nobody has decided what "equivalent" should mean for this method.

Merging is conservative: below the threshold nodes stay separate. Over-merging
destroys the distinction between two genuinely different predictions, which is
worse for this method than a little redundancy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Sequence, Tuple

from src.common.errors import ConfigError
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.graph.schema import PropositionNode

LOGGER = get_logger("graph.merge")

MERGE_MODES = ("none", "lexical", "llm")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalise_text(text: str) -> str:
    return _NON_ALNUM.sub(" ", (text or "").lower()).strip()


def text_similarity(a: str, b: str) -> float:
    """Symmetric normalised similarity in [0, 1].

    Two details of `SequenceMatcher` have to be disarmed, because both were
    measured to distort these propositions badly:

    * **autojunk.** On sequences longer than 200 characters it treats elements
      appearing in more than 1% of `b` as junk. Propositions run to ~300
      characters, so common letters get discarded and the ratio is computed on
      whatever is left. Measured over 1,323 cross-hypothesis pairs from the debug
      runs, leaving it on shifted the similarity by a mean of 0.234 and up to
      0.473, and it depressed the cross-hypothesis maximum from 0.677 to 0.460.
    * **argument order.** Because autojunk keys off `b` alone, the function was
      asymmetric: 95% of those pairs scored differently depending on which text
      came first, worst case 0.460 against 0.056 for the same two propositions.
      An asymmetric similarity makes merging depend on iteration order, which is
      not a property a deduplication step is allowed to have.

    Sorting the pair before comparing makes symmetry structural rather than a
    property of the implementation.
    """
    na, nb = normalise_text(a), normalise_text(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na > nb:
        na, nb = nb, na
    return SequenceMatcher(None, na, nb, autojunk=False).ratio()


@dataclass
class MergeOutcome:
    nodes: List[PropositionNode] = field(default_factory=list)
    merges: List[Dict[str, Any]] = field(default_factory=list)
    remap: Dict[str, str] = field(default_factory=dict)  # old id -> surviving id

    def record(self) -> Dict[str, Any]:
        return {"n_nodes": len(self.nodes), "n_merges": len(self.merges),
                "merges": self.merges, "remap": self.remap}


def merge_propositions(
    nodes: Sequence[PropositionNode],
    *,
    mode: str = "lexical",
    threshold: Optional[float] = None,
    event_log: Optional[EventLog] = None,
) -> MergeOutcome:
    """Collapse equivalent propositions, keeping the first occurrence."""
    log = event_log or NULL_EVENT_LOG
    outcome = MergeOutcome()
    if mode not in MERGE_MODES:
        raise ConfigError("unknown graph.semantic_merge mode {!r}; expected {}".format(mode, MERGE_MODES))
    if mode == "llm":
        raise NotImplementedError(
            "graph.semantic_merge='llm' is not implemented: the spec leaves "
            "merge_threshold unresolved (§14), so what counts as equivalent is a "
            "research decision, not an implementation one."
        )
    if mode == "none":
        outcome.nodes = list(nodes)
        outcome.remap = {n.id: n.id for n in nodes}
        return outcome

    if threshold is None:
        raise ConfigError(
            "graph.merge_threshold is null. Set it to merge lexically, or set "
            "graph.semantic_merge='none' to pool without merging."
        )

    for node in nodes:
        match: Optional[PropositionNode] = None
        score = 0.0
        for kept in outcome.nodes:
            candidate_score = text_similarity(node.text, kept.text)
            if candidate_score >= threshold and candidate_score > score:
                match, score = kept, candidate_score
        if match is None:
            outcome.nodes.append(node)
            outcome.remap[node.id] = node.id
            continue

        # Fold into the surviving node, preserving where it came from.
        match.merged_from.append(node.id)
        for origin in ([node.generation_origin_hypothesis] + node.merged_origin_hypotheses):
            if origin and origin not in match.merged_origin_hypotheses:
                match.merged_origin_hypotheses.append(origin)
        match.empirically_assessable = match.empirically_assessable or node.empirically_assessable
        outcome.remap[node.id] = match.id
        outcome.merges.append({
            "merged": node.id, "into": match.id, "similarity": round(score, 3),
            "merged_text": node.text, "kept_text": match.text,
        })
        log.decision("proposition_merged", merged=node.id, into=match.id,
                     similarity=round(score, 3))
        LOGGER.debug("merged %s into %s (%.3f)", node.id, match.id, score)
    return outcome
