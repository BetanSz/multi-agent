---
name: refactor-army
description: Orchestrates the full agentic refactor army pipeline. Two execution modes — Sequential (interactive, one phase at a time) or Parallel (science audit + antipattern audit + perf baseline dispatched simultaneously, then unified synthesis before any code is touched). Both modes converge at the architectural refactor and produce a complete refactor log under refactors/refactor_N_<slug>/. Invoke via /refactor-army "path/to/codebase [optional concern]".
argument-hint: '"path/to/codebase" or "path/to/codebase — specific concern"'
---

> **Using skill refactor-army.**

# Agentic Refactor Army

Two execution modes, one human checkpoint (placed differently per mode), phases 3–6 shared. No skipping phases within a mode.

**Freedom level: LOW for sequencing** — the three phases are mandatory and must run in order. **MEDIUM within each phase** — judgment is required on what counts as an antipattern, what warrants deep restructuring, and what is worth flagging vs. fixing silently.

## Default communication mode

Use this framing whenever you surface a problem, a decision, or a blocker to the user. Keep it short — target 6–10 lines. Any sub-skill (refactor-science, refactor-antipatterns, refactor-structure…) may override this with its own communication style when active.

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

## Setup — before anything

### 1. Parse the argument

Extract from the argument:
- **Codebase path** — the root folder to analyse
- **User concern** (optional) — anything after `—` or `"` is a specific problem the user wants prioritized

If the codebase path is missing, stop and ask for it.

### 2. Create the refactor folder

Determine the run number N (count existing `refactors/refactor_*/` folders + 1) and derive a slug from the codebase name or the user concern.

```
refactors/refactor_N_<slug>/
```

Create it now. All artifacts from all phases land here.

Confirm: `"Refactor folder: refactors/refactor_N_<slug>/ created."`

### 3. Mode selection

Ask the user:

> **Choose execution mode:**
>
> **A — Sequential (interactive):** Phases run one by one in order. You can discuss findings at each step before moving forward. The science audit is fully interactive.
>
> **B — Parallel:** Science audit, antipattern audit, and performance baseline are launched simultaneously as independent agents — each writes its own report. Key findings from all three are then presented as a unified synthesis before any code is touched.
>
> Which mode? (A or B)

Proceed to the section matching the user's choice.

---

## Sequential Mode

---

## Phase 1 — Science Audit (interactive)

**Invoke skill:** `skills/refactor/refactor-science/SKILL.md` (`refactor-science`)

Pass:
- The codebase path
- The user concern (if any) as the pre-loaded flag for Step 0

**This phase is inherently interactive.** The skill will:
- Ask the user about their concern (Step 0)
- Present the pipeline portrait and collect the user's reaction
- Run all audit lenses independently of the user's response
- Surface flags, risks, and evaluation gaps

**Do not rush this phase.** The audit is the diagnostic — the refactor is only as good as the diagnosis.

When the science audit is complete, write its output to:
```
refactors/refactor_N_<slug>/phase1_science_audit.md
```

If the refactor-science skill writes its own output file, copy or symlink it here. Then print:

```
Phase 1 complete. Audit written to refactors/refactor_N_<slug>/phase1_science_audit.md.

Key findings carried into Phase 2:
- [list the top 3-5 flags from the audit that are relevant to code structure]

Starting Phase 2 — Superficial Refactor (autonomous).
```

---

## Phase 2 — Antipattern Audit (autonomous)

**Invoke skill:** `skills/refactor/refactor-antipatterns/SKILL.md` (`refactor-antipatterns`)

Pass:
- The codebase path
- The science audit findings as pre-loaded context (so the antipattern pass is informed by the evaluation failures the audit found)

The skill will:
- Audit all 14 agentic antipatterns (AP-1 through AP-14)
- Check test gaps (AT-1 through AT-6 coverage)
- Produce a combined findings table — no code changes yet

When complete, write the findings table to:

```
refactors/refactor_N_<slug>/phase2_antipattern_findings.md
```

---

## Checkpoint — Findings Review (mandatory human gate)

Stop. Present the findings table to the user:

```
Phase 2 complete. Findings:

[paste the phase2_antipattern_findings.md table]

Phase 3 will apply all fixes — antipatterns + architectural restructuring.
Anything to exclude or deprioritise before Phase 3 begins?
If not, say "go" and Phase 3 starts.
```

**Do not proceed until the user responds.** Silence is not confirmation.

When the user confirms, proceed to Phase 3.

---

## Parallel Mode

### Parallel Analysis Block

Dispatch the following three agents **simultaneously in a single response** — do not wait for one before starting the others. Each agent receives only the context it needs (codebase path, user concern, its own skill file). They do not share context with each other at this stage.

**Agent 1 — Science Audit (autonomous)**

Invoke skill: `skills/refactor/refactor-science/SKILL.md`

Pass:
- The codebase path
- The user concern (if any)
- Instruction: **run in autonomous mode — skip all interactive steps (Step 0, user-reaction collection). Produce only the written audit output.**

Output: `refactors/refactor_N_<slug>/phase1_science_audit.md`

**Agent 2 — Antipattern Audit (autonomous)**

Invoke skill: `skills/refactor/refactor-antipatterns/SKILL.md`

Pass:
- The codebase path
- Instruction: run fully autonomously, no cross-context from Agent 1.

Output: `refactors/refactor_N_<slug>/phase2_antipattern_findings.md`

**Agent 3 — Performance Baseline (autonomous)**

Invoke skill: `skills/refactor/refactor-perf/SKILL.md`

Pass:
- The codebase path
- Instruction: **profile-only mode — run CPU and memory profiling on the primary entry point(s) with representative input. Do NOT apply any fixes. Produce only the baseline profile report.**

Output: `refactors/refactor_N_<slug>/phase_perf_baseline.md`

Wait until all three output files exist before proceeding.

---

### Parallel Synthesis — Unified Findings (mandatory human gate)

Read all three reports. Cross-reference them: do any antipatterns explain the profiling hotspots? Does the science audit flag the same structural area as the antipattern audit? Consolidate into a synthesis block and present it to the user:

```
Parallel analysis complete. Here is the unified synthesis across all three lenses:

## Top findings — Science Audit
- [top 3–5 flags, one line each, with severity]

## Top findings — Antipattern Audit
- [top 3–5 antipatterns by severity, one line each: AP-N — name — affected file]

## Top findings — Performance Baseline
- [top 2–3 hotspots: function/module — CPU% or memory — root cause hypothesis]

## Cross-references
- [any finding that appears in 2 or more lenses — these are the highest-priority items]

## Proposed execution order for Phase 3
1. [item — reason this must come first]
2. [item]
...

Phase 3 will apply all fixes in the proposed order.
Anything to exclude or reorder before Phase 3 begins?
If not, say "go" and Phase 3 starts.
```

**Do not proceed until the user responds.** Silence is not confirmation.

When the user confirms (or adjusts the order), proceed to Phase 3 with:
- `phase1_science_audit.md` as the science context
- `phase2_antipattern_findings.md` as the antipattern context
- `phase_perf_baseline.md` as the performance context
- The user's confirmed execution order as the sequencing constraint for Phase 3

---

## Phase 3 — Architectural Refactor (autonomous)

*Both Sequential and Parallel modes converge here.*

**Invoke skill:** `skills/refactor/refactor-structure/SKILL.md` (`refactor-structure`)

Pass:
- The codebase path
- The science audit findings (`phase1_science_audit.md`)
- The antipattern findings (`phase2_antipattern_findings.md`)
- The performance baseline (`phase_perf_baseline.md`) — if it exists (parallel mode only)
- The user's confirmation, any exclusions, and the agreed execution order from the checkpoint

The skill will:
- Apply module depth/seam/deletion-test lens
- Execute all fixes from the findings table (antipatterns + code smells)
- Apply KISS/DRY structural redesign where warranted
- Run `pytest tests/ -v` after each structural change

When complete, write:
```
refactors/refactor_N_<slug>/phase3_architecture.md
```

---

## Phase 4 — Data Migration (conditional)

**Run this phase only if Phase 3 changed the schema or semantics of data already stored in Cosmos DB, Blob Storage, or any persistent store.** If no stored data is affected, skip to Phase 5.

**Invoke skill:** `skills/refactor/refactor-data/SKILL.md` (`refactor-data`)

Pass:
- The affected container(s) or `'assess from codebase'`
- The Phase 3 architectural changes as context

The skill will classify the change, assess impact, cost-gate any LLM reprocessing, and execute migration with a 3-document sample before full scale.

When complete, write:
```
refactors/refactor_N_<slug>/phase4_data_migration.md
```

---

## Phase 5 — Test Verification (autonomous)

**Invoke skill:** `skills/sprint/test-run-agent/SKILL.md` (`test-run-agent`)

Pass:
- The project path
- The Phase 2 findings (AT-1 through AT-6 gap list) — so the runner can report which gaps are now covered

The skill will:
- Run the full test suite (`pytest tests/ -v`)
- Report how many AT-1→AT-6 gaps identified in Phase 2 are now covered
- Confirm nothing regressed

When complete, write:
```
refactors/refactor_N_<slug>/phase5_test_verification.md
```

---

## Phase 6 — Performance Optimization (conditional)

**Run this phase only if any of the following are true:**
- The science audit (Phase 1) flagged latency, cost, or throughput concerns
- The user's original concern mentioned "slow", "expensive", "high token usage", or similar
- Phase 2 antipattern fixes included AP-8 (N+1) or AP-11 (operation granularity) — profiling validates the fix
- The user explicitly requests a performance pass

**If none apply:** skip Phase 6 and proceed to the Final Report.

**Parallel mode note:** `phase_perf_baseline.md` already exists — pass it to the skill so it skips re-profiling and goes directly to applying optimisations.

**Invoke skill:** `skills/refactor/refactor-perf/SKILL.md` (`refactor-perf`)

Pass:
- The codebase path
- The refactor folder path — the skill reads `phase1_science_audit.md` and `phase3_architecture.md` automatically
- Instruction: called as Phase 6 of `refactor-army` — context from prior phases is pre-loaded

The refactor-perf skill will:
- Profile CPU and memory on the primary entry point(s) with representative input
- Apply targeted Python optimizations: vectorization, generators, caching, async I/O, data structure substitution, serialization reduction
- Produce a before/after performance delta

When complete, write:
```
refactors/refactor_N_<slug>/phase6_optimization.md
```

Then print:
```
Phase 6 complete. Optimization report: refactors/refactor_N_<slug>/phase6_optimization.md.
Net change: [summary line from refactor-perf output]

Proceeding to Final Report.
```

---

## Final Report

Write `refactors/refactor_N_<slug>/refactor_log.md`:

```markdown
# Refactor Log — refactor_N_<slug>
**Date:** YYYY-MM-DD
**Codebase:** <path>
**User concern:** <concern or "none">

## Phase 1 — Science Audit
[3-5 sentence summary of key findings]
Full report: phase1_science_audit.md

## Phase 2 — Antipattern Audit
[N antipatterns found, top 3 by severity]
Full findings: phase2_antipattern_findings.md

## Phase 3 — Architectural Refactor
[What was restructured and why]
Full report: phase3_architecture.md

## Phase 4 — Data Migration
[if run: strategy, N docs migrated; if skipped: note reason]
Full report: phase4_data_migration.md (if run)

## Phase 5 — Test Verification
[N tests passed, AT gaps closed]
Full report: phase5_test_verification.md

## Phase 6 — Performance Optimization
[if run: top bottlenecks addressed, before/after delta; if skipped: note reason]
[parallel mode: baseline was pre-computed — only delta from Phase 3 fixes is reported here]
Full report: phase6_optimization.md (if run)

## Net impact
- Code quality: [qualitative assessment]
- API economy: [token/cost change if applicable]
- Test coverage: [AT-1 through AT-6 gaps closed]
- Runtime performance: [before/after delta if Phase 4 ran]
- Outstanding risks: [anything not addressed]
```

Then print:

```
Agentic Refactor Army complete.

refactors/refactor_N_<slug>/
  phase1_science_audit.md
  phase2_antipattern_findings.md
  phase_perf_baseline.md    ← parallel mode only
  phase3_architecture.md
  phase4_data_migration.md  ← if Phase 4 ran
  phase5_test_verification.md
  phase6_optimization.md    ← if Phase 6 ran
  refactor_log.md
```

## Rules

- Never start Phase 2 before Phase 1 is complete and its output is written.
- Never start Phase 3 before the checkpoint has explicit user confirmation.
- Never skip the diff summary — it is the only human checkpoint in an otherwise autonomous pipeline.
- If the science audit reveals a fundamental design problem (wrong objective, wrong metric, wrong data), stop at the end of Phase 1 and surface it explicitly before proceeding. A broken pipeline should not be refactored — it should be redesigned. Escalate to the user.
- Phase 4 data migration (`refactor-data`) is conditional on whether stored data is affected — the skill handles the cost gate internally.
- Phase 6 performance optimization is conditional — only trigger it when one of its four conditions is met (cost/latency flagged, user mentions perf, AP-8/AP-11 were fixed, user requests it). Do not run by default.
- Do not create new refactor skills, SKILL.md files, or skill folders in the target repository being refactored. Refactor existing project code only.
