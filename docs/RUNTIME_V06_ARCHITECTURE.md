# E.L.I.Z.A. Runtime v0.6 Architecture

## 1. Zero-Shot Planning Goal
v0.6 replaces deterministic mock logic with true live LLM interactions. The runtime architecture (World Model, Memory, Planner, Validator, Executor, Tool Registry) remains from v0.5, but is now exposed to a generalized live model through `CloudAPIAdapter` and `ModelRouter`.

## 2. Structured Output Enforcement
The `ModelRouter` and underlying `CloudAPIAdapter` now strictly use JSON Schemas to enforce structured outputs from the LLM. 
The LLM must independently map the natural language `goal` to a set of valid JSON `steps` where each `action` conforms exactly to the tool signatures provided dynamically in the prompt.

## 3. Generalization vs Overfitting
To prove cognitive architecture capability rather than benchmark overfitting, the architecture strictly decouples the `TaskGenerator` from the `Agent Context`. The agent receives only sensory observations and has no structural knowledge of the overarching benchmark logic or solution sequence.

## 4. Live Adaptability
- **Tool Selection:** The LLM receives the `ToolRegistry` schemas dynamically. It must select the correct tools (e.g., `calculator`, `memory_search`, `environment_action`).
- **Memory Triggering:** It must recognize when it needs historical context and use `memory_search`.
- **Replanning Trigger:** When `PlanExecutor` encounters environmental change and triggers `revise_plan`, the LLM must generate a recovered plan based on the failure observation injected into the prompt.
