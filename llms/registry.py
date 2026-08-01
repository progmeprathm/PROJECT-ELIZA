"""
Model Capability Registry.
Maintains quantitative benchmarks and capability ratings across supported local and cloud LLMs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ModelCapability(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class ModelMetadata:
    name: str
    provider: str  # ollama, vllm, cloud, custom
    reasoning: ModelCapability
    coding: ModelCapability
    speed: ModelCapability
    cost: str  # free, low, medium, high
    context_window_k: int
    is_local: bool
    vision_capable: bool = False
    recommended_tasks: List[str] = field(default_factory=list)


class ModelRegistry:
    """Registry maintaining metadata and benchmark scores for all registered model engines."""

    def __init__(self) -> None:
        self.registry: Dict[str, ModelMetadata] = {}
        self._populate_default_registry()

    def _populate_default_registry(self) -> None:
        self.register(
            ModelMetadata(
                name="deepseek-coder",
                provider="vllm",
                reasoning=ModelCapability.HIGH,
                coding=ModelCapability.VERY_HIGH,
                speed=ModelCapability.HIGH,
                cost="free",
                context_window_k=64,
                is_local=True,
                recommended_tasks=["coding", "debugging", "refactoring"],
            )
        )
        self.register(
            ModelMetadata(
                name="qwen-2.5-72b",
                provider="vllm",
                reasoning=ModelCapability.VERY_HIGH,
                coding=ModelCapability.HIGH,
                speed=ModelCapability.MEDIUM,
                cost="free",
                context_window_k=128,
                is_local=True,
                recommended_tasks=["long_reasoning", "planning", "scientific_review"],
            )
        )
        self.register(
            ModelMetadata(
                name="llama-3.1-8b",
                provider="ollama",
                reasoning=ModelCapability.MEDIUM,
                coding=ModelCapability.MEDIUM,
                speed=ModelCapability.VERY_HIGH,
                cost="free",
                context_window_k=128,
                is_local=True,
                recommended_tasks=["conversation", "chat", "general"],
            )
        )
        self.register(
            ModelMetadata(
                name="gemma-2-9b",
                provider="ollama",
                reasoning=ModelCapability.MEDIUM,
                coding=ModelCapability.MEDIUM,
                speed=ModelCapability.VERY_HIGH,
                cost="free",
                context_window_k=32,
                is_local=True,
                recommended_tasks=["summarization", "fast_filtering"],
            )
        )
        self.register(
            ModelMetadata(
                name="mistral-large",
                provider="cloud",
                reasoning=ModelCapability.HIGH,
                coding=ModelCapability.HIGH,
                speed=ModelCapability.HIGH,
                cost="medium",
                context_window_k=128,
                is_local=False,
                recommended_tasks=["analysis", "multi_language"],
            )
        )

    def register(self, metadata: ModelMetadata) -> None:
        self.registry[metadata.name] = metadata

    def get(self, name: str) -> Optional[ModelMetadata]:
        return self.registry.get(name)

    def list_all(self) -> List[ModelMetadata]:
        return list(self.registry.values())
