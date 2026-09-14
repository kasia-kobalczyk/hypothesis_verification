"""LLM cost dashboard — daily spend, totals, and a budget check.

    python scripts/cost_dashboard.py --serve          # auto-refreshing website
    python scripts/cost_dashboard.py                  # one-shot summary in the terminal
    python scripts/cost_dashboard.py --export cost.html   # static snapshot to share
    python scripts/cost_dashboard.py --estimate direct_rag --units 440

Costs come from the durable ledger in `data/cost/ledger.jsonl`, which is merged
from the append-only `events.jsonl` files. Deleting a run directory does not
erase its cost.

`--serve` rescans the event logs on every poll, so a run in progress shows up
within seconds without restarting the server.
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common.config import load_config  # noqa: E402
from src.common.io import repo_root, resolve_path  # noqa: E402
from src.common.logging_utils import configure_logging, get_logger  # noqa: E402
from src.experiments.costs import (  # noqa: E402
    CostLedger,
    DEFAULT_SOURCES,
    estimate_cost,
    load_pricing,
    summarise,
)

LOGGER = get_logger("scripts.cost_dashboard")
PAGE = repo_root() / "src" / "experiments" / "assets" / "cost_dashboard.html"


def build_summary(config, *, budget_usd: Optional[float]) -> Dict[str, Any]:
    ledger = CostLedger(pricing=load_pricing(config.cost.pricing_path))
    scan = ledger.scan(tuple(config.cost.event_sources) or DEFAULT_SOURCES)
    data = summarise(ledger, budget_usd=budget_usd)
    data["scan"] = scan
    return data


def print_summary(data: Dict[str, Any]) -> None:
    t = data["totals"]
    pricing = data["pricing"]
    print("\nLLM cost — hypothesis verification")
    print("=" * 52)
    print("  project total   ${:.4f}{}".format(
        t["cost_usd"], "" if pricing["verified"] else "   (ESTIMATE: rates unverified)"))
    print("  today (UTC)     ${:.4f}".format(data["today"]["cost_usd"]))
    print("  calls           {:,}   over {} day(s)".format(t["calls"], t["n_days"]))
    print("  tokens          {:,} ({:,} in / {:,} out)".format(
        t["total_tokens"], t["prompt_tokens"], t["completion_tokens"]))
    if t["unpriced_calls"]:
        print("  UNPRICED        {:,} call(s) on {} — total is a floor".format(
            t["unpriced_calls"], ", ".join(t["unpriced_models"])))

    budget = data["budget"]
    if budget.get("budget_usd"):
        print("  budget          ${:.2f} of ${:.2f} spent ({:.0%}) — {}".format(
            budget["spent_usd"], budget["budget_usd"], budget["fraction"], budget["status"].upper()))

    print("\n  {:<12} {:>10} {:>8} {:>12}".format("day", "cost", "calls", "tokens"))
    for row in data["daily"]:
        print("  {:<12} {:>10} {:>8,} {:>12,}".format(
            row["day"], "${:.4f}".format(row["cost_usd"]), row["calls"], row["total_tokens"]))

    print("\n  {:<26} {:>10} {:>8}".format("method / purpose", "cost", "calls"))
    for row in sorted(data["by_purpose"], key=lambda r: -r["cost_usd"]):
        print("  {:<26} {:>10} {:>8,}".format(
            str(row["purpose"])[:26], "${:.4f}".format(row["cost_usd"]), row["calls"]))
    print()


def export_html(data: Dict[str, Any], out: Path) -> Path:
    """Write a self-contained snapshot with the data inlined."""
    page = PAGE.read_text(encoding="utf-8")
    payload = json.dumps(data).replace("</", "<\\/")
    page = page.replace("<script>", "<script>window.__COSTS__ = {};\n".format(payload), 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, config=None, budget_usd=None, **kwargs):
        self.config = config
        self.budget_usd = budget_usd
        super().__init__(*args, **kwargs)

    def _send(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?")[0].rstrip("/") or "/"
        try:
            if path in ("/", "/index.html"):
                self._send(PAGE.read_bytes(), "text/html; charset=utf-8")
            elif path in ("/api/costs.json", "/api/costs"):
                # Rescanned per request: a run in progress appears within one poll.
                data = build_summary(self.config, budget_usd=self.budget_usd)
                self._send(json.dumps(data).encode("utf-8"), "application/json")
            else:
                self.send_error(404, "not found")
        except Exception as exc:  # pragma: no cover - surfaced in the page
            LOGGER.exception("request failed: %s", exc)
            self.send_error(500, str(exc))

    def log_message(self, fmt: str, *args: Any) -> None:
        return  # the access log is noise here


def serve(config, *, host: str, port: int, budget_usd: Optional[float], open_browser: bool) -> int:
    handler = partial(Handler, config=config, budget_usd=budget_usd)
    server = ThreadingHTTPServer((host, port), handler)
    url = "http://{}:{}/".format("localhost" if host in ("", "0.0.0.0") else host, server.server_port)
    print("\ncost dashboard: {}".format(url))
    print("refreshes every 10s from the event logs; Ctrl-C to stop\n")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:  # pragma: no cover
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="LLM cost dashboard.")
    parser.add_argument("--config", default="configs/mvp.yaml")
    parser.add_argument("--serve", action="store_true", help="run the auto-refreshing website")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--open", action="store_true", help="open a browser at the dashboard")
    parser.add_argument("--export", default=None, help="write a static HTML snapshot here")
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("--budget", type=float, default=None, help="override cost.budget_usd")
    parser.add_argument("--estimate", default=None,
                        help="project the cost of N more calls of this purpose prefix")
    parser.add_argument("--units", type=int, default=1, help="how many calls to project")
    parser.add_argument("--log-level", default="WARNING")
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    config = load_config(args.config)
    budget = args.budget if args.budget is not None else config.cost.budget_usd

    if args.estimate:
        ledger = CostLedger(pricing=load_pricing(config.cost.pricing_path))
        ledger.scan(tuple(config.cost.event_sources) or DEFAULT_SOURCES)
        result = estimate_cost(ledger, purpose_prefix=args.estimate, n_units=args.units)
        if not result["available"]:
            print("no history for purpose {!r} — cannot estimate. Run a small subset first "
                  "(--instances RBV-01) and try again.".format(args.estimate))
            return 1
        print("\n{} x {} calls".format(args.units, args.estimate))
        print("  observed  {} call(s), mean ${:.4f} / {:,.0f} tokens".format(
            result["n_observed_calls"], result["mean_cost_usd"], result["mean_total_tokens"]))
        print("  projected ${:.2f} and {:,.0f} tokens".format(
            result["projected_cost_usd"], result["projected_total_tokens"]))
        print("  (mean of past calls; a method with longer prompts will cost more)\n")
        return 0

    if args.serve:
        return serve(config, host=args.host, port=args.port,
                     budget_usd=budget, open_browser=args.open)

    data = build_summary(config, budget_usd=budget)
    if args.export:
        out = export_html(data, resolve_path(args.export))
        print("wrote static snapshot to {}".format(out))
        return 0
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    print_summary(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
