"""On-disk cache for raw provider responses.

IMPLEMENTATION_SPEC.md §8. The cached artifact is the **raw provider payload**,
not the filtered result set. Normalisation and temporal filtering are re-run on
every read, so:

* a fixed cache + fixed code always yields the same eligible set (reproducible);
* a bug fix in normalisation or filtering takes effect on cached data without
  needing new API calls (auditable);
* the cutoff can never be "baked in" wrongly and then replayed.

A normalised snapshot is written alongside each entry for human inspection; it
is never read back.

The cache key includes the cutoff date even though filtering happens after the
cache read: it keeps entries from one instance from masquerading as another's,
and makes the stored artifact self-describing.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

from src.common.config import LiteratureCacheConfig
from src.common.errors import CacheMissError
from src.common.io import ensure_dir, read_json, resolve_path, slugify, stable_hash, utc_now_iso, write_json
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger

LOGGER = get_logger("literature.cache")

CACHE_FORMAT_VERSION = 1


class LiteratureCache:
    def __init__(
        self,
        config: LiteratureCacheConfig,
        *,
        event_log: Optional[EventLog] = None,
        root: Optional["str | Path"] = None,
    ):
        self.config = config
        self.event_log = event_log or NULL_EVENT_LOG
        self.root = resolve_path(root if root is not None else config.dir)
        if config.enabled:
            ensure_dir(self.root)

    # ------------------------------------------------------------------ #
    @staticmethod
    def build_key(
        *,
        provider: str,
        provider_version: str,
        query: str,
        instance_id: str,
        cutoff_date: Optional[date],
        top_k: int,
        retrieval_path: str = "search",
        provider_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return {
            "cache_format": CACHE_FORMAT_VERSION,
            "provider": provider,
            "provider_version": provider_version,
            "query": query,
            "instance_id": instance_id,
            "cutoff_date": cutoff_date.isoformat() if cutoff_date else None,
            "top_k": top_k,
            "retrieval_path": retrieval_path,
            "provider_config": provider_config or {},
        }

    @staticmethod
    def digest(key: Dict[str, Any]) -> str:
        return stable_hash(key, length=24)

    def path_for(self, key: Dict[str, Any]) -> Path:
        return (
            self.root
            / slugify(str(key.get("provider", "provider")))
            / slugify(str(key.get("instance_id", "instance")))
            / "{}.json".format(self.digest(key))
        )

    # ------------------------------------------------------------------ #
    def get(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Return the cached entry, or `None` on a miss.

        In offline mode a miss raises `CacheMissError`: an empty result would be
        indistinguishable from "the provider found nothing" (spec §29).
        """
        if not self.config.enabled:
            if self.config.offline:
                raise CacheMissError("offline mode requires literature.cache.enabled=true")
            return None
        path = self.path_for(key)
        if self.config.refresh and not self.config.offline:
            return None
        if not path.exists():
            if self.config.offline:
                raise CacheMissError(
                    "offline: no cached response for query {!r} (instance {}, top_k {})".format(
                        key.get("query"), key.get("instance_id"), key.get("top_k")
                    )
                )
            return None
        try:
            entry = read_json(path)
        except Exception as exc:  # corrupted cache entry
            LOGGER.warning("unreadable cache entry %s: %s", path, exc)
            self.event_log.error("cache", "unreadable entry: {}".format(exc), path=str(path))
            if self.config.offline:
                raise CacheMissError("offline: cache entry {} is unreadable".format(path))
            return None
        self.event_log.api_call(
            str(key.get("provider")), str(key.get("retrieval_path")), cache="hit",
            params={"query": key.get("query"), "instance_id": key.get("instance_id")},
        )
        return entry

    def put(
        self,
        key: Dict[str, Any],
        payload: Dict[str, Any],
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Path:
        path = self.path_for(key)
        if not self.config.enabled:
            return path
        entry = {
            "key": key,
            "digest": self.digest(key),
            "retrieved_at": utc_now_iso(),
            "meta": meta or {},
            "raw": payload,
        }
        write_json(path, entry)
        return path

    def put_snapshot(self, key: Dict[str, Any], snapshot: Dict[str, Any]) -> Optional[Path]:
        """Write the normalised/filtered view next to the raw entry (audit only)."""
        if not self.config.enabled:
            return None
        path = self.path_for(key).with_suffix(".normalised.json")
        write_json(path, snapshot)
        return path

    @property
    def status(self) -> str:
        if not self.config.enabled:
            return "disabled"
        if self.config.refresh:
            return "refresh"
        if self.config.offline:
            return "offline"
        return "enabled"
