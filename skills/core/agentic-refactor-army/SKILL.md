---
name: agentic-refactor-army
description: Orchestrates the full agentic refactor army pipeline — science audit (interactive) → antipattern + depth refactor (autonomous) → diff review checkpoint → deep architectural refactor (autonomous) → performance optimization (conditional, Phase 4). Produces a complete refactor log under refactors/refactor_N_<slug>/. Invoke via /agentic-refactor-army "path/to/codebase [optional concern]".
argument-hint: '"path/to/codebase" or "path/to/codebase — specific concern"'
---

> **Using skill agentic-refactor-army.**

# Agentic Refactor Army

Three-phase pipeline. One human checkpoint. No skipping phases.

**Freedom level: LOW for sequencing** — the three phases are mandatory and must run in order. **MEDIUM within each phase** — judgment is required on what counts as an antipattern, what warrants deep restructuring, and what is worth flagging vs. fixing silently.

## Default communication mode

Use this framing whenever you surface a problem, a decision, or a blocker to the user. Keep it short — target 6–10 lines. Any sub-skill (scientific-audit, agentic-antipattern-audit, architectural-refactor…) may override this with its own communication style when active.

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

Create it now. All artifacts from all three phases land here.

Confirm: `"Refactor folder: refactors/refactor_N_<slug>/. Starting Phase 1 — Science Audit."`

---

## Phase 1 — Science Audit (interactive)

**Invoke skill:** `skills/utility/deep-scientific-refactor/SKILL.md` (`deep-scientific-refactor`)

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

If the deep-scientific-refactor skill writes its own output file, copy or symlink it here. Then print:

```
Phase 1 complete. Audit written to refactors/refactor_N_<slug>/phase1_science_audit.md.

Key findings carried into Phase 2:
- [list the top 3-5 flags from the audit that are relevant to code structure]

Starting Phase 2 — Superficial Refactor (autonomous).
```

---

## Phase 2 — Antipattern Audit (autonomous)

**Invoke skill:** `skills/utility/agentic-antipattern-audit/SKILL.md` (`agentic-antipattern-audit`)

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

When the user confirms, proceed.

---

## Phase 3 — Architectural Refactor (autonomous)

**Invoke skill:** `skills/utility/architectural-refactor/SKILL.md` (`architectural-refactor`)

Pass:
- The codebase path
- The science audit findings (Phase 1 output)
- The antipattern findings (Phase 2 output) — so the refactor works from the confirmed findings table
- The user's confirmation and any exclusions from the checkpoint

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

**Invoke skill:** `skills/utility/data-migration/SKILL.md` (`data-migration`)

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

**Invoke skill:** `skills/core/test-runner-agent/SKILL.md` (`test-runner-agent`)

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

**If none apply:** skip Phase 4 and proceed to the Final Report.

**Invoke skill:** `skills/utility/optimization-refactor/SKILL.md` (`optimization-refactor`)

Pass:
- The codebase path
- The refactor folder path — the skill reads `phase1_science_audit.md` and `phase3_architecture.md` automatically
- Instruction: called as Phase 6 of `agentic-refactor-army` — context from prior phases is pre-loaded

The optimization-refactor skill will:
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
Net change: [summary line from optimization-refactor output]

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
- Phase 4 data migration (`data-migration`) is conditional on whether stored data is affected — the skill handles the cost gate internally.
- Phase 6 performance optimization is conditional — only trigger it when one of its four conditions is met (cost/latency flagged, user mentions perf, AP-8/AP-11 were fixed, user requests it). Do not run by default.
- Do not create new refactor skills, SKILL.md files, or skill folders in the target repository being refactored. Refactor existing project code only.
