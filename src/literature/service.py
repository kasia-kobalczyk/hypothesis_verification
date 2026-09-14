"""The temporally constrained literature-search service.

This is the **only** surface through which literature may reach a model.

IMPLEMENTATION_SPEC.md §4 and §7:

* the public API is `search_literature(query, instance_id, top_k)` — there is no
  cutoff parameter, and no keyword that could introduce one, so a method or
  agent cannot widen its own temporal window;
* the cutoff is read from the frozen `CutoffRegistry` on every call;
* every access path (search, metadata lookup, reference expansion, citation
  expansion) funnels through `_retrieve`, which applies the same filter;
* `render_for_prompt` re-checks eligibility from scratch before text is handed
  to a model, so a tampered record still cannot leak.

Excluded records are retained inside `RetrievalRecord.excluded` for debugging
only; `search_literature` returns eligible papers exclusively.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Callable, Dict, List, Optional, Sequence

from src.benchmark.temporal import CutoffInfo, CutoffRegistry
from src.common.config import AppConfig
from src.common.dates import PartialDate
from src.common.io import utc_now_iso
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger
from src.literature.base import LiteratureProvider, Paper, RetrievalRecord
from src.literature.cache import LiteratureCache
from src.literature.crossref import CrossrefClient
from src.literature.dedup import deduplicate
from src.literature.semantic_scholar import SemanticScholarProvider
from src.literature.temporal_filter import TemporalFilter

LOGGER = get_logger("literature.service")


class LiteratureSearchService:
    def __init__(
        self,
        *,
        provider: LiteratureProvider,
        cutoff_registry: CutoffRegistry,
        temporal_filter: TemporalFilter,
        cache: LiteratureCache,
        config: AppConfig,
        event_log: Optional[EventLog] = None,
    ):
        self._provider = provider
        self._cutoffs = cutoff_registry
        self._filter = temporal_filter
        self._cache = cache
        self._config = config
        self.event_log = event_log or NULL_EVENT_LOG
        self.records: List[RetrievalRecord] = []
        self.stats: Dict[str, int] = {
            "queries": 0,
            "cache_hits": 0,
            "provider_calls": 0,
            "eligible_returned": 0,
            "excluded": 0,
            "errors": 0,
        }

    # ------------------------------------------------------------------ #
    # Public API (agent-facing). Note: no cutoff parameter, by design.
    # ------------------------------------------------------------------ #
    def search_literature(self, query: str, instance_id: str, top_k: int = 10) -> List[Paper]:
        """Return eligible pre-cutoff literature for `query` (spec §4)."""
        return self.search(query, instance_id, top_k=top_k).eligible

    def search(self, query: str, instance_id: str, top_k: Optional[int] = None) -> RetrievalRecord:
        """Like `search_literature`, but returns the full diagnostic record."""
        k = int(top_k if top_k is not None else self._config.literature.top_k)
        cutoff = self._cutoffs.require(instance_id)
        limit = min(100, max(k, k * max(1, self._config.literature.overfetch_factor)))

        def call() -> Dict[str, Any]:
            return self._provider.search_raw(query, limit=limit, max_date=cutoff.cutoff_date)

        return self._retrieve(
            query=query,
            cutoff=cutoff,
            top_k=k,
            retrieval_path="search",
            provider_call=call,
            limit=limit,
        )

    def get_paper_details(self, provider_id: str, instance_id: str) -> Optional[Paper]:
        """Metadata lookup. Returns `None` when the paper is not pre-cutoff."""
        cutoff = self._cutoffs.require(instance_id)
        record = self._retrieve(
            query="paper:{}".format(provider_id),
            cutoff=cutoff,
            top_k=1,
            retrieval_path="lookup",
            provider_call=lambda: self._provider.paper_raw(provider_id),
            limit=1,
        )
        return record.eligible[0] if record.eligible else None

    def expand_references(
        self, provider_id: str, instance_id: str, top_k: Optional[int] = None
    ) -> List[Paper]:
        """Outgoing references, cutoff-filtered like any other access path."""
        k = int(top_k if top_k is not None else self._config.literature.top_k)
        cutoff = self._cutoffs.require(instance_id)
        limit = min(1000, max(k, k * max(1, self._config.literature.overfetch_factor)))
        record = self._retrieve(
            query="references:{}".format(provider_id),
            cutoff=cutoff,
            top_k=k,
            retrieval_path="references",
            provider_call=lambda: self._provider.references_raw(provider_id, limit=limit),
            limit=limit,
        )
        return record.eligible

    def expand_citations(
        self, provider_id: str, instance_id: str, top_k: Optional[int] = None
    ) -> List[Paper]:
        """Incoming citations. Almost all of these are post-cutoff by
        construction; they are filtered exactly like search results."""
        k = int(top_k if top_k is not None else self._config.literature.top_k)
        cutoff = self._cutoffs.require(instance_id)
        limit = min(1000, max(k, k * max(1, self._config.literature.overfetch_factor)))
        record = self._retrieve(
            query="citations:{}".format(provider_id),
            cutoff=cutoff,
            top_k=k,
            retrieval_path="citations",
            provider_call=lambda: self._provider.citations_raw(provider_id, limit=limit),
            limit=limit,
        )
        return record.eligible

    # ------------------------------------------------------------------ #
    def render_for_prompt(
        self,
        papers: Sequence[Paper],
        instance_id: str,
        *,
        max_papers: Optional[int] = None,
        abstract_char_limit: Optional[int] = None,
    ) -> str:
        """Format papers for model context, after re-checking eligibility.

        This is the last gate before literature becomes prompt text.
        """
        cutoff = self._cutoffs.require(instance_id)
        selected = list(papers)[: max_papers if max_papers is not None else len(papers)]
        self._filter.assert_no_leak(selected, cutoff)  # raises TemporalLeakError

        limit = (
            abstract_char_limit
            if abstract_char_limit is not None
            else self._config.literature.abstract_char_limit
        )
        blocks: List[str] = []
        for index, paper in enumerate(selected, start=1):
            abstract = paper.abstract or "[no abstract available]"
            if limit and len(abstract) > limit:
                abstract = abstract[:limit].rstrip() + " [...]"
            lines = [
                "[{}] {}".format(index, paper.title or "[no title]"),
                "    id: {}".format(paper.paper_id),
                "    date: {}".format(
                    paper.publication_date or (str(paper.year) if paper.year else "unknown")
                ),
                "    venue: {}{}".format(paper.venue or "unknown", " (preprint)" if paper.is_preprint else ""),
                "    authors: {}".format(
                    ", ".join(a.name for a in paper.authors[:8]) or "unknown"
                ),
                "    abstract: {}".format(abstract),
            ]
            if paper.versions:
                lines.append(
                    "    note: merged with {} other version(s) of the same work".format(len(paper.versions))
                )
            if paper.possibly_related_to:
                lines.append(
                    "    note: possibly the same work as {}".format(", ".join(paper.possibly_related_to))
                )
            blocks.append("\n".join(lines))
        return "\n\n".join(blocks)

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #
    def _retrieve(
        self,
        *,
        query: str,
        cutoff: CutoffInfo,
        top_k: int,
        retrieval_path: str,
        provider_call: Callable[[], Dict[str, Any]],
        limit: int,
    ) -> RetrievalRecord:
        key = LiteratureCache.build_key(
            provider=self._provider.name,
            provider_version=self._provider.version,
            query=query,
            instance_id=cutoff.instance_id,
            cutoff_date=cutoff.cutoff_date,
            top_k=limit,
            retrieval_path=retrieval_path,
            provider_config=self._provider.config_fingerprint(),
        )
        record = RetrievalRecord(
            query=query,
            instance_id=cutoff.instance_id,
            provider=self._provider.name,
            provider_version=self._provider.version,
            top_k=top_k,
            cutoff_date=cutoff.cutoff_date,
            retrieval_path=retrieval_path,
            retrieved_at=utc_now_iso(),
        )
        self.stats["queries"] += 1

        entry = self._cache.get(key)  # raises CacheMissError in offline mode
        if entry is not None:
            payload = entry.get("raw") or {}
            record.cache_status = "hit"
            record.retrieved_at = entry.get("retrieved_at") or record.retrieved_at
            self.stats["cache_hits"] += 1
        else:
            try:
                payload = provider_call()  # never degraded to [] (spec §29)
            except Exception:
                # Re-raised: callers must distinguish "provider down" from
                # "nothing found". Counted so a dead provider is visible in
                # summary.json rather than only in the per-instance errors.
                self.stats["errors"] += 1
                self.stats["provider_calls"] += 1
                raise
            record.cache_status = "refresh" if self._cache.config.refresh else "miss"
            self.stats["provider_calls"] += 1
            self._cache.put(key, payload, meta={"retrieval_path": retrieval_path, "limit": limit})

        papers = self._provider.normalise(payload, query=query, retrieval_path=retrieval_path)
        if isinstance(payload, dict):
            record.n_raw = len(payload.get("data") or []) if "data" in payload else (1 if payload else 0)
        record.n_normalised = len(papers)

        outcome = self._filter.apply(papers, cutoff)
        record.excluded.extend(outcome.excluded)
        record.notes.extend(outcome.notes)

        # Preprint policy is applied after dating, so an excluded preprint still
        # carries the `eligible_date` an audit needs.
        if not self._config.literature.include_preprints:
            kept: List[Paper] = []
            for paper in outcome.eligible:
                if paper.is_preprint:
                    paper.temporal_eligible = False
                    paper.exclusion_reason = "preprint_excluded_by_config"
                    record.excluded.append(paper)
                else:
                    kept.append(paper)
            outcome.eligible = kept

        dedup = deduplicate(outcome.eligible, self._config.literature.dedup, event_log=self.event_log)
        record.n_duplicates_collapsed = dedup.n_collapsed
        eligible = dedup.papers

        total_eligible = len(eligible)
        if len(eligible) > top_k:
            record.notes.append(
                "{} eligible results found; returning the top {}".format(total_eligible, top_k)
            )
            eligible = eligible[:top_k]

        # Final gate: recompute eligibility, ignoring the stored flags.
        self._filter.assert_no_leak(eligible, cutoff)

        record.eligible = eligible
        record.n_eligible = len(eligible)
        record.n_excluded = len(record.excluded)
        self.stats["eligible_returned"] += record.n_eligible
        self.stats["excluded"] += record.n_excluded

        self._cache.put_snapshot(
            key,
            {
                "key": key,
                "cache_status": record.cache_status,
                "snapshot_at": utc_now_iso(),
                "n_normalised": record.n_normalised,
                "eligible": [p.model_dump(mode="json", exclude={"raw"}) for p in record.eligible],
                "excluded": [
                    {
                        "paper_id": p.paper_id,
                        "title": p.title,
                        "eligible_date": p.eligible_date.isoformat() if p.eligible_date else None,
                        "reason": p.exclusion_reason,
                    }
                    for p in record.excluded
                ],
                "duplicate_groups": dedup.groups,
                "notes": record.notes,
            },
        )
        self.event_log.emit(
            "retrieval",
            instance_id=cutoff.instance_id,
            query=query,
            retrieval_path=retrieval_path,
            cache=record.cache_status,
            cutoff_date=cutoff.cutoff_date.isoformat() if cutoff.cutoff_date else None,
            n_normalised=record.n_normalised,
            n_eligible=record.n_eligible,
            n_excluded=record.n_excluded,
            n_duplicates_collapsed=record.n_duplicates_collapsed,
            exclusion_reasons=outcome.counts,
        )
        self.records.append(record)
        return record

    # ------------------------------------------------------------------ #
    def bind_event_log(self, event_log: EventLog) -> None:
        """Redirect service-level events (retrieval, filtering, dedup).

        The runner uses this so that each instance's decisions also land in
        `instances/<id>/events.jsonl`. Lower-level HTTP/cache events keep the
        run-wide log they were constructed with.
        """
        self.event_log = event_log
        self._filter.event_log = event_log

    def records_for(self, instance_id: str) -> List[RetrievalRecord]:
        return [r for r in self.records if r.instance_id == instance_id]

    def reset_records(self) -> None:
        self.records = []


class InstanceSearchTool:
    """Instance-bound view of the service, handed to methods and agents.

    Carries no cutoff and exposes no way to set one; `instance_id` is fixed at
    construction time.
    """

    def __init__(self, service: LiteratureSearchService, instance_id: str):
        self._service = service
        self._instance_id = instance_id

    @property
    def instance_id(self) -> str:
        return self._instance_id

    def search(self, query: str, top_k: Optional[int] = None) -> List[Paper]:
        return self._service.search(query, self._instance_id, top_k=top_k).eligible

    def search_with_record(self, query: str, top_k: Optional[int] = None) -> RetrievalRecord:
        return self._service.search(query, self._instance_id, top_k=top_k)

    def references(self, provider_id: str, top_k: Optional[int] = None) -> List[Paper]:
        return self._service.expand_references(provider_id, self._instance_id, top_k=top_k)

    def citations(self, provider_id: str, top_k: Optional[int] = None) -> List[Paper]:
        return self._service.expand_citations(provider_id, self._instance_id, top_k=top_k)

    def paper(self, provider_id: str) -> Optional[Paper]:
        return self._service.get_paper_details(provider_id, self._instance_id)

    def render(self, papers: Sequence[Paper], **kwargs: Any) -> str:
        return self._service.render_for_prompt(papers, self._instance_id, **kwargs)


class ForbiddenLiteratureService:
    """Stand-in handed to methods that must not touch the literature at all.

    IMPLEMENTATION_SPEC.md §30 ("baseline isolation"): the direct judge is
    literature-free. Rather than trusting that by inspection, it receives this
    object, and any attribute access raises.
    """

    def __init__(self, method_name: str):
        object.__setattr__(self, "_method_name", method_name)

    def __getattr__(self, item: str) -> Any:
        from src.common.errors import BaselineIsolationError

        raise BaselineIsolationError(
            "method {!r} must not access the literature service (attempted: {!r})".format(
                object.__getattribute__(self, "_method_name"), item
            )
        )


# --------------------------------------------------------------------------- #
# Wiring
# --------------------------------------------------------------------------- #
def build_crossref_verifier(
    crossref: CrossrefClient, config: AppConfig
) -> Callable[[str], Optional[PartialDate]]:
    """Crossref-based date verifier: earliest public availability for a DOI.

    Returns the `PartialDate` rather than a resolved day, so the filter records
    the granularity Crossref actually provided.
    """

    def verify(doi: str) -> Optional[PartialDate]:
        dates = crossref.get_dates(doi)
        if dates is None:
            return None
        candidates = []
        for partial in dates.dates.values():
            resolved = partial.resolve(
                year_only_day=config.temporal.year_only_day,
                month_only_day=config.temporal.month_only_day,
            )
            if resolved is not None:
                candidates.append((resolved, partial))
        if not candidates:
            return None
        return min(candidates, key=lambda item: item[0])[1]

    return verify


def build_literature_service(
    config: AppConfig,
    cutoff_registry: CutoffRegistry,
    *,
    event_log: Optional[EventLog] = None,
    provider: Optional[LiteratureProvider] = None,
    crossref: Optional[CrossrefClient] = None,
) -> LiteratureSearchService:
    """Construct the provider, cache, verifier and filter into a service."""
    log = event_log or NULL_EVENT_LOG
    if provider is None:
        if config.literature.provider == "semantic_scholar":
            provider = SemanticScholarProvider(config.literature, event_log=log)
        elif config.literature.provider == "mock":
            from src.literature.mock import MockLiteratureProvider

            LOGGER.warning(
                "literature.provider=mock: synthetic records only, not scientific evidence"
            )
            provider = MockLiteratureProvider(config.literature, event_log=log)
        else:
            raise ValueError(
                "unsupported literature provider: {}".format(config.literature.provider)
            )

    verifier = None
    if config.literature.verify_dates_with_crossref != "never":
        crossref = crossref or CrossrefClient(config.crossref, event_log=log)
        verifier = build_crossref_verifier(crossref, config)

    temporal_filter = TemporalFilter(
        config.temporal, config.literature, date_verifier=verifier, event_log=log
    )
    cache = LiteratureCache(config.literature.cache, event_log=log)
    return LiteratureSearchService(
        provider=provider,
        cutoff_registry=cutoff_registry,
        temporal_filter=temporal_filter,
        cache=cache,
        config=config,
        event_log=log,
    )
