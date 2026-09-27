# Semantic Memory

## 1. Overview
In E.L.I.Z.A. v0.4, episodic memory retrieval relies on embedding semantic text into high-dimensional vectors. The core premise is that the agent should be able to recall relevant past experiences even if its current internal query uses entirely different terminology from the original observation.

## 2. Embedding Providers
The system abstracts vectorization via the `EmbeddingProvider` interface.

### RealEmbeddingProvider
- Utilizes OpenAI's `/v1/embeddings` API.
- Default model: `text-embedding-3-small`.
- Generates 1536-dimensional vectors capable of deep semantic matching (e.g., mapping "credential" close to "access code").
- **Usage:** Intended for live cognition runs where robust natural language generalization is required.

### DeterministicPseudoEmbedding
- Calculates character frequency mapped into a 128-dimensional vector.
- **Usage:** Serves exclusively as the offline deterministic fallback for CI/CD and regression testing. It does not possess true semantic understanding but provides structurally identical cosine similarity operations.

## 3. Performance on Paraphrasing
A controlled `run_v04_semantic_test.py` validates the difference between the providers. When querying for the password using terms like "passcode" or "security code":
- The `RealEmbeddingProvider` successfully maps these to the stored episode about the "access code".
- The `DeterministicPseudoEmbedding` predictably fails because it lacks language topology.

## 4. Integration with Memory System
Upon storing an episode, the `ECOSMemorySystem` extracts the `observation` string and embeds it. During retrieval, the `CognitiveShell`'s goal is embedded and compared against all stored episodes using Cosine Similarity. Episodes scoring above the threshold (0.05) are injected into the reasoning prompt as `[MEMORY] RETRIEVED EXPERIENCES`.
