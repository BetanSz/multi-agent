# Sprint 1 — How to Start Things

**Goal:** Define the methodology for starting any sprint in this project.
**Date:** 2026-05-19

This file is the output of running `brainstorming` + `process-interviewer` on the question:
*"How should every sprint begin in the multi-agent system?"*

The conclusions here become the standard operating procedure — and eventually the input format that the multi-agent system consumes automatically.

---

## Prise de décision — Architecture & Constraints

### Environment
- All execution runs inside **VS Code** (Claude Code extension)
- Resources, infrastructure, and project outputs target **Azure** and the **Microsoft ecosystem** (Azure DevOps, Azure OpenAI, Entra ID, etc.)
- No Linux servers, no Docker orchestration — Windows + Azure is the baseline

### Orchestration model — chosen approach

Three approaches were evaluated:

| | Approach | Description |
|---|---|---|
| **A** | Skill-Composed Pipeline | Wire existing superpowers skills via a thin runner |
| **B** | File-Based DAG Orchestrator | Python script parses sprint file, builds task graph, runs true parallel OS processes |
| **C** | Claude-Orchestrates-Claude ✅ | One conductor Claude session spawns parallel subagents via `Agent()` tool — no new infrastructure |

**Decision: Start with Approach C.**

A Claude Code conversation IS the orchestrator. The conductor session reads the sprint file, identifies parallel task groups, dispatches subagents simultaneously, collects outputs, runs a review pass, and writes the synthesis. Zero infrastructure to build — validated within Sprint 1-3 before investing in a DAG runner.

Approach C was chosen because:
- No new code to build before the first sprint executes
- Native parallelism via multiple `Agent()` calls in one response
- The conversation context already holds the sprint plan, HITL approvals, and agent coordination
- Failure modes are visible in the same window the user monitors

**HITL handling:** Sprint file has a `hitl:` section listing pre-approved external actions. Conductor checks this list before delegating any task that touches Azure resources or external APIs — never prompts mid-sprint.

---

## Part 1 — Design (from `brainstorming`)

### Sprint model
- **Duration:** ~1 day of human work = ~1 hour of AI agent time
- **Origin:** User defines the sprint topic; LLM may propose the next sprint at the end of the current one
- **Execution:** Fully autonomous — no human intervention once sprint starts
- **Scheduling:** User launches before sleeping / going to the gym; agents run overnight or during breaks

### Sprint file format (`sprint_N_<topic>.md`)
Each sprint gets one file at repo root. Structure:
1. **Goal** — one-paragraph objective
2. **Tasks** — list with `depends_on:` fields to express the DAG
3. **HITL approvals** — pre-approved external actions (Azure resource creation, API calls, etc.)
4. **Prise de décision** — architectural or scope decisions made during sprint design
5. **Outputs** — written by agents after execution
6. **WISHLIST** — deferred ideas for future sprints

### Agent orchestration
- Conductor session reads sprint file
- Independent tasks → parallel `Agent()` calls
- Dependent tasks → sequential execution, gated on prior output
- Review pass before synthesis
- Final output written to `sprint_N_output.md` or appended to sprint file

### Skills in play
- `launch-sprint` → **main entry point**, orchestrates all steps below
- `brainstorming` → design phase, produces Part 1
- `process-interviewer` → extraction phase, produces Part 2
- `orchestrate` / `spawn-agent` / `synthesize` → execution phase (Bureau core skills)
- `dispatching-parallel-agents` → fan-out for parallel tasks

### Skill announcement convention
Every skill must begin its first response with:
> **Using skill \<name\>.**

This applies to all skills in `skills/` and `.agents/skills/`. The user must always know which skill is active.

---

## Part 2 — Process (from `process-interviewer`)

### Entry point

```
/launch_sprint "plain-text description of what this sprint builds"
```

Works identically in Claude Code (VS Code extension) and GitHub Copilot Chat. The argument is a free-text sprint description — no preparation required beforehand.

### Full pipeline

#### Step 1 — Brainstorm
- System explores 2-3 architectural approaches for the sprint
- User approves one direction before anything continues
- No implementation until design is signed off

#### Step 2 — Process interview
- Interviewer sharpens the approved design into a concrete plan
- Produces: task list with explicit `depends_on:` dependencies, chosen quality level, known external dependencies
- **Quality level chosen here (locked for the sprint):**
  - **L1** — feature built; LLM + human test after execution
  - **L2** — feature built + existing tests pass (no regression)
  - **L3** — new tests defined upfront (TDD-light) + all tests (new + existing) pass

#### Step 3 — HITL upfront review
- System analyzes the full plan and generates a HITL checklist
- Checklist contains every action requiring human credentials, Azure portal operations, external approvals, or non-reversible resource creation
- User executes each item on the checklist and confirms it works
- **Autonomous phase does not start until checklist is 100% confirmed**
- Big architectural choices that surface here → go back to Step 1/2; do not proceed with unresolved architecture

#### Step 4 — Autonomous execution (Approach C)
- Conductor session reads the sprint file
- Identifies parallel task groups (tasks with no shared dependency)
- Dispatches independent tasks as simultaneous `Agent()` calls
- Dependent tasks run sequentially, each gated on prior output
- Agents operate on the target project's codebase directly
- No human prompts during execution

#### Mid-sprint HITL pause (exception path)
- If agents encounter an unexpected blocker requiring human action (something genuinely missed from Step 3 — always a minor operational issue, never an architectural decision):
  1. Execution stops
  2. System surfaces the exact action required
  3. User performs it and confirms
  4. Execution resumes from where it stopped
- Architectural decisions surfacing mid-sprint = planning failure → stop sprint, restart from Step 1

#### Step 5 — Completion & reporting
- Agents verify output against the chosen quality level (L1/L2/L3)
- Sprint file updated with `## Outputs` section
- `sprint_log.md` written at repo root with:
  - Summary of what was built
  - Every minor architectural choice made autonomously by agents during execution
  - Any items deferred or blocked
- Optional: conductor proposes draft `sprint_N+1_*.md` for user review

### Sprint file structure (contract between projects)

Every sprint file follows this structure so any project can generate one and this system can consume it:

```markdown
# Sprint N — <topic>

## Goal
One-paragraph description of what this sprint builds.

## Quality level
L1 | L2 | L3

## Tasks
- id: task-1
  description: ...
  depends_on: []
- id: task-2
  description: ...
  depends_on: [task-1]

## HITL approvals
Pre-approved actions the agents may take without interrupting:
- [ ] Create Azure Storage Account "xyz" in resource group "rg-dev"
- [ ] ...

## Prise de décision
Architectural or scope decisions locked before execution starts.

## Outputs
> Filled by agents after execution.

## WISHLIST
> Deferred ideas for future sprints.
```

### Key constraints
- All skills are plain markdown `SKILL.md` files in `skills/` — no Claude-internal storage, readable by any tool
- Azure and Microsoft ecosystem for all infrastructure (Azure DevOps, Azure OpenAI, Entra ID, etc.)
- Execution runtime: VS Code on Windows
- Skills repo is the source of truth — other projects import from here, do not duplicate

---

## Part 3 — Sprint Start SOP (conclusions)

### The reusable methodology — every sprint, every time

1. **`/launch_sprint "description"`** — one command starts everything
2. **Brainstorm** — approve direction before any detail work
3. **Interview** — lock the plan, lock the quality level
4. **HITL checklist** — clear all human blockers upfront; autonomous phase only starts when this is done
5. **Agents run** — parallel where possible, sequential where needed, no interruptions
6. **Mid-sprint pause** — only for genuinely missed minor operational blockers; architectural gaps abort the sprint
7. **`sprint_log.md`** — agents document what they built and every autonomous decision they made

### What makes a sprint ready to execute
- Design approved (brainstorm complete)
- Plan is specific enough that any agent could execute a task without clarification
- Quality level locked
- HITL checklist 100% confirmed by user
- No unresolved architectural questions

### What this system is not
- Not a replacement for architectural thinking — that happens in Steps 1-2
- Not fully zero-touch — the HITL phase is mandatory and human-performed
- Not bound to one project — any project can generate a sprint file and hand it to this system

---

## WISHLIST

- [ ] **Migrate to Approach B (DAG orchestrator)** if Approach C shows limitations at scale — a Python script that parses the sprint file task DAG and spawns true OS-parallel Claude Code processes, with live `_sprint/status.md` tracking
- [ ] **Scheduled execution** — Windows Task Scheduler or Azure DevOps pipeline trigger to launch a sprint automatically at a set time (e.g., 23:00)
- [ ] **Sprint suggestion flow** — at end of each sprint, conductor proposes `sprint_N+1_*.md` draft for user review before next session
- [ ] **Token/time budget enforcement** — conductor monitors elapsed time and token spend, gracefully stops and summarizes if limits approach
- [ ] **Skills as importable modules** — make `skills/` folder importable in other Bureau projects (Copilot Studio + Claude Code both read the same INDEX.md)
- [ ] **`skill-amendment` skill** — when agents encounter friction or gaps with an existing skill during a sprint, capture the improvement in `sprint_log.md > ## Skill improvements`; build a dedicated skill later that takes those notes and proposes a diff to the source SKILL.md in this repo
