# E.L.I.Z.A. Runtime v0.3 Architecture

## 1. Semantic Separation
The primary architectural shift in v0.3 is the strict semantic separation between the **World Model** and the **Memory System**. 

- The `ECOSWorldModel` has been refactored to drop ephemeral string observations. It only updates its `_state` dictionary based on the ground truth provided by the environment, acting purely as a snapshot of the current world.
- The `ECOSMemorySystem` handles chronological event logs via the `store()` method, creating an `episode` object at the end of each cognitive cycle.

## 2. Embedding Abstraction
The memory retrieval system has abstracted its embedding mechanism into an `EmbeddingProvider` interface. 
- For offline determinism and reproducible benchmarks, it uses `DeterministicPseudoEmbedding` (a 128-dimensional character frequency hash).
- This pattern allows a seamless drop-in of a `RealEmbeddingProvider` (e.g., OpenAI `text-embedding-3-small`) in future milestones without altering the cognitive shell or retrieval logic.

## 3. Information Provenance in the Shell
The `CognitiveShell` enforces strict provenance tags in the prompt sent to the LLM:
```text
GOAL: <intent>
[WORLD_MODEL] CURRENT STATE: <dict>
[WORLD_MODEL] CURRENT BELIEFS: <list>
[OBSERVATION] CURRENT MESSAGE: <string>
[MEMORY] RETRIEVED EXPERIENCES: <list>
```
This guarantees zero information leakage between historical memory and current world state, enabling controlled experiments like the v0.3 Four-Way Benchmark.
