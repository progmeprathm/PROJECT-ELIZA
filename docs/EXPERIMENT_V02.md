# E.L.I.Z.A. Runtime v0.2 Experiment

## 1. Goal
The objective is to demonstrate that the E.L.I.Z.A. runtime correctly leverages persistent episodic memory (Memory), world modeling (State Tracking), and sequential logic (Cognition) in a closed loop to solve a puzzle requiring long-term knowledge retention.

## 2. Methodology & Configurations
The experiment is executed in `run_rrs_simulation.py` inside a deterministic 1D GridWorld using the `MockAdapter` to ensure reproducibility. Three agent configurations are tested on the exact same environment:

- **Configuration A (Stateless LLM)**: No memory, no world model. Evaluates based purely on the current environment observation.
- **Configuration B (LLM + World Model)**: Maintains state and short-term beliefs about the world, but no chronological memory retrieval.
- **Configuration C (E.L.I.Z.A.)**: Full ECOS architecture. Synthesizes memory, world model, and current state.

## 3. The Memory Relevance Environment
1. The agent starts at location 0. Target is location 4.
2. Location 1 contains a note with a password ("8592").
3. Location 3 is blocked by a locked door requiring action `unlock_door_8592`.
4. The agent must discover the password early, move away, and then recall/apply the password later when it encounters the door.

## 4. Results (Deterministic Mock Baseline)
- **Config A**: FAILED (Cycles: 10). The stateless agent never chooses to read the note because it lacks context, and repeatedly bangs against the locked door.
- **Config B**: SUCCEEDED (Cycles: 6). Succeeded because the `ECOSWorldModel` retains past observations as short-term beliefs, thus holding the password in the context window.
- **Config C**: SUCCEEDED (Cycles: 6). Successfully completed the cognitive cycle:
  - Perception (Read note) -> Embedded to Memory.
  - Encounter door -> Recalled memory via semantic search.
  - Action (Unlock door).

## 5. Metrics Tracked
- `experiment`: Configuration name
- `provider`: "mock" or "cloud"
- `cycles`: Integer count of iterations.
- `goal_achieved`: Boolean success.
- `actions`: Chronological trace of actions taken.
- `errors`: List of validation or execution errors.

## 6. Reproducibility & Live Providers
The default configuration runs purely offline using the deterministic `MockAdapter` and local character-frequency embeddings. Setting `ELIZA_MODEL_PROVIDER=cloud` with valid API keys will route tasks to external models, producing nondeterministic traces depending on model capability.

## 7. Limitations
- Config B currently acts as a pseudo-memory because `ECOSWorldModel` accumulates all past observations. In future iterations, the World Model will be strictly semantic (graph-based facts) rather than a chronological log of events (which is Memory's job).
- The embedding scheme is mathematically naive (character frequency hash) to avoid external dependencies, though structurally identical to actual semantic vector DB pipelines.
