---
name: launch-refactor
description: Orchestrates the full agentic refactor army pipeline — science audit (interactive) → superficial antipattern refactor (autonomous) → diff review checkpoint → deep architectural refactor (autonomous). Produces a complete refactor log under refactors/refactor_N_<slug>/. Invoke via /agentic-refactor-army "path/to/codebase [optional concern]".
argument-hint: '"path/to/codebase" or "path/to/codebase — specific concern"'
---

> **Using skill agentic-refactor-army.**

# Agentic Refactor Army

Three-phase pipeline. One human checkpoint. No skipping phases.

**Freedom level: LOW for sequencing** — the three phases are mandatory and must run in order. **MEDIUM within each phase** — judgment is required on what counts as an antipattern, what warrants deep restructuring, and what is worth flagging vs. fixing silently.

## Default communication mode

Use this framing whenever you surface a problem, a decision, or a blocker to the user. Keep it short — target 6–10 lines. Any sub-skill (deep-scientific-refactor, deep-pipeline-refactor…) may override this with its own communication style when active.

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

## Phase 2 — Superficial Refactor (autonomous)

**Invoke skill:** `skills/utility/deep-pipeline-refactor/SKILL.md` (`deep-pipeline-refactor`) — **Phase 1 only** (antipattern audit + fixes).

Pass:
- The codebase path
- The science audit findings as pre-loaded context (so the antipattern pass is informed by the evaluation failures the audit found)
- Instruction: **run Phase 1 of deep-pipeline-refactor only** — do not proceed to Phase 2 (deep restructuring) yet

The deep-pipeline-refactor skill will:
- Audit all 11 agentic antipatterns
- Check test gaps (AT-1 through AT-6 coverage)
- Apply fixes that do not change the architecture — renaming, deduplication, client consolidation, prompt string extraction, silent failure wrapping, AP-11 call batching

When Phase 1 of deep-pipeline-refactor is complete, write a diff summary:

```
refactors/refactor_N_<slug>/phase2_antipattern_fixes.md
```

Format:
```markdown
# Phase 2 — Antipattern Fixes

## Changes made
| File | Change | Antipattern |
|------|--------|-------------|
| src/pipeline.py | Consolidated 3 OpenAI clients → 1 | AP-2 client over-instantiation |
| pipeline/step_03.py | Batched 35 NER calls → 1 structured output call | AP-11 operation granularity |
| ... | ... | ... |

## Changes NOT made (deferred to Phase 3)
- [list structural issues that require deep refactor]

## API economy impact
- Before: ~280,000 input tokens / run
- After: ~8,000 input tokens / run
```

---

## Checkpoint — Diff Review (mandatory human gate)

Stop. Present the diff summary to the user:

```
Phase 2 complete. Here is what changed:

[paste the phase2_antipattern_fixes.md changes table]

Deferred to Phase 3 (deep refactor):
[list]

Anything to revert before Phase 3 begins?
If not, say "go" and Phase 3 starts.
```

**Do not proceed until the user responds.** Silence is not confirmation.

If the user asks to revert something:
1. Undo those specific changes
2. Update `phase2_antipattern_fixes.md` to mark them reverted
3. Re-present the table and ask again

When the user confirms, proceed.

---

## Phase 3 — Deep Architectural Refactor (autonomous)

**Invoke skill:** `skills/utility/deep-pipeline-refactor/SKILL.md` (`deep-pipeline-refactor`) — **Phase 2 and Phase 3**.

Pass:
- The codebase path
- The science audit findings (Phase 1 output)
- The antipattern fixes already applied (Phase 2 output) — so the deep refactor does not re-address what is already fixed
- The user's confirmation and any revert instructions from the checkpoint

The deep-pipeline-refactor skill will:
- Apply structural redesign (execution flow, abstraction levels, module boundaries)
- If stored data is affected: evaluate migration cost and strategy (Phase 3 of deep-pipeline-refactor)

When complete, write:
```
refactors/refactor_N_<slug>/phase3_architecture.md
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

## Phase 2 — Antipattern Fixes
[N antipatterns fixed, top 3 by impact]
Full diff: phase2_antipattern_fixes.md

## Phase 3 — Architectural Refactor
[What was restructured and why]
Full report: phase3_architecture.md

## Net impact
- Code quality: [qualitative assessment]
- API economy: [token/cost change if applicable]
- Test coverage: [AT-1 through AT-6 gaps closed]
- Outstanding risks: [anything not addressed]
```

Then print:

```
Agentic Refactor Army complete.

refactors/refactor_N_<slug>/
  phase1_science_audit.md
  phase2_antipattern_fixes.md
  phase3_architecture.md
  refactor_log.md
```

## Rules

- Never start Phase 2 before Phase 1 is complete and its output is written.
- Never start Phase 3 before the checkpoint has explicit user confirmation.
- Never skip the diff summary — it is the only human checkpoint in an otherwise autonomous pipeline.
- If the science audit reveals a fundamental design problem (wrong objective, wrong metric, wrong data), stop at the end of Phase 1 and surface it explicitly before proceeding. A broken pipeline should not be refactored — it should be redesigned. Escalate to the user.
- Phase 3 data migration (deep-pipeline-refactor Phase 3) is conditional on whether stored data is affected — follow the cost gate logic in the deep-pipeline-refactor skill.
- Do not create new refactor skills, SKILL.md files, or skill folders in the target repository being refactored. Refactor existing project code only.
