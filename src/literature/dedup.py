"""Conservative version deduplication.

IMPLEMENTATION_SPEC.md §6, §21: a preprint and its journal version are one piece
of evidence, not two. But an over-eager merge destroys genuinely independent
replications, which matters more for this method than a little redundancy — so
the rule is:

* merge only on strong identity evidence (same DOI, same arXiv id, or
  near-identical title *plus* author overlap);
* between the two thresholds, keep both records and flag `possibly_related_to`
  so the evidence assessor can take the dependence into account;
* never merge across the cutoff boundary implicitly — dedup runs *after*
  temporal filtering, so the surviving representative is always eligible.

Deduplication is by construction unable to admit a record; it only removes or
annotates. That keeps it outside the temporal-safety argument.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Sequence, Set, Tuple

from src.common.config import DedupConfig
from src.common.io import stable_hash
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.base import Paper
from src.literature.crossref import normalise_doi

LOGGER = get_logger("literature.dedup")

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalise_title(title: Optional[str]) -> str:
    if not title:
        return ""
    return _NON_ALNUM.sub(" ", title.lower()).strip()


def title_similarity(a: Optional[str], b: Optional[str]) -> float:
    ta, tb = normalise_title(a), normalise_title(b)
    if not ta or not tb:
        return 0.0
    if ta == tb:
        return 1.0
    return SequenceMatcher(None, ta, tb).ratio()


def _author_families(paper: Paper) -> Set[str]:
    return {a.family_name for a in paper.authors if a.family_name}


def _external_ids(paper: Paper) -> Dict[str, str]:
    raw = paper.raw or {}
    ids = raw.get("externalIds") or {}
    if not isinstance(ids, dict):
        return {}
    return {str(k): str(v) for k, v in ids.items() if v is not None}


def _identity_keys(paper: Paper) -> List[str]:
    """Strong identity keys: equality implies the same scientific work."""
    keys: List[str] = []
    doi = normalise_doi(paper.doi)
    if doi:
        keys.append("doi:" + doi)
    for id_type in ("ArXiv", "DOI", "PubMed", "PubMedCentral", "DBLP", "ACL"):
        value = _external_ids(paper).get(id_type)
        if value:
            keys.append("{}:{}".format(id_type.lower(), value.lower()))
    return keys


def _link_possibly_related(a: Paper, b: Paper) -> None:
    """Flag two records as potentially the same work, without duplicating links.

    `deduplicate` runs more than once over the same `Paper` objects (per query in
    the service, then across queries in a method), so the annotation must be
    idempotent.
    """
    if b.paper_id not in a.possibly_related_to:
        a.possibly_related_to.append(b.paper_id)
    if a.paper_id not in b.possibly_related_to:
        b.possibly_related_to.append(a.paper_id)


@dataclass
class DedupOutcome:
    papers: List[Paper] = field(default_factory=list)       # representatives, original order
    collapsed: List[Paper] = field(default_factory=list)    # merged-away records
    groups: Dict[str, List[str]] = field(default_factory=dict)
    possibly_related: List[Tuple[str, str, float]] = field(default_factory=list)

    @property
    def n_collapsed(self) -> int:
        return len(self.collapsed)


def deduplicate(
    papers: Sequence[Paper],
    config: DedupConfig,
    *,
    event_log: Optional[EventLog] = None,
) -> DedupOutcome:
    """Collapse duplicate versions; annotate uncertain pairs."""
    log = event_log or NULL_EVENT_LOG
    outcome = DedupOutcome()
    if not config.enabled or not papers:
        outcome.papers = list(papers)
        return outcome

    representatives: List[Paper] = []
    rep_of_key: Dict[str, Paper] = {}

    for paper in papers:
        keys = _identity_keys(paper)
        match: Optional[Paper] = None
        reason = ""

        for key in keys:
            if key in rep_of_key:
                match = rep_of_key[key]
                reason = "identity:{}".format(key.split(":", 1)[0])
                break

        if match is None:
            for candidate in representatives:
                score = title_similarity(paper.title, candidate.title)
                if score >= config.title_similarity_threshold:
                    shared = _author_families(paper) & _author_families(candidate)
                    if config.require_author_overlap and not shared:
                        outcome.possibly_related.append((paper.paper_id, candidate.paper_id, score))
                        _link_possibly_related(paper, candidate)
                        log.decision(
                            "possibly_related", reason="title_match_without_author_overlap",
                            a=paper.paper_id, b=candidate.paper_id, similarity=round(score, 3),
                        )
                        continue
                    match = candidate
                    reason = "title_similarity:{:.3f}".format(score)
                    break
                if score >= config.possibly_related_threshold:
                    outcome.possibly_related.append((paper.paper_id, candidate.paper_id, score))
                    _link_possibly_related(paper, candidate)
                    log.decision(
                        "possibly_related", reason="title_similarity_below_threshold",
                        a=paper.paper_id, b=candidate.paper_id, similarity=round(score, 3),
                    )

        if match is None:
            representatives.append(paper)
            for key in keys:
                rep_of_key.setdefault(key, paper)
            continue

        group_id = match.duplicate_group or "grp-{}".format(stable_hash(match.paper_id, length=8))
        match.duplicate_group = group_id
        paper.duplicate_group = group_id
        paper.duplicate_of = match.paper_id
        # `paper` may itself represent a group from an earlier dedup pass; carry
        # its members across so the chain is not lost (§21: dependence signal).
        for member in [paper.paper_id] + list(paper.versions):
            if member not in match.versions and member != match.paper_id:
                match.versions.append(member)
        outcome.collapsed.append(paper)
        outcome.groups.setdefault(group_id, [match.paper_id]).append(paper.paper_id)
        for key in _identity_keys(paper):
            rep_of_key.setdefault(key, match)
        log.decision(
            "deduplicated", group=group_id, representative=match.paper_id,
            collapsed=paper.paper_id, reason=reason,
        )
        LOGGER.debug("collapsed %s into %s (%s)", paper.paper_id, match.paper_id, reason)

    outcome.papers = representatives
    return outcome
