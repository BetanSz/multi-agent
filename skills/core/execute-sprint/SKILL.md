---
name: execute-sprint
description: Autonomous sprint execution engine. Reads a confirmed sprint file, builds the task DAG from depends_on fields, and dispatches agents (plan → code → review → test) in the correct order — parallel when safe, sequential when dependent — without human interaction except genuine unexpected blockers. Trigger after the HITL checklist in launch-sprint is fully confirmed, or call directly with a path to an already-approved sprint file.
argument-hint: "path/to/sprint_N_*.md"
---

> **Using skill execute-sprint.**

# Execute Sprint

You are the autonomous execution engine for the sprint system. Your job: read the sprint file, build the task DAG, dispatch agents in order, and complete every task without prompting the user — except for a genuine unexpected blocker.

**Freedom level: LOW** — fixed DAG execution sequence. Retry counts and routing decisions are owned by this skill; subagents report results only.

## 1 — Load the sprint file

Argument: path passed by the caller, or find `sprint_N_*.md` at repo root.

Parse:
- **Quality level** (`L1` / `L2` / `L3`) from the header
- **Task list**: every `id`, `description`, `depends_on`, `agent_notes`, and `agent_type` field
- **Prise de décision** section — these decisions are locked; agents must not re-open them

**Before doing anything else, create the output directory:**
```
_army/
  outputs/
  status.md   ← create empty if it does not exist
```
If the directory already exists, leave it. This directory must exist before any agent runs.

## 2 — Build the task DAG

Scan all `depends_on` lists. Group tasks into execution waves:

- **Wave 0**: tasks with empty `depends_on: []`
- **Wave N**: tasks whose every dependency belongs to a wave < N

Within a wave, all tasks are independent of each other. Across waves, tasks must be strictly sequential.

## 3 — Execute the DAG

### Parallel dispatch (within a wave)
When a wave contains more than one task, dispatch all tasks in that wave as simultaneous `Agent()` calls in a **single response**. Do not wait for one to finish before starting another.

### Sequential gating (across waves)
Do not start wave N+1 until every task in wave N has a confirmed output file at `_army/outputs/`.

### Output file verification (after every agent step)
After each agent step (plan, code, review, test-generator, test-runner), **verify the expected output file exists** before proceeding:

```
_army/outputs/plan-<task-id>.md      ← after plan-agent
_army/outputs/code-<task-id>.md      ← after code-agent
_army/outputs/review-<task-id>.md    ← after review-agent
_army/outputs/test-generator-<task-id>.md  ← after test-generator
_army/outputs/test-runner-<task-id>.md     ← after test-runner
```

If the file does not exist after the agent step: **the step did not complete**. Do not proceed. Either re-run the step or trigger a mid-sprint HITL pause. A missing output file is never acceptable — it means the audit trail has a gap.

---

## 4 — Per-task agent sequence

Run the following agents in order for each task. Each agent is a separate `Agent()` call with the prompt contract below.

### 4.1 plan-agent — only if `agent_type: plan+code`

Read `skills/core/plan-agent/SKILL.md`.
Output: `_army/outputs/plan-<task-id>.md`

### 4.2 code-agent — always

Read `skills/core/code-agent/SKILL.md`.
If step 4.1 ran, pass the plan output as context.
Output: `_army/outputs/code-<task-id>.md`

### 4.3 review-agent — always

Read `skills/core/review-agent/SKILL.md`.
Pass the code output as context.
Output: `_army/outputs/review-<task-id>.md`

Verdicts:
- **APPROVE** — proceed to 4.4
- **REQUEST CHANGES** — return to code-agent with review feedback. Maximum 2 retries; after the second retry, run review-agent once more. If still REQUEST CHANGES after 2 retries → treat as BLOCK.
- **BLOCK** — trigger mid-sprint HITL pause (see section 5)

### 4.4 test-generator-agent — only if quality level is L3

Read `skills/core/test-generator-agent/SKILL.md`.
Output: `_army/outputs/test-generator-<task-id>.md`

### 4.5 test-runner-agent — only if quality level is L2 or L3

Read `skills/core/test-runner-agent/SKILL.md`.
Output: `_army/outputs/test-runner-<task-id>.md`

Verdicts:
- **PASS** — task complete. Write a one-line summary to `_army/status.md`.
- **FAIL** — return to code-agent with full failure context. Maximum 2 retries, then run test-runner-agent again. If still FAIL after 2 retries → trigger mid-sprint HITL pause.

---

## 5 — Agent prompt contract

Every subagent call must include all of the following:

```
Task: <task description from sprint file>

agent_notes: <agent_notes verbatim from sprint file>

Quality level: <L1 | L2 | L3>
- L1: implement feature; produce manual verification checklist
- L2: implement feature; all pre-existing tests must pass
- L3: write failing tests first (TDD-light), then implement until all tests pass

Skills to read (in order):
1. <skill path(s) — see sequence in section 4>

Output convention:
- Write your output to _army/outputs/<skill>-<task-id>.md
- If blocked, append a BLOCKED entry to _army/status.md with exact reason

Locked decisions (do not re-open):
<paste the Prise de décision section from the sprint file>
```

**Azure tasks**: if `agent_notes` mentions any Azure resource (storage, deployment, AI, diagnostics, validation, environment setup), append the relevant skill path(s):
- Storage → `.agents/skills/azure-storage/SKILL.md`
- Deployment → `.agents/skills/azure-deploy/SKILL.md`
- AI services → `.agents/skills/azure-ai/SKILL.md`
- Diagnostics → `.agents/skills/azure-diagnostics/SKILL.md`
- Environment / auth → `.agents/skills/azure-prepare/SKILL.md`
- Policy / naming → `.agents/skills/azure-validate/SKILL.md`

**Python stack:** when an Azure skill offers both Python and .NET SDK examples, always prefer the Python reference.

---

## 6 — Mid-sprint HITL pause (exception path only)

Use this only when an action is genuinely blocked by something that was missed in the HITL checklist — always a minor operational issue (missing credential, unprovisioned resource). Never pause for architectural questions; those are locked in `Prise de décision`.

Protocol:
1. Stop all agent dispatch immediately.
2. State precisely: what is blocked, what action the user must take, and which task will resume.
3. Wait for the user to confirm the action is done.
4. Resume from the blocked task, re-running its agent sequence from the failed step.

Never say "want to continue?" Never ask about duration or token usage.

---

## 7 — Progress reporting in chat

Format all progress output in the chat clearly so the human can follow without reading raw files.

**On DAG build**, print a numbered phase map — one line per task:
```
Sprint: <topic> | Quality: L1/L2/L3 | Tasks: N

Phase 1 — <task name>: <one-line description>
Phase 2 — <task name>: <one-line description>
  Phase 2.1 — <subtask if parallel>
  Phase 2.2 — <subtask if parallel>
```

**On each phase start**, print a header:
```
─────────────────────────────────────────
Phase N — <task name>
<2-line description of what this phase builds and why it matters for the sprint>
─────────────────────────────────────────
```

**On each agent handoff within a phase** (plan → code → review → test), print a one-liner:
```
  → plan-agent: designing <scope>
  → code-agent: implementing <what>
  → review-agent: reviewing <what>
  → test-runner: running <suite>
```

**On phase completion**, print:
```
  ✓ Phase N complete — <one-line summary of what was produced>
```

**On BLOCK or mid-sprint pause**, print clearly:
```
  ✗ Phase N blocked — <reason> — waiting for human input
```

Keep descriptions concrete (name the files, functions, or schemas involved), not generic ("implementing features").

## 9 — Mandatory closing steps

**The sprint is not complete until both closing files exist. Do not report the sprint as done, do not output a completion message, do not stop — until steps 9.1 and 9.2 are finished.**

### 9.1 — Sprint log (mandatory)

Read and execute `skills/core/sprint-reporter/SKILL.md` now. Do not skip this step even if the sprint ran smoothly and the result feels obvious.

Pass:
- The sprint file path
- All completed task IDs and their output file paths
- Any mid-sprint HITL pauses
- Any autonomous decisions made by agents

Confirm `sprint_N_log.md` was written (in the sprint docs folder confirmed during HITL, or repo root) before proceeding to 9.2.

### 9.2 — Pre-mortem (mandatory)

Read and execute `skills/core/sprint-premortem/SKILL.md` now.

Pass the same sprint topic/number. sprint-premortem reads the codebase and sprint log, writes `sprint_N_premortem.md` to the sprint docs folder.

Confirm `sprint_N_premortem.md` was written.

---

Only after both files exist, print the sprint completion summary:
```
Sprint complete.
  <sprint-docs-folder>/sprint_N_log.md       — full execution log
  <sprint-docs-folder>/sprint_N_premortem.md — risk analysis (Tigers / Paper Tigers / Elephants)
```
