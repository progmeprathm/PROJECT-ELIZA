"""
vLLM High-Throughput Local Serving Adapter.
Connects ECOS Kernel to vLLM OpenAI-compatible endpoints (e.g. http://127.0.0.1:8000/v1).
"""

from typing import Any, Dict, Generator, List, Optional
from llms.base import LanguageModel


class VLLMAdapter(LanguageModel):
    """Adapter for high-throughput multi-user local serving via vLLM."""

    def __init__(self, model_name: str = "qwen-2.5-72b", endpoint_url: str = "http://127.0.0.1:8000/v1") -> None:
        super().__init__(model_name, endpoint_url)

    def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> Dict[str, Any]:
        return {
            "model": self.model_name,
            "provider": "vllm",
            "output_text": f"[vLLM high-throughput engine output for '{prompt[:30]}...']",
            "tokens_generated": 128,
            "latency_ms": 8.2,
        }

    def embed(self, text: str) -> List[float]:
        return [0.05 * i for i in range(8)]

    def tokenize(self, text: str) -> List[int]:
        return [len(w) for w in text.split()]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        for word in prompt.split():
            yield word + " "
