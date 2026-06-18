---
name: sprint-executor
description: Autonomous sprint execution engine. Reads a confirmed sprint file, builds the task DAG from depends_on fields, and dispatches agents (plan → code → review → test) in the correct order — parallel when safe, sequential when dependent — without human interaction except genuine unexpected blockers. Trigger after the HITL checklist in sprint-army is fully confirmed, or call directly with a path to an already-approved sprint file.
argument-hint: "path/to/sprint_N_*.md"
---

> **Using skill sprint-executor.**

# Execute Sprint

You are the autonomous execution engine for the sprint system. Your job: read the sprint file, build the task DAG, dispatch agents in order, and complete every task without prompting the user — except for a genuine unexpected blocker.

**Freedom level: LOW** — fixed DAG execution sequence. Retry counts and routing decisions are owned by this skill; subagents report results only.

## 1 — Load the sprint file

Argument: path passed by the caller, or find `sprint_N_*.md` in `sprints/` or at repo root.

Parse:
- **Sprint number N** and **topic slug** from the filename (e.g. `sprint_4_ner_extraction.md` → N=4, slug=`ner_extraction`)
- **Quality level** (`L1` / `L2` / `L3`) from the header
- **Task list**: every `id`, `description`, `depends_on`, `agent_notes`, and `agent_type` field
- **Prise de décision** section — these decisions are locked; agents must not re-open them

**Before doing anything else:**

1. Create `sprints/sprint_N_<slug>/` if it does not exist (this is the sprint folder for all outputs)
2. Create `sprints/sprint_N_<slug>/status.md` (empty) if it does not exist
3. If the sprint file is at repo root, move it into `sprints/sprint_N_<slug>/`

**Generate a description slug for every task** — used in all output filenames:
- Take the task `description`, extract the first 3–4 meaningful words (skip articles, prepositions, conjunctions)
- Lowercase, underscores, max 30 characters
- Examples:
  - "Extend Settings and azure_clients with multi-model support" → `extend_settings_clients`
  - "Define Pydantic schemas for all three passes" → `pydantic_schemas`
  - "Write pipeline/step_04_ner_extract.py" → `pipeline_step_04`
  - "Create tests/ folder and write initial test suite" → `create_test_suite`
  - "Run test suite and fix until green" → `run_tests`

## 2 — Build the task DAG

Scan all `depends_on` lists. Group tasks into execution waves:

- **Wave 0**: tasks with empty `depends_on: []`
- **Wave N**: tasks whose every dependency belongs to a wave < N

Within a wave, all tasks are independent of each other. Across waves, tasks must be strictly sequential.

## 3 — Execute the DAG

### Agent context isolation

Each dispatched agent receives **only the context it needs** — the relevant skill file, the sprint task block, and any upstream output files it depends on. Agents must never inherit the orchestrator's full session context or history. Construct each agent's prompt explicitly. This keeps agents focused and prevents context pollution between parallel tasks.

### Parallel dispatch (within a wave)
When a wave contains more than one task, dispatch all tasks in that wave as simultaneous `Agent()` calls in a **single response**. Do not wait for one to finish before starting another.

### Sequential gating (across waves)
Do not start wave N+1 until every task in wave N has a confirmed output file in `sprints/sprint_N_<slug>/`.

### Output file verification (after every agent step)
After each agent step, **verify the expected output file exists** before proceeding.

All files live in `sprints/sprint_N_<slug>/`. Naming pattern: `task_{id}_{desc-slug}_{agent}.md`

```
task_{id}_{desc-slug}_plan.md      ← after plan-agent
task_{id}_{desc-slug}_code.md      ← after code-agent
task_{id}_{desc-slug}_review.md    ← after review-agent
task_{id}_{desc-slug}_test_gen.md  ← after test-generator-agent
task_{id}_{desc-slug}_test_run.md  ← after test-runner-agent
```

Example for task-2 "Define Pydantic schemas":
```
sprints/sprint_4_ner_extraction/task_2_pydantic_schemas_code.md
sprints/sprint_4_ner_extraction/task_2_pydantic_schemas_review.md
```

If the file does not exist after the agent step: **the step did not complete**. Do not proceed. Either re-run the step or trigger a mid-sprint HITL pause. A missing output file is never acceptable — it means the audit trail has a gap.

---

## 4 — Per-task agent sequence

Run the following agents in order for each task. Each agent is a separate `Agent()` call with the prompt contract below.

### 4.1 plan-agent — only if `agent_type: plan+code`

Read `skills/sprint/plan-agent/SKILL.md`.
Output: `sprints/sprint_N_<slug>/task_{id}_{desc-slug}_plan.md`

### 4.2 test-generator-agent — only if quality level is L3

**Runs before code-agent.** Tests are written against the plan spec, not the implementation. This is the TDD contract: failing tests exist before any production code is written.

Read `skills/sprint/test-gen-agent/SKILL.md`.
Pass the plan output as primary input (or the task description from the sprint file if no plan step ran).
Output: `sprints/sprint_N_<slug>/task_{id}_{desc-slug}_test_gen.md`

### 4.3 code-agent — always

Read `skills/sprint/code-agent/SKILL.md`.
If step 4.1 ran, pass the plan output as context.
If quality level is L3, also pass the test_gen output — code-agent must write code that makes those failing tests pass.
Output: `sprints/sprint_N_<slug>/task_{id}_{desc-slug}_code.md`

### 4.4 review-agent — always

Read `skills/sprint/review-agent/SKILL.md`.
Pass the code output as context.
Output: `sprints/sprint_N_<slug>/task_{id}_{desc-slug}_review.md`

Verdicts:
- **APPROVE** — proceed to 4.5
- **REQUEST CHANGES** — return to code-agent with review feedback. Maximum 2 retries; after the second retry, run review-agent once more. If still REQUEST CHANGES after 2 retries → treat as BLOCK.
- **BLOCK** — trigger mid-sprint HITL pause (see section 5)

### 4.5 test-runner-agent — only if quality level is L2 or L3

Read `skills/sprint/test-run-agent/SKILL.md`.
Output: `sprints/sprint_N_<slug>/task_{id}_{desc-slug}_test_run.md`

Verdicts:
- **PASS** — task complete. Write a one-line summary to `sprints/sprint_N_<slug>/status.md`.
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
- Sprint folder: sprints/sprint_N_<slug>/  (conductor will tell you the exact path)
- Write your output to: sprints/sprint_N_<slug>/task_{id}_{desc-slug}_{agent}.md
  where {agent} is one of: plan, code, review, test_gen, test_run
- If blocked, append a BLOCKED entry to sprints/sprint_N_<slug>/status.md with exact reason

Locked decisions (do not re-open):
<paste the Prise de décision section from the sprint file>
```

**Azure tasks**: if `agent_notes` mentions any Azure resource (storage, deployment, AI, diagnostics, validation, environment setup), append the relevant skill path(s):
- Storage → `skills/azure-storage/SKILL.md`
- Deployment → `skills/azure-deploy/SKILL.md`
- AI services → `skills/azure-ai/SKILL.md`
- Diagnostics → `skills/azure-diagnostics/SKILL.md`
- Environment / auth → `skills/azure-prepare/SKILL.md`
- Policy / naming → `skills/azure-validate/SKILL.md`

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

Read and execute `skills/sprint/sprint-reporter/SKILL.md` now. Do not skip this step even if the sprint ran smoothly and the result feels obvious.

Pass:
- The sprint file path
- All completed task IDs and their output file paths
- Any mid-sprint HITL pauses
- Any autonomous decisions made by agents

Confirm `sprints/sprint_N_<slug>/sprint_N_log.md` was written before proceeding to 9.2.

### 9.2 — Pre-mortem (mandatory)

Read and execute `skills/sprint/sprint-premortem/SKILL.md` now.

Pass the sprint folder path. sprint-premortem reads the codebase and sprint log, writes `sprint_N_premortem.md` to `sprints/sprint_N_<slug>/`.

Confirm `sprints/sprint_N_<slug>/sprint_N_premortem.md` was written.

---

Only after both files exist, run `git status` and print the sprint completion summary:

```
Sprint complete — sprints/sprint_N_<slug>/
  sprint_N_log.md        — full execution log
  sprint_N_premortem.md  — risk analysis (Tigers / Paper Tigers / Elephants)
  task_*_code.md         — N implementation records
  task_*_review.md       — N review records

Uncommitted changes:
  [actual git status --short output]

These changes were NOT committed. Review and commit when ready:
  git add <files> && git commit -m "feat: <sprint topic>"
```

If the working tree is clean, print: `Working tree clean — nothing to commit.`
