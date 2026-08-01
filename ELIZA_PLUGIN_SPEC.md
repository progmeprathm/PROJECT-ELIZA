# ELIZA Plugin Specification

> **Version**: 1.0.0 (Phase 2 Executable Architecture)  
> **Status**: Canonical Plugin Guide

This document defines how third-party developers extend ELIZA by building modular plugins for Memory, Reasoning, Planning, Simulation, and Learning.

---

## 1. Plugin Base Architecture
All plugins extend `BasePlugin` and implement subsystem-specific interfaces:
- `PlannerPlugin`: Implements `PlannerAPI`
- `MemoryPlugin`: Implements `MemoryAPI`
- `ReasonerPlugin`: Implements `ReasonerAPI`
- `SimulatorPlugin`: Implements `SimulatorAPI`

## 2. Plugin Contract Requirements
1. Must declare `ModuleManifest` (ID, Version, Capabilities, Dependencies).
2. Must communicate strictly via `EventBus` / `CCPMessage` or Cognitive ISA Instruction emission. Zero direct coupling.
3. Must expose `health()` check endpoint returning status (`Healthy`, `Warning`, `Critical`, `Offline`).
4. Must handle `initialize()`, `start()`, `pause()`, `resume()`, `stop()`, and `shutdown()` hooks.
