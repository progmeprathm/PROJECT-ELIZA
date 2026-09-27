# E.L.I.Z.A. v0.6 Experiment: Live Model Benchmark

## 1. Experimental Design
The v0.6 benchmark tests whether a real LLM (e.g. OpenAI's `gpt-4o-mini`) can independently utilize the E.L.I.Z.A. runtime architecture to solve generalized, randomized tasks without any benchmark-specific hardcoded logic in the live prompt path. 

### Task Families
We generated 5 parameterized task families, testing:
- **A**: Information Retrieval (Memory)
- **B**: Arithmetic Tool Use (Calculator)
- **C**: Navigation
- **D**: Dependency Planning
- **E**: Recovery (Environmental Change triggering Replanning)

### Configurations
Tasks were run against 7 configurations:
- `MODEL_ONLY`: Raw LLM prompted to choose tools based on observations, lacking persistent `WorldModel` or `Planner`.
- `A` to `F`: The standard v0.5 ablation path (Stateless, World Model, Memory, Cognitive Core, Planning, Full v0.6).

## 2. Live Results
*(Note: As no LIVE API keys were injected during testing, `LIVE_MODEL = NOT_RUN` was recorded. The `mock` mode executed properly to validate reproducibility and structural soundness, but yields deterministic failure since it does not generalize to randomized tasks natively.)*

### Generalization Proof
The primary intent of v0.6 was establishing the framework to prove that:
`Raw Model Capability < Model + E.L.I.Z.A. Architecture`

When a live model is applied to `MODEL_ONLY` on complex dependency tasks (Family D) and environmental change tasks (Family E), it is expected to fail or hallucinate tool calls due to context window limits or lack of structured replanning. 
Conversely, configuration `F` (Full E.L.I.Z.A. v0.6) forces the LLM to output structured JSON plans (`planner_v05.py`), validates them against dynamic `ToolRegistry` schemas, and executes them in an isolated loop that explicitly detects errors ("Incorrect code.") and triggers constrained replanning (`revise_plan`).

## 3. Tool Use & Memory
The LLM dynamically receives:
- `CalculatorTool`
- `MemorySearchTool`
- `EnvironmentActionTool`

The `CloudAPIAdapter` enforces strict JSON schema output matching these tools. If the model incorrectly attempts `interact_item` when it should have called `environment_action` with `interact_item` as a parameter, the `PlanValidator` intercepts it as `PLAN_VALIDATION_FAILURE`, preventing arbitrary crashes.

## 4. Limitations
- **API Availability:** Live testing requires external API credentials (`OPENAI_API_KEY`).
- **Context Limits:** Deep replanning loops heavily inflate prompt length with historical traces, potentially exceeding token limits.
- **Model Discrepancies:** Not all providers natively support strict OpenAI-style JSON Schemas; graceful fallbacks (e.g., regex extraction) are necessary if porting to simpler models.

## 5. Scientific Conclusion
The architecture constructed in v0.6 enables robust empirical testing of foundational models as they interact with E.L.I.Z.A.'s cognitive structures. By completely decoupling the `TaskGenerator` from the `Agent Context` and running trials on completely randomized variants (e.g., differing passcodes, multipliers, and event triggers), the framework ensures any success by the model is a genuine consequence of its ability to parse the `Planner` schema, invoke `Tools`, and adapt to `Replanning` requests—not a result of benchmark overfitting.
