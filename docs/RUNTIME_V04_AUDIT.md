# E.L.I.Z.A. Runtime v0.4 Audit

## 1. Current Provider Architecture
- `ModelRouter` correctly delegates generation to either `MockAdapter` or `CloudAPIAdapter` based on the `ELIZA_MODEL_PROVIDER` environment variable.
- Fallback logic exists when the primary provider fails.

## 2. Embedding Abstraction
- The `EmbeddingProvider` interface is defined in `ecos/memory/system.py`.
- Currently, only `DeterministicPseudoEmbedding` is implemented, which calculates character frequency vectors (128-d).
- A `RealEmbeddingProvider` (e.g., OpenAI embeddings) must be added here and conditionally instantiated based on `ELIZA_EMBEDDING_PROVIDER`.

## 3. Current Memory Pipeline
- `ECOSMemorySystem` stores episodes and computes vectors upon `store()`.
- Retrieval uses cosine similarity with a threshold > 0.05.
- Currently, string matching in `DeterministicPseudoEmbedding` relies on overlapping characters. It will not handle semantic paraphrasing (e.g., "password" vs "credential") well, necessitating a true embedding model for v0.4.

## 4. Current Environment Interface
- `SimpleEnvironment` is a 1D grid with deterministic states and fixed language observations.
- It returns states like `{"agent_location": 3, "door_locked": True, "message": "Door is locked..."}`.
- For v0.4, we need a `Grid2DEnvironment` implementing similar interfaces but with 2D coordinates (x, y), obstacles, and natural language variations for observations.

## 5. Changes Required for v0.4
- Create `ecos/simulation/grid2d.py` for the 2D environment.
- Add `RealEmbeddingProvider` using `urllib` to hit OpenAI's embedding endpoint (`/v1/embeddings`), with automatic fallback.
- Update `ModelRouter` or `CloudAPIAdapter` if needed for better structured output fallback.
- Create `run_v04_benchmark.py` with CLI args `--mode mock|live` and trial looping.
- Add retrieval tests for semantic paraphrasing.
