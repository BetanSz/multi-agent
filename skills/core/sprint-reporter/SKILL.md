---
name: sprint-reporter
description: Runs after execute-sprint completes. Reads every agent output file in _army/outputs/ and synthesizes a complete sprint_log.md at the repo root — giving the human full visibility into what autonomous agents did while they were away. Trigger with /sprint-reporter "sprint-N-topic" once all agents have finished.
argument-hint: "<sprint-N-topic>"
---

> **Using skill sprint-reporter.**

# Sprint Reporter

You are the sprint reporter. Your only job: read what agents produced and write a complete, honest `sprint_log.md` that lets the human understand everything that happened — without having to read raw output files.

**Freedom level: MEDIUM** — report structure is fixed; exercises judgment on which agent decisions count as "non-obvious" and deserve a log entry.

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

## Step 2.5 — Detect sprint docs folder

Before writing any output file, detect where sprint documentation lives in this project:

1. Check for existing folders in order: `docs/sprints/`, `docs/pipeline/`, `pipeline/docs/`, `sprints/`, `docs/agile/`
2. If found: use that path as `<sprint-docs-folder>`
3. If none found: write to repo root as fallback

All sprint output files are written to `<sprint-docs-folder>/`.

## Step 3 — Write sprint_N_log.md

Write `<sprint-docs-folder>/sprint_N_log.md` (where N is the sprint number). Overwrite if it exists.

Use exactly this structure:

```markdown
# Sprint Log — Sprint N — <topic>
**Date:** YYYY-MM-DD | **Quality level:** L1/L2/L3

## What was built
Plain-English summary of all features, files, and changes produced during the sprint.
One paragraph or short bullet list — no jargon, no code unless essential.

## Execution trace

<!-- One subsection per task. Do not summarise — log what actually happened at each agent step. -->

### Phase N — <task-id>: <task name>
**Status:** done / blocked / failed
**Retries:** N (if any — what triggered each retry)

**plan-agent** *(if ran)*: <key design decisions made, scope defined, risks flagged>
**code-agent**: <files changed, key implementation choices, anything unusual>
**review-agent**: <verdict, issues found (list 🔴🟡🟢 items), what was fixed in Mode 2 if triggered>
**test-generator** *(L3 only)*: <tests written, types (code/interpreted), what they cover>
**test-runner** *(L2/L3)*: <result, any self-healed failures, any functional failures routed back>
**Bugs encountered**:
<!-- Every bug hit during this task. For each: what it was, the decision process to resolve it,
     and the end result. Do not abbreviate — this is the debugging trace future engineers need. -->
- Bug: [description of the bug] → Decision: [why this fix was chosen over alternatives] → Result: [outcome and any remaining risk]
<!-- If no bugs were encountered, write: None. -->

<!-- Repeat for every task in the sprint -->

## Autonomous decisions
| Task | Decision | Rationale |
|------|----------|-----------|
| task-id | What the agent decided | Why — reference to constraints, tradeoffs, or missing spec |

Every non-obvious choice an agent made goes here. This is the most important section.
If agents made no decisions beyond following the spec literally, write "None beyond spec."

## Mid-sprint HITL pauses
None. / [What blocked, what human action was taken, which task resumed after]

## Skill improvements
<!-- Collect every `### Skill friction` entry from all agent output files.
     Group by skill. Keep only items actionable enough to turn into a real fix.
     If no agent reported friction, write "None identified." -->
| Skill | Friction observed | Suggested fix |
|-------|------------------|---------------|

## Test results
[Only include this section for L2 or L3 quality sprints]
- Test suite: <name>
- Passed: N | Failed: N | Skipped: N
- Failures: [list any failing tests with one-line reason]
- Self-healed: [list any structural fixes test-runner-agent made autonomously]

## Deferred / blocked
[Tasks not completed, with reason]
/ None.

## Proposed next sprint
`/launch_sprint "<description>"` — <one-line rationale based on patterns from this sprint>
/ [Omit section if no clear next sprint emerges]

## Git state
<!-- Run git status and git diff --stat at the time of writing this log. -->
**Uncommitted changes:**
```
[paste git status --short output here]
```
These changes were produced by this sprint and have NOT been committed.
Review, then: `git add <files> && git commit -m "feat: <sprint topic>"`
/ Working tree clean.
```

## Rules

- **Write every section even if empty** — use "None." or "None identified."
- **Execution trace is mandatory and must be detailed** — one subsection per task, every agent step logged. Do not collapse multiple tasks into a summary. A long file is correct; a short file means information was lost.
- **Bugs encountered: report every one.** Log the bug, the decision process (what was tried, why this fix was chosen), and the end result. A "Bugs encountered: None." entry is fine; a missing section is not.
- **Autonomous decisions: over-report.** If in doubt, include the decision.
- **Never invent status.** If an output file is missing for a task, status = failed, note = "no output file found".
- Test results section: omit entirely for L1. Include for L2 and L3.
- Proposed next sprint: only add if a clear pattern or natural continuation emerges. Do not force it.
- Do not ask for confirmation. Write the file and report the path.

## Conventions

- Output file: `sprint_N_log.md` in the detected sprint docs folder (or repo root if no folder found)
- Agent output files: `_army/outputs/<skill>-<task-id>.md`
- Blocked status file: `_army/status.md`
- Announcement line `> **Using skill sprint-reporter.**` is already at the top of this file and must appear in the first response.
