---
name: launch-sprint
description: Entry point for the multi-agent sprint system. Launches the full sprint pipeline: brainstorm → process-interview → HITL checklist → autonomous agent execution → sprint log. Use when the user types /launch_sprint "description" or asks to start, run, or kick off a sprint. This skill orchestrates all other skills in sequence and must be invoked before any sprint work begins. Also use when a previous sprint's conductor proposes a next sprint.
argument-hint: '"plain-text description of what this sprint builds"'
---

> **Using skill launch-sprint.**

# Launch Sprint

You are the sprint conductor. Your job is to take a sprint description through the full pipeline and produce working features in the target codebase — autonomously, with zero mid-sprint interruptions (except genuine unexpected blockers).

**Freedom level: LOW** — strict 5-step pipeline. Steps are sequential and gated. Cannot skip or reorder steps.

Read `references/sprint-file-template.md` now — it is the contract between this system and any calling project.

## Pipeline

### Step 1 — Brainstorm
Invoke the `brainstorming` skill by reading `.agents/skills/brainstorming/SKILL.md`.

Apply it to: **"[the sprint argument the user passed]"**

Do not proceed to Step 2 until the user has confirmed a direction (or multiple directions) to pursue. If the sprint is already well-defined, a quick confirmation is sufficient — brainstorming is not mandatory if scope is clear.

### Step 2 — Process interview
Invoke the `process-interviewer` skill by reading `skills/utility/process-interviewer/SKILL.md`.

Goal: sharpen the approved design into a concrete sprint file. By the end of this step you must have:
- Task list with explicit `depends_on:` fields
- Quality level locked (L1 / L2 / L3)
- All known external dependencies surfaced

Write the sprint file (`sprint_N_<topic>.md`) to `sprints/sprint_N_<topic>/` — create the folder if it does not exist. Use the template in `references/sprint-file-template.md`.

### Step 3 — HITL upfront review
Read and follow `skills/core/hitl-analyzer/SKILL.md`. Pass the sprint file path as argument.

Do not proceed to Step 4 until hitl-analyzer outputs "HITL REVIEW COMPLETE — autonomous execution may begin".

### Step 4 — Autonomous execution
Read and follow `skills/core/execute-sprint/SKILL.md`. Pass the sprint file path as argument.

All agent dispatch, DAG execution, retry logic, and mid-sprint HITL handling is owned by execute-sprint.

### Step 5 — Sprint log
Read and follow `skills/core/sprint-reporter/SKILL.md`. Pass the sprint topic/number as argument.

sprint-reporter reads `_army/outputs/` and produces `sprint_log.md`.

### Step 6 — Pre-mortem
Read and follow `skills/core/sprint-premortem/SKILL.md`. Pass the same sprint topic/number as argument.

sprint-premortem reads `sprint_log.md` and all agent outputs, applies prospective hindsight, and produces `sprint_<N>_premortem.md` with Tigers, Paper Tigers, and Elephants.
