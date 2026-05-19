---
name: synthesize
description: Collect outputs from all agents in a run, merge them into a unified result, and produce the final deliverable — a PR, a summary, a set of files, or a report. Use after all agents have completed their tasks.
argument-hint: "<task-id>"
---

> **Skill activated — begin your first response with exactly: "I'm using the skill synthesize."**

> If you need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

# /synthesize

Merge all agent outputs into one coherent result.

## Usage

```
/synthesize <task-id>
```

## Process

1. **Check status** — read `_army/status.md`, confirm all agents are done (no BLOCKED items)
2. **Read all outputs** — load every file in `_army/outputs/` for this task-id
3. **Check review verdict** — if review-agent returned REQUEST CHANGES, route back to code-agent; if BLOCK, halt and notify human
4. **Merge** — combine plan, code changes, and review into a final summary
5. **Produce deliverable** — based on what's connected:
   - With `~~source control`: open or update a PR with description and review notes
   - Without: write `_army/final-<task-id>.md` with everything a human needs to act
6. **Notify** — post summary to `~~chat` if connected

## Output format

Write to `_army/final-<task-id>.md`:

```markdown
## Final Output: <task name>

### What was built
<!-- Plain English summary -->

### Files changed
<!-- From code-agent output -->

### Review verdict
<!-- From review-agent output -->

### How to deploy / test
<!-- Steps for a human to verify -->

### Open items
<!-- Any HUMAN REVIEW NEEDED or BLOCKED items that remain -->
```

## Constraints

- Do NOT proceed if review verdict is BLOCK
- Do NOT merge or deploy — produce the artifact and let a human decide
- If any agent output is missing, report what's missing and stop

## Placeholders

<!-- TODO: open PR via ~~source control with auto-generated description -->
<!-- TODO: post final summary to ~~chat -->
<!-- TODO: close ticket in ~~project tracker -->
