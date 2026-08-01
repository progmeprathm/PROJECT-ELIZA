# ELIZA State Machine Specification

> **Version**: 1.0.0 (Phase 2 Executable Architecture)  
> **Status**: Canonical State Machine Transition Reference

```
  +--------+
  |  IDLE  |
  +---+----+
      | (Observation Received)
      v
+-----+------+
| PERCEIVING |
+-----+------+
      | (Attention Allocated)
      v
+-----+------+
| REASONING  |
+-----+------+
      | (Goal Created)
      v
+-----+------+
|  PLANNING  |
+-----+------+
      | (Plan Generated)
      v
+-----+------+
| SIMULATING |
+-----+------+
      | (Safety Approved)
      v
+-----+------+
| EXECUTING  |
+-----+------+
      | (Action Completed)
      v
+-----+------+
| LEARNING   |
+-----+------+
      | (Consolidation Done)
      v
  +--------+
  |  IDLE  |
  +--------+
```

---

## State Transition Rules

1. **`IDLE -> PERCEIVING`**: Triggered by `ObservationReceived`.
2. **`PERCEIVING -> REASONING`**: Triggered by `AttentionAllocated`.
3. **`REASONING -> PLANNING`**: Triggered by `GoalCreated`.
4. **`PLANNING -> SIMULATING`**: Triggered by `PlanCreated`.
5. **`SIMULATING -> EXECUTING`**: Triggered by `DecisionApproved`.
6. **`EXECUTING -> LEARNING`**: Triggered by `ActionCompleted`.
7. **`LEARNING -> IDLE`**: Triggered by `MemoryConsolidated`.
