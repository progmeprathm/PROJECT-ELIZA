# E.L.I.Z.A. Runtime v0.3 Audit

## 1. What constitutes current world state
Currently, `ECOSWorldModel` maintains `_state` containing values like `agent_location` and `door_locked`. This genuinely represents the current deterministic state of the environment.

## 2. What currently persists historically
In `ecos/world/graph.py`, the `process_observation` method extracts `obs["message"]` and creates a `Belief` object which is appended to `self._beliefs`. This list of beliefs grows unbounded over time, effectively storing a chronological history of all environmental messages, including ephemeral ones (like reading a note).

## 3. What the LLM receives from World Model
The LLM receives:
- `world_state`: The current deterministic snapshot of the environment.
- `beliefs`: The 5 most recent `Belief` statements (which are just the last 5 observation messages).

## 4. What the LLM receives from Memory
The LLM receives:
- `retrieved_mems`: The top 3 episodic memories retrieved via cosine similarity using the character-frequency pseudo-embedding.

## 5. Where information duplication occurs
When an event happens (e.g., Agent reads the note):
1. The message ("The password for the door is 8592") becomes a Belief in the World Model.
2. The entire cognitive cycle (including that same message) is saved as an episodic Memory.
This means the World Model acts as a short-term memory buffer, breaking the separation of concerns. This is why Configuration B (World Model Only) succeeded in v0.2.
