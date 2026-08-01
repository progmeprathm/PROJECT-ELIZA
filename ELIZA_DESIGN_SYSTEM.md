# ELIZA Design System

## 1. Visual Identity
The visual style is minimalist and information-dense without clutter. It uses card-based layouts, dockable panels, split views, and supports a keyboard-first workflow.

## 2. Color Semantics
Colors in ELIZA carry specific semantic meaning regarding cognitive processes. Do not use these colors purely for aesthetics; they must represent their assigned cognitive function.

- **Blue (`--md-sys-color-primary`)**: Reasoning, logical deduction, and chat interaction.
- **Green (`--ecos-success`)**: Memory, context retrieval, and successful states.
- **Purple (`--md-sys-color-tertiary`)**: Planning, goal decomposition, and milestones.
- **Orange (`--ecos-warning`)**: Simulation, speculative execution, sandboxed outputs, and warnings.
- **Red (`--md-sys-color-error`)**: Errors, conflicts, contradictions, or safety vetos.
- **Gray (`--md-sys-color-secondary`)**: Archived data, inactive tasks, disabled UI states, secondary text.

## 3. Typography
- **Primary UI (Sans-Serif)**: `Inter`. Used for all conversational text, labels, headers, and standard UI elements.
- **Code & Data (Monospace)**: `JetBrains Mono`. Used for reasoning traces, terminal output, logs, metrics, and JSON payloads.

## 4. Components

### 4.1 Layout Components
- **Split Views**: A standard `grid-cols-[1fr_400px]` or adjustable flex-pane for side-by-side editing and chatting.
- **Dockable Panels**: Modular cards that can be collapsed or expanded (e.g., the Developer/Brain Drawer).

### 4.2 Interactive Elements
- **Filled Buttons**: Used for primary actions (e.g., "Create Goal", "Approve Plan").
- **Outlined Buttons**: Used for secondary actions (e.g., "Cancel", "How I got this answer").
- **Status Bar**: A VS Code-style footer fixed to the bottom of ELIZA Studio, displaying GPU, Memory, Scheduler state, Running Tasks, Latency, and Notifications.

## 5. Motion and Animation
- Transitions should be fast and deliberate (150ms-300ms).
- Use `ease-out` for incoming elements (like opening a drawer).
- Avoid bouncy or "playful" animations; stick to crisp sliding and fading to maintain a professional workspace feel.
