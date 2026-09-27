"""
LLM Model Adapters Suite.
"""

from llms.adapters.cloud import CloudAPIAdapter
from llms.adapters.ollama import OllamaAdapter
from llms.adapters.specialized import DeepSeekAdapter, GemmaAdapter, LlamaAdapter, QwenAdapter
from llms.adapters.vllm import VLLMAdapter

__all__ = [
    "OllamaAdapter",
    "VLLMAdapter",
    "CloudAPIAdapter",
    "DeepSeekAdapter",
    "QwenAdapter",
    "LlamaAdapter",
    "GemmaAdapter",
]
