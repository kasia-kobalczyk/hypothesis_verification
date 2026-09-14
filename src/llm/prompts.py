"""Versioned prompt templates.

IMPLEMENTATION_SPEC.md §31: prompts are part of the experimental method. Each
template is a file named `<name>_v<N>.txt`; every run records the template name
and a content hash, so a result can always be traced to the exact prompt text
that produced it. Templates are never edited in place — a change means a new
version file.

`string.Template` (`$placeholder`) is used rather than `str.format` so that JSON
examples inside a prompt do not need brace escaping.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Any, Dict, FrozenSet, List, Optional

from src.common.errors import ConfigError
from src.common.io import resolve_path, text_hash


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    path: Path
    text: str

    @property
    def sha(self) -> str:
        return text_hash(self.text)

    @property
    def placeholders(self) -> FrozenSet[str]:
        """The `$name` slots this template declares.

        Callers use this to pass only what a template actually asks for, which
        makes some properties structural rather than a matter of wording: a
        generation prompt that does not declare `$alternatives` cannot be shown
        the competing hypotheses, whatever its prose says.
        """
        names = set()
        for match in Template.pattern.finditer(self.text):
            name = match.group("named") or match.group("braced")
            if name:
                names.add(name)
        return frozenset(names)

    def render(self, **values: Any) -> str:
        try:
            return Template(self.text).substitute(**values)
        except KeyError as exc:
            raise ConfigError(
                "prompt {!r} is missing a value for placeholder {}".format(self.name, exc)
            )

    def record(self) -> Dict[str, str]:
        return {"name": self.name, "sha256_16": self.sha, "path": str(self.path)}


class PromptLibrary:
    def __init__(self, directory: "str | Path"):
        self.directory = resolve_path(directory)
        self._cache: Dict[str, PromptTemplate] = {}

    def get(self, name: str) -> PromptTemplate:
        if name in self._cache:
            return self._cache[name]
        path = self.directory / "{}.txt".format(name)
        if not path.exists():
            raise ConfigError("prompt template not found: {}".format(path))
        template = PromptTemplate(name=name, path=path, text=path.read_text(encoding="utf-8"))
        self._cache[name] = template
        return template

    def render(self, name: str, **values: Any) -> str:
        return self.get(name).render(**values)

    def available(self) -> List[str]:
        return sorted(p.stem for p in self.directory.glob("*.txt"))

    def manifest(self, names: Optional[List[str]] = None) -> Dict[str, Dict[str, str]]:
        """Name -> {sha, path} for the prompts used by a run."""
        return {name: self.get(name).record() for name in (names or self.available())}
