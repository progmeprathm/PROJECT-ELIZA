# Collective Memory v0.9

## 1. Episodic vs Consolidated Knowledge
The `CognitiveWorkspace` maintains state for a single ongoing task. Upon completion (Success or Failure), observations and outcomes map to Episodic Memory. Consolidated knowledge emerges in `CoordinationMemory` when repeated episodes signal a structural pattern (e.g. cross-agent dependencies or environmental logic).

## 2. Preventing Context Pollution
Rather than indiscriminately copying the collective memory into every agent's prompt, the system relies on the `CoordinatorAgent` to search and fetch only the relevant `CollectiveLearningEvent` or `pattern` necessary to fulfill a capability request, keeping the `AgentContext` budget strictly under its 4000-token limit.

## 3. Negative Transfer and Conflict
If the `Coordinator` assigns a task based on an old pattern and the `Executor` encounters environmental change, a failure is triggered. `CoordinationMemory` detects this contradiction (`record_negative_transfer`) and flags the pattern as `CONFLICTED`, forcing future resolutions to be conditional rather than blindly absolute.
