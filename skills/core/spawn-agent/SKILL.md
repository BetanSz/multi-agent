---
name: spawn-agent
description: Define and activate a specialized agent with a specific role, context, and task. Use when the orchestrator needs to delegate a subtask to a focused agent. The agent receives its role, a clear task, and the context it needs — nothing more.
argument-hint: "<role> <task description>"
---

> **Skill activated — begin your first response with exactly: "I'm using the skill spawn-agent."**

> If you need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

# /spawn-agent

Activate a focused agent with a single role and task.

## Usage

```
/spawn-agent <role> "<task>"
```

Roles: `planner` | `coder` | `reviewer` | `researcher`

## Process

### Step 1 — Load role definition
Read the role definition from `references/agent-roles.md` for the specified role. This sets the agent's identity, constraints, and output format.

### Step 2 — Load context
Read relevant context from:
- `_army/plan.md` — the overall task plan
- Any files listed as input for this subtask
- Connected `~~source control` files if referenced

### Step 3 — Select model
Read `references/model-routing.md` to determine the right model for this role. Route via `~~ai router` if configured, otherwise use the current model.

### Step 4 — Execute with constraints
Run the agent with:
- Role identity locked (no scope creep)
- Output path specified (`_army/outputs/<role>-<task-id>.md`)
- Stop condition: agent writes `DONE` marker to output file

### Step 5 — Report
Write result summary to `_army/status.md`.

## Output

`_army/outputs/<role>-<task-id>.md` — structured output from the agent

## Placeholders

<!-- TODO: model selection logic via ~~ai router -->
<!-- TODO: parallelism support — spawn multiple agents simultaneously -->
