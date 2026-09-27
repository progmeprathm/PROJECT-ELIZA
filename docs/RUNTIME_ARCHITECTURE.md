# E.L.I.Z.A. Runtime Architecture v0.1

## 1. Runtime Architecture
The E.L.I.Z.A. runtime operates on the ECOS (Evolutionary Learning Intelligence & Zero-shot Architecture) kernel. 
It establishes a closed-loop cognitive cycle that integrates perception, memory, world-modeling, and reasoning to determine actions within a defined environment.

## 2. Cognitive Cycle
The runtime executes a continuous or stepped loop (orchestrated by the `CognitiveShell`):
1. **Perception**: An observation from the environment is ingested.
2. **WorldModel Update**: The observed state updates the `ECOSWorldModel`, forming new factual beliefs.
3. **Memory Retrieval**: The `ECOSMemorySystem` retrieves relevant past experiences based on the current goal and state.
4. **Reasoning**: The `ModelRouter` formats the state, memories, beliefs, and goal into a prompt for the execution engine (LLM).
5. **Action**: The LLM outputs structured reasoning and a specific action to take.
6. **Execution**: The chosen action is sent to the Environment.
7. **Consolidation**: The action and its rationale are stored back into the `ECOSMemorySystem` for future cycles.

## 3. Component Interactions
- **CognitiveShell ↔ Environment**: The shell polls observations and dispatches actions.
- **CognitiveShell ↔ WorldModel**: Ingests observations and extracts current state/beliefs.
- **CognitiveShell ↔ MemorySystem**: Retrieves relevant memory and stores post-decision rationales.
- **CognitiveShell ↔ ModelRouter**: Dispatches the assembled cognitive context for LLM generation.

## 4. Data Flow
`Observation -> ECOSWorldModel -> State & Beliefs`
`Goal + State -> ECOSMemorySystem -> Relevant Memories`
`(Goal + State + Beliefs + Memories) -> ModelRouter -> Reasoning & Action`
`Action -> Environment -> New Observation`

## 5. Model Provider Interface
The `ModelRouter` manages execution via the abstract `LanguageModel` interface. 
Models (such as DeepSeek, Qwen, Llama, Mistral) are abstracted behind adapter classes (e.g., `CloudAPIAdapter`, `OllamaAdapter`). 
The router uses `TaskIntent` to dynamically route the cognitive load to the most suitable provider, maintaining a model-agnostic architecture. For testing, it implements deterministic fallbacks when live providers are unavailable or schema validation fails.

## 6. Memory Integration
The `ECOSMemorySystem` (implementing `MemoryModule`) acts as the episodic and semantic store. 
During the loop, it provides context by matching the current situation against past cycles. New experiences are inserted at the end of each cycle.

## 7. World-Model Integration
The `ECOSWorldModel` tracks the deterministic properties of the current environment state (e.g., location, inventory). 
It differentiates between absolute observations (state) and assertions (`Belief` objects) that provide confidence-weighted interpretations of the world.

## 8. Environment Interface
The `SimpleEnvironment` (GridWorld) represents the external world. It exposes two core methods:
- `reset()`: Re-initializes state and returns the first observation.
- `step(action, action_target)`: Executes an action and returns the resulting observation.

## 9. Experiment Methodology
The primary validation is the **Goal Achievement Experiment** (`run_rrs_simulation.py`). 
An agent is placed in an environment with missing capabilities (a locked door) and must utilize the cognitive loop to perceive its state, navigate, acquire items (key), and unlock pathways to reach its goal autonomously.

## 10. Known Limitations
- The current implementation relies on deterministic LLM fallbacks when no API key is provided, mimicking ideal reasoning rather than true LLM inference.
- Memory retrieval is simple string-matching rather than dense vector embeddings.
- The environment is a hardcoded 1D grid.

## 11. Next Recommended Milestone
**Phase 0.2: Live Provider & Vector Memory**
- Connect `CloudAPIAdapter` to a live OpenAI-compatible endpoint.
- Upgrade `ECOSMemorySystem` to use a lightweight vector store (e.g., ChromaDB or simple cosine similarity over local embeddings).
- Expand the `SimpleEnvironment` into a 2D or interactive text-based grid with probabilistic outcomes.
