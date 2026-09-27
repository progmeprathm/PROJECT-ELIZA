# Tool System

## 1. Tool Interface
The `ecos.tools.base.Tool` class mandates that every tool define a strict `input_schema` and `output_schema` to guide the LLM's structured output.

## 2. ToolRegistry
The `ToolRegistry` aggregates tools and serves their JSON schemas to the `Planner` during the reasoning prompt. It also handles dynamic execution and dependency injection (via a `context` dictionary containing the `environment` and `memory_system`).

## 3. Implemented Tools
- **CalculatorTool**: Evaluates arithmetic expressions safely (avoiding raw unrestricted `eval`).
- **MemorySearchTool**: Allows explicit queries against the `ECOSMemorySystem`.
- **EnvironmentActionTool**: Exposes the standard `move_north`, `move_east`, `read_note`, etc., interactions with the underlying simulation.

## 4. Validation
Tool arguments are strictly checked against `input_schema` before execution. If a tool fails (e.g. invalid arithmetic expression), it returns an error dict rather than crashing the cognitive loop, allowing the `PlanExecutor` to catch the failure and trigger replanning.
