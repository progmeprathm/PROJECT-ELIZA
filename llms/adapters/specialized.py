"""
Specialized Model Adapters.
Dedicated model adapters for DeepSeek (coding), Qwen (reasoning), Llama (chat), Gemma (summarization), Mistral.
"""

from llms.adapters.cloud import CloudAPIAdapter
from llms.adapters.ollama import OllamaAdapter
from llms.adapters.vllm import VLLMAdapter


class DeepSeekAdapter(CloudAPIAdapter):
    def __init__(self) -> None:
        super().__init__(model_name="deepseek-coder", provider="deepseek")


class QwenAdapter(CloudAPIAdapter):
    def __init__(self) -> None:
        super().__init__(model_name="qwen-2.5-72b", provider="qwen")


class LlamaAdapter(OllamaAdapter):
    def __init__(self) -> None:
        super().__init__(model_name="llama-3.1-8b")


class GemmaAdapter(OllamaAdapter):
    def __init__(self) -> None:
        super().__init__(model_name="gemma-2-9b")


class MistralAdapter(CloudAPIAdapter):
    def __init__(self) -> None:
        super().__init__(model_name="mistral-large", provider="mistral")
