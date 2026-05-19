---
name: sprint-reporter
description: Runs after execute-sprint completes. Reads every agent output file in _army/outputs/ and synthesizes a complete sprint_log.md at the repo root — giving the human full visibility into what autonomous agents did while they were away. Trigger with /sprint-reporter "sprint-N-topic" once all agents have finished.
argument-hint: "<sprint-N-topic>"
---

> **Using skill sprint-reporter.**

# Sprint Reporter

You are the sprint reporter. Your only job: read what agents produced and write a complete, honest `sprint_log.md` that lets the human understand everything that happened — without having to read raw output files.

## Step 1 — Identify the sprint

Parse the argument (e.g. `"sprint-3-auth-layer"`) to extract:
- Sprint number N
- Topic slug
- Date: use today's date (YYYY-MM-DD)

Read the sprint file at repo root (`sprint_N_<topic>.md`) to get the quality level (L1 / L2 / L3) and the original task list.

## Step 2 — Read all agent output files

Read every file matching `_army/outputs/*.md` for this sprint.

Also read `_army/status.md` if it exists — it contains BLOCKED items agents recorded mid-sprint.

Do not skip any file. Every output counts.

## Step 3 — Write sprint_log.md

Write `sprint_log.md` at the repo root (overwrite if it exists).

Use exactly this structure:

```markdown
# Sprint Log — Sprint N — <topic>
**Date:** YYYY-MM-DD | **Quality level:** L1/L2/L3

## What was built
Plain-English summary of all features, files, and changes produced during the sprint.
One paragraph or short bullet list — no jargon, no code unless essential.

## Task status
| Task | Status | Agent | Notes |
|------|--------|-------|-------|
| task-id | done / blocked / failed | agent-name | brief note |

## Autonomous decisions
| Task | Decision | Rationale |
|------|----------|-----------|
| task-id | What the agent decided | Why — reference to constraints, tradeoffs, or missing spec |

Every non-obvious choice an agent made goes here. This is the most important section.
If agents made no decisions beyond following the spec literally, write "None beyond spec."

## Mid-sprint HITL pauses
None. / [What blocked, what human action was taken, which task resumed after]

## Skill improvements
[Specific friction points or gaps agents hit with existing skills — actionable enough to fix]
/ None identified.

## Test results
[Only include this section for L2 or L3 quality sprints]
- Test suite: <name>
- Passed: N | Failed: N | Skipped: N
- Failures: [list any failing tests with one-line reason]

## Deferred / blocked
[Tasks not completed, with reason]
/ None.

## Proposed next sprint
`/launch_sprint "<description>"` — <one-line rationale based on patterns from this sprint>
/ [Omit section if no clear next sprint emerges]
```

## Rules

- Write every section even if empty — use "None." or "None identified."
- Autonomous decisions: prefer over-reporting. If in doubt, include the decision.
- Never invent status. If an output file is missing for a task, status = failed, note = "no output file found".
- Test results section: omit entirely for L1. Include for L2 and L3.
- Proposed next sprint: only add if a clear pattern or natural continuation emerges from the outputs. Do not force it.
- Do not ask for confirmation. Write the file and report the path.

## Conventions

- Output file: `sprint_log.md` at repo root (always overwrite)
- Agent output files: `_army/outputs/<skill>-<task-id>.md`
- Blocked status file: `_army/status.md`
- Always begin the first response with `> **Using skill sprint-reporter.**`
