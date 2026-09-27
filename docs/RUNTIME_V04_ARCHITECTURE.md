# E.L.I.Z.A. Runtime v0.4 Architecture

## 1. Provider and Embedding Abstraction
v0.4 extends the abstraction layers to support real external LLMs and real embedding models simultaneously.
- **ModelRouter**: Continues to route reasoning tasks. Can be toggled to `MockAdapter` or `CloudAPIAdapter` via `ELIZA_MODEL_PROVIDER`.
- **EmbeddingProvider**: The `ECOSMemorySystem` now takes an explicit `EmbeddingProvider`. Controlled by `ELIZA_EMBEDDING_PROVIDER`.

## 2. Robust Fallback Mechanism
To ensure E.L.I.Z.A. remains fully testable without API credentials, `RealEmbeddingProvider` implements a strict fallback safety net. If initialized without credentials (or if the API errors), it explicitly records `fallback_used=True` and defaults to the local `DeterministicPseudoEmbedding` (a 128-dimensional character hashing fallback). This ensures continuous integration without fabricating successful API calls.

## 3. 2D Environment Architecture
The cognitive loop has been updated to integrate with `Grid2DEnvironment`.
- State Representation: `agent_location` is now a tuple `(x, y)`.
- Navigational Actions: `move_north`, `move_south`, `move_east`, `move_west`.
- Spatial Awareness: The MockAdapter pathing was updated to deterministically solve the 2D grid logic during offline benchmarks.

## 4. Linguistic Variation
To stress-test Semantic Memory Retrieval, the 2D Environment implements natural language variation in its observations. When the agent reads the note, the environment randomly returns one of several paraphrased observations (e.g. "The paper beside you says the entry number is 8592" vs "Written on the card is the credential: 8592"). This forces the memory retrieval system to rely on semantic vectors rather than exact string matches.

## 5. Trace Provenance
The `CognitiveShell` now explicitly captures `traces` during benchmarks, tracking exactly what was retrieved, the World Model state, the LLM used, and the generated decision. This runtime trace provides auditable proof of information provenance.
