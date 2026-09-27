# E.L.I.Z.A. Runtime Integration Audit

## 1. Current Architecture
The E.L.I.Z.A. project has a well-defined architecture specified in a series of canonical `.md` files. 
The Python backend contains structural representations of this architecture across various modules (`ecos/`, `llms/`, `companion/`).
Currently, the system is primarily a **mocked architectural shell** used to validate design boundaries via `run_tests.py` and simulated milestones (`run_master_validation.py`, `run_rrs_simulation.py`).

## 2. Runtime Data Flow (Intended)
```text
Input 
  ↓ 
CognitiveShell (Entry point for interactions)
  ↓ 
Perception / Context Construction
  ↓ 
WorldModel Retrieval (Current state / beliefs)
  ↓ 
Memory Retrieval (Past experiences)
  ↓ 
ModelRouter (Dispatches to specific LLM provider)
  ↓ 
Reasoning / Decision (LLM processing)
  ↓ 
Action (Generated decision to execute)
  ↓ 
Environment / Simulator (Execution context)
  ↓ 
Observation (Result of action)
  ↓ 
WorldModel Update (New beliefs/state)
  ↓ 
Memory Update (Store experience)
  ↓ 
Cycle Result
```

## 3. Existing Gaps
- **Model Providers:** The `llms/adapters/cloud.py` and related adapters return hardcoded JSON strings instead of calling actual LLM endpoints.
- **Environment:** There is no actual interactive environment or simulator. `run_rrs_simulation.py` just prints static success messages.
- **CognitiveShell:** Hardcodes responses for specific commands instead of orchestrating a cognitive loop.
- **Cognitive Loop Orchestration:** No module currently links `Memory`, `WorldModel`, and `ModelRouter` into a cohesive, sequential loop.
- **WorldModel:** `ECOSWorldModel` supports adding and revising beliefs but doesn't track rich entities or differentiate between observed state and beliefs in a dynamic way.
- **Memory:** `ECOSMemorySystem` supports basic string-matching retrieval from an in-memory dictionary.

## 4. Integration Points
- **CognitiveShell (`companion/shell.py`)**: Needs to be refactored to orchestrate the cycle rather than return mock strings.
- **ModelRouter (`llms/router.py`)**: Needs at least one adapter to be connected to a real provider (e.g., via OpenAI-compatible endpoint), while retaining a mock for deterministic tests.
- **Memory System (`ecos/memory/system.py`)**: Can remain in-memory but must be actively queried and updated by the CognitiveShell during the loop.
- **WorldModel (`ecos/world/graph.py`)**: Needs enhancements to handle deterministic environment states and integrate into the loop.
- **Simulator (`run_rrs_simulation.py`)**: Needs to be completely rewritten to initialize a simple environment (e.g., GridWorld or StateMachine), instantiate the CognitiveShell, and run N cycles to achieve a goal.

## 5. Files to Modify
- `companion/shell.py`: Implement `run_cycle`.
- `ecos/world/graph.py`: Complete `WorldModel` implementation (state tracking, observation ingestion).
- `ecos/memory/system.py`: Ensure episodic/semantic distinction is sufficient for the loop.
- `llms/adapters/cloud.py` (or similar): Implement a real OpenAI/provider client.
- `run_rrs_simulation.py`: Replace mock prints with an actual Goal Achievement simulation loop.

## 6. Files That Should Remain Untouched
- Canonical Specs (`ELIZA_*.md`)
- `run_tests.py` and existing test architectures (we must ensure they continue passing).
- `ELIZA_OBJECTS.py` (Unless missing fields for runtime integration).
- Any Advanced `ecos/civilization/` or `ecos/evolution/` modules (out of scope).

## 7. Proposed Minimal Implementation Path
1. **Model Provider**: Implement a real provider in `CloudAPIAdapter` (e.g., OpenAI API) using an environment variable `OPENAI_API_KEY`, but fallback to deterministic mock if not set.
2. **Environment Simulator**: Define a simple `Environment` class with an agent location/goal, actions, and observations.
3. **WorldModel & Memory**: Enhance `ECOSWorldModel` to track state and `ECOSMemorySystem` to store experiences.
4. **Cognitive Loop (CognitiveShell)**: Implement `run_cycle()` in `CognitiveShell` that performs:
   `Perception -> Retrieve Memory -> Retrieve WorldState -> Prompt LLM -> Parse Action -> Environment Step -> Update WorldState -> Update Memory -> Return Result`
5. **RRS Experiment**: Update `run_rrs_simulation.py` to run the loop against the Environment until the goal is achieved.
6. **Tests**: Add integration tests validating the loop.
7. **Studio UI**: Update UI backend logic to query live memory and world model states, if necessary.
