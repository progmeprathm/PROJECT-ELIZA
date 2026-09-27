# E.L.I.Z.A. Runtime v0.2 Architecture

## 1. Provider Architecture
The v0.2 runtime abstracts the Language Model connection entirely via the `ModelRouter`. Providers are configured using environment variables, notably `ELIZA_MODEL_PROVIDER`. 
- `mock`: Uses `MockAdapter` for deterministic, offline testing without an external API.
- `cloud`: Uses `CloudAPIAdapter` for actual connection to an OpenAI-compatible endpoint.

## 2. Runtime Flow
1. **Perceive:** Observations flow from the Environment into the CognitiveShell.
2. **World Modeling:** Observation updates deterministic state and assertions in `ECOSWorldModel`.
3. **Memory Retrieval:** The `ECOSMemorySystem` retrieves related episodic or semantic memory using embedding-based cosine similarity.
4. **Reasoning:** A constructed prompt is sent to `ModelRouter`, which delegates to the configured adapter.
5. **Validation:** The router enforces structured JSON schema. The CognitiveShell catches `ACTION_VALIDATION_ERROR`s.
6. **Action:** Valid actions are passed to the Environment.
7. **Consolidation:** The episode (observation, action, reasoning, state) is embedded and stored back into memory.

## 3. Action Validation
To prevent hallucinated interactions, the system employs schema validation at the router level and authoritative action validation at the environment level. Unknown or impossible actions (e.g., unlocking a door without a key or wrong password) are caught by the environment which returns an error observation, preventing state corruption.

## 4. Error Handling
- **MODEL_ERROR**: Thrown when a cloud provider times out or API keys are missing.
- **ACTION_VALIDATION_ERROR**: Caught when the model fails to return a valid action structure.
The shell returns these as explicit reasons in its output trace rather than failing silently.
