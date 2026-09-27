# E.L.I.Z.A. Runtime v0.5 Audit

## 1. Current Runtime Flow (v0.4)
The current cognitive loop in `CognitiveShell` runs as a reactive cycle:
`Observation -> World Model -> Memory -> ModelRouter (LLM) -> Decision -> Execution (in benchmark runner) -> Memory Update`.
There is no representation of a "Plan". The LLM is prompted to select a single action to execute.

## 2. Current Action Representation
Actions are simple strings (e.g., `move_north`, `unlock_door_8592`) selected from a static schema. There is no concept of a "Tool" or structured arguments aside from suffix-based parsing (like `_8592`).

## 3. Current Observation Representation
Observations are dictionaries: `{"agent_location": (x, y), "door_locked": True, "message": "..."}`.

## 4. Current Memory & World Model
- **World Model**: Maintains `_state` and `_beliefs`. It purely represents current environment state.
- **Memory**: Stores `episode` dicts and computes embedding vectors (Real or Deterministic).

## 5. ModelRouter Behavior & Provider Interfaces
`ModelRouter` supports structured JSON output via `schema`. `CloudAPIAdapter` and `MockAdapter` return standard JSON. The architecture is solid for reasoning and tool use.

## 6. Existing Validation & Tracing
`CognitiveShell` does basic action presence validation (`ACTION_VALIDATION_ERROR`).
`run_v04_benchmark.py` captures detailed runtime traces for provenance.

## 7. Missing Planning Capabilities
- No `Plan` object to sequence multiple steps.
- No `PlanValidator` or `ToolRegistry`.
- The agent cannot replan; it merely reacts to the immediate observation.
- The agent cannot execute tools (e.g. calculator).

## 8. Risks/Confounds
- LLMs might try to execute multiple tools in a single step instead of sequential planning.
- The `MockAdapter` logic must be expanded to handle planning deterministically so that the v0.5 offline baseline reproduces cleanly.
- Strict provenance (leakage prevention) must be maintained when updating the planner with world model and memory context.
