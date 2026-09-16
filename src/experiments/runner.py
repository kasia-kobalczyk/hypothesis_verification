"""Common experiment runner (IMPLEMENTATION_SPEC.md §24, §9).

Every run creates a self-contained artifact directory:

    runs/<run_id>/
        config.yaml          resolved configuration actually used
        manifest.json        dataset, prompts + hashes, env presence, versions
        events.jsonl         structured log of API calls and decisions
        errors.jsonl         every recorded error, across instances
        metrics.json         per-instance metric rows
        summary.json         aggregate metrics
        summary.md
        instances/<id>/
            input.json, presentation.json, prompts.json, queries.json,
            retrieval.json, evidence.json, model_outputs.json, scores.json,
            events.jsonl, report.md

`TemporalLeakError` is never caught here: a leak invalidates the experiment, so
the run aborts loudly instead of recording a failed instance.
"""

from __future__ import annotations

import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Type

import yaml

from src.baselines.artifact_baselines import QuestionHiddenJudge, StyleArtifactBaseline
from src.baselines.direct_judge import DirectJudge
from src.baselines.direct_rag import DirectRag
from src.methods.consequence_graph import ConsequenceGraphVerifier
from src.benchmark.loader import (
    BenchmarkInstance,
    build_cutoff_registry,
    load_instances,
    load_case_instances,
    load_k_set_instances,
    load_pair_instances,
)
from src.benchmark.pairs import load_pair_subset
from src.benchmark.presentation import build_presentation
from src.common.config import AppConfig
from src.common.env import (
    AZURE_BASE_VARS,
    AZURE_KEY_VARS,
    AZURE_VERSION_VARS,
    CROSSREF_MAILTO_VARS,
    S2_KEY_VARS,
    env_presence,
)
from src.common.errors import BudgetExceededError, MissingCutoffError, TemporalLeakError
from src.common.io import (
    append_jsonl,
    ensure_dir,
    file_hash,
    resolve_path,
    stable_hash,
    utc_now_iso,
    write_json,
)
from src.common.logging_utils import EventLog, TeeEventLog, get_logger
from src.experiments.base import InstanceContext, InstanceResult, Method
from src.experiments.metrics import aggregate_metrics, instance_metrics
from src.experiments.reports import render_instance_report, render_run_summary
from src.inference.parameters import load_ordinal_mappings
from src.literature.service import (
    ForbiddenLiteratureService,
    InstanceSearchTool,
    build_literature_service,
)
from src.llm.client import build_llm_client, resolve_deployment

LOGGER = get_logger("experiments.runner")

METHODS: Dict[str, Type[Method]] = {
    # Closed-book judge: also the explicit parametric-memorisation diagnostic.
    "direct_judge": DirectJudge,
    "direct_rag": DirectRag,
    # Artifact diagnostics: what the ranking signal is worth without the
    # question, and without any science at all.
    "question_hidden_judge": QuestionHiddenJudge,
    "style_artifact": StyleArtifactBaseline,
    # The proposed method (milestone 2).
    "consequence_graph": ConsequenceGraphVerifier,
}

# Artifacts the runner knows how to write, in a stable order.
ARTIFACT_FILES = (
    "prompts",
    "queries",
    "retrieval",
    "evidence",
    "model_outputs",
    "graph",
    "edge_judgments",
    "scores",
    "yield_by_origin",
)


def build_method(name: str, config: AppConfig) -> Method:
    if name not in METHODS:
        raise KeyError("unknown method {!r}; available: {}".format(name, sorted(METHODS)))
    return METHODS[name](config)


def _interpretation_warning(status: str) -> "str | None":
    if status == "evaluation":
        return None
    if status == "pilot_diagnostic":
        return (
            "DIAGNOSTIC PILOT: this run is a behavioural observation, not a "
            "performance measurement. The benchmark carries no gold hypothesis, so "
            "no accuracy is computed; the ranking is a record of what the method "
            "did. Nothing in the method may be tuned on these cases afterwards."
        )
    return (
        "DEVELOPMENT SET: aggregate accuracy here is not evidence for the method. "
        "Compare against the style_artifact and question_hidden_judge floors."
    )


class ExperimentRunner:
    def __init__(
        self,
        config: AppConfig,
        method_name: str,
        *,
        instance_ids: Optional[Sequence[str]] = None,
        run_id: Optional[str] = None,
        label: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        self.config = config
        self.method_name = method_name
        self.method = build_method(method_name, config)
        self.instance_ids = list(instance_ids) if instance_ids else None
        self.limit = limit
        self.label = label
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        digest = stable_hash(config.dump(), length=8)
        self.run_id = run_id or "{}_{}_{}".format(method_name, timestamp, digest)
        self.run_dir = ensure_dir(resolve_path(config.run.output_root) / self.run_id)
        self.event_log = EventLog(self.run_dir / "events.jsonl")
        self.deployment, self.deployment_source = resolve_deployment(config.llm)

    # ------------------------------------------------------------------ #
    def _write_manifest(self, instances: List[BenchmarkInstance]) -> Dict[str, Any]:
        dataset_path = resolve_path(self.config.dataset.path)
        prompt_names = self.method.prompt_versions()
        from src.llm.prompts import PromptLibrary

        prompts = PromptLibrary(self.config.prompts.dir)
        manifest = {
            "run_id": self.run_id,
            "label": self.label,
            "method": self.method_name,
            "started_at": utc_now_iso(),
            "dataset": {
                "kind": self.config.dataset.kind,
                "status": self.config.dataset.status,
                "path": str(dataset_path),
                "sha256_16": file_hash(dataset_path) if dataset_path.exists() else None,
                "n_instances": len(instances),
                "instance_ids": [i.id for i in instances],
                "negative_pools": list(self.config.dataset.negatives.pools),
                "max_negatives": self.config.dataset.negatives.max_negatives,
            },
            "prompts": prompts.manifest(prompt_names),
            "llm": {
                "provider": self.config.llm.provider,
                "deployment": self.deployment,
                "deployment_source": self.deployment_source,
                "temperature": self.config.llm.temperature,
                "seed": self.config.llm.seed,
            },
            "literature": {
                "provider": self.config.literature.provider,
                "top_k": self.config.literature.top_k,
                "cache": self.config.literature.cache.model_dump(mode="json"),
                "verify_dates_with_crossref": self.config.literature.verify_dates_with_crossref,
            },
            "temporal_policy": self.config.temporal.model_dump(mode="json"),
            "ordinal_mappings": self.config.ordinal_mappings_path,
            "pairs": self._pairs_manifest(),
            "env_present": dict(
                env_presence(*(AZURE_KEY_VARS + AZURE_BASE_VARS + AZURE_VERSION_VARS + S2_KEY_VARS + CROSSREF_MAILTO_VARS))
            ),
            "cutoffs": {
                i.id: {
                    "cutoff_date": i.cutoff_date.isoformat() if i.cutoff_date else None,
                    "basis": i.cutoff_basis,
                    "ambiguous": i.cutoff_ambiguous,
                }
                for i in instances
            },
        }
        write_json(self.run_dir / "manifest.json", manifest)
        return manifest

    def _check_budget(self) -> Dict[str, Any]:
        """Report spend to date, and honour the configured cap before spending more."""
        from src.experiments.costs import CostLedger, DEFAULT_SOURCES, load_pricing, summarise

        cost_config = self.config.cost
        try:
            ledger = CostLedger(pricing=load_pricing(cost_config.pricing_path))
            ledger.scan(tuple(cost_config.event_sources) or DEFAULT_SOURCES)
            summary = summarise(ledger, budget_usd=cost_config.budget_usd)
        except Exception as exc:  # cost tracking must never block a run by failing
            LOGGER.warning("cost ledger unavailable (%s); continuing without a budget check", exc)
            return {"available": False, "error": str(exc)}

        spent = summary["totals"]["cost_usd"]
        budget = summary["budget"]
        LOGGER.info(
            "spend to date: $%.4f over %d call(s)%s",
            spent, summary["totals"]["calls"],
            "" if summary["pricing"]["verified"] else " (estimate; rates unverified)",
        )
        if budget.get("budget_usd") and budget["status"] in ("serious", "critical"):
            message = "project spend ${:.2f} is {:.0%} of the ${:.2f} budget".format(
                spent, budget["fraction"], budget["budget_usd"]
            )
            if budget["status"] == "critical" and cost_config.on_exceed == "refuse":
                raise BudgetExceededError(
                    message + "; refusing to start (cost.on_exceed=refuse). Raise "
                    "cost.budget_usd or clear it to continue."
                )
            LOGGER.warning("%s", message)
        self.event_log.emit("budget_check", spent_usd=spent, budget=budget,
                            pricing_verified=summary["pricing"]["verified"])
        return {"available": True, "spent_usd_before_run": spent, "budget": budget}

    def _run_cost(self) -> Dict[str, Any]:
        """Cost of this run alone, priced from its own event log."""
        from src.experiments.costs import CostLedger, load_pricing, summarise

        try:
            # Scan this run's own log wherever it lives: `run.output_root` is
            # configurable, so a pattern rooted at the repo would silently find
            # nothing and report a $0.00 run.
            ledger = CostLedger(
                pricing=load_pricing(self.config.cost.pricing_path),
                ledger_path=str(self.run_dir / "cost_ledger.jsonl"),
                index_path=str(self.run_dir / "cost_index.json"),
                root=self.run_dir.parent,
            )
            ledger.scan(("{}/events.jsonl".format(self.run_dir.name),))
            summary = summarise(ledger)
            return {
                "cost_usd": summary["totals"]["cost_usd"],
                "calls": summary["totals"]["calls"],
                "total_tokens": summary["totals"]["total_tokens"],
                "unpriced_calls": summary["totals"]["unpriced_calls"],
                "pricing_verified": summary["pricing"]["verified"],
                "by_purpose": summary["by_purpose"],
            }
        except Exception as exc:  # pragma: no cover - reporting must not fail a run
            LOGGER.warning("could not price this run: %s", exc)
            return {"error": str(exc)}

    def _pairs_manifest(self) -> Dict[str, Any]:
        path = resolve_path(self.config.dataset.pairs_path)
        if not path.exists():
            return {"path": str(path), "present": False}
        subset = load_pair_subset(path)
        out: Dict[str, Any] = {
            "path": str(path),
            "present": True,
            "sha256_16": file_hash(path),
        }
        out.update(subset.counts())
        return out

    # ------------------------------------------------------------------ #
    def run(self) -> Dict[str, Any]:
        config = self.config
        if config.dataset.kind == "cases":
            instances = load_case_instances(
                config, dataset_path=config.dataset.case_path,
                instance_ids=self.instance_ids)
        elif config.dataset.kind == "k_sets":
            instances = load_k_set_instances(
                config, dataset_path=config.dataset.k_set_path,
                instance_ids=self.instance_ids)
        else:
            loader = load_pair_instances if config.dataset.kind == "pairs" else load_instances
            instances = loader(config, instance_ids=self.instance_ids)
        if self.limit is not None:
            instances = instances[: self.limit]
        if not instances:
            raise ValueError("no instances selected")

        registry = build_cutoff_registry(instances)
        self._write_manifest(instances)
        with (self.run_dir / "config.yaml").open("w", encoding="utf-8") as fh:
            yaml.safe_dump(config.dump(), fh, sort_keys=False, allow_unicode=True)

        mappings = load_ordinal_mappings(config.ordinal_mappings_path)

        # Primary evaluation unit. Absent -> pairwise metrics are reported as
        # null rather than silently falling back to listwise.
        pairs_path = resolve_path(config.dataset.pairs_path)
        pair_subset = None
        if config.dataset.kind == "pairs":
            LOGGER.info("pair slice: each instance is one gold-vs-negative pair")
        elif config.dataset.kind == "cases":
            LOGGER.info(
                "explanatory-case slice: %d case(s), no gold hypothesis -- "
                "gold-dependent metrics are skipped, not fabricated", len(instances))
        elif config.dataset.kind == "k_sets":
            sizes = sorted({len(i.hypotheses) for i in instances})
            LOGGER.info(
                "controlled listwise slice: k=%s over %d set(s). Chance top-1 is 1/k, "
                "so do not compare top-1 across k -- use normalised gold rank or the "
                "pairwise win rate.", sizes, len(instances))
        elif pairs_path.exists():
            pair_subset = load_pair_subset(pairs_path)
            LOGGER.info(
                "loaded %d frozen pair(s) across %d instance(s) from %s",
                len(pair_subset), len(pair_subset.instance_ids), pairs_path,
            )
            without = pair_subset.instances_without_pairs()
            if without:
                # Excluded from the primary metric by construction; say so.
                LOGGER.warning(
                    "%s: no evaluable pair after R2 screening; excluded from the "
                    "primary metric (still reported in listwise diagnostics)",
                    ", ".join(without),
                )
        elif config.dataset.kind != "pairs":
            LOGGER.warning(
                "no frozen pair subset at %s; the primary metric will be null "
                "(run scripts/build_pair_subset.py)", pairs_path,
            )
        from src.llm.prompts import PromptLibrary

        prompts = PromptLibrary(config.prompts.dir)
        llm = build_llm_client(config.llm, event_log=self.event_log)

        service = None
        if self.method.requires_literature:
            service = build_literature_service(config, registry, event_log=self.event_log)

        self._check_budget()

        if config.dataset.status != "evaluation":
            # One source of truth for this wording: the log line and the
            # `interpretation_warning` in summary.json must not be able to say
            # different things about the same run.
            LOGGER.warning("%s (%s)", _interpretation_warning(config.dataset.status),
                           config.dataset.kind)
        LOGGER.info(
            "run %s: method=%s instances=%d llm=%s/%s",
            self.run_id, self.method_name, len(instances), config.llm.provider, self.deployment,
        )

        metric_rows: List[Dict[str, Any]] = []
        results: List[InstanceResult] = []

        for instance in instances:
            instance_dir = ensure_dir(self.run_dir / "instances" / instance.id)
            # Instance events are mirrored into the run-wide log.
            instance_log = TeeEventLog(
                [self.event_log, EventLog(instance_dir / "events.jsonl")],
                defaults={"instance_id": instance.id},
            )
            presentation = build_presentation(instance, config.run)
            write_json(instance_dir / "input.json", instance.input_record())
            write_json(instance_dir / "presentation.json", presentation.to_record())
            instance_log.emit(
                "instance_start",
                method=self.method_name,
                n_hypotheses=len(instance.hypotheses),
                cutoff_date=instance.cutoff_date.isoformat() if instance.cutoff_date else None,
                cutoff_ambiguous=instance.cutoff_ambiguous,
            )

            llm.event_log = instance_log
            if service is not None:
                service.reset_records()
                service.bind_event_log(instance_log)

            result = self._run_one(
                instance=instance,
                instance_dir=instance_dir,
                instance_log=instance_log,
                presentation=presentation,
                prompts=prompts,
                llm=llm,
                mappings=mappings,
                service=service,
            )
            results.append(result)

            for stem in ARTIFACT_FILES:
                if stem in result.artifacts:
                    write_json(instance_dir / "{}.json".format(stem), result.artifacts[stem])

            if not instance.has_gold:
                row = {"instance_id": instance.id, "scored": False,
                       "no_gold": True, "n_hypotheses": len(instance.hypotheses),
                       "scores": result.scores, "ranking": result.ranking}
                row.update(result.diagnostics)
            else:
                row = instance_metrics(
                    instance,
                    result.scores,
                    diagnostics=dict(result.diagnostics),
                    # On a pair slice the instance IS the pair, so the primary metric
                    # comes from the instance itself. Same for a controlled k-set:
                    # every negative in it passed R2, so every gold-vs-negative
                    # comparison is a legitimate pair and at k=2 this reduces exactly
                    # to Acc_pair. On an 11-candidate ResearchBench slice the pairs
                    # come from v1's frozen R2 subset instead, because most of that
                    # row's candidates were never screened.
                    pair_negative_ids=(
                        [h.id for h in instance.hypotheses if not h.gold]
                        if config.dataset.kind in ("pairs", "k_sets")
                        else (pair_subset.negatives_for(instance.id) if pair_subset is not None else None)
                    ),
                    pair_status=(
                        "evaluable" if config.dataset.kind in ("pairs", "k_sets")
                        else (pair_subset.status_for(instance.id) if pair_subset is not None else "evaluable")
                    ),
                )
            row["status"] = result.status
            row["method"] = self.method_name
            row["cutoff_date"] = instance.cutoff_date.isoformat() if instance.cutoff_date else None
            row["cutoff_ambiguous"] = instance.cutoff_ambiguous
            row["load_warnings"] = list(instance.load_warnings)
            metric_rows.append(row)

            report = result.report or render_instance_report(
                instance, result, presentation, metrics=row,
                dataset_status=config.dataset.status,
            )
            (instance_dir / "report.md").write_text(report, encoding="utf-8")
            write_json(instance_dir / "result.json", result.model_dump(mode="json", exclude={"artifacts", "report"}))

            for error in result.errors:
                append_jsonl(self.run_dir / "errors.jsonl", error)

            instance_log.emit("instance_complete", status=result.status, **result.diagnostics)
            llm.event_log = self.event_log
            if service is not None:
                service.bind_event_log(self.event_log)

            LOGGER.info(
                "%s: status=%s gold_rank=%s top1=%s",
                instance.id, result.status, row.get("gold_rank"), row.get("top1_strict"),
            )

        summary = {
            "run_id": self.run_id,
            "dataset_status": config.dataset.status,
            "interpretation_warning": _interpretation_warning(config.dataset.status),
            "label": self.label,
            "method": self.method_name,
            "dataset": str(resolve_path(config.dataset.path)),
            "finished_at": utc_now_iso(),
            "n_instances": len(instances),
            "n_ok": sum(1 for r in results if r.status == "ok"),
            "n_error": sum(1 for r in results if r.status == "error"),
            "n_skipped": sum(1 for r in results if r.status == "skipped"),
            "cutoffs": {
                "n_ambiguous": sum(1 for i in instances if i.cutoff_ambiguous),
                "n_ambiguous_scored": sum(
                    1 for i, row in zip(instances, metric_rows)
                    if i.cutoff_ambiguous and row.get("scored")
                ),
                "n_missing": sum(1 for i in instances if not i.has_cutoff),
                "ambiguous_instances": [i.id for i in instances if i.cutoff_ambiguous],
            },
            "load_warnings": {
                i.id: i.load_warnings for i in instances if i.load_warnings
            },
            "llm_provider": config.llm.provider,
            "llm_deployment": self.deployment,
            "llm_usage": dict(getattr(llm, "usage_totals", {})),
            "llm_calls": getattr(llm, "n_calls", 0),
            "llm_parse_failures": getattr(llm, "n_parse_failures", 0),
            "cost": self._run_cost(),
            "literature_stats": dict(service.stats) if service is not None else None,
            "pairs": self._pairs_manifest(),
            "metrics": aggregate_metrics(metric_rows),
        }
        write_json(self.run_dir / "metrics.json", {"instances": metric_rows})
        write_json(self.run_dir / "summary.json", summary)
        (self.run_dir / "summary.md").write_text(render_run_summary(summary), encoding="utf-8")
        LOGGER.info("run %s complete: %s", self.run_id, summary["metrics"])
        return summary

    # ------------------------------------------------------------------ #
    def _run_one(
        self,
        *,
        instance: BenchmarkInstance,
        instance_dir: Path,
        instance_log: EventLog,
        presentation,
        prompts,
        llm,
        mappings,
        service,
    ) -> InstanceResult:
        reason = None
        if self.method.requires_literature and self.config.dataset.require_cutoff and not instance.has_cutoff:
            reason = (
                "no frozen cutoff date ({}); literature-based methods refuse to run "
                "(dataset.require_cutoff=true)".format(instance.cutoff_notes or "unresolved")
            )
        elif (
            self.method.requires_literature
            and self.config.dataset.require_unambiguous_cutoff
            and instance.cutoff_ambiguous
        ):
            reason = (
                "cutoff flagged ambiguous ({}); refused by "
                "dataset.require_unambiguous_cutoff".format(instance.cutoff_notes or "unverified")
            )
        if reason is not None:
            LOGGER.warning("%s skipped: %s", instance.id, reason)
            instance_log.emit("skipped", instance_id=instance.id, reason=reason)
            return InstanceResult(
                instance_id=instance.id, method=self.method_name, status="skipped", skip_reason=reason
            )

        if instance.cutoff_ambiguous:
            # Running these is the default (an ambiguous cutoff is conservative,
            # i.e. too early), but the count has to reach summary.json so nobody
            # reads a headline metric without knowing how many cutoffs are
            # unverified. See IMPLEMENTATION_SPEC.md §3.
            LOGGER.warning(
                "%s: cutoff %s is flagged ambiguous (%s)",
                instance.id, instance.cutoff_date, instance.cutoff_notes,
            )

        literature: Any
        if self.method.requires_literature:
            literature = InstanceSearchTool(service, instance.id)
        else:
            literature = ForbiddenLiteratureService(self.method_name)

        ctx = InstanceContext(
            instance=instance,
            config=self.config,
            llm=llm,
            prompts=prompts,
            presentation=presentation,
            literature=literature,
            mappings=mappings,
            event_log=instance_log,
            output_dir=instance_dir,
        )

        try:
            return self.method.run_instance(ctx)
        except TemporalLeakError:
            raise  # never downgraded: the experiment is invalid
        except MissingCutoffError as exc:
            ctx.record_error("runner.cutoff", exc)
            return InstanceResult(
                instance_id=instance.id, method=self.method_name, status="skipped",
                skip_reason=str(exc), errors=list(ctx.errors),
            )
        except Exception as exc:  # noqa: BLE001 - one bad instance must not kill the run
            ctx.record_error("runner", exc, traceback=traceback.format_exc(limit=20))
            LOGGER.exception("%s failed: %s", instance.id, exc)
            return InstanceResult(
                instance_id=instance.id, method=self.method_name, status="error", errors=list(ctx.errors)
            )
