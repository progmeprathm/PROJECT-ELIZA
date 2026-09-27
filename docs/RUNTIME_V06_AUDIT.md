# E.L.I.Z.A. Runtime v0.6 Audit

## 1. Components Reusable Without Modification
- **World Model (`ecos/world/graph.py`)**: Already maintains state independently and handles beliefs.
- **Memory (`ecos/memory/system.py`)**: `ECOSMemorySystem` and semantic retrieval mechanisms are reusable.
- **Plan Object & Executor (`ecos/planning/plan.py`, `executor.py`)**: Well-structured and execute JSON steps correctly.
- **Tool System (`ecos/tools/`)**: Tool interfaces (`ToolRegistry`, `CalculatorTool`, etc.) strictly enforce schema logic and error handling.

## 2. Components Coupled to Mock Behavior
- **`run_v05_benchmark.py`**: Hardcoded to `PlanningWorld`. Does not support randomized, zero-shot task generation.
- **`PlanningWorld`**: Hardcoded locations, fixed values (e.g., base code = 12). Lacks variability and multiple difficulty tiers.

## 3. Benchmark-Specific Logic to Remove
- The `Planner` and `CognitiveShell` in v0.5 were heavily supported by `MockAdapter`, which contained exact strings (e.g. `12 * 4` or `move_east`) based on prompt matching. The live provider must receive zero benchmark hints.

## 4. Live Provider Readiness & Structured Output
- `ModelRouter` and `CloudAPIAdapter` support the `schema` argument, meaning they are ready to produce JSON for `Planner`.
- However, if the LLM output is slightly malformed (e.g., markdown code blocks), the current `CloudAPIAdapter` might fail. We need robust JSON parsing in the router or adapter to strip ```json blocks.

## 5. Tracing Limitations
- The current trace in `executor.py` captures basic tool outputs, but does not capture granular `model_output_errors` or `plan_validation_errors` consistently across reactive and planned runtimes.
- Need a formalized Trace object or logging for the experiment metrics.

## 6. Goal for v0.6
Introduce a robust `TaskGenerator` with unseen variants, and a benchmark runner that evaluates `MODEL_ONLY` vs `A-F` cleanly.
