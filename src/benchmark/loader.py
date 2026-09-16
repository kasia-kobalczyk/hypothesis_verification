"""Loader for the frozen ResearchBench 20-case development slice.

IMPLEMENTATION_SPEC.md §2. The raw JSONL is treated as read-only ground truth:

* hypothesis and question text are copied **verbatim** — no stripping, no
  normalisation, no canonicalisation (§2, §34);
* the frozen slice is never rewritten; temporal metadata is joined at load time
  from `data/metadata/source_dates.jsonl`;
* more than two candidate hypotheses are supported (the slice has 1 gold + 10
  raw ResearchBench negatives per item).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from src.benchmark.temporal import (
    CutoffInfo,
    CutoffRegistry,
    SourceDateRecord,
    load_source_date_records,
)
from src.common.config import AppConfig, DatasetConfig
from src.common.errors import BenchmarkDataError
from src.common.io import read_jsonl, resolve_path
from src.common.logging_utils import get_logger
from src.literature.crossref import normalise_doi

LOGGER = get_logger("benchmark.loader")

POOL_FIELDS = {
    "model": "model_negative_hypotheses",
    "fake": "fake_negative_hypotheses",
}


class Hypothesis(BaseModel):
    """One candidate hypothesis, text preserved verbatim from ResearchBench."""

    model_config = ConfigDict(extra="forbid")

    id: str
    text: str
    gold: bool = False
    # Provenance inside the original ResearchBench row.
    source_field: str = ""
    source_index: Optional[int] = None


class BenchmarkInstance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    researchbench_sample_id: str
    question: str
    hypotheses: List[Hypothesis]
    source_doi: str

    # Joined temporal metadata (never stored in the frozen slice itself).
    cutoff_date: Optional[date] = None
    cutoff_basis: Optional[str] = None
    cutoff_ambiguous: bool = False
    cutoff_notes: Optional[str] = None
    blocked_dois: List[str] = Field(default_factory=list)
    source_title: Optional[str] = None
    source_authors: List[str] = Field(default_factory=list)
    # Anything the loader had to skip or could not join; surfaced in artifacts.
    load_warnings: List[str] = Field(default_factory=list)

    # ResearchBench bookkeeping
    discipline: Optional[str] = None
    screen_rank: Optional[int] = None
    source_variant: Optional[str] = None

    # Untouched original row, for auditing.
    raw: Dict[str, Any] = Field(default_factory=dict, repr=False)

    @property
    def hypothesis_ids(self) -> List[str]:
        return [h.id for h in self.hypotheses]

    @property
    def gold_hypothesis(self) -> Hypothesis:
        gold = [h for h in self.hypotheses if h.gold]
        if len(gold) != 1:
            raise BenchmarkDataError(
                "instance {} has {} gold hypotheses, expected exactly 1".format(self.id, len(gold))
            )
        return gold[0]

    @property
    def has_gold(self) -> bool:
        """Some benchmarks carry no gold at all.

        The explanatory-hypothesis benchmark (BENCH-GRAPH-PILOT-001) resolves cases as
        favored / mixed / regime_dependent / component_wise, and the resolution is a
        HIDDEN annotation. Marking a winner in the verifier-visible dataset would embed
        the answer in the benchmark input, so these instances carry none and
        gold-dependent metrics are skipped rather than fabricated.
        """
        return sum(1 for h in self.hypotheses if h.gold) == 1

    def hypothesis(self, hypothesis_id: str) -> Hypothesis:
        for h in self.hypotheses:
            if h.id == hypothesis_id:
                return h
        raise KeyError("unknown hypothesis {!r} in instance {}".format(hypothesis_id, self.id))

    @property
    def has_cutoff(self) -> bool:
        return self.cutoff_date is not None

    def cutoff_info(self) -> CutoffInfo:
        return CutoffInfo(
            instance_id=self.id,
            source_doi=normalise_doi(self.source_doi),
            cutoff_date=self.cutoff_date,
            basis=self.cutoff_basis,
            ambiguous=self.cutoff_ambiguous,
            blocked_dois=frozenset(self.blocked_dois),
            notes=self.cutoff_notes,
            source_title=self.source_title,
            source_authors=frozenset(self.source_authors),
        )

    def input_record(self) -> Dict[str, Any]:
        """Serialisable snapshot written to `runs/<id>/instances/<iid>/input.json`."""
        return {
            "id": self.id,
            "researchbench_sample_id": self.researchbench_sample_id,
            "question": self.question,
            "hypotheses": [h.model_dump(mode="json") for h in self.hypotheses],
            "source_doi": self.source_doi,
            "cutoff_date": self.cutoff_date.isoformat() if self.cutoff_date else None,
            "cutoff_basis": self.cutoff_basis,
            "cutoff_ambiguous": self.cutoff_ambiguous,
            "cutoff_notes": self.cutoff_notes,
            "blocked_dois": list(self.blocked_dois),
            "source_title": self.source_title,
            "source_authors": list(self.source_authors),
            "load_warnings": list(self.load_warnings),
            "discipline": self.discipline,
            "screen_rank": self.screen_rank,
            "source_variant": self.source_variant,
        }


# --------------------------------------------------------------------------- #
def _build_hypotheses(
    row: Dict[str, Any],
    cfg: DatasetConfig,
    instance_id: str,
    warnings: List[str],
) -> List[Hypothesis]:
    gold_text = row.get("gold_hypothesis")
    if not isinstance(gold_text, str) or not gold_text:
        raise BenchmarkDataError("{}: missing gold_hypothesis".format(instance_id))

    hypotheses = [
        Hypothesis(id="H0", text=gold_text, gold=True, source_field="gold_hypothesis", source_index=None)
    ]

    next_index = 1
    for pool in cfg.negatives.pools:
        field = POOL_FIELDS[pool]
        values = row.get(field) or []
        if not isinstance(values, list):
            raise BenchmarkDataError("{}: {} is not a list".format(instance_id, field))
        kept = values if cfg.negatives.max_negatives is None else values[: cfg.negatives.max_negatives]
        for offset, text in enumerate(kept):
            if not isinstance(text, str) or not text:
                # Never silent: the slice is meant to be preserved verbatim, so a
                # dropped candidate has to show up in the run artifacts.
                message = "dropped malformed negative {}[{}]".format(field, offset)
                LOGGER.warning("%s: %s", instance_id, message)
                warnings.append(message)
                continue
            hypotheses.append(
                Hypothesis(
                    id="H{}".format(next_index),
                    text=text,  # verbatim
                    gold=False,
                    source_field=field,
                    source_index=offset,
                )
            )
            next_index += 1

    if len(hypotheses) < 2:
        raise BenchmarkDataError(
            "{}: need at least 2 candidate hypotheses, got {}".format(instance_id, len(hypotheses))
        )
    return hypotheses


def _attach_metadata(instance: BenchmarkInstance, record: Optional[SourceDateRecord]) -> None:
    if record is None:
        instance.cutoff_ambiguous = True
        instance.cutoff_notes = (
            "no temporal metadata resolved for this DOI; run "
            "`python -m src.benchmark.resolve_dates`"
        )
        instance.blocked_dois = [d for d in [normalise_doi(instance.source_doi)] if d]
        return
    instance.cutoff_date = record.cutoff_date
    instance.cutoff_basis = record.selected_cutoff_basis
    instance.cutoff_ambiguous = record.ambiguous
    instance.cutoff_notes = record.notes
    instance.source_title = record.source_title
    instance.source_authors = list(record.source_authors)
    blocked = set(record.blocked_dois)
    source = normalise_doi(instance.source_doi)
    if source:
        blocked.add(source)
    instance.blocked_dois = sorted(blocked)


def load_instances(
    config: AppConfig,
    *,
    instance_ids: Optional[Sequence[str]] = None,
    dataset_path: Optional["str | Path"] = None,
    metadata_path: Optional["str | Path"] = None,
) -> List[BenchmarkInstance]:
    """Load the development slice and join its frozen temporal metadata."""
    path = resolve_path(dataset_path or config.dataset.path)
    if not path.exists():
        raise BenchmarkDataError("dataset not found: {}".format(path))

    meta_path = resolve_path(metadata_path or config.dataset.metadata_path)
    records: Dict[str, SourceDateRecord] = {}
    if meta_path.exists():
        records = load_source_date_records(meta_path)
        LOGGER.info("loaded temporal metadata for %d DOIs from %s", len(records), meta_path)
    else:
        LOGGER.warning(
            "temporal metadata file %s not found; instances will have no cutoff date", meta_path
        )

    wanted = set(instance_ids) if instance_ids else None
    instances: List[BenchmarkInstance] = []
    seen: set = set()

    for row in read_jsonl(path):
        instance_id = row.get("dev_id") or row.get("id")
        if not instance_id:
            raise BenchmarkDataError("{}: row without dev_id".format(path))
        if instance_id in seen:
            raise BenchmarkDataError("duplicate instance id {!r} in {}".format(instance_id, path))
        seen.add(instance_id)
        if wanted is not None and instance_id not in wanted:
            continue

        doi = row.get("doi") or ""
        warnings: List[str] = []
        instance = BenchmarkInstance(
            id=instance_id,
            researchbench_sample_id=row.get("sample_id") or "",
            question=row.get("research_question") or "",
            hypotheses=_build_hypotheses(row, config.dataset, instance_id, warnings),
            load_warnings=warnings,
            source_doi=doi,
            discipline=row.get("discipline"),
            screen_rank=row.get("screen_rank"),
            source_variant=row.get("source_variant"),
            raw=row,
        )
        _attach_metadata(instance, records.get(normalise_doi(doi) or doi))
        instances.append(instance)

    if wanted is not None:
        missing = wanted - {i.id for i in instances}
        if missing:
            raise BenchmarkDataError("unknown instance id(s): {}".format(sorted(missing)))

    LOGGER.info("loaded %d instances from %s", len(instances), path)
    return instances


def load_pair_instances(
    config: AppConfig,
    *,
    instance_ids: Optional[Sequence[str]] = None,
    dataset_path: Optional["str | Path"] = None,
    limit: Optional[int] = None,
) -> List[BenchmarkInstance]:
    """Load a frozen pair slice (v2) as two-candidate instances.

    A pair is an instance with k=2: gold plus one screened negative. That matters
    for the consequence verifier, whose node budget is spent per candidate — with
    eleven candidates, depth 1 alone exceeds `graph.max_nodes`.

    Temporal metadata is joined from `data/metadata/source_dates.jsonl` when the
    DOI is present there, so blocked DOIs and the source title still reach the
    literature filter; the pair's own `cutoff_date` is the fallback.
    """
    path = resolve_path(dataset_path or config.dataset.pair_slice_path)
    if not path.exists():
        raise BenchmarkDataError("pair slice not found: {}".format(path))

    meta_path = resolve_path(config.dataset.metadata_path)
    records: Dict[str, SourceDateRecord] = (
        load_source_date_records(meta_path) if meta_path.exists() else {}
    )

    wanted = set(instance_ids) if instance_ids else None
    instances: List[BenchmarkInstance] = []
    for row in read_jsonl(path):
        pair_id = row.get("pair_id")
        if not pair_id:
            raise BenchmarkDataError("{}: row without pair_id".format(path))
        if wanted is not None and pair_id not in wanted:
            continue
        instance = BenchmarkInstance(
            id=pair_id,
            researchbench_sample_id=row.get("researchbench_sample_id") or "",
            question=row.get("question") or "",
            hypotheses=[
                Hypothesis(id="H0", text=row["gold_hypothesis"], gold=True,
                           source_field="gold_hypothesis"),
                Hypothesis(id="H1", text=row["negative_hypothesis"], gold=False,
                           source_field="negative_hypothesis",
                           source_index=row.get("negative_index")),
            ],
            source_doi=row.get("doi") or "",
            discipline=row.get("discipline"),
            raw=row,
        )
        record = records.get(normalise_doi(instance.source_doi) or "")
        _attach_metadata(instance, record)
        if instance.cutoff_date is None and row.get("cutoff_date"):
            # The pair carries the cutoff resolved when the slice was frozen.
            from datetime import date as _date

            instance.cutoff_date = _date.fromisoformat(row["cutoff_date"])
            instance.cutoff_notes = "cutoff taken from the frozen pair record"
        instances.append(instance)
        if limit is not None and len(instances) >= limit:
            break

    if wanted is not None:
        missing = wanted - {i.id for i in instances}
        if missing:
            raise BenchmarkDataError("unknown pair id(s): {}".format(sorted(missing)))
    LOGGER.info("loaded %d pair instance(s) from %s", len(instances), path)
    return instances


def load_k_set_instances(
    config: AppConfig,
    *,
    dataset_path: "str | Path",
    instance_ids: Optional[Sequence[str]] = None,
    limit: Optional[int] = None,
) -> List[BenchmarkInstance]:
    """Load a controlled listwise slice (`benchmark/k_slices/k<N>_sets.jsonl`).

    Same shape as the pair loader, generalised to k-1 negatives. The sets are
    nested across k by construction, so `H1` at k=3 is the same hypothesis as `H1`
    at k=2 for the same row -- which is what makes a k-scaling comparison
    within-row rather than confounded by which negatives were drawn.
    """
    path = resolve_path(dataset_path)
    if not path.exists():
        raise BenchmarkDataError("k-set slice not found: {}".format(path))

    meta_path = resolve_path(config.dataset.metadata_path)
    records: Dict[str, SourceDateRecord] = (
        load_source_date_records(meta_path) if meta_path.exists() else {}
    )

    wanted = set(instance_ids) if instance_ids else None
    instances: List[BenchmarkInstance] = []
    for row in read_jsonl(path):
        set_id = row.get("instance_id")
        if not set_id:
            raise BenchmarkDataError("{}: row without instance_id".format(path))
        if wanted is not None and set_id not in wanted:
            continue
        hypotheses = [Hypothesis(id="H0", text=row["gold_hypothesis"], gold=True,
                                 source_field="gold_hypothesis")]
        for index, negative in enumerate(row.get("negatives") or [], start=1):
            hypotheses.append(Hypothesis(
                id="H{}".format(index), text=negative["text"], gold=False,
                source_field=negative.get("source_field") or "model_negative_hypotheses",
                source_index=negative.get("source_index")))
        if len(hypotheses) != int(row.get("k") or len(hypotheses)):
            raise BenchmarkDataError(
                "{}: {} declares k={} but carries {} candidate(s)".format(
                    path, set_id, row.get("k"), len(hypotheses)))
        instance = BenchmarkInstance(
            id=set_id,
            researchbench_sample_id=row.get("row_id") or "",
            question=row.get("question") or "",
            hypotheses=hypotheses,
            source_doi=row.get("doi") or "",
            discipline=row.get("discipline"),
            raw=row,
        )
        _attach_metadata(instance, records.get(normalise_doi(instance.source_doi) or ""))
        if instance.cutoff_date is None and row.get("cutoff_date"):
            from datetime import date as _date

            instance.cutoff_date = _date.fromisoformat(row["cutoff_date"])
            instance.cutoff_notes = "cutoff taken from the frozen k-set record"
        instances.append(instance)
        if limit is not None and len(instances) >= limit:
            break

    if wanted is not None:
        missing = wanted - {i.id for i in instances}
        if missing:
            raise BenchmarkDataError("unknown k-set id(s): {}".format(sorted(missing)))
    LOGGER.info("loaded %d k-set instance(s) from %s", len(instances), path)
    return instances


# --------------------------------------------------------------------------- #
# Hard projection for the explanatory-hypothesis benchmark
# --------------------------------------------------------------------------- #
# The benchmark is split into two files: `cases_visible.jsonl`, which the verifier
# may see, and `cases_hidden.json`, which holds the resolving study, the resolution
# label and the reference discriminators. Keeping them in separate files is a
# convention; this whitelist is the enforcement.
#
# The loader projects every row down to these keys and REFUSES any key it does not
# know. So if a hidden annotation is ever pasted into the visible file -- by a merge,
# a regenerated manifest, or a well-meaning edit -- the run fails at load time
# instead of quietly carrying the answer into the model's context. A whitelist fails
# closed on fields nobody has thought of yet; a blacklist would not.
VISIBLE_CASE_FIELDS = frozenset({
    "case_id", "domain", "phenomenon", "cutoff", "hypotheses",
})
VISIBLE_HYPOTHESIS_FIELDS = frozenset({"hypothesis_id", "text"})


def project_visible_case(row: Dict[str, Any], *, where: str) -> Dict[str, Any]:
    """Return `row` restricted to verifier-visible fields, or raise.

    Raises rather than dropping: a silently dropped field looks identical to a field
    that was never there, and the difference matters when the thing dropped is the
    answer.
    """
    unknown = sorted(set(row) - VISIBLE_CASE_FIELDS)
    if unknown:
        raise BenchmarkDataError(
            "{}: case {} carries non-visible field(s) {}. The verifier-visible "
            "dataset may contain only {}. Hidden annotations belong in "
            "cases_hidden.json, which the loader never opens.".format(
                where, row.get("case_id", "?"), unknown,
                sorted(VISIBLE_CASE_FIELDS)))
    hypotheses = []
    for hyp in row.get("hypotheses") or []:
        unknown_h = sorted(set(hyp) - VISIBLE_HYPOTHESIS_FIELDS)
        if unknown_h:
            raise BenchmarkDataError(
                "{}: case {} hypothesis {} carries non-visible field(s) {}".format(
                    where, row.get("case_id", "?"), hyp.get("hypothesis_id", "?"),
                    unknown_h))
        hypotheses.append({k: hyp[k] for k in VISIBLE_HYPOTHESIS_FIELDS if k in hyp})
    projected = {k: row[k] for k in VISIBLE_CASE_FIELDS if k in row}
    projected["hypotheses"] = hypotheses
    return projected


def load_case_instances(
    config: AppConfig,
    *,
    dataset_path: "str | Path",
    instance_ids: Optional[Sequence[str]] = None,
    limit: Optional[int] = None,
) -> List[BenchmarkInstance]:
    """Load the explanatory-hypothesis benchmark (BENCH-GRAPH-PILOT-001).

    Differs from the ResearchBench loaders in three ways, all forced by the benchmark
    rather than chosen:

    * **The cutoff is frozen in the record**, not resolved from Crossref. These are
      curated historical cutoffs tied to a specific scientific dispute, and
      re-deriving them from publication metadata would change their meaning.
    * **No gold hypothesis.** The resolution is a hidden annotation, and half the
      cases resolve mixed / regime-dependent / component-wise. Marking a winner here
      would put the answer in the verifier input.
    * **No source DOI.** The "source" would be the post-cutoff resolver, which must
      not appear in verifier context at all. Temporal safety comes from the frozen
      cutoff date, which every resolver postdates.

    Only verifier-visible fields are read. The hidden annotations live in a separate
    file that this function never opens.
    """
    path = resolve_path(dataset_path)
    if not path.exists():
        raise BenchmarkDataError("case slice not found: {}".format(path))

    wanted = set(instance_ids) if instance_ids else None
    instances: List[BenchmarkInstance] = []
    for row in read_jsonl(path):
        case_id = row.get("case_id")
        if not case_id:
            raise BenchmarkDataError("{}: row without case_id".format(path))
        if wanted is not None and case_id not in wanted:
            continue
        row = project_visible_case(row, where=str(path))
        hypotheses = [
            Hypothesis(id=h["hypothesis_id"], text=h["text"], gold=False,
                       source_field="frozen_manifest", source_index=index)
            for index, h in enumerate(row.get("hypotheses") or [])
        ]
        if len(hypotheses) < 2:
            raise BenchmarkDataError(
                "{}: case {} has {} hypotheses, expected >= 2".format(
                    path, case_id, len(hypotheses)))
        instance = BenchmarkInstance(
            id=case_id,
            researchbench_sample_id="",
            question=row.get("phenomenon") or "",
            hypotheses=hypotheses,
            source_doi="",
            discipline=row.get("domain"),
            raw=row,
        )
        from datetime import date as _date

        cutoff = row.get("cutoff")
        if not cutoff:
            raise BenchmarkDataError("{}: case {} has no cutoff".format(path, case_id))
        instance.cutoff_date = _date.fromisoformat(cutoff)
        instance.cutoff_basis = "frozen_benchmark_manifest"
        instance.cutoff_notes = (
            "cutoff frozen in the benchmark manifest; not derived from publication "
            "metadata. Every resolving study postdates it.")
        instances.append(instance)
        if limit is not None and len(instances) >= limit:
            break

    if wanted is not None:
        missing = wanted - {i.id for i in instances}
        if missing:
            raise BenchmarkDataError("unknown case id(s): {}".format(sorted(missing)))
    LOGGER.info("loaded %d explanatory case(s) from %s", len(instances), path)
    return instances


def build_cutoff_registry(instances: Iterable[BenchmarkInstance]) -> CutoffRegistry:
    """Freeze the per-instance temporal constraints used by the literature layer."""
    return CutoffRegistry(instance.cutoff_info() for instance in instances)
