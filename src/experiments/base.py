"""Method interface shared by all verification methods."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.benchmark.loader import BenchmarkInstance
from src.benchmark.presentation import Presentation
from src.common.config import AppConfig
from src.common.logging_utils import EventLog
from src.inference.parameters import OrdinalMappings
from src.llm.client import BaseLLMClient
from src.llm.prompts import PromptLibrary


@dataclass
class InstanceContext:
    """Everything a method may use for one instance.

    `literature` is an `InstanceSearchTool` for literature-based methods and a
    `ForbiddenLiteratureService` for literature-free ones, so isolation is
    enforced by the object graph rather than by convention.
    """

    instance: BenchmarkInstance
    config: AppConfig
    llm: BaseLLMClient
    prompts: PromptLibrary
    presentation: Presentation
    literature: Any
    mappings: OrdinalMappings
    event_log: EventLog
    output_dir: Path
    errors: List[Dict[str, Any]] = field(default_factory=list)

    def record_error(self, where: str, exc: BaseException, **extra: Any) -> Dict[str, Any]:
        entry: Dict[str, Any] = {
            "instance_id": self.instance.id,
            "where": where,
            "type": type(exc).__name__,
            "message": str(exc),
        }
        entry.update(extra)
        self.errors.append(entry)
        self.event_log.error(where, str(exc), error_type=type(exc).__name__, **extra)
        return entry


class InstanceResult(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    instance_id: str
    method: str
    status: str = "ok"  # ok | error | skipped
    scores: Dict[str, float] = Field(default_factory=dict)
    ranking: List[str] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    # filename stem -> JSON-serialisable payload, written by the runner
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    usage: Dict[str, int] = Field(default_factory=dict)
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    report: Optional[str] = None
    skip_reason: Optional[str] = None


class Method(abc.ABC):
    """A hypothesis-ranking method."""

    name: str = "abstract"
    requires_literature: bool = False

    def __init__(self, config: AppConfig):
        self.config = config

    @abc.abstractmethod
    def run_instance(self, ctx: InstanceContext) -> InstanceResult:
        """Rank the candidate hypotheses of `ctx.instance`."""

    def prompt_versions(self) -> List[str]:
        """Prompt template names this method uses (recorded in the run manifest)."""
        return []
