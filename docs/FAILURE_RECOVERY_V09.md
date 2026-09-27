# Failure Recovery v0.9

## 1. Failure Injection
In tasks representing `Family D` (Failure Recovery) or `Family G` (Conflict), failure is highly probable on the initial execution cycle due to simulated stale intelligence or tool breakage.

## 2. Reassignment Loop
When the `AgentRuntime` catches `AGENT_FAILED`, it triggers an event. The `CoordinatorAgent` intercepts the failure. Using the `DynamicDelegator`, the coordinator excludes the failed candidate (`Executor A`) and re-queries the `AgentRegistry` for an alternative candidate (`Executor B`) with the appropriate capability. 

## 3. Idempotency & Provenance
Failed state changes are rejected from entering the `WorldModel`, preventing duplication or state-tearing. Only cleanly verified, recovering iterations are stored, preserving rigorous event provenance.
