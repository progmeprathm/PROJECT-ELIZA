# E.L.I.Z.A. Runtime v0.2 Audit

## 1. Deterministic Fallback Trigger
The deterministic fallback is currently located in `companion/shell.py` within the `run_cycle` method. If the `decision_result` from the `ModelRouter` does not contain a structured `"action"` key (which the mock providers currently omit), it falls back to explicit state-matching rules to ensure deterministic execution for tests.

## 2. ModelRouter Provider Selection
`ModelRouter` (`llms/router.py`) maps `TaskIntent` (e.g., `CODING`, `REASONING`) to string identifiers (e.g., `"qwen-2.5-72b"`). It currently initializes a hardcoded dictionary of instantiated specialized adapters and fetches from it.

## 3. CloudAPIAdapter Interface
`CloudAPIAdapter` (`llms/adapters/cloud.py`) implements the `LanguageModel` interface, exposing:
- `generate(prompt, schema, temperature)`
- `embed(text)`
- `tokenize(text)`
- `stream(prompt)`
It currently returns hardcoded JSON output in `generate` and does not actually make HTTP requests.

## 4. Prompt Construction
Prompts are constructed locally inside `CognitiveShell.run_cycle` using Python f-strings, injecting `world_state`, `beliefs`, `retrieved_mems`, and the `goal/input`.

## 5. Model Response Parsing
In `CognitiveShell.run_cycle`, the response is parsed implicitly as a Python dictionary. The shell tries to extract `"action"` and `"reasoning"` using `decision_result.get()`.

## 6. Action Validation
There is weak action validation in the shell. The main validation boundary is inside `SimpleEnvironment.step` (`ecos/simulation/environment.py`), which checks for exact string matches like `"move_forward"` and ignores unknown actions.

## 7. Memory Storage & Retrieval
`ECOSMemorySystem` (`ecos/memory/system.py`) stores memories in a standard Python dictionary `_store_dict`. Retrieval is implemented as a simple substring match: `query.lower() in str(mem.payload).lower()`. It does not support semantic retrieval.

## 8. Secrets & Configuration
Secrets management exists in `llms/keys.py`. It provides `get_api_key`, `set_api_key`, and a lightweight `load_dotenv` function. It supports an in-memory registry falling back to `os.environ`.

## 9. Provider Substitution Architecture
The architecture is well-suited for provider substitution. `CognitiveShell` calls `ModelRouter.route_task()`. `ModelRouter` can be modified to check configuration variables (e.g., `ELIZA_MODEL_PROVIDER`) and instantiate/inject either a real `CloudAPIAdapter` implementation or a Mock provider, without requiring changes to the shell.
