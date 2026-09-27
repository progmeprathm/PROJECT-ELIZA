# E.L.I.Z.A. Memory Architecture v0.2

## 1. Storage Abstraction
The Memory System implements the `MemoryModule` interface, abstracting away the underlying storage medium. Memories are stored as `Memory` objects containing a payload (the actual data), importance scores, provenance metadata, and access timestamps.

## 2. Embedding Strategy
For the v0.2 milestone, we have transitioned from a basic substring matcher to a vector-based semantic retrieval system. To keep the core infrastructure lightweight and avoid heavyweight external dependencies (like ChromaDB or SentenceTransformers) at this stage, we implemented a robust but simple local hashing/embedding fallback based on character frequency and ASCII mapping (normalized to a 128-dimensional vector). This provides the structural foundation for semantic retrieval while remaining 100% deterministic and offline-capable.

## 3. Retrieval Strategy
Retrieval relies on cosine similarity between the embedded query and the embedded memory payloads.
1. The query text is embedded into a vector.
2. The system calculates the dot product (cosine similarity) against all stored memories.
3. Memories are sorted by similarity score (descending).
4. Top-K memories that exceed a minimum similarity threshold (0.05) are returned.
5. `last_accessed` timestamps are updated for retrieved memories, enabling future consolidation strategies.

## 4. Episodic vs Semantic Distinction
- **Episodic Memory**: At the end of every Cognitive Cycle, an "episode" dictionary is stored. It contains the cycle goal, the observation, the action taken, the reasoning summary, and the state of the world before the action. This serves as an episodic log of sequential experience.
- **Semantic Memory**: The system currently treats all stored elements as semantic context during retrieval. Future iterations (v0.3+) will segregate dense vector databases to abstract conceptual meaning (semantic) vs chronological events (episodic).

## 5. Offline Capabilities
The current fallback vector implementation allows tests and CI/CD pipelines to run semantic similarity tests without requiring network access to cloud embedding models (e.g., `text-embedding-3-small`). This guarantees deterministic experiment reproducibility.
