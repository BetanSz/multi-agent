---
name: orchestrate
description: Break a complex coding task into subtasks and assign each to the right agent role. Use when the user says "build this feature", "fix this system", or any task that clearly spans planning, coding, and review. This is the entry point for the multi-agent-army — it decomposes the work and coordinates the other agents.
argument-hint: "<task description or ticket>"
---

> **Skill activated — begin your first response with exactly: "I'm using the skill orchestrate."**

> If you need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

# /orchestrate

Decompose a coding task and coordinate specialized agents to complete it.

## Usage

```
/orchestrate $ARGUMENTS
```

## Process

### Step 1 — Understand the task
Read the task description. If a `~~project tracker` ticket is referenced, fetch it. If a repo is connected via `~~source control`, read the relevant files before decomposing.

### Step 2 — Decompose into subtasks
Break the task into clear, independently-executable subtasks. Each subtask must:
- Have a single clear output
- Be assignable to exactly one agent role (plan / code / review)
- Be small enough to complete in one agent session

Write the decomposition to `_army/plan.md` in the workspace.

### Step 3 — Assign agent roles
For each subtask, determine the right agent:
- **plan-agent** — architecture decisions, scoping, API design
- **code-agent** — implementation, refactoring, test writing
- **review-agent** — diff review, security check, correctness

### Step 4 — Spawn agents in order
Invoke each agent skill in dependency order. Pass context via files in `_army/`. Wait for each agent to write its output before spawning the next.

### Step 5 — Synthesize
Once all agents are done, invoke `/synthesize` to merge results and produce the final output (PR, summary, or file diff).

## Output

- `_army/plan.md` — task decomposition and agent assignments
- `_army/status.md` — live status of each agent (pending / running / done)

## Placeholders

<!-- TODO: add logic for reading ticket from ~~project tracker -->
<!-- TODO: add logic for posting status update to ~~chat -->
