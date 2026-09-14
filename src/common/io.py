"""Filesystem, hashing and (de)serialisation helpers."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    """Absolute path of the repository root (the directory holding `src/`)."""
    return _REPO_ROOT


def resolve_path(path: "str | Path", base: Optional[Path] = None) -> Path:
    """Resolve `path` against the repository root unless it is absolute."""
    p = Path(path)
    if p.is_absolute():
        return p
    return (base or repo_root()) / p


def ensure_dir(path: "str | Path") -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


class _JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:  # noqa: D102
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, set):
            return sorted(o)
        if hasattr(o, "model_dump"):  # pydantic v2
            return o.model_dump(mode="json")
        return super().default(o)


def dumps(obj: Any, *, indent: Optional[int] = 2, sort_keys: bool = False) -> str:
    return json.dumps(obj, cls=_JSONEncoder, indent=indent, sort_keys=sort_keys, ensure_ascii=False)


def write_json(path: "str | Path", obj: Any, *, indent: Optional[int] = 2) -> Path:
    """Atomically write `obj` as JSON (temp file + rename)."""
    p = Path(path)
    ensure_dir(p.parent)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(dumps(obj, indent=indent))
            fh.write("\n")
        os.replace(tmp, str(p))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return p


def read_json(path: "str | Path") -> Any:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def read_jsonl(path: "str | Path") -> Iterator[Dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:  # pragma: no cover - defensive
                raise ValueError("{}:{}: invalid JSON line: {}".format(path, line_no, exc))


def write_jsonl(path: "str | Path", rows: Iterable[Any], *, append: bool = False) -> Path:
    p = Path(path)
    ensure_dir(p.parent)
    mode = "a" if append else "w"
    with p.open(mode, encoding="utf-8") as fh:
        for row in rows:
            fh.write(dumps(row, indent=None))
            fh.write("\n")
    return p


def append_jsonl(path: "str | Path", row: Any) -> Path:
    return write_jsonl(path, [row], append=True)


def stable_hash(obj: Any, *, length: int = 16) -> str:
    """Deterministic hash of a JSON-serialisable object.

    Used for cache keys and for recording prompt/config identity in run
    artifacts, so a run can be matched back to the exact inputs that produced it.
    """
    payload = json.dumps(obj, cls=_JSONEncoder, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length]


def file_hash(path: "str | Path", *, length: int = 16) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:length]


def text_hash(text: str, *, length: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def slugify(value: str, *, max_length: int = 120) -> str:
    """Filesystem-safe slug (used for DOI-keyed raw metadata files)."""
    keep: List[str] = []
    for ch in value.strip().lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in "-_.":
            keep.append(ch)
        else:
            keep.append("_")
    slug = "".join(keep).strip("_") or "empty"
    if len(slug) > max_length:
        slug = slug[: max_length - 9] + "_" + hashlib.sha256(value.encode()).hexdigest()[:8]
    return slug


def utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
