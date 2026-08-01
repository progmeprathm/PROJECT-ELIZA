"""
Cloud API Adapter.
Connects ECOS Kernel to cloud-managed API providers (OpenAI, Anthropic, Mistral Cloud).
"""

from typing import Any, Dict, Generator, List, Optional
from llms.base import LanguageModel
from llms.keys import get_api_key, load_dotenv

# Load any local .env file on module import
load_dotenv()


class CloudAPIAdapter(LanguageModel):
    """Adapter for cloud-managed LLM APIs."""

    def __init__(self, model_name: str = "mistral-large", api_key: Optional[str] = None, provider: str = "mistral") -> None:
        super().__init__(model_name, endpoint_url="https://api.mistral.ai/v1")
        # Use provided key, or try to get from keys registry/env
        self.api_key = api_key or get_api_key(provider)

    def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError(f"Missing API key for cloud provider '{self.model_name}'")
            
        return {
            "model": self.model_name,
            "provider": "cloud",
            "output_text": f"[Cloud API output for '{prompt[:30]}...']",
            "tokens_generated": 85,
            "latency_ms": 120.0,
        }

    def embed(self, text: str) -> List[float]:
        return [0.12 * i for i in range(8)]

    def tokenize(self, text: str) -> List[int]:
        return [ord(c) for c in text[:8]]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        yield f"Cloud stream response for {self.model_name}"
