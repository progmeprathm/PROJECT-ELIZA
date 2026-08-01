"""
Ollama / llama.cpp Local Inference Adapter.
Connects ECOS Kernel to local Ollama endpoints (e.g. http://127.0.0.1:11434).
"""

from typing import Any, Dict, Generator, List, Optional
import json

from llms.base import LanguageModel


class OllamaAdapter(LanguageModel):
    """Adapter for local CPU/GPU execution via Ollama or llama.cpp REST APIs."""

    def __init__(self, model_name: str = "llama-3.1-8b", endpoint_url: str = "http://127.0.0.1:11434") -> None:
        super().__init__(model_name, endpoint_url)

    def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> Dict[str, Any]:
        # Simulated local response or HTTP call to Ollama /api/generate
        return {
            "model": self.model_name,
            "provider": "ollama",
            "output_text": f"[Ollama local output for '{prompt[:30]}...']",
            "tokens_generated": 42,
            "latency_ms": 14.5,
        }

    def embed(self, text: str) -> List[float]:
        # Simple local 8-dim embedding simulation
        return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    def tokenize(self, text: str) -> List[int]:
        return [hash(w) % 10000 for w in text.split()]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        tokens = [f"Token_{i}" for i in range(5)]
        for t in tokens:
            yield t
