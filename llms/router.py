"""
Model Router.
Dynamically routes cognitive requests to the optimal LLM execution engine based on task intent, registry metadata, and benchmarks.
"""

import os
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
        
        provider_config = os.environ.get("ELIZA_MODEL_PROVIDER", "mock").lower()

        # Instantiate adapters pool based on config
        from llms.adapters.mock import MockAdapter
        from llms.adapters.cloud import CloudAPIAdapter
        
        if provider_config == "cloud":
            default_adapter = CloudAPIAdapter()
        else:
            default_adapter = MockAdapter()
            
        self.adapters: Dict[str, LanguageModel] = {
            "default": default_adapter,
            "deepseek-coder": CloudAPIAdapter(model_name="deepseek-coder") if provider_config == "cloud" else MockAdapter(model_name="deepseek-coder"),
            "qwen-2.5-72b": CloudAPIAdapter(model_name="qwen-2.5-72b") if provider_config == "cloud" else MockAdapter(model_name="qwen-2.5-72b"),
            "llama-3.1-8b": CloudAPIAdapter(model_name="llama-3.1-8b") if provider_config == "cloud" else MockAdapter(model_name="llama-3.1-8b"),
            "gemma-2-9b": CloudAPIAdapter(model_name="gemma-2-9b") if provider_config == "cloud" else MockAdapter(model_name="gemma-2-9b"),
            "mistral-large": CloudAPIAdapter(model_name="mistral-large") if provider_config == "cloud" else MockAdapter(model_name="mistral-large"),
        }

    def route_task(self, intent: TaskIntent, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Route prompt to optimal model adapter based on task intent, with local fallback."""
        selected_model_name = self.select_model(intent)
        adapter = self.adapters.get(selected_model_name, self.adapters["default"])

        try:
            # Execute on selected engine
            result = adapter.generate(prompt=prompt, schema=schema)
            if "routed_by" not in result:
                result["routed_by"] = "ModelRouter"
            result["task_intent"] = intent.value
            result["selected_model"] = selected_model_name
            return result
        except Exception as e:
            # Automatic fallback
            fallback_adapter = self.adapters["default"]
            try:
                result = fallback_adapter.generate(prompt=prompt, schema=schema)
                result["routed_by"] = "ModelRouter_Fallback"
                result["task_intent"] = intent.value
                result["selected_model"] = "fallback"
                result["fallback_reason"] = str(e)
                return result
            except Exception as e2:
                raise RuntimeError(f"MODEL_ERROR: Fallback failed. {e2}")

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
