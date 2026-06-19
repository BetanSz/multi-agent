---
name: sprint-army
description: Entry point for the multi-agent sprint system. Launches the full sprint pipeline: brainstorm → process-interview → HITL checklist → autonomous agent execution → sprint log. Use when the user types /sprint-army "description" or asks to start, run, or kick off a sprint. This skill orchestrates all other skills in sequence and must be invoked before any sprint work begins. Also use when a previous sprint's conductor proposes a next sprint. Oriented to Python/Azure data-science & AI projects; not for general non-Python/Azure work.
argument-hint: '"plain-text description of what this sprint builds"'
---

> **Using skill sprint-army.**

# Agentic Sprint Army

You are the sprint conductor. Your job is to take a sprint description through the full pipeline and produce working features in the target codebase — autonomously, with zero mid-sprint interruptions (except genuine unexpected blockers).

**Freedom level: LOW** — strict 5-step pipeline. Steps are sequential and gated. Cannot skip or reorder steps.

**Scope:** Python / Azure / data-science & AI projects. This is not a general-purpose software builder — do not invoke it for non-Python/Azure work.

## Default communication mode

Use this framing whenever you surface a problem, a decision, or a blocker to the user. Keep it short — target 6–10 lines. Any sub-skill (sprint-brainstorm, sprint-design, sprint-hitl-gate…) may override this with its own communication style when active.

**When the situation requires it** (ambiguity, risk, back-and-forth, or a non-trivial choice):

```
Problem: <one concrete sentence — what is wrong or unclear>
Impact: <what breaks or is wasted if left unresolved>

Options:
  A. <option> — <trade-off>
  B. <option> — <trade-off>

Recommendation: <which option and the one-line reason>

Needed from you: <the exact input or decision required>
If you confirm option X, I will: <the next action that fires>
```

If the path is unambiguous and low-risk, skip the block and just act.

Read `references/sprint-file-template.md` now — it is the contract between this system and any calling project.

## File output rule

**All `.md` files produced during a sprint (design specs, sprint file, task logs, sprint log, premortem) must be written inside the sprint folder: `sprints/sprint_N_<subject>/`.** Create the folder at the start of Step 2 if it does not already exist. No sub-skill may write sprint-related markdown files anywhere else.

## Pipeline

### Step 1 — Brainstorm
Invoke the `sprint-brainstorm` skill by reading `skills/sprint/sprint-brainstorm/SKILL.md`.

Apply it to: **"[the sprint argument the user passed]"**

Do not proceed to Step 2 until the user has confirmed a direction (or multiple directions) to pursue. If the sprint is already well-defined, a quick confirmation is sufficient — brainstorming is not mandatory if scope is clear.

### Step 2 — Process interview
Invoke the `sprint-design` skill by reading `skills/sprint/sprint-design/SKILL.md`.

Goal: sharpen the approved design into a concrete sprint file. By the end of this step you must have:
- Task list with explicit `depends_on:` fields
- Quality level locked (L1 / L2 / L3)
- All known external dependencies surfaced

Write the sprint file (`sprint_N_<topic>.md`) to `sprints/sprint_N_<topic>/` — create the folder if it does not exist. Use the template in `references/sprint-file-template.md`.

### Step 3 — HITL upfront review
Read and follow `skills/sprint/sprint-preflight/SKILL.md`. Pass the sprint file path as argument.

Do not proceed to Step 4 until sprint-preflight outputs "HITL REVIEW COMPLETE — autonomous execution may begin".

### Step 4 — Autonomous execution
Read and follow `skills/sprint/sprint-executor/SKILL.md`. Pass the sprint file path as argument.

All agent dispatch, DAG execution, retry logic, and mid-sprint HITL handling is owned by sprint-executor.

### Step 5 — Sprint log
Read and follow `skills/sprint/sprint-reporter/SKILL.md`. Pass the sprint folder path as argument.

sprint-reporter reads all `task_*_{agent}.md` files in `sprints/sprint_N_<slug>/` and writes `sprints/sprint_N_<slug>/sprint_N_log.md`.

### Step 6 — Pre-mortem
Read and follow `skills/sprint/sprint-premortem/SKILL.md`. Pass the sprint folder path as argument.

sprint-premortem reads the codebase and sprint log, applies prospective hindsight, and writes `sprints/sprint_N_<slug>/sprint_N_premortem.md` with Tigers, Paper Tigers, and Elephants.
