# Live Model Benchmark

## 1. Six-Way Ablation + MODEL_ONLY Baseline
We run seven configurations on identical tasks:
1. **MODEL_ONLY**: Raw LLM with tools, but no persistent `WorldModel`, `Memory`, or structured `Planner` orchestration.
2. **A - Stateless**: Reactive E.L.I.Z.A. core without persistent memory or planning.
3. **B - World Model Only**: Reactive, with current state tracking.
4. **C - Memory Only**: Reactive, with historical episodic memory.
5. **D - Cognitive Core**: Reactive, with both World Model and Memory.
6. **E - Planning**: Planned architecture, with initial planning (no closed-loop recovery).
7. **F - Full v0.6**: Full architecture with Closed-Loop Monitoring and Replanning.

## 2. Live Provider Configuration
Set via environment variables:
- `ELIZA_MODEL_PROVIDER=cloud`
- `OPENAI_API_KEY=sk-...`

If no key is present, the test runner gracefully outputs `LIVE_MODEL = NOT_RUN`.

## 3. Metric Tracking
The test runner records granular metrics across tasks:
- `goal_completion`
- `tool` choice success
- `replan_count`
- Detailed `traces` of every cycle's state and decision.
