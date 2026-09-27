# E.L.I.Z.A. Observability Architecture & Roadmap

This document outlines the architecture for connecting the E.L.I.Z.A. Runtime to the Studio UX, based on the principle of separating State APIs from the Event Bus.

## Architectural Foundation

```text
                E.L.I.Z.A. RUNTIME
                       │
                 ┌─────┴─────┐
                 │   STATE   │
                 │   STORE   │
                 └─────┬─────┘
                       │
                 ┌─────┴─────┐
                 │ EVENT BUS │
                 └─────┬─────┘
                       │
        ┌──────────────┼───────────────┐
        │              │               │
      Logs          Metrics          Replay
        │              │               │
        └──────────────┼───────────────┘
                       │
                  API / SSE
                       │
                       ▼
              E.L.I.Z.A. STUDIO
                       │
       ┌───────────────┼────────────────┐
       │               │                │
 Mission Control   Workspace       Cognition
```

## Phase 0 — Runtime Observability Contract
Define a strict schema for all events: `Event`, `EventType`, `EventID`, `Timestamp`, `RuntimeID`, `GoalID`, `TaskID`, `AgentID`, `Source`, `Payload`, `Provenance`, `SchemaVersion`.

## Phase 1 — Runtime Event Bus
Implement a runtime-scoped EventBus (`ecos/kernel/events.py`, `ecos/kernel/event_bus.py`) ensuring subscriber isolation, non-blocking delivery, bounded queues, and guaranteed runtime resilience (UI subscriber failure must not stop cognition).

## Phase 2 — Instrument the Runtime
Instrument execution state across the system:
- **ModelRouter**: `ModelRequested`, `ModelResponded`, `ModelFailed`, `ModelRouterFailover`, `LatencyMetric`
- **Agents**: `AgentCreated`, `AgentStateChanged`, `AgentTaskStarted`, `AgentTaskCompleted`, `AgentTaskFailed`
- **Coordinator**: `GoalCreated`, `GoalTreeUpdated`, `TaskDelegated`, `TaskReassigned`, `CoordinationCompleted`
- **Tools**: `ToolCalled`, `ToolExecuted`, `ToolFailed`
- **Verification & Replanning**: `VerificationStarted`, `VerificationCompleted`, `VerificationFailed`, `ReplanTriggered`, `PlanUpdated`

## Phase 3 — Memory + World Model
Emit structural telemetry (without leaking sensitive/raw content by default).
- **Memory**: `MemoryRetrieved`, `MemoryStored`, `MemoryInvalidated`
- **World Model**: `WorldModelUpdated`, `GraphNodeAdded`, `GraphEdgeAdded`, `GraphEdgeUpdated`

## Phase 4 — State API
Establish canonical state endpoints for Studio to fetch the snapshot upon initial load or reconnect:
`GET /api/state`, `GET /api/goals`, `GET /api/agents`, `GET /api/memory`, `GET /api/worldmodel`, `GET /api/runtime`, `GET /api/metrics`.

## Phase 5 — Live Event Transport
Implement Server-Sent Events (SSE) via `GET /api/stream` to push unilateral backend events to the frontend.

## Phase 6 — Studio State Engine
Introduce a frontend Event Dispatcher and State Store in E.L.I.Z.A. Studio. Incoming SSE events update the State Store, which reactively re-renders UI components.

## Phase 7 — Mission Control UI
Implement the Studio UX: Active Goals, Agent Activity, Runtime Timeline, System Health, and Cognition dashboards.

## Phase 8 — Reliability
Validate subscriber isolation, browser disconnect/reconnect resilience, UI crash handling, and backpressure handling at 1000 events/sec.

## Phase 9 — Replay
Build a Replay Engine that reads event logs to reconstruct the runtime timeline for forensic cognitive debugging.

## Phase 10 — Validation
Measure correctness: verify that Studio successfully reproduces the sequence of execution without missing state transitions or slowing down the runtime.
