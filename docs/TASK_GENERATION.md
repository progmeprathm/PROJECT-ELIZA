# Task Generation

## 1. The TaskGenerator
We built `ecos/simulation/task_generator.py` to procedurally generate evaluation instances across five core cognitive families:

- **Family A: Information Retrieval** (Discover a code early, travel multiple rooms, use code).
- **Family B: Arithmetic Tool Use** (Discover values A and B, compute A*B, use result).
- **Family C: Navigation** (Traverse sequential environments).
- **Family D: Dependency Planning** (Unlock checkpoint 1 to get the code for checkpoint 2).
- **Family E: Recovery / Environmental Change** (An environmental variable changes dynamically while the agent is executing, forcing a replan).

## 2. Seed-Based Randomization
Tasks rely on parameterized seeds. Values, codes, multipliers, and room arrangements are randomized, forcing the LLM to process the specific observation rather than a hard-coded solution.

## 3. Unified TaskEnvironment
The `TaskEnvironment` parses the generated `Task` objects, handles dynamic events (e.g., changing items mid-run for Family E), and tracks flags (unlocked doors) to output consistent text observations.
