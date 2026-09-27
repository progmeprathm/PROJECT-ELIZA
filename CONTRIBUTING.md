# Contributing to E.L.I.Z.A.

First off, thank you for considering contributing to E.L.I.Z.A.! It's people like you that make E.L.I.Z.A. such a powerful cognitive operating system.

## 🧠 Core Philosophy
The E.L.I.Z.A. Kernel does not think. It makes thinking possible.
When contributing to the core `ecos` package, strictly adhere to the constraints defined in `ELIZA_KERNEL_SPEC.md`.

## 🌳 Branching Strategy
This repository relies heavily on git branches to isolate product variants while keeping the local development environment side-by-side. 
- `main` branch contains the core ECOS Kernel and CLI.
- `variant/studio` branch contains the Observability dashboard.
- `variant/desktop` branch contains the consumer-facing companion app.
- `variant/multi-tenant` branch contains the cloud-ready server.

If you are modifying the kernel, open your PR against `main`. 
If you are modifying a specific UI variant, open your PR against the respective `variant/*` branch.

## 🚀 How to Submit a Pull Request
1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes (`python run_tests.py`).
4. Ensure your code follows PEP 8 standards.
5. Issue that pull request!
