# Persistent Cognitive State

## 1. Restart Survival
The `ELIZARuntime` provides `snapshot()` and `restore()` methods to persist its state across process crashes or system reboots. The state separates short-term working context from long-term memory constraints.

## 2. Evidence Precedence
If an agent relies on an active historical rule (`Consolidated Knowledge`), but execution encounters a `VerificationSystem` mismatch against the current `World Model`, the runtime explicitly flags the rule as `CONFLICTED`. The canonical precedence ensures: `CURRENT_OBSERVATION > VERIFIED_CURRENT_STATE > ACTIVE_KNOWLEDGE > EPISODIC_MEMORY`. 

## 3. Governance Lifecycle
Stored rules are managed dynamically (e.g. `CANDIDATE -> ACTIVE -> CONFLICTED -> INVALIDATED -> ARCHIVED`), ensuring E.L.I.Z.A. adapts to environment drift in long-horizon sequences.
