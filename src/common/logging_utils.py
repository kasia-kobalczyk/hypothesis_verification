"""Console logging plus a structured JSONL event log per run.

IMPLEMENTATION_SPEC.md §9 requires every external API input/output and every
normalisation decision to be recoverable after the fact. Human-readable console
logging and machine-readable event logging are therefore separate concerns:

* `get_logger()`  -> stdlib logger, for the operator watching the run;
* `EventLog`      -> append-only JSONL, for post-hoc diagnosis.
"""

from __future__ import annotations

import logging
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.common.io import append_jsonl, ensure_dir, utc_now_iso

_CONFIGURED = False
_LOCK = threading.Lock()


def configure_logging(level: Optional[str] = None) -> None:
    """Install the console handler once; set the level whenever one is given.

    `get_logger` calls this without a level, so importing a module never
    overrides a level an entry point has already chosen.
    """
    global _CONFIGURED
    with _LOCK:
        root = logging.getLogger("hv")
        if not _CONFIGURED:
            handler = logging.StreamHandler(stream=sys.stderr)
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
                    datefmt="%H:%M:%S",
                )
            )
            root.setLevel(logging.INFO)
            root.handlers = [handler]
            root.propagate = False
            _CONFIGURED = True
        if level is not None:
            root.setLevel(getattr(logging, str(level).upper(), logging.INFO))


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger("hv." + name)


class EventLog:
    """Append-only structured log.

    Events are plain dicts with a `kind`, an ISO timestamp and arbitrary payload.
    A `None` path makes the log a no-op sink, which keeps call sites free of
    `if event_log is not None` noise in tests.
    """

    def __init__(
        self,
        path: Optional["str | Path"] = None,
        *,
        mirror_to_memory: bool = False,
        defaults: Optional[Dict[str, Any]] = None,
    ):
        self.path = Path(path) if path is not None else None
        if self.path is not None:
            ensure_dir(self.path.parent)
        self.mirror_to_memory = mirror_to_memory
        self.defaults = dict(defaults or {})
        self.events: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def emit(self, kind: str, **payload: Any) -> Dict[str, Any]:
        event: Dict[str, Any] = {"ts": utc_now_iso(), "kind": kind}
        event.update(self.defaults)
        event.update(payload)
        with self._lock:
            if self.path is not None:
                append_jsonl(self.path, event)
            if self.mirror_to_memory:
                self.events.append(event)
        return event

    # Convenience wrappers -------------------------------------------------- #
    def api_call(
        self,
        provider: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        status: Optional[int] = None,
        n_results: Optional[int] = None,
        cache: Optional[str] = None,
        error: Optional[str] = None,
        attempt: int = 1,
        elapsed_s: Optional[float] = None,
        **extra: Any
    ) -> Dict[str, Any]:
        return self.emit(
            "api_call",
            provider=provider,
            endpoint=endpoint,
            params=params or {},
            status=status,
            n_results=n_results,
            cache=cache,
            error=error,
            attempt=attempt,
            elapsed_s=elapsed_s,
            **extra
        )

    def decision(self, what: str, **payload: Any) -> Dict[str, Any]:
        """Record a normalisation / filtering decision."""
        return self.emit("decision", what=what, **payload)

    def error(self, where: str, message: str, **payload: Any) -> Dict[str, Any]:
        return self.emit("error", where=where, message=message, **payload)


class TeeEventLog(EventLog):
    """Fan an event out to several logs.

    Used so that per-instance work appears both in the run-wide `events.jsonl`
    and in `instances/<id>/events.jsonl`, without call sites having to know
    which sinks exist.
    """

    def __init__(self, sinks: List[EventLog], *, defaults: Optional[Dict[str, Any]] = None):
        super().__init__(None, defaults=defaults)
        self.sinks = list(sinks)

    def emit(self, kind: str, **payload: Any) -> Dict[str, Any]:
        merged = dict(self.defaults)
        merged.update(payload)
        event: Dict[str, Any] = {"kind": kind}
        for sink in self.sinks:
            event = sink.emit(kind, **merged)
        return event


NULL_EVENT_LOG = EventLog(None)
