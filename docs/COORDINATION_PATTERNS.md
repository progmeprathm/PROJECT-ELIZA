# Coordination Patterns

## 1. Formalization of Strategy
A coordination pattern is explicitly tracked in `CoordinationMemory.patterns` mapping a descriptive strategy (e.g. `Parallel Execution`) to an array of `applicable_tasks` families.

## 2. Pattern Application
If a `CollectiveLearningEvent` logs that a specific pattern succeeded, subsequent visits to structurally similar tasks will bias the `CoordinatorAgent` toward employing that verified pattern over a generic fallback.

## 3. Metric Transparency
Patterns track `success_count` and `failure_count`. The `DelegationPolicy.ADAPTIVE` engine leverages these pattern profiles just as it leverages individual `AgentPerformanceTracker` stats to maximize efficiency per model call.
