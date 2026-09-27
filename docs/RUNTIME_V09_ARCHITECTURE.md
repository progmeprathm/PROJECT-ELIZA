# E.L.I.Z.A. Runtime v0.9 Architecture

## 1. Centralized Engine: AgentRuntime
To enforce strict state lifecycle boundaries, all agent execution now routes through `ecos/agents/runtime.py`. It emits explicit, trace-friendly events (`AGENT_STARTED`, `AGENT_FAILED`, etc.) ensuring no state transitions are hidden.

## 2. Dynamic Delegation
Instead of hardcoding workflows, the `CoordinatorAgent` uses `DynamicDelegator`. Based on the selected `DelegationPolicy` (Fixed, Capability, Adaptive), the delegator queries the `AgentRegistry` and dynamically assigns agents using `PerformanceTracker` profiles to prioritize historically successful workers.

## 3. Cognitive Workspace and Verification
Agents perform tasks and append candidate solutions to the `CognitiveWorkspace`. An independent `VerificationSystem` intercepts these candidates and tests them for validity (e.g. valid JSON structure, matching expected criteria) before allowing the `Coordinator` to declare the task completed.

## 4. Coordination Memory
Successfully orchestrated patterns and failure recoveries are saved in `CoordinationMemory` via `CollectiveLearningEvent`. This fulfills the requirement that architecture itself can become persistent knowledge, enabling cross-agent transfer.
