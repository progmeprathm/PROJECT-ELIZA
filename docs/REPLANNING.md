# Replanning

## 1. Monitoring Expected Results
The `PlanExecutor` evaluates the result of each step. If the output indicates a failure—such as a tool throwing an error, or the environment returning an "Incorrect", "Unknown", or "prevents" message—the executor immediately halts the active plan.

## 2. The Replanning Trigger
Upon failure:
1. The step `status` is marked `FAILED`.
2. The plan `status` becomes `REPLANNING`.
3. The `Planner.revise_plan()` method is invoked.

## 3. Contextual Injection
When replanning, the `Planner` injects the failure observation directly into the new prompt:
`Note: The previous plan failed. Failure observation: {observation}`
This ensures the LLM understands *why* the plan failed and can adapt (e.g. calculating a new code if the environmental multiplier changed).

## 4. Bounded Recovery
Replanning is bounded by a `max_replans` parameter (default 3) to prevent infinite loops in the event of systemic failure.
