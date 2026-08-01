"""
Abstract Model Interface (LanguageModel ABC).
Stable execution engine contract for all open-source and cloud model adapters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Optional


class LanguageModel(ABC):
    """Abstract Base Class for all LLM execution engines in ELIZA."""

    def __init__(self, model_name: str, endpoint_url: Optional[str] = None) -> None:
        self.model_name = model_name
        self.endpoint_url = endpoint_url

    @abstractmethod
    def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate response given a prompt and optional JSON schema for structured output."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate vector embedding representation of input text."""
        pass

    @abstractmethod
    def tokenize(self, text: str) -> List[int]:
        """Convert input text into token IDs."""
        pass

    @abstractmethod
    def stream(self, prompt: str) -> Generator[str, None, None]:
        """Stream response chunks for real-time output."""
        pass
