"""
Cloud API Adapter.
Connects ECOS Kernel to cloud-managed API providers (OpenAI-compatible endpoints).
"""

import os
import json
import urllib.request
import urllib.error
from typing import Any, Dict, Generator, List, Optional
from llms.base import LanguageModel
from llms.keys import get_api_key, load_dotenv

# Load any local .env file on module import
load_dotenv()


class CloudAPIAdapter(LanguageModel):
    """Adapter for cloud-managed LLM APIs (OpenAI format)."""

    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None, provider: str = "openai") -> None:
        super().__init__(model_name, endpoint_url=os.environ.get("ELIZA_API_ENDPOINT", "https://api.openai.com/v1"))
        self.api_key = api_key or get_api_key(provider)
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY", "")

    def generate(self, prompt: str, schema: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> Dict[str, Any]:
        # Dynamically resolve keys and endpoints per-request (Multi-Tenant Support)
        resolved_key = os.environ.get("OPENAI_API_KEY", "")
        resolved_endpoint = "https://api.openai.com/v1"

        if "llama" in self.model_name.lower() or "gemma" in self.model_name.lower() or "mixtral" in self.model_name.lower():
            resolved_key = os.environ.get("GROQ_API_KEY", "")
            resolved_endpoint = "https://api.groq.com/openai/v1"
        elif "deepseek" in self.model_name.lower():
            resolved_key = os.environ.get("DEEPSEEK_API_KEY", resolved_key)
            resolved_endpoint = "https://api.deepseek.com"
            
        if not resolved_key:
            raise ValueError(f"Missing API key for cloud provider '{self.model_name}' (Endpoint: {resolved_endpoint})")

        messages = [{"role": "user", "content": prompt}]
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature
        }

        # Groq/Deepseek don't fully support structured outputs the exact same way OpenAI does,
        # but if using OpenAI, we can keep the strict schema
        if schema and "openai.com" in resolved_endpoint:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "decision_schema",
                    "schema": schema,
                    "strict": True
                }
            }
        elif schema:
            # For Groq/DeepSeek, append instructions to the prompt to return JSON
            payload["response_format"] = {"type": "json_object"}
            messages[0]["content"] = prompt + f"\n\nReturn ONLY a valid JSON object matching this schema: {json.dumps(schema)}"
            
        req = urllib.request.Request(
            f"{resolved_endpoint}/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {resolved_key}"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result["choices"][0]["message"]["content"]
                
                try:
                    # If we expected JSON, try to parse it
                    parsed_content = json.loads(content)
                    if isinstance(parsed_content, dict):
                        return {**parsed_content, "model": self.model_name, "provider": "cloud"}
                except Exception:
                    pass
                
                return {
                    "model": self.model_name,
                    "provider": "cloud",
                    "output_text": content
                }
        except urllib.error.URLError as e:
            raise RuntimeError(f"MODEL_ERROR: Provider unavailable or timeout: {e}")

    def embed(self, text: str) -> List[float]:
        # Simple local embedding fallback to avoid extra API calls for testing
        return [float(ord(c)) / 255.0 for c in text[:64]] + [0.0] * max(0, 64 - len(text))

    def tokenize(self, text: str) -> List[int]:
        return [ord(c) for c in text[:8]]

    def stream(self, prompt: str) -> Generator[str, None, None]:
        yield f"Cloud stream response for {self.model_name}"
