# E.L.I.Z.A. Runtime v0.3 Controlled Cognition Benchmark

## 1. Goal
The primary objective of v0.3 is to establish a rigorous cognitive architecture by isolating the functional contributions of the World Model (current state), Memory (historical experiences), and the LLM (reasoning). This ensures that success on memory-dependent tasks is driven by episodic memory retrieval, rather than the World Model acting as a chronological log.

## 2. Methodology
The experiment runs a 1D GridWorld puzzle:
- Location 0: Start
- Location 1: Contains a note with password `8592`.
- Location 3: Locked door requiring `unlock_door_8592`.
- Location 4: Target.
The task requires perceiving the password early, moving away (losing direct observation of the note), and retrieving the password from memory later to unlock the door.

Four configurations are tested against identical conditions:
- **Config A (Stateless)**: No memory, no world model.
- **Config B (World Model Only)**: Maintains current beliefs and state, no historical memory.
- **Config C (Memory Only)**: Maintains chronological experience, no persistent state.
- **Config D (E.L.I.Z.A.)**: Full cognitive architecture (Memory + World Model).

## 3. Results (Mock Provider)
- **Config A (Stateless)**: FAILED. Loops blindly against the locked door.
- **Config B (World Model Only)**: FAILED. Reads the note, but since the `ECOSWorldModel` was refactored to drop ephemeral observations and only store current state, it forgets the password by the time it reaches the door.
- **Config C (Memory Only)**: FAILED. Lacking a persistent World Model to track whether it had already read the note or to synthesize its location context cleanly, it failed to trigger the reading action and moved past the note.
- **Config D (E.L.I.Z.A.)**: SUCCEEDED. The agent used the World Model to understand it was at the note, read it, and later used Semantic Memory Retrieval to pull the password episode into context when facing the locked door.

## 4. Information Provenance and Leakage Test
- Verified that `ECOSWorldModel` no longer appends chronological observations (`obs['message']`) into its belief graph.
- Verified that the `CognitiveShell` explicitly tags sources in the LLM prompt (e.g., `[WORLD_MODEL] CURRENT STATE: ...`, `[MEMORY] RETRIEVED EXPERIENCES: ...`).
- Confirmed that without `use_memory=True`, the LLM has absolutely no access to the `8592` string when at Location 3. Information leakage is zero.

## 5. Conclusion
The v0.3 benchmark empirically demonstrates that:
`World Model ≠ Memory`
The World Model alone cannot solve the task. Memory alone cannot solve the task. The E.L.I.Z.A. combined architecture successfully solves it via controlled information flow.
