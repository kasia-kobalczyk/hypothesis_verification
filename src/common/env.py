"""Environment variable access, including a dependency-free `.env` loader.

`python-dotenv` is not installed in the target environment, so `.env` parsing is
implemented here. Secrets are never logged; only the *names* of variables that
were found are reported.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

from src.common.io import repo_root

_LOADED = False


def load_dotenv(path: Optional[Path] = None, *, override: bool = False) -> List[str]:
    """Load `KEY=value` pairs from a `.env` file. Returns the names that were set."""
    env_path = Path(path) if path is not None else repo_root() / ".env"
    if not env_path.exists():
        return []
    names: List[str] = []
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        if override or key not in os.environ:
            os.environ[key] = value
            names.append(key)
    return names


def ensure_env_loaded() -> None:
    """Load `.env` once per process."""
    global _LOADED
    if not _LOADED:
        load_dotenv()
        _LOADED = True


def get_env(*names: str, default: Optional[str] = None) -> Optional[str]:
    """First non-empty value among `names`, else `default`."""
    ensure_env_loaded()
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def env_presence(*names: str) -> Dict[str, bool]:
    """Which of `names` are set, without revealing their values (safe to log)."""
    ensure_env_loaded()
    return {name: bool(os.environ.get(name)) for name in names}


# Canonical variable names used by the project.
AZURE_KEY_VARS = ("AZURE_API_KEY", "AZURE_OPENAI_API_KEY")
AZURE_BASE_VARS = ("AZURE_API_BASE", "AZURE_OPENAI_ENDPOINT")
AZURE_VERSION_VARS = ("AZURE_API_VERSION", "AZURE_OPENAI_API_VERSION")
LLM_MODEL_VARS = ("LLM_MODEL", "LLM_DEPLOYMENT", "AZURE_OPENAI_DEPLOYMENT")
S2_KEY_VARS = ("S2_API_KEY", "SEMANTIC_SCHOLAR_API_KEY")
CROSSREF_MAILTO_VARS = ("CROSSREF_MAILTO",)
