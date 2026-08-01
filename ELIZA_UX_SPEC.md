# ELIZA UX Specification

## 1. Overall Navigation
The ELIZA UI features a comprehensive sidebar navigation mapping to core OS modules:
- Home
- Workspace
- Chat
- Goals
- Memory
- World Model
- Planner
- Simulation
- Projects
- Knowledge
- Skills
- Agents
- Marketplace
- Benchmarks
- Settings

## 2. Core Functional Views

### 2.1 Home Screen
Answers three questions: What am I doing? What changed? What should I do next?
- No empty chat screens.
- **Today's Focus**: Highest priority goal and progress %.
- **Running Processes**: Active OS daemon tasks.
- **Upcoming Tasks**: The next steps in the current plan.
- **Recent Activity**: Newly acquired knowledge, completed benchmarks.

### 2.2 Goals & Projects
- **Goals**: Structured as `Goal -> Milestones -> Tasks -> Subtasks -> Progress -> Completion`. Every goal includes Description, Deadline, Priority, Dependencies, Resources, Confidence, Status, and History.
- **Projects**: The top-level container (similar to GitHub Projects). Structure: `Project -> Goals -> Knowledge -> Documents -> Code -> Experiments -> Benchmarks`.

### 2.3 Memory & World Model
- **Memory**: Divided into Working, Semantic, Episodic, Long-Term, and Archived. Shows clear trace: `Transformer -> Beliefs -> Experiences -> Plans -> Research Notes`.
- **World Model**: An interactive graph showing Nodes, Relationships, Evidence, Confidence, Contradictions, and Sources.

### 2.4 Planner & Simulator
- **Planner**: Displays multiple alternative plans side-by-side with Estimated Cost, Risk, Time, and Recommendation.
- **Simulator**: Allows running speculative scenarios (`Current Plan -> Simulation -> Outcome -> Confidence -> Recommendation`) before committing changes to reality.

### 2.5 Reasoning Inspector
Every step of the cognitive process is visible:
`Question -> Evidence -> Retrieved Memory -> Reasoning -> Alternative -> Decision -> Confidence`.

### 2.6 Federation Modules
- **Knowledge**: A searchable, versioned structured wiki (Entities, Policies, Architecture).
- **Skills**: Versioned executable behaviors (Coding, Planning, Teaching) with performance metrics.
- **Agents**: Specialized sub-personas (Architect, Researcher) with specific Capabilities, Memory, and Goals.
- **Benchmarks**: Historical tracking graphs (Memory 92%, Planning 84%, etc.).
- **Marketplace**: Plugin ecosystem for expanding capabilities (Memory++, Vision).

## 3. User Journeys

### Journey 1: New User
`Welcome -> Choose Purpose -> Create Workspace -> Create First Goal -> Chat Begins -> ELIZA Creates Plan -> User Reviews -> Execute -> Reflection`

### Journey 2: Research
`Research Question -> Literature Search -> Knowledge Graph -> Hypothesis -> Simulation -> Experiment -> Results -> Publication Draft`

### Journey 3: Software Development
`Idea -> Architecture -> Repository -> Implementation -> Tests -> Benchmarks -> Deployment`

### Journey 4: Startup Founder
`Vision -> Market Research -> Competitors -> Product -> Roadmap -> Execution -> Launch`

### Journey 5: Student
`Topic -> Learning Plan -> Lessons -> Practice -> Assessment -> Reflection`

### Journey 6: Daily Use (The Golden Loop)
`Morning Open ELIZA -> Dashboard -> Continue Yesterday's Goal -> Planner Suggests Tasks -> Work -> Reflection -> Close`
