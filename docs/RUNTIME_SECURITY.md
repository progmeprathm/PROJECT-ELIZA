# Runtime Security & Governance

## 1. Resource Budgets
An autonomous runtime must remain bounded. `ELIZARuntime` enforces explicit constraints defined at instantiation:
- `max_model_calls`
- `max_tool_calls`
- `max_replans`
- `max_runtime_seconds`

## 2. Execution Boundaries
Direct external system modifications (e.g. executing unsafe code) remain entirely walled off. `PlanValidator` + `ToolRegistry` ensure actions map solely to predefined, verifiable operations.

## 3. Capability Enforcement
Agent assignment is verified by `DynamicDelegator`. If an assigned agent lacks a tool capability string, `VerificationSystem` rejects it, throwing `CAPABILITY_DENIED`. The runtime cannot spawn arbitrary threads, overwrite evaluator boundaries, or manipulate underlying LLM training parameters.
