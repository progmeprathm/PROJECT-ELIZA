# ELIZA Human Interface Guidelines (HIG)

## 1. Core Philosophy
The ELIZA UI/UX must communicate clarity and cognition, not "AI magic." It is a tool for professional thought, research, and engineering. Users do not come to ELIZA simply for answers; they come to make measurable progress toward meaningful goals.

### 1.1 Goal-Centric, Not Chat-Centric
The fundamental interaction paradigm is the **Golden Loop**:
`Goal -> Understand -> Plan -> Execute -> Evaluate -> Learn -> Repeat`

The conversational interface (chat) is merely an access point to guide the work happening in the persistent workspace.

### 1.2 Progressive Disclosure
Hide complexity until it is needed. New users should see a simple conversational interface (Companion), while power users can expose dockable panels and detailed cognitive state tracking (Studio).

### 1.3 Transparency and Reversibility
- Every automated change must be visible.
- Every decision must link back to evidence (via the Reasoning Inspector).
- Every action should be reversible where practical.
- Long-running processes must always show progress and allow pausing or cancellation.

## 2. Product Ecosystem
- **ELIZA Companion**: A conversational interface for daily interaction (Desktop / Web / Mobile). Focuses on quick onboarding, chat, and light goal execution.
- **ELIZA Studio**: A visual cognitive workspace for professionals (creators, researchers, engineers). Features dockable windows, split views, and full access to the cognitive kernel.
- **ELIZA Developer SDK**: APIs and plugins for extending the ECOS kernel.

## 3. Platform Experience Guidelines

### Desktop UX (Primary Workspace)
- Resizable and dockable panels.
- Keyboard-first workflow (Command palette, robust shortcuts).
- Multiple workspaces.
- Integrated terminal and live event stream.

### Mobile UX (On-the-Go)
- Notifications for long-running task completions.
- Voice interaction for quick updates.
- Goal review and rapid approvals.
- Memory search and status monitoring.
- *Avoid attempting full-scale development on mobile.*

### Web UX (Collaboration)
- Real-time multiplayer synchronization.
- Shared projects and team goals.
- Shared Knowledge graphs.
- Live comments and annotations.
