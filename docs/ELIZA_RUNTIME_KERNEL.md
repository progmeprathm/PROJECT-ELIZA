# ELIZA Runtime Kernel

The kernel (`ecos/kernel/`) establishes the foundational OS for E.L.I.Z.A.'s cognition.

## 1. Components
- **`runtime.py`**: The `ELIZARuntime` class implementing `IRuntime`.
- **`policy.py`**: The `MetaRuntimePolicy` that yields `RuntimePolicyAction` based on state logic and constraints.
- **`state.py`**: A unified dictionary-backed representation of current working variables, distinct from permanent storage.
- **`events.py`**: The `RuntimeEvent` schema strictly typing output operations for tracing.
- **`snapshot.py`**: Save and load functionality mapping the runtime object directly to disk storage for restart survival.

## 2. API Contract
A developer interacts with E.L.I.Z.A. via:
```python
runtime = ELIZARuntime(config)
runtime.run("goal")
```
No hidden scripts or benchmark logic bypass the kernel.
