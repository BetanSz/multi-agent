# Sprint 2 — Multi-Agent Execution Layer

**Goal:** Build the full execution layer of the multi-agent sprint system — the skills that make autonomous agent execution real, structured, and auditable.
**Date:** 2026-05-19
**Quality level:** L1 — validated by running a real sprint after this one. Skills are text output; correctness is proven by execution, not automated tests.

---

## Prise de décision

- **Orchestration model:** Chat session = conductor. Coordination lives in conversation context, not files.
- **Audit trail:** Each subagent writes `_army/outputs/<skill>-<task-id>.md`. These are audit records, not coordination signals. They become the input for `sprint-reporter` and the migration path to Approach B (DAG runner) when needed.
- **Agent sequence per task:** plan-agent (conditional) → code-agent → review-agent → [test-generator + test-runner if L2/L3]
- **review-agent modes:** review-only (default) / fix (non-architectural REQUEST CHANGES) / architectural-fix (test before + change + test after)
- **Azure skills:** `microsoft/azure-skills` (6 skills) installed in `.agents/skills/` — callable by any subagent on demand
- **Skill announcement:** Every skill begins with `> **Using skill <name>.**`
- **All skills are plain markdown** — no Claude-internal storage, readable by Claude Code and GitHub Copilot equally

---

## Tasks

- id: task-1
  description: Build `hitl-analyzer` skill
  depends_on: []
  agent_type: plan+code
  agent_notes: |
    Interactive pre-flight skill. Reads the sprint file, identifies ALL blockers
    (architecture choices, Azure resources, credentials, git state, permissions,
    non-reversible ops). Is pushy — challenges assumptions, asks for confirmation.
    Does NOT close until each item is executed AND confirmed working by the user.
    Output: numbered checklist written into sprint file under `## HITL approvals`.
    Gate: autonomous execution cannot start until checklist is 100% confirmed.
    Save to: skills/core/hitl-analyzer/SKILL.md

- id: task-2
  description: Build `execute-sprint` skill
  depends_on: []
  agent_type: plan+code
  agent_notes: |
    Core execution orchestrator. Reads sprint file task DAG.
    Default: sequential execution. Parallel only when task group has no shared depends_on.
    Per task, dispatches subagents with: task description, agent_notes, quality level,
    explicit skill paths to read, _army/ coordination convention.
    Agent sequence per task:
      1. plan-agent (if agent_type = plan+code)
      2. code-agent (always) — reads skills/core/code-agent/SKILL.md
      3. review-agent (always) — reads skills/core/review-agent/SKILL.md
      4. test-generator (if L3) — reads skills/core/test-generator-agent/SKILL.md
      5. test-runner (if L2 or L3) — reads skills/core/test-runner-agent/SKILL.md
    Mid-sprint HITL pause: stop → surface action → wait → resume. Only for minor
    operational blockers missed from HITL review. Never for architecture.
    Azure tasks: instruct subagent to read relevant .agents/skills/azure-*/SKILL.md.
    Never ask "want to continue?" Never prompt on duration or tokens.
    Save to: skills/core/execute-sprint/SKILL.md

- id: task-3
  description: Build `sprint-reporter` skill
  depends_on: [task-1, task-2]
  agent_type: code
  agent_notes: |
    Reads all _army/outputs/<task-id>.md files after execution completes.
    Synthesizes sprint_log.md at repo root.
    Required sections: what was built, task status table, autonomous decisions
    (every minor architectural/implementation choice agents made + rationale),
    mid-sprint HITL pauses (if any), skill improvements (friction encountered),
    deferred/blocked items.
    This is the human's window into what the agents did while they were away.
    Save to: skills/core/sprint-reporter/SKILL.md

- id: task-4
  description: Update `code-agent` skill with project coding standards
  depends_on: []
  agent_type: code
  agent_notes: |
    Current skill is too rigid ("implement exactly what the plan says, nothing more").
    Update with these characteristics (reference skills for content to pull in):
    - Follow good practices: guard clauses, no duplication, no magic numbers
      (pull patterns from skills/other/openclaw-maintenance/codex-review/SKILL.md
      and .agents/skills/superficial-file-refactor/SKILL.md)
    - Stay with current stack — all major architectural/stack decisions locked in plan
    - Write efficient code: use native object methods, prefer built-ins
    - Be Pythonic: list comprehensions, generators, dict lookups, lru_cache
      (pull from .agents/skills/python-performance-optimization/SKILL.md)
    - Minimal footprint: don't alter code unrelated to the feature
    - No unnecessary refactors beyond task scope
    - Streamlined logic: avoid repetition, single responsibility
    - Code readable by intermediate developer — not overly clever
    - When hitting ambiguity not resolved by plan: write BLOCKED to _army/status.md, stop
    Keep output format unchanged (_army/outputs/code-<task-id>.md)
    Save to: skills/core/code-agent/SKILL.md (overwrite)

- id: task-5
  description: Update `review-agent` with 3-mode review + performance analysis
  depends_on: [task-4]
  agent_type: code
  agent_notes: |
    Current skill is review-only, cannot modify code. Update to 3 modes:
    MODE 1 — Review (default): structured comments, severity labels
      (🔴 blocking / 🟡 important / 🟢 nit), verdict APPROVE/REQUEST CHANGES/BLOCK.
      Check: scope vs plan, correctness, security, performance, maintainability,
      unused API calls/initializations, best practices.
      Pull checklist patterns from .agents/skills/code-review-excellence/SKILL.md
      Pull performance checks from .agents/skills/python-performance-optimization/SKILL.md
      Report section: "Major architectural change advised?" YES/NO with rationale.
      If YES and not making the change now: flag as BLOCK, explain what change is needed.
    MODE 2 — Fix (non-architectural REQUEST CHANGES): makes fixes directly in code,
      documents every change made, re-runs review pass to confirm resolved.
    MODE 3 — Architectural fix: ONLY when architectural change is clearly beneficial
      and low-risk. Protocol: run existing tests as baseline → make change →
      run tests again → report delta. Only proceed if both states pass.
      Document decision in _army/outputs/review-<task-id>.md under "Autonomous decisions".
    Output format: _army/outputs/review-<task-id>.md (extend existing format)
    Save to: skills/core/review-agent/SKILL.md (overwrite)

- id: task-6
  description: Build `test-generator-agent` skill (L3 sprints)
  depends_on: [task-4]
  agent_type: code
  agent_notes: |
    NEW skill. Used only for L3 quality sprints.
    Reads the task description and code-agent output.
    Writes failing tests for every new feature/function introduced.
    Must follow TDD protocol: test written BEFORE checking if it passes.
    Reference: .agents/skills/test-driven-development/SKILL.md for TDD protocol.
    Output: test files written to target project, plus summary in
    _army/outputs/test-generator-<task-id>.md listing what tests were written and why.
    Save to: skills/core/test-generator-agent/SKILL.md

- id: task-7
  description: Build `test-runner-agent` skill (L2 and L3 sprints)
  depends_on: [task-6]
  agent_type: code
  agent_notes: |
    NEW skill. Runs tests and reports results.
    L2 mode: runs existing test suite only. Fails on any regression.
    L3 mode: runs existing tests + new tests from test-generator-agent.
             Fails if any test fails.
    On failure: writes FAILING_TESTS report to _army/outputs/test-runner-<task-id>.md
    with exact failures, then signals conductor to loop back to code-agent with context.
    On pass: writes PASS report, execution proceeds.
    Save to: skills/core/test-runner-agent/SKILL.md

- id: task-8
  description: Update `launch_sprint` to call new skills explicitly (no inline logic)
  depends_on: [task-1, task-2, task-3]
  agent_type: code
  agent_notes: |
    Remove all inline logic from Steps 3, 4, 5.
    Step 3 → explicit call: read skills/core/hitl-analyzer/SKILL.md
    Step 4 → explicit call: read skills/core/execute-sprint/SKILL.md
    Step 5 → explicit call: read skills/core/sprint-reporter/SKILL.md
    launch_sprint becomes a pure pipeline conductor — it sequences skills,
    holds context, and enforces gates (Step 4 cannot start until Step 3 confirms).
    Save to: skills/core/launch-sprint/SKILL.md (overwrite)

- id: task-9
  description: Update INDEX.md with all new and updated skills
  depends_on: [task-1, task-2, task-3, task-4, task-5, task-6, task-7, task-8]
  agent_type: code
  agent_notes: |
    Add new skills to Core section: hitl-analyzer, execute-sprint, sprint-reporter,
    test-generator-agent, test-runner-agent.
    Mark code-agent and review-agent as updated with brief description of changes.
    Save to: skills/INDEX.md

---

## HITL approvals

None — this sprint builds markdown skill files only. No Azure resources, no external
APIs, no credentials required. Autonomous execution can start immediately.

---

## Outputs

> To be filled by agents after execution.

---

## WISHLIST

- [ ] `skill-amendment` flow — agents capture skill friction in sprint_log.md `## Skill improvements`; future skill builds a diff-proposal mechanism
- [ ] Migrate to Approach B (DAG runner) after 2-3 real sprints validate the patterns
- [ ] `test-runner-agent` should support multiple test runners (pytest, jest, dotnet test) — v1 assumes pytest
- [ ] **Tournament mode in execute-sprint** — for a single task, dispatch N code-agents with different approaches in parallel, then review-agent evaluates all and picks the winner. Useful when multiple valid implementations exist and the best is non-obvious.
