"""Cost accounting: pricing, durability, and the budget guard.

The invariant that matters most here mirrors the rest of the project: a missing
price is reported as missing, never as zero. A cost tracker that silently prices
unknown models at $0.00 is worse than no tracker, because it reads as authority.
"""

from __future__ import annotations

import json

import pytest

from src.common.errors import BudgetExceededError, ConfigError
from src.experiments.costs import (
    CostLedger,
    PricingTable,
    estimate_cost,
    load_pricing,
    price_event,
    summarise,
)

RATES = {
    "version": "test",
    "currency": "USD",
    "verified": False,
    "models": {"gpt-4.1": {"input": 2.0, "output": 8.0, "aliases": ["gpt-4.1-2025-04-14"]}},
}


def event(ts, *, model="gpt-4.1-2025-04-14", prompt=1000, completion=500, call_id="c1", purpose="direct_judge"):
    return {
        "ts": ts,
        "kind": "llm_call",
        "purpose": purpose,
        "model": model,
        "call_id": call_id,
        "instance_id": "RBV-01",
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                  "total_tokens": prompt + completion},
    }


def write_events(path, events):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for e in events:
            fh.write(json.dumps(e) + "\n")


@pytest.fixture
def pricing():
    return PricingTable(RATES, source_path="test")


@pytest.fixture
def ledger(tmp_path, pricing):
    return CostLedger(
        pricing=pricing,
        ledger_path=str(tmp_path / "ledger.jsonl"),
        index_path=str(tmp_path / "index.json"),
        root=tmp_path,
    )


# --------------------------------------------------------------------------- #
# Pricing
# --------------------------------------------------------------------------- #
def test_cost_is_split_by_input_and_output_rate(pricing):
    call = price_event(event("2026-09-11T10:00:00Z"), pricing=pricing, source="s", run_id=None, line_no=1)
    # 1000 in @ $2/M + 500 out @ $8/M
    assert call.cost_usd == pytest.approx(0.002 + 0.004)
    assert call.priced is True
    assert call.day == "2026-09-11"


def test_aliases_and_deployment_suffixes_resolve(pricing):
    for model in ("gpt-4.1", "GPT-4.1-2025-04-14", "gpt-4.1-2025-04-14-eu"):
        assert pricing.rate_for(model) is not None, model


def test_unknown_model_is_unpriced_never_zero(pricing):
    call = price_event(
        event("2026-09-11T10:00:00Z", model="some-new-model"),
        pricing=pricing, source="s", run_id=None, line_no=1,
    )
    assert call.cost_usd is None, "an unknown model must not be priced at 0.00"
    assert call.priced is False
    assert call.total_tokens == 1500, "its tokens are still counted"
    assert "some-new-model" in pricing.unknown_models


def test_unpriced_calls_are_surfaced_in_the_summary(ledger, tmp_path):
    write_events(tmp_path / "runs" / "r1" / "events.jsonl", [
        event("2026-09-11T10:00:00Z", call_id="a"),
        event("2026-09-11T11:00:00Z", model="mystery-model", call_id="b"),
    ])
    ledger.scan(("runs/*/events.jsonl",))
    data = summarise(ledger)
    assert data["totals"]["unpriced_calls"] == 1
    assert data["totals"]["unpriced_models"] == ["mystery-model"]
    assert data["totals"]["total_tokens"] == 3000, "unpriced tokens still count"
    assert data["totals"]["cost_usd"] == pytest.approx(0.006), "and the total is a floor"


def test_malformed_pricing_is_rejected():
    with pytest.raises(ConfigError):
        PricingTable({"models": {"x": {"input": 1.0}}})


def test_shipped_pricing_file_loads_and_is_marked_unverified():
    table = load_pricing("configs/pricing.yaml")
    assert table.rate_for("gpt-4.1-kasia") is not None
    assert table.verified is False, (
        "flip `verified: true` only after checking rates against the Azure agreement"
    )


# --------------------------------------------------------------------------- #
# Ledger durability and incremental scanning
# --------------------------------------------------------------------------- #
def test_rescanning_does_not_double_count(ledger, tmp_path):
    path = tmp_path / "runs" / "r1" / "events.jsonl"
    write_events(path, [event("2026-09-11T10:00:00Z", call_id="a")])

    first = ledger.scan(("runs/*/events.jsonl",))
    second = ledger.scan(("runs/*/events.jsonl",))
    assert first["new_calls"] == 1
    assert second["new_calls"] == 0
    assert summarise(ledger)["totals"]["calls"] == 1

    # Appending is picked up from the stored offset.
    write_events(path, [event("2026-09-11T12:00:00Z", call_id="b")])
    third = ledger.scan(("runs/*/events.jsonl",))
    assert third["new_calls"] == 1
    assert summarise(ledger)["totals"]["calls"] == 2


def test_costs_survive_deleting_the_run(tmp_path, pricing):
    """Run directories get cleaned up; the spend still happened."""
    import shutil

    run_dir = tmp_path / "runs" / "r1"
    write_events(run_dir / "events.jsonl", [event("2026-09-11T10:00:00Z", call_id="a")])
    paths = dict(ledger_path=str(tmp_path / "ledger.jsonl"), index_path=str(tmp_path / "index.json"))

    first = CostLedger(pricing=pricing, root=tmp_path, **paths)
    first.scan(("runs/*/events.jsonl",))
    assert summarise(first)["totals"]["cost_usd"] > 0

    shutil.rmtree(run_dir)
    reloaded = CostLedger(pricing=pricing, root=tmp_path, **paths)
    reloaded.scan(("runs/*/events.jsonl",))
    assert summarise(reloaded)["totals"]["calls"] == 1, "the ledger is the record, not the run dir"


def test_instance_logs_are_not_scanned_by_default():
    """The runner tees each call into the run log and the instance log."""
    from src.common.config import AppConfig

    sources = AppConfig().cost.event_sources
    assert not any("instances" in pattern for pattern in sources)


def test_only_llm_call_events_are_priced(ledger, tmp_path):
    write_events(tmp_path / "runs" / "r1" / "events.jsonl", [
        {"ts": "2026-09-11T09:00:00Z", "kind": "retrieval", "instance_id": "RBV-01"},
        {"ts": "2026-09-11T09:01:00Z", "kind": "decision", "what": "excluded"},
        event("2026-09-11T10:00:00Z", call_id="a"),
    ])
    ledger.scan(("runs/*/events.jsonl",))
    assert summarise(ledger)["totals"]["calls"] == 1


def test_malformed_lines_are_skipped_not_fatal(ledger, tmp_path):
    path = tmp_path / "runs" / "r1" / "events.jsonl"
    write_events(path, [event("2026-09-11T10:00:00Z", call_id="a")])
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"kind": "llm_call", broken\n')
    write_events(path, [event("2026-09-11T11:00:00Z", call_id="b")])

    ledger.scan(("runs/*/events.jsonl",))
    assert summarise(ledger)["totals"]["calls"] == 2


# --------------------------------------------------------------------------- #
# Aggregation, budget, estimate
# --------------------------------------------------------------------------- #
def test_daily_and_breakdown_aggregation(ledger, tmp_path):
    write_events(tmp_path / "runs" / "r1" / "events.jsonl", [
        event("2026-09-10T10:00:00Z", call_id="a", purpose="direct_judge"),
        event("2026-09-11T10:00:00Z", call_id="b", purpose="direct_judge"),
        event("2026-09-11T11:00:00Z", call_id="c", purpose="direct_rag.assessment"),
    ])
    ledger.scan(("runs/*/events.jsonl",))
    data = summarise(ledger)

    assert [d["day"] for d in data["daily"]] == ["2026-09-10", "2026-09-11"]
    assert data["daily"][1]["calls"] == 2
    assert {b["purpose"] for b in data["by_purpose"]} == {"direct_judge", "direct_rag.assessment"}
    assert data["by_run"][0]["run_id"] == "r1"
    assert data["totals"]["n_days"] == 2


@pytest.mark.parametrize(
    "spent_calls,budget,status",
    [
        (1, 100.0, "good"),      # 0.006 / 100   = 0.006%
        (1, 0.01, "warning"),    # 0.006 / 0.01  = 60%
        (1, 0.007, "serious"),   # 0.006 / 0.007 = 86%
        (1, 0.001, "critical"),  # 0.006 / 0.001 = 600%
    ],
)
def test_budget_status_bands(ledger, tmp_path, spent_calls, budget, status):
    write_events(tmp_path / "runs" / "r1" / "events.jsonl",
                 [event("2026-09-11T10:00:00Z", call_id="c{}".format(i)) for i in range(spent_calls)])
    ledger.scan(("runs/*/events.jsonl",))
    assert summarise(ledger, budget_usd=budget)["budget"]["status"] == status


def test_no_budget_means_track_but_never_block(ledger):
    block = summarise(ledger)["budget"]
    assert block["budget_usd"] is None and block["status"] == "none"


def test_estimate_refuses_to_guess_without_history(ledger):
    assert estimate_cost(ledger, purpose_prefix="consequence_graph", n_units=100)["available"] is False


def test_estimate_projects_from_observed_calls(ledger, tmp_path):
    write_events(tmp_path / "runs" / "r1" / "events.jsonl", [
        event("2026-09-11T10:00:00Z", call_id="a", purpose="direct_rag.assessment"),
        event("2026-09-11T11:00:00Z", call_id="b", purpose="direct_rag.query_generation"),
    ])
    ledger.scan(("runs/*/events.jsonl",))
    result = estimate_cost(ledger, purpose_prefix="direct_rag", n_units=440)
    assert result["available"] is True
    assert result["n_observed_calls"] == 2
    assert result["projected_cost_usd"] == pytest.approx(0.006 * 440)


# --------------------------------------------------------------------------- #
# Runner integration
# --------------------------------------------------------------------------- #
def test_run_records_its_own_cost(config):
    from src.experiments.runner import ExperimentRunner
    from src.common.io import read_json

    cfg = config.model_copy(update={"llm": config.llm.model_copy(update={"provider": "mock"})})
    runner = ExperimentRunner(cfg, "direct_judge", instance_ids=["RBV-01"])
    summary = runner.run()

    cost = summary["cost"]
    assert cost["calls"] == 1
    assert cost["cost_usd"] == 0.0, "the mock client reports zero tokens"
    assert cost["pricing_verified"] is False
    assert read_json(runner.run_dir / "summary.json")["cost"]["calls"] == 1


def test_refuse_mode_blocks_before_any_model_call(config, tmp_path, monkeypatch):
    from src.experiments.runner import ExperimentRunner

    cfg = config.model_copy(
        update={
            "llm": config.llm.model_copy(update={"provider": "mock"}),
            "cost": config.cost.model_copy(update={"budget_usd": 0.000001, "on_exceed": "refuse"}),
        }
    )
    runner = ExperimentRunner(cfg, "direct_judge", instance_ids=["RBV-01"])
    with pytest.raises(BudgetExceededError):
        runner.run()


def test_a_broken_ledger_never_blocks_a_run(config, monkeypatch):
    """Cost tracking is bookkeeping; it must not take the experiment down."""
    from src.experiments import runner as runner_module

    cfg = config.model_copy(
        update={
            "llm": config.llm.model_copy(update={"provider": "mock"}),
            "cost": config.cost.model_copy(update={"pricing_path": "configs/does-not-exist.yaml"}),
        }
    )
    summary = runner_module.ExperimentRunner(cfg, "direct_judge", instance_ids=["RBV-01"]).run()
    assert summary["n_ok"] == 1


# --------------------------------------------------------------------------- #
# Dashboard page
# --------------------------------------------------------------------------- #
def _page_text():
    from src.common.io import repo_root

    return (repo_root() / "src" / "experiments" / "assets" / "cost_dashboard.html").read_text(
        encoding="utf-8"
    )


def test_dashboard_page_has_no_external_dependencies():
    """It must render on a laptop with no network and no CDN."""
    import re

    page = _page_text()
    assert not re.search(r'<script[^>]+src=', page), "no external scripts"
    assert not re.search(r'<link[^>]+href=', page), "no external stylesheets"
    assert "http://" not in page.replace("http-equiv", "")
    assert "https://" not in page


def test_dashboard_page_supports_both_themes():
    page = _page_text()
    assert "prefers-color-scheme: dark" in page
    assert '[data-theme="dark"]' in page
    # Light values are defined unconditionally, dark only overrides them.
    assert "--surface-1: #fcfcfb" in page and "--surface-1: #1a1a19" in page


def test_dashboard_page_has_the_pieces_the_reader_needs():
    page = _page_text()
    for marker in ('id="hero"', 'id="kpis"', 'id="chart"', 'id="tip"',
                   'id="t-daily"', 'id="t-model"', 'id="t-purpose"'):
        assert marker in page, marker
    # A table view exists alongside the chart (accessibility fallback).
    assert "<table" in page
    # Single series: no legend box is rendered.
    assert "legend" not in page.lower()


def test_static_export_inlines_the_data_and_labels_itself_stale(tmp_path, ledger, monkeypatch):
    import sys

    sys.path.insert(0, "scripts")
    from cost_dashboard import export_html

    data = summarise(ledger)
    out = export_html(data, tmp_path / "snapshot.html")
    page = out.read_text(encoding="utf-8")

    assert "window.__COSTS__" in page
    assert page.index("window.__COSTS__") < page.index("const REFRESH_MS")
    assert "static snapshot" in page, "a frozen page must say so rather than look live"
