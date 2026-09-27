# E.L.I.Z.A. Studio (Engineering Control Deck)

This is the **Cognitive Engineering / Observability** branch of the E.L.I.Z.A. operating system. 

It is designed for AI developers, researchers, and system operators who need to observe, debug, and safely guide the multi-agent cognitive architecture. It operates entirely on the principle of the "Glass Box", exposing the underlying mechanics of memory, coordination, routing, and tool usage.

## Features
- **Mission Control Dashboard:** A high-density, dark-mode terminal view providing real-time runtime tracking.
- **Cognition Inspector:** Tools to actively inspect the World Model and Episodic Memory structures.
- **Runtime Telemetry:** Exposes the `ModelRouter` failovers, API latencies, and agent delegations.
- **Hot-swappable Configuration:** Set API keys and execution engines directly from the bottom-left settings pane without touching the `.env` file.

## How to Run

1. Open a terminal in this directory (`Eliza-Studio`).
2. Run the studio server:
```bash
python run_eliza_studio.py
```
3. Open your browser and navigate to `http://127.0.0.1:8000`
4. The dashboard will initialize. Use the Settings gear in the bottom left navigation menu to apply your API keys or enable local execution.
