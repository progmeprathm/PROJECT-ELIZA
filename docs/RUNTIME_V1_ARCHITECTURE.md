# E.L.I.Z.A. Runtime v1.0 Architecture

## 1. The Canonical Cognitive Loop
The v1.0 engine formally defines E.L.I.Z.A.'s cognitive loop:
`Perception -> World Model -> Memory -> Knowledge -> Planner -> Coordinator -> Specialized Agents -> Tools -> Execution -> Verification -> Replanning -> Learning -> Persistent State`. 

## 2. Kernel Design
The kernel acts as a central nervous system. Rather than duplicating subsystem databases, `ELIZARuntime` operates by requesting actions via `MetaRuntimePolicy` and delegating execution to the `CoordinatorAgent`, capturing outputs into standard `RuntimeState`.

## 3. Strict Determinism and Snapshotting
Through `RuntimeSnapshot`, the exact configuration of WorldModel, Knowledge, and Workspace can be serialized to disk. This enables restarting the runtime mid-task or reloading the agent in a new environment with its historical knowledge completely intact.
