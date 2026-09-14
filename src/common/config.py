"""Typed configuration objects loaded from YAML.

IMPLEMENTATION_SPEC.md §28: anything likely to change scientifically is
configuration, not a Python constant. `extra="forbid"` is used so that a typo in
a YAML key fails loudly instead of silently reverting to a default.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

try:  # Python 3.8
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore

from src.common.errors import ConfigError
from src.common.io import read_json, resolve_path


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------- #
# Sections
# --------------------------------------------------------------------------- #
class RunConfig(_Base):
    seed: int = 20260911
    hypothesis_order: Literal["shuffled", "as_loaded"] = "shuffled"
    anonymise_labels: bool = True
    output_root: str = "runs"


class NegativesConfig(_Base):
    pools: List[Literal["model", "fake"]] = Field(default_factory=lambda: ["model"])
    max_negatives: Optional[int] = None

    @field_validator("pools")
    @classmethod
    def _non_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("dataset.negatives.pools must not be empty")
        return v


class DatasetConfig(_Base):
    # instances : an 11-candidate ResearchBench slice (v1 dev20)
    # pairs     : a frozen gold-vs-negative pair slice (v2), loaded as k=2 instances
    # k_sets    : a controlled listwise slice at one k (benchmark/k_slices/),
    #             every negative independently R2-screened; `k_set_path` selects it
    kind: Literal["instances", "pairs", "k_sets"] = "instances"
    # development : for building and debugging the method. Aggregate accuracy on
    #               such a slice is NOT evidence for the method — both v1 and v2
    #               carry artifacts that let a no-science baseline score highly.
    # evaluation  : a slice whose construction protocol was frozen in advance and
    #               whose style diagnostics are clean.
    status: Literal["development", "evaluation"] = "development"
    path: str = "data/researchbench_dev20.jsonl"
    metadata_path: str = "data/metadata/source_dates.jsonl"
    # v1's frozen R2 pair subset over the dev20 instances. Used for the PRIMARY
    # metric when `kind: instances`; it is a metric definition, not a dataset.
    pairs_path: str = "benchmark/dev/pairs_v1.jsonl"
    # The v2 pair slice, loaded as k=2 instances when `kind: pairs`.
    pair_slice_path: str = "benchmark/v2/researchbench_v2_pairs.jsonl"
    # One controlled listwise slice, used when `kind: k_sets`. Build the family
    # with scripts/build_k_slices.py; run one k per run and report stratified by
    # k, never averaged (chance top-1 is 1/k).
    k_set_path: str = "benchmark/k_slices/k3_sets.jsonl"
    negatives: NegativesConfig = Field(default_factory=NegativesConfig)
    require_cutoff: bool = True
    # Also refuse instances whose cutoff resolved but was flagged ambiguous.
    # Off by default: ambiguous cutoffs are conservative (too early), so they are
    # reported rather than dropped.
    require_unambiguous_cutoff: bool = False
    review_sources: "ReviewSourceConfig" = Field(default_factory=lambda: ReviewSourceConfig())


class ReviewSourceConfig(_Base):
    """Excluding review articles as source papers (task validity).

    A review's "gold hypothesis" summarises published work, so the finding is in
    the pre-cutoff literature by construction. Detection is venue/title matching
    because Crossref types reviews as `journal-article`; see
    `src/benchmark/review_sources.py` for what that misses.

    `action` is deliberately explicit: frozen development slices are only
    flagged, while a new evaluation benchmark excludes.
    """

    enabled: bool = True
    action: Literal["flag", "exclude"] = "exclude"
    venue_patterns: List[str] = Field(default_factory=list)
    title_patterns: List[str] = Field(default_factory=list)


class VersionSearchConfig(_Base):
    """Discovery of other versions of the source paper (preprints included).

    Thresholds are deliberately looser than `literature.dedup`: here a false
    positive only moves the cutoff earlier and blocks one DOI (both
    conservative), while a false negative leaves the source study's own text
    inside the eligible window.
    """

    enabled: bool = True
    provider: Literal["crossref"] = "crossref"
    rows: int = Field(default=20, ge=1, le=100)
    title_similarity_threshold: float = 0.75
    # A candidate with no usable author list must match the title almost exactly.
    title_similarity_threshold_no_authors: float = 0.92
    # Author overlap alone never qualifies a record as a version.
    min_author_overlap: int = Field(default=1, ge=1)
    # Share of the smaller author list that must overlap. An alternate version of
    # a study carries essentially the same author list; a different study by an
    # overlapping author does not. On the development slice, true preprint pairs
    # score 0.87-0.97 and same-author-different-study pairs 0.20-0.33.
    min_author_overlap_fraction: float = Field(default=0.5, ge=0.0, le=1.0)
    include_types: List[str] = Field(
        default_factory=lambda: [
            "journal-article",
            "posted-content",
            "proceedings-article",
            "report",
            "dissertation",
        ]
    )


class TemporalConfig(_Base):
    boundary: Literal["inclusive", "exclusive"] = "inclusive"
    unknown_date_policy: Literal["exclude", "include"] = "exclude"
    cutoff_offset_days: int = 1
    include_preprints_in_cutoff_basis: bool = True
    block_source_doi: bool = True
    conflict_policy: Literal["latest", "earliest"] = "latest"
    year_only_day: Literal["first", "last"] = "last"
    month_only_day: Literal["first", "last"] = "last"
    # Crossref links only a minority of preprints to their journal version, so
    # DOI blocking alone does not keep an unlinked preprint of the source paper
    # out of the eligible set. Title matching is the conservative fallback.
    block_source_by_title: bool = True
    source_title_similarity_threshold: float = 0.92
    # Require a shared author before treating a title match as the source study.
    # Prevents an unrelated paper with a similar title from being blocked, and
    # keeps "same authors" from being sufficient on its own.
    block_source_requires_author_overlap: bool = True
    version_search: VersionSearchConfig = Field(default_factory=VersionSearchConfig)


class HTTPConfig(_Base):
    timeout_s: float = 30.0
    max_retries: int = 5
    backoff_base_s: float = 2.0
    backoff_max_s: float = 60.0
    min_request_interval_s: float = 0.0


class LiteratureCacheConfig(_Base):
    enabled: bool = True
    dir: str = "data/cache/literature"
    refresh: bool = False
    offline: bool = False


class DedupConfig(_Base):
    enabled: bool = True
    title_similarity_threshold: float = 0.92
    possibly_related_threshold: float = 0.80
    require_author_overlap: bool = True


class LiteratureConfig(_Base):
    provider: Literal["semantic_scholar", "mock"] = "semantic_scholar"
    include_preprints: bool = True
    top_k: int = Field(default=10, ge=1)
    # Ask the provider for `top_k * overfetch_factor` records so that locally
    # filtered-out results do not shrink the returned set below top_k.
    overfetch_factor: int = Field(default=3, ge=1)
    provider_prefilter_by_date: bool = True
    verify_dates_with_crossref: Literal["never", "boundary_only", "always"] = "always"
    verify_boundary_window_days: int = 180
    abstract_char_limit: int = 2000
    http: HTTPConfig = Field(default_factory=lambda: HTTPConfig(min_request_interval_s=1.1))
    cache: LiteratureCacheConfig = Field(default_factory=LiteratureCacheConfig)
    dedup: DedupConfig = Field(default_factory=DedupConfig)


class SimpleCacheConfig(_Base):
    enabled: bool = True
    dir: str = "data/cache/crossref"


class CrossrefConfig(_Base):
    base_url: str = "https://api.crossref.org"
    mailto: Optional[str] = None
    date_fields: List[str] = Field(
        default_factory=lambda: [
            "published-online",
            "published-print",
            "published",
            "issued",
            "posted",
            "created",
        ]
    )
    # Subset of `date_fields` allowed to *set* the cutoff. None = all of them.
    # `created` is deliberately absent: it is the Crossref deposit timestamp, not
    # a statement of public availability, so it is kept as diagnostic metadata
    # only (it still flags a possible earlier article-in-press).
    cutoff_basis_fields: Optional[List[str]] = Field(
        default_factory=lambda: [
            "published-online",
            "published-print",
            "published",
            "issued",
            "posted",
        ]
    )
    http: HTTPConfig = Field(default_factory=lambda: HTTPConfig(min_request_interval_s=0.2))
    cache: SimpleCacheConfig = Field(default_factory=SimpleCacheConfig)


class LLMConfig(_Base):
    provider: Literal["azure", "mock"] = "azure"
    # None = fall back to $LLM_MODEL, else the built-in default. Resolved by
    # `src.llm.client.resolve_deployment`, which records where it came from.
    deployment: Optional[str] = None
    temperature: float = 0.0
    max_tokens: int = 4096
    top_p: float = 1.0
    seed: Optional[int] = 20260911
    request_timeout_s: float = 120.0
    max_retries: int = 4
    backoff_base_s: float = 2.0
    parse_retries: int = 2
    json_mode: bool = True


class PromptsConfig(_Base):
    dir: str = "src/llm/prompts"
    # NOTE: there is deliberately no `include_cutoff_date` option. The cutoff is
    # enforced by the backend and never rendered into a prompt (§7); a test
    # asserts no template mentions a date.


class DirectJudgeConfig(_Base):
    prompt_version: str = "direct_judge_v2"
    mode: Literal["listwise"] = "listwise"


class QuestionHiddenJudgeConfig(_Base):
    """Direct judge with the scientific question withheld (artifact diagnostic)."""

    prompt_version: str = "direct_judge_no_question_v1"
    mode: Literal["listwise"] = "listwise"


class StyleArtifactConfig(_Base):
    """Surface-feature ranking: the no-science floor."""

    # Any key of `src.baselines.artifact_baselines.surface_features`.
    feature: str = "n_chars"
    prefer: Literal["longest", "shortest"] = "longest"


class DirectRagConfig(_Base):
    query_prompt_version: str = "direct_rag_query_v1"
    assess_prompt_version: str = "direct_rag_assess_v2"
    # `ge=1` matters scientifically: a zero here would silently produce
    # `no_evidence` for every hypothesis instead of an error (spec §29).
    queries_per_hypothesis: int = Field(default=2, ge=1)
    top_k: int = Field(default=10, ge=1)
    max_papers_in_prompt: int = Field(default=10, ge=1)
    # ordinal_map is the primary scoring rule: the ordinal evidence label is
    # mapped through the centralised log-LR table. Ties (e.g. every hypothesis
    # `no_evidence`) are a legitimate outcome, not something to break.
    ranking_signal: Literal["llm_score", "ordinal_map"] = "ordinal_map"
    # Rewrite a support/contradiction label to `no_evidence` when the assessor
    # was shown no papers. The original label is kept in the artifacts.
    enforce_no_evidence_without_papers: bool = True


class BaselinesConfig(_Base):
    direct_judge: DirectJudgeConfig = Field(default_factory=DirectJudgeConfig)
    direct_rag: DirectRagConfig = Field(default_factory=DirectRagConfig)
    question_hidden_judge: QuestionHiddenJudgeConfig = Field(default_factory=QuestionHiddenJudgeConfig)
    style_artifact: StyleArtifactConfig = Field(default_factory=StyleArtifactConfig)


class GraphConfig(_Base):
    """Consequence-graph generation (IMPLEMENTATION_SPEC.md §14)."""

    max_depth: int = Field(default=2, ge=1)
    # Which generation prompt to use. v2 generates atomic, non-contrastive
    # consequences and is the current method; v1 asked each proposition to be
    # discriminative on its own, which collapsed evidence yield at large k
    # (docs/DECISIONS.md #17). v1 is retained for provenance and replay.
    # v3 (multi-level abstraction) is the METHOD as of DECISIONS #35: structural
    # validation on 20 development rows raised evidence yield from 12% at specific
    # nodes to 39-45% at abstracted ones, took zero-yield rows from 8 to 0, and did
    # it without collapsing discriminativeness (median 0.132/0.123/0.123) or
    # dropping a single why_implied link (0 of 258). v1 and v2 remain as ablations.
    generate_prompt: Literal["consequence_generate_v1", "consequence_generate_v2",
                             "consequence_generate_v3"] = "consequence_generate_v3"
    # Root consequences requested per candidate hypothesis. This is the budget
    # that matters: it does not change meaning when k changes, whereas a global
    # node cap silently stops expanding candidates once k grows.
    max_root_consequences_per_hypothesis: int = Field(default=3, ge=1)
    # Total safety cap on pooled propositions, to bound cost if generation
    # misbehaves. It must not be small enough to truncate depth 1 --
    # build_graph refuses before spending anything if it is.
    max_nodes: int = Field(default=80, ge=1)
    # Children per proposition at depth >= 2.
    max_children_per_node: int = Field(default=3, ge=1)
    # none | lexical | llm  (llm is unimplemented: see src/graph/merge.py)
    semantic_merge_mode: Literal["none", "lexical", "llm"] = "lexical"
    # TODO(research): §14 leaves this unresolved. 0.82 is a working placeholder
    # chosen to be conservative — below it, nodes stay separate. It has not been
    # validated, and over-merging is the costlier error for this method.
    merge_threshold: Optional[float] = 0.82


class EvidenceConfig(_Base):
    """Literature assessment of a proposition node.

    `evidence_assess_v1` judges whether the records bear on the proposition, and was
    measured to mean "directly investigates it" 99% of the time, letting unrecorded
    inferential bridges into the evidence label (DECISIONS #25, #28).
    `evidence_assess_v2` judges only DIRECT bearing on the node and routes every
    bridge to the graph edges (DECISIONS #29). v1 remains the default until the
    node-level comparison is in.
    """

    # v2 is the METHOD; v1 is retained as an ablation (DECISIONS #33). v1 was
    # measured to make negative-origin nodes informative 27% of the time against
    # 17% for gold-origin -- implicit bridging favours generic fabricated claims.
    # v2 removes that asymmetry (12% vs 15%).
    assess_prompt: Literal["evidence_assess_v1", "evidence_assess_v2"] = "evidence_assess_v2"


class QueryPolicyConfig(_Base):
    """Deterministic shaping applied to every generated search query.

    Measured on the dev slice: Semantic Scholar returns 2 results for a ten-word
    query, 39 for five words, 252 for three. The cap is what makes generated
    queries retrievable at all; the direction-word rule keeps them
    outcome-neutral (spec §17).
    """

    # Hard cap on content words. Enforced in code — the prompt only asks.
    max_terms: int = Field(default=6, ge=1)
    # Backoff never shortens a query below this.
    min_terms: int = Field(default=3, ge=1)
    # Extra searches allowed when a query returns zero provider results.
    # 0 disables lexical backoff.
    backoff_steps: int = Field(default=2, ge=0)
    strip_direction_words: bool = True
    # Words that encode the outcome the searcher wants. Stripped as standalone
    # tokens only, never inside a protected phrase.
    direction_words: List[str] = Field(
        default_factory=lambda: [
            "increase", "increases", "increased", "increasing",
            "decrease", "decreases", "decreased", "decreasing",
            "higher", "lower", "elevated", "reduces", "reduction",
            "enhance", "enhances", "enhanced", "enhancement",
            "improve", "improves", "improved", "impair", "impairs", "impaired",
            "worsen", "worsens", "worsened",
            "support", "supports", "supporting", "supported",
            "refute", "refutes", "confirm", "confirms", "confirmed",
            "prove", "proves", "proven", "proof",
            "evidence", "demonstrates", "demonstrate", "shows", "show",
            "cause", "causes", "caused", "causing",
        ]
    )
    # Entity names that legitimately contain a direction word. Matched before
    # the token pass, so "reduced graphene oxide" survives intact.
    protected_phrases: List[str] = Field(
        default_factory=lambda: [
            "reduced graphene oxide",
            "increased intracranial pressure",
            "reduced glutathione",
        ]
    )
    # Function words: no outcome, but they consume slots under the cap.
    stopwords: List[str] = Field(
        default_factory=lambda: [
            "a", "an", "the", "of", "in", "on", "for", "and", "or", "with",
            "that", "this", "these", "those", "to", "from", "by", "as", "at",
            "its", "their", "between", "during", "via", "using", "based",
        ]
    )


class RetrievalConfig(_Base):
    """Retrieval policy shared by every literature-based method."""

    # Milestone 2 (consequence graph); unused in milestone 1.
    queries_per_node: int = 2
    query_policy: QueryPolicyConfig = Field(default_factory=QueryPolicyConfig)


class InferenceConfig(_Base):
    # independent : every observed node contributes its own likelihood term against
    #               H directly (spec §21's conditional-independence shortcut).
    # family      : each root consequence family (a depth-1 proposition plus its
    #               chain descendants) is ONE dependent evidence unit, marginalised
    #               exactly over its latent X nodes; families are then combined under
    #               conditional independence. Motivated empirically, not
    #               aesthetically: under `independent`, rows with MORE informative
    #               nodes became LESS stable under edge-label perturbation, which is
    #               the signature of double-counting correlated descendants
    #               (DECISIONS #36-37).
    aggregation: Literal["independent", "family"] = "independent"

    """Bayesian propagation (IMPLEMENTATION_SPEC.md §22)."""

    prior: Literal["uniform"] = "uniform"
    # How several routes from one hypothesis to one proposition combine.
    #   noisy_or : any route suffices (default)
    #   max      : the strongest route
    #   mean     : average of the routes
    # TODO(research): §22 leaves this unresolved; all three are implemented so
    # the choice can be made on evidence rather than on what was easy to write.
    multi_parent_rule: Literal["noisy_or", "max", "mean"] = "noisy_or"
    # P(X_v = 1 | X_parent = 0): what a proposition's probability falls back to
    # when its parent does not hold. 0.5 = "the parent being false tells us
    # nothing", which is the conservative reading of an uncertain implication.
    # TODO(research): also unvalidated.
    parent_false_baseline: float = Field(default=0.5, ge=0.0, le=1.0)


class CostConfig(_Base):
    """Cost accounting and the spend guard."""

    pricing_path: str = "configs/pricing.yaml"
    # Event logs the ledger merges from. Instance-level logs are excluded on
    # purpose: the runner tees each call into both, so scanning them would
    # double-count.
    event_sources: List[str] = Field(
        default_factory=lambda: ["runs/*/events.jsonl", "benchmark/*/*_events.jsonl"]
    )
    # Project spend cap in USD. null = track but never block.
    budget_usd: Optional[float] = None
    # What to do when the project total already exceeds the budget at run start.
    #   warn   : log loudly and continue
    #   refuse : raise before any model call is made
    on_exceed: Literal["warn", "refuse"] = "warn"


class AppConfig(_Base):
    run: RunConfig = Field(default_factory=RunConfig)
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    temporal: TemporalConfig = Field(default_factory=TemporalConfig)
    literature: LiteratureConfig = Field(default_factory=LiteratureConfig)
    crossref: CrossrefConfig = Field(default_factory=CrossrefConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    prompts: PromptsConfig = Field(default_factory=PromptsConfig)
    evidence: EvidenceConfig = Field(default_factory=EvidenceConfig)
    baselines: BaselinesConfig = Field(default_factory=BaselinesConfig)
    ordinal_mappings_path: str = "configs/ordinal_mappings.yaml"
    cost: CostConfig = Field(default_factory=CostConfig)
    graph: GraphConfig = Field(default_factory=GraphConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    inference: InferenceConfig = Field(default_factory=InferenceConfig)

    # Provenance of this configuration object; filled in by `load_config`.
    source_path: Optional[str] = None

    def dump(self) -> Dict[str, Any]:
        return self.model_dump(mode="json")


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_update(out[key], value)
        else:
            out[key] = value
    return out


def _coerce_scalar(text: str) -> Any:
    """Parse a CLI override value using YAML scalar rules (true/1.5/null/str)."""
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return text


def parse_override(item: str) -> Dict[str, Any]:
    """Turn `a.b.c=value` into a nested dict."""
    if "=" not in item:
        raise ConfigError("override must look like key.path=value, got: {!r}".format(item))
    path, _, raw = item.partition("=")
    keys = [k for k in path.strip().split(".") if k]
    if not keys:
        raise ConfigError("empty override key in {!r}".format(item))
    node: Dict[str, Any] = {}
    cursor = node
    for key in keys[:-1]:
        cursor[key] = {}
        cursor = cursor[key]
    cursor[keys[-1]] = _coerce_scalar(raw)
    return node


def load_config(
    path: "str | Path",
    *,
    overrides: Optional[List[str]] = None,
) -> AppConfig:
    """Load a YAML config, apply `key.path=value` overrides, and validate."""
    config_path = resolve_path(path)
    if not config_path.exists():
        raise ConfigError("config file not found: {}".format(config_path))
    with config_path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    if not isinstance(raw, dict):
        raise ConfigError("config root must be a mapping: {}".format(config_path))
    for item in overrides or []:
        raw = _deep_update(raw, parse_override(item))
    raw.setdefault("source_path", str(config_path))
    try:
        return AppConfig(**raw)
    except Exception as exc:  # pydantic ValidationError
        raise ConfigError("invalid configuration in {}: {}".format(config_path, exc))


def load_yaml(path: "str | Path") -> Dict[str, Any]:
    p = resolve_path(path)
    if not p.exists():
        raise ConfigError("file not found: {}".format(p))
    if p.suffix == ".json":
        return read_json(p)
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ConfigError("expected a mapping in {}".format(p))
    return data
