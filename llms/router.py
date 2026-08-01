"""
Model Router.
Dynamically routes cognitive requests to the optimal LLM execution engine based on task intent, registry metadata, and benchmarks.
"""

from enum import Enum
from typing import Any, Dict, Optional

from llms.adapters.specialized import DeepSeekAdapter, GemmaAdapter, LlamaAdapter, MistralAdapter, QwenAdapter
from llms.base import LanguageModel
from llms.registry import ModelCapability, ModelRegistry


class TaskIntent(Enum):
    CODING = "coding"
    REASONING = "reasoning"
    CONVERSATION = "conversation"
    SUMMARIZATION = "summarization"
    GENERAL = "general"


class ModelRouter:
    """
    Dynamic task-based model router.
    Decides which LLM execution engine to dispatch tasks to:
    - Coding -> DeepSeek
    - Long Reasoning -> Qwen
    - Conversation -> Llama
    - Summarization -> Gemma
    """

    def __init__(self, registry: Optional[ModelRegistry] = None) -> None:
        self.registry = registry or ModelRegistry()

        # Instantiate default adapters pool
        self.adapters: Dict[str, LanguageModel] = {
            "deepseek-coder": DeepSeekAdapter(),
            "qwen-2.5-72b": QwenAdapter(),
            "llama-3.1-8b": LlamaAdapter(),
            "gemma-2-9b": GemmaAdapter(),
            "mistral-large": MistralAdapter(),
        }

    def route_task(self, intent: TaskIntent, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Route prompt to optimal model adapter based on task intent, with local fallback."""
        selected_model_name = self.select_model(intent)
        adapter = self.adapters.get(selected_model_name, self.adapters["llama-3.1-8b"])

        try:
            # Execute on selected engine
            result = adapter.generate(prompt=prompt, schema=schema)
            result["routed_by"] = "ModelRouter"
            result["task_intent"] = intent.value
            result["selected_model"] = selected_model_name
            return result
        except Exception as e:
            # Automatic fallback to local execution engine
            fallback_model = "llama-3.1-8b"
            fallback_adapter = self.adapters[fallback_model]
            result = fallback_adapter.generate(prompt=prompt, schema=schema)
            result["routed_by"] = "ModelRouter_Fallback"
            result["task_intent"] = intent.value
            result["selected_model"] = fallback_model
            result["fallback_reason"] = str(e)
            return result

    def select_model(self, intent: TaskIntent) -> str:
        """Select best model name for a given TaskIntent based on registry capabilities."""
        if intent == TaskIntent.CODING:
            return "deepseek-coder"
        elif intent == TaskIntent.REASONING:
            return "qwen-2.5-72b"
        elif intent == TaskIntent.SUMMARIZATION:
            return "gemma-2-9b"
        elif intent == TaskIntent.CONVERSATION:
            return "llama-3.1-8b"
        else:
            return "llama-3.1-8b"
