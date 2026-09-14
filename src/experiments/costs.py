"""Token-cost accounting for every model call the project makes.

Two properties matter more than the arithmetic:

* **Durability.** Costs are derived from `events.jsonl`, but run directories get
  deleted. Priced calls are therefore merged into an append-only ledger at
  `data/cost/ledger.jsonl`, which survives the runs it came from. A deleted run
  still counts against the project total.
* **No silent zeros.** A model with no entry in `configs/pricing.yaml` is
  reported as `unpriced` — its tokens and call count are visible, and its cost is
  `None`, never `0.00`. A cost tracker that quietly prices unknown models at zero
  is worse than none.

Scanning is incremental: event logs are append-only, so each source file is read
from the byte offset last consumed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from src.common.config import load_yaml
from src.common.errors import ConfigError
from src.common.io import ensure_dir, read_json, resolve_path, write_json
from src.common.logging_utils import get_logger

LOGGER = get_logger("experiments.costs")

# Event logs to scan. Instance-level logs are deliberately excluded: the runner
# tees every call into both, and scanning both would double-count.
DEFAULT_SOURCES = ("runs/*/events.jsonl", "benchmark/*/*_events.jsonl")

LEDGER_PATH = "data/cost/ledger.jsonl"
INDEX_PATH = "data/cost/scan_index.json"


# --------------------------------------------------------------------------- #
# Pricing
# --------------------------------------------------------------------------- #
@dataclass
class ModelRate:
    name: str
    input_per_m: float
    output_per_m: float

    def cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        return (prompt_tokens / 1e6) * self.input_per_m + (
            completion_tokens / 1e6
        ) * self.output_per_m


class PricingTable:
    """Model name -> rate, with alias resolution and explicit unknowns."""

    def __init__(self, data: Dict[str, Any], *, source_path: Optional[str] = None):
        self.version = str(data.get("version", "unversioned"))
        self.currency = str(data.get("currency", "USD"))
        self.verified = bool(data.get("verified", False))
        self.source = str(data.get("source", ""))
        self.source_path = source_path
        self._rates: Dict[str, ModelRate] = {}
        for name, entry in (data.get("models") or {}).items():
            if not isinstance(entry, dict) or "input" not in entry or "output" not in entry:
                raise ConfigError("pricing entry {!r} needs `input` and `output`".format(name))
            rate = ModelRate(name, float(entry["input"]), float(entry["output"]))
            for key in [name] + list(entry.get("aliases") or []):
                self._rates[str(key).strip().lower()] = rate
        self.unknown_models: Dict[str, int] = {}

    def rate_for(self, model: Optional[str]) -> Optional[ModelRate]:
        if not model:
            return None
        key = str(model).strip().lower()
        rate = self._rates.get(key)
        if rate is not None:
            return rate
        # Tolerate a deployment suffix on a known snapshot ("gpt-4.1-2025-04-14-eu").
        for known, candidate in self._rates.items():
            if key.startswith(known):
                return candidate
        self.unknown_models[str(model)] = self.unknown_models.get(str(model), 0) + 1
        return None

    def record(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "currency": self.currency,
            "verified": self.verified,
            "source": self.source,
            "path": self.source_path,
            "n_models": len({id(r) for r in self._rates.values()}),
        }


def load_pricing(path: str = "configs/pricing.yaml") -> PricingTable:
    return PricingTable(load_yaml(path), source_path=str(resolve_path(path)))


# --------------------------------------------------------------------------- #
# Ledger
# --------------------------------------------------------------------------- #
@dataclass
class CallCost:
    """One priced model call."""

    key: str
    ts: str
    day: str
    source: str
    run_id: Optional[str]
    instance_id: Optional[str]
    purpose: Optional[str]
    model: Optional[str]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: Optional[float]  # None = unpriced model
    priced: bool

    def to_row(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "ts": self.ts,
            "day": self.day,
            "source": self.source,
            "run_id": self.run_id,
            "instance_id": self.instance_id,
            "purpose": self.purpose,
            "model": self.model,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "cost_usd": self.cost_usd,
            "priced": self.priced,
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "CallCost":
        return cls(**{k: row.get(k) for k in cls.__dataclass_fields__})  # type: ignore[attr-defined]


def _run_id_for(path: Path, root: Path) -> Optional[str]:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) >= 2 and parts[0] == "runs":
        return parts[1]
    return None


def _day_of(ts: str) -> str:
    return (ts or "")[:10] or "unknown"


def price_event(
    event: Dict[str, Any],
    *,
    pricing: PricingTable,
    source: str,
    run_id: Optional[str],
    line_no: int,
) -> Optional[CallCost]:
    """Turn one `llm_call` event into a priced row."""
    if event.get("kind") != "llm_call":
        return None
    usage = event.get("usage") or {}
    prompt_tokens = int(usage.get("prompt_tokens") or 0)
    completion_tokens = int(usage.get("completion_tokens") or 0)
    total_tokens = int(usage.get("total_tokens") or (prompt_tokens + completion_tokens))
    model = event.get("model")
    rate = pricing.rate_for(model)
    ts = str(event.get("ts") or "")
    # Stable across rescans: the same call in the same file gets the same key.
    call_id = event.get("call_id") or "line{}".format(line_no)
    return CallCost(
        key="{}::{}::{}".format(source, call_id, ts),
        ts=ts,
        day=_day_of(ts),
        source=source,
        run_id=run_id,
        instance_id=event.get("instance_id"),
        purpose=event.get("purpose"),
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_usd=rate.cost(prompt_tokens, completion_tokens) if rate else None,
        priced=rate is not None,
    )


class CostLedger:
    """Durable record of every priced call, merged from append-only event logs."""

    def __init__(
        self,
        *,
        pricing: PricingTable,
        ledger_path: str = LEDGER_PATH,
        index_path: str = INDEX_PATH,
        root: Optional[Path] = None,
    ):
        from src.common.io import repo_root

        self.pricing = pricing
        self.root = root or repo_root()
        self.ledger_path = resolve_path(ledger_path, self.root)
        self.index_path = resolve_path(index_path, self.root)
        self.rows: Dict[str, CallCost] = {}
        self.index: Dict[str, Dict[str, Any]] = {}
        self._load()

    # -- persistence ---------------------------------------------------- #
    def _load(self) -> None:
        if self.ledger_path.exists():
            with self.ledger_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        LOGGER.warning("skipping malformed ledger line in %s", self.ledger_path)
                        continue
                    call = CallCost.from_row(row)
                    self.rows[call.key] = call
        if self.index_path.exists():
            try:
                self.index = read_json(self.index_path) or {}
            except Exception:  # pragma: no cover - defensive
                self.index = {}

    def save(self) -> None:
        ensure_dir(self.ledger_path.parent)
        ordered = sorted(self.rows.values(), key=lambda c: (c.ts, c.key))
        with self.ledger_path.open("w", encoding="utf-8") as fh:
            for call in ordered:
                fh.write(json.dumps(call.to_row(), ensure_ascii=False))
                fh.write("\n")
        write_json(self.index_path, self.index)

    # -- scanning ------------------------------------------------------- #
    def sources(self, patterns: Sequence[str] = DEFAULT_SOURCES) -> List[Path]:
        found: List[Path] = []
        for pattern in patterns:
            found.extend(sorted(self.root.glob(pattern)))
        return found

    def scan(self, patterns: Sequence[str] = DEFAULT_SOURCES) -> Dict[str, int]:
        """Merge new events into the ledger. Returns a small scan summary."""
        new_rows = 0
        files_scanned = 0
        for path in self.sources(patterns):
            key = str(path.relative_to(self.root))
            state = self.index.get(key) or {"offset": 0, "lines": 0}
            try:
                size = path.stat().st_size
            except OSError:  # pragma: no cover - racing deletion
                continue
            offset = int(state.get("offset", 0))
            if size < offset:
                # Truncated or replaced: re-read from the start.
                offset, state = 0, {"offset": 0, "lines": 0}
            if size == offset:
                continue

            files_scanned += 1
            run_id = _run_id_for(path, self.root)
            line_no = int(state.get("lines", 0))
            with path.open("r", encoding="utf-8") as fh:
                fh.seek(offset)
                for line in fh:
                    line_no += 1
                    line = line.strip()
                    if not line or '"llm_call"' not in line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        LOGGER.warning("%s:%d: malformed event line", key, line_no)
                        continue
                    call = price_event(
                        event, pricing=self.pricing, source=key, run_id=run_id, line_no=line_no
                    )
                    if call is not None and call.key not in self.rows:
                        self.rows[call.key] = call
                        new_rows += 1
                new_offset = fh.tell()
            self.index[key] = {"offset": new_offset, "lines": line_no}

        if new_rows or files_scanned:
            self.save()
        return {"files_scanned": files_scanned, "new_calls": new_rows, "total_calls": len(self.rows)}

    # -- aggregation ---------------------------------------------------- #
    def calls(self) -> List[CallCost]:
        return sorted(self.rows.values(), key=lambda c: (c.ts, c.key))


def _bucket(calls: Iterable[CallCost], key: str) -> List[Dict[str, Any]]:
    buckets: Dict[Any, Dict[str, Any]] = {}
    for call in calls:
        name = getattr(call, key) or "unknown"
        bucket = buckets.setdefault(
            name,
            {key: name, "calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
             "total_tokens": 0, "cost_usd": 0.0, "unpriced_calls": 0},
        )
        bucket["calls"] += 1
        bucket["prompt_tokens"] += call.prompt_tokens
        bucket["completion_tokens"] += call.completion_tokens
        bucket["total_tokens"] += call.total_tokens
        if call.cost_usd is None:
            bucket["unpriced_calls"] += 1
        else:
            bucket["cost_usd"] += call.cost_usd
    return sorted(buckets.values(), key=lambda b: b[key])


def summarise(
    ledger: CostLedger,
    *,
    budget_usd: Optional[float] = None,
) -> Dict[str, Any]:
    """Everything the dashboard renders, computed once."""
    calls = ledger.calls()
    priced = [c for c in calls if c.cost_usd is not None]
    unpriced = [c for c in calls if c.cost_usd is None]
    total = sum(c.cost_usd or 0.0 for c in priced)

    daily = _bucket(calls, "day")
    for row in daily:
        row["day_label"] = row["day"]
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_row = next((row for row in daily if row["day"] == today), None)

    return {
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "pricing": ledger.pricing.record(),
        "totals": {
            "cost_usd": total,
            "calls": len(calls),
            "prompt_tokens": sum(c.prompt_tokens for c in calls),
            "completion_tokens": sum(c.completion_tokens for c in calls),
            "total_tokens": sum(c.total_tokens for c in calls),
            "unpriced_calls": len(unpriced),
            "unpriced_models": sorted({c.model or "unknown" for c in unpriced}),
            "first_call": calls[0].ts if calls else None,
            "last_call": calls[-1].ts if calls else None,
            "n_days": len(daily),
        },
        "today": {
            "day": today,
            "cost_usd": today_row["cost_usd"] if today_row else 0.0,
            "calls": today_row["calls"] if today_row else 0,
            "total_tokens": today_row["total_tokens"] if today_row else 0,
        },
        "budget": _budget_block(total, budget_usd),
        "daily": daily,
        "by_model": _bucket(calls, "model"),
        "by_purpose": _bucket(calls, "purpose"),
        "by_run": _bucket(calls, "run_id"),
    }


def _budget_block(total: float, budget_usd: Optional[float]) -> Dict[str, Any]:
    if not budget_usd:
        return {"budget_usd": None, "spent_usd": total, "status": "none"}
    fraction = total / budget_usd if budget_usd else 0.0
    if fraction >= 1.0:
        status = "critical"
    elif fraction >= 0.8:
        status = "serious"
    elif fraction >= 0.5:
        status = "warning"
    else:
        status = "good"
    return {
        "budget_usd": budget_usd,
        "spent_usd": total,
        "remaining_usd": budget_usd - total,
        "fraction": fraction,
        "status": status,
    }


def estimate_cost(
    ledger: CostLedger,
    *,
    purpose_prefix: str,
    n_units: int,
) -> Dict[str, Any]:
    """Project the cost of `n_units` more calls of a given purpose, from history.

    Returns `available: False` rather than a guess when there is no history — an
    invented estimate is worse than no estimate before a large run.
    """
    matching = [
        c for c in ledger.calls()
        if (c.purpose or "").startswith(purpose_prefix) and c.cost_usd is not None
    ]
    if not matching:
        return {"available": False, "purpose_prefix": purpose_prefix, "n_units": n_units}
    mean = sum(c.cost_usd or 0.0 for c in matching) / len(matching)
    mean_tokens = sum(c.total_tokens for c in matching) / len(matching)
    return {
        "available": True,
        "purpose_prefix": purpose_prefix,
        "n_units": n_units,
        "n_observed_calls": len(matching),
        "mean_cost_usd": mean,
        "mean_total_tokens": mean_tokens,
        "projected_cost_usd": mean * n_units,
        "projected_total_tokens": mean_tokens * n_units,
    }
