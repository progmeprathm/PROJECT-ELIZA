# Cognitive Information Flow

## 1. Abstract Flow
```text
Environment
    ↓ (Observation)
World Model ─────────┐ (Current State & Beliefs)
                     │
Memory ──────────────┤ (Retrieved Historical Episodes)
                     ↓
                  Cognition (CognitiveShell + ModelRouter)
                     ↓ (Action String)
                   Action
    ↓
Environment (State transition)
```

## 2. Definitions & Boundaries

### Environment
The external source of ground truth. It owns the absolute state of the universe, enforces physical laws (e.g., doors being locked), and emits Observations to the agent.

### World Model
The agent's internal representation of the **CURRENT STATE** of the environment.
- **Allowed:** Tracking `agent_location: 3`, `door_locked: true`. General factual beliefs or rules discovered.
- **Forbidden:** Storing a chronological log of what the agent saw or did. Observations that are no longer true or no longer observable must not persist here unless abstracted into a permanent world fact.

### Memory
The agent's representation of **PAST EXPERIENCES**.
- **Allowed:** Storing Episodic Memory (what happened, when, why, and the exact observation at the time).
- **Forbidden:** Acting as the primary source of truth for the *current* state of the room.

### Cognition (LLM / ModelRouter)
The reasoning engine. It does not store state. It receives a prompt clearly tagged with Information Provenance:
- `[WORLD_MODEL] CURRENT STATE:`
- `[OBSERVATION] CURRENT MESSAGE:`
- `[MEMORY] RETRIEVED EXPERIENCES:`
It synthesizes this separated data to emit a structured Action.

## 3. Strict Provenance
By explicitly tagging information sources in the prompt, the system guarantees that the reasoning engine knows *where* it learned something (e.g., knowing the door is currently locked via Observation vs remembering the password was 8592 via Memory).
