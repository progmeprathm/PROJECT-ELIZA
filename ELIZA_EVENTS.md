# ELIZA Events Specification

> **Version**: 1.0.0 (Phase 2 Executable Architecture)  
> **Status**: Canonical Event Registry

This document lists every event type, payload structure, priority, producer, consumers, and lifecycle.

---

| Event Name | Producer | Consumers | Priority | Description |
|---|---|---|---|---|
| `ObservationReceived` | Perception | Memory, WorldModel | Normal | Raw sensor evidence received |
| `AttentionAllocated` | Executive | Memory, Reasoner | High | Cognitive resource budget allocated |
| `MemoryRetrieved` | Memory | Reasoner, Planner | Normal | Ranked items retrieved from memory |
| `MemoryStored` | Memory | StateManager | Low | New item committed to memory |
| `BeliefCreated` | Reasoner | WorldModel | High | New belief established |
| `BeliefUpdated` | WorldModel | Planner, Reasoner | High | Belief confidence or state revised |
| `BeliefRejected` | WorldModel | Memory | High | Belief contradicted by evidence |
| `GoalCreated` | Executive | Planner | High | New cognitive goal initialized |
| `GoalUpdated` | Executive | Planner | Normal | Goal priority or progress changed |
| `GoalCompleted` | Executive | Reflection | High | Goal successfully achieved |
| `PlanCreated` | Planner | Simulator | High | Plan generated for active goal |
| `PlanUpdated` | Planner | Executive | Normal | Plan steps or risk revised |
| `SimulationStarted` | Simulator | StateManager | Normal | Counterfactual sandbox running |
| `SimulationCompleted` | Simulator | Executive, Safety | High | Sandbox evidence generated |
| `DecisionGenerated` | Executive | Safety | Critical | Action option selected |
| `DecisionApproved` | Safety | Executive | Critical | Action passed safety evaluation |
| `ActionStarted` | Executive | StateManager | High | Action execution commenced |
| `ActionCompleted` | Executive | Reflection | High | Action finished execution |
| `ReflectionCompleted` | Reflection | Learner | High | Cognitive cycle insights extracted |
| `LearningAccepted` | Learner | Policy, Memory | High | Verified improvement accepted |
| `LearningRejected` | Learner | StateManager | Normal | Unverified learning rejected |
| `PolicyUpdated` | Learner | Executive, Safety | High | System behavioral rule updated |
| `HealthChanged` | HealthMonitor | Executive, Kernel | Critical | System health status updated |
| `CheckpointCreated` | StateManager | Kernel | Normal | Transactional checkpoint saved |
