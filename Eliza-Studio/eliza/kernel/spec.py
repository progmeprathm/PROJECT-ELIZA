"""
ECOS Kernel Specifications, Interfaces, and Lifecycle Dataclasses.
Enforces Section V & VI of ELIZA_KERNEL_SPEC.md.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time

from eliza.core.events import CognitiveEvent, EventBus


class ModuleState(str, Enum):
    """Module Lifecycle States (Section V)."""
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    UNLOADED = "unloaded"


class TaskState(str, Enum):
    """Task Model States (Section X)."""
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ModuleManifest:
    module_id: str
    version: str
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleHealth:
    module_id: str
    status: str = "Healthy"  # Healthy, Warning, Critical, Offline
    latency_ms: float = 0.0
    memory_usage_mb: float = 0.0
    error_count: int = 0


class ICognitiveModule(ABC):
    """
    Interface for all ECOS Kernel Plugins / Cognitive Modules (Section VI).
    No module may directly invoke another module; communication occurs strictly through EventBus.
    """

    @property
    @abstractmethod
    def manifest(self) -> ModuleManifest:
        pass

    @property
    @abstractmethod
    def state(self) -> ModuleState:
        pass

    @abstractmethod
    def initialize(self, event_bus: EventBus, config: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def resume(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    @abstractmethod
    def health(self) -> ModuleHealth:
        pass

    @abstractmethod
    def handle_event(self, event: CognitiveEvent) -> None:
        pass

    @abstractmethod
    def publish_event(self, event: CognitiveEvent) -> None:
        pass
