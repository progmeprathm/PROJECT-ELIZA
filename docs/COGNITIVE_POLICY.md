# Cognitive Policy

## 1. Meta-Runtime Decision Engine
The `MetaRuntimePolicy` controls the overarching flow of E.L.I.Z.A. It observes `RuntimeState` (number of failures, current workflow status, and available knowledge base) and maps it to a `RuntimePolicyAction`.

## 2. Dynamic Transitions
Rather than relying on hardcoded workflows (`EXECUTE -> VERIFY -> REPLAN`), the policy engine dictates whether the agent should `DELEGATE`, `VERIFY`, or completely `ABORT`. 
This allows E.L.I.Z.A. to fail safely and gracefully. If an agent loops on a bad task indefinitely, `MetaRuntimePolicy` recognizes the budget constraints (`max_model_calls`, `max_replans`) and executes `ABORT`, emitting `BUDGET_EXCEEDED` to keep compute boundaries sane.
