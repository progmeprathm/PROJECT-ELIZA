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
        import urllib.request
        import urllib.error
        
        payload = {
            "model": self.model_name.replace("-local-fallback", "").replace("-local", ""),
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if schema:
            payload["format"] = "json"
            payload["prompt"] = prompt + f"\n\nReturn ONLY a valid JSON object matching this schema: {json.dumps(schema)}"

        req = urllib.request.Request(
            f"{self.endpoint_url}/api/generate",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result.get("response", "")
                
                if schema:
                    try:
                        parsed = json.loads(content)
                        return {**parsed, "model": self.model_name, "provider": "ollama-local"}
                    except Exception:
                        pass

                return {
                    "model": self.model_name,
                    "provider": "ollama-local",
                    "output_text": content,
                    "tokens_generated": result.get("eval_count", 0)
                }
        except urllib.error.URLError as e:
            raise RuntimeError(f"Ollama server not running or model not found. Make sure Ollama is installed and running on {self.endpoint_url}. Error: {str(e)}")

    def embed(self, text: str) -> List[float]:
        # Simple local 8-dim embedding simulation
        return [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    def tokenize(self, text: str) -> List[int]:
        return [hash(w) % 10000 for w in text.split()]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        tokens = [f"Token_{i}" for i in range(5)]
        for t in tokens:
            yield t
