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
            "llama-3.1-8b-instant": CloudAPIAdapter(model_name="llama-3.1-8b-instant") if provider_config == "cloud" else MockAdapter(model_name="llama-3.1-8b-instant"),
            "gemma2-9b-it": CloudAPIAdapter(model_name="gemma2-9b-it") if provider_config == "cloud" else MockAdapter(model_name="gemma2-9b-it"),
            "llama-3.1-70b-versatile": CloudAPIAdapter(model_name="llama-3.1-70b-versatile") if provider_config == "cloud" else MockAdapter(model_name="llama-3.1-70b-versatile"),
        }

    def route_task(self, intent: TaskIntent, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Route prompt to optimal model adapter based on task intent, with waterfall fallback."""
        import os
        
        # 1. FORCE LOCAL CHECK
        if os.environ.get("ELIZA_FORCE_LOCAL") == "1":
            from llms.adapters.ollama import OllamaAdapter
            adapter = OllamaAdapter(model_name="llama-3-local")
            try:
                result = adapter.generate(prompt=prompt, schema=schema)
                result["routed_by"] = "ModelRouter_LocalOnly"
                return result
            except Exception as e:
                return {"error": f"Local LLM Failed: {str(e)}"}

        # 2. NORMAL CLOUD ROUTING
        selected_model_name = self.select_model(intent)
        
        # Define the Waterfall Chain
        fallback_chain = [
            (selected_model_name, self.adapters.get(selected_model_name, self.adapters["default"])),
            ("default (OpenAI Backup)", self.adapters["default"]),
            ("llama-3.1-8b-instant (Groq Backup)", self.adapters.get("llama-3.1-8b-instant", self.adapters["default"]))
        ]

        # Iterate through the cloud models
        for model_id, adapter in fallback_chain:
            try:
                result = adapter.generate(prompt=prompt, schema=schema)
                if "routed_by" not in result:
                    result["routed_by"] = "ModelRouter"
                result["task_intent"] = intent.value
                result["selected_model"] = model_id
                return result
            except Exception as e:
                print(f"[ModelRouter] Warning: {model_id} failed ({str(e)}). Trying next available LLM...")
                continue # Try the next one in the chain

        # 3. TOTAL CLOUD FAILURE -> AUTOMATIC OFFLINE FALLBACK
        print(f"[ModelRouter] CRITICAL: All Cloud APIs failed (Rate Limits/Offline). Shifting to Local LLM...")
        try:
            from llms.adapters.ollama import OllamaAdapter
            fallback_adapter = OllamaAdapter(model_name="llama-3-local-fallback")
            result = fallback_adapter.generate(prompt=prompt, schema=schema)
            result["routed_by"] = "ModelRouter_OfflineFallback"
            result["task_intent"] = intent.value
            result["selected_model"] = "ollama-local"
            return result
        except Exception as e2:
            raise RuntimeError(f"MODEL_ERROR: Complete Fallback chain failed. {str(e2)}")

    def select_model(self, intent: TaskIntent) -> str:
        """Select best model name for a given TaskIntent based on registry capabilities."""
        if intent == TaskIntent.CODING:
            return "deepseek-coder"
        elif intent == TaskIntent.REASONING:
            return "llama-3.1-70b-versatile"
        elif intent == TaskIntent.SUMMARIZATION:
            return "gemma2-9b-it"
        elif intent == TaskIntent.CONVERSATION:
            return "llama-3.1-8b-instant"
        else:
            return "llama-3.1-8b-instant"
