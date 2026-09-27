# Planning Architecture

## 1. The Plan Object
In v0.5, a plan is a structured runtime object (`ecos.planning.plan.Plan`), not a free-form string. It contains:
- `plan_id`: Unique identifier
- `goal`: The overarching objective
- `assumptions`: Contextual beliefs the LLM relied upon when generating the plan
- `steps`: An array of `PlanStep` objects
- `status`: E.g., `CREATED`, `ACTIVE`, `COMPLETED`, `REPLANNING`, `FAILED`

## 2. The PlanStep Object
Each step must contain:
- `description`: Natural language intent
- `action`: A structured dict containing `tool` and `arguments`
- `expected_result`: What the model anticipates happening
- `dependencies`: Edges to prior step IDs (forcing sequential validation)

## 3. Planner
The `Planner` leverages the `ModelRouter` to synthesize a plan based on the goal, the `WorldModel` context, retrieved `Memory`, and the dynamically injected JSON schema of available `Tools`.

## 4. Executor and Validator
- `PlanValidator` ensures the plan is structurally sound and references valid tools before it ever executes.
- `PlanExecutor` steps through the plan, catching environmental failures, and triggering `revise_plan()` upon unexpected observations or errors.
