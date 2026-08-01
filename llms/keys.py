import os
from typing import Dict, Optional

# In-memory registry of API keys
_API_KEYS: Dict[str, str] = {}

def set_api_key(provider: str, api_key: str) -> None:
    """
    Set an API key for a specific provider (e.g., 'openai', 'anthropic', 'deepseek', 'mistral').
    This takes precedence and also exports to os.environ.
    """
    provider_normalized = provider.strip().lower()
    _API_KEYS[provider_normalized] = api_key
    # Also set in environment for any adapters that might read os.environ directly
    env_var = f"{provider_normalized.upper()}_API_KEY"
    os.environ[env_var] = api_key

def get_api_key(provider: str) -> Optional[str]:
    """
    Retrieve an API key for a specific provider.
    Checks in-memory registry first, then environment variables.
    """
    provider_normalized = provider.strip().lower()
    
    # 1. Check in-memory registry
    if provider_normalized in _API_KEYS:
        return _API_KEYS[provider_normalized]
    
    # 2. Check environment variables
    env_var = f"{provider_normalized.upper()}_API_KEY"
    if env_var in os.environ:
        return os.environ[env_var]
        
    return None

def load_dotenv(filepath: str = ".env") -> None:
    """
    Lightweight .env loader to load API keys securely without external dependencies.
    """
    if not os.path.exists(filepath):
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("\"'")
                os.environ[key] = val
                
                # If it's an API key format provider_API_KEY, auto-register
                if key.endswith("_API_KEY"):
                    provider = key.replace("_API_KEY", "").lower()
                    _API_KEYS[provider] = val
