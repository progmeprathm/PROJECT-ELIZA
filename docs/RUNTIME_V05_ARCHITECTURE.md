# E.L.I.Z.A. Runtime v0.5 Architecture

## 1. Core Paradigm Shift
v0.5 introduces a paradigm shift from a purely reactive `Observe -> Act` cognitive loop to a proactive `Goal -> Plan -> Execute -> Evaluate -> Replan` cycle. This establishes explicit planning as a first-class cognitive capability.

## 2. Component Hierarchy
The architecture rigorously ensures that planning does NOT bypass the underlying cognitive core:
```text
           Goal
            │
         Planner (v0.5)
            │
       PlanValidator
            │
       PlanExecutor
            │
      Tool / Environment
            │
         Observation
            │
    World Model Update
            │
      Memory Update
            │
      Plan Evaluation
            │
   Continue OR Replan
```

## 3. Abstraction Additions
- **Planning Abstraction**: `Plan`, `PlanStep`, `Planner`, and `PlanExecutor`.
- **Tool Abstraction**: `Tool`, `ToolRegistry`. The agent no longer emits generic action strings but invokes structured JSON tool definitions.
- **Environment**: A specialized deterministic `PlanningWorld` to validate the orchestration of sequential capabilities.

## 4. Preservation of Determinism
The `MockAdapter` was meticulously extended to simulate the exact structured output (JSON containing `assumptions` and `steps`) required by the v0.5 Planner without resorting to uncontrolled `eval()`.
