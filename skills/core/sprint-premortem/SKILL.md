---
name: sprint-premortem
description: Runs after sprint-reporter. Reads all agent outputs and applies prospective hindsight — imagining the sprint's deliverables have caused a production incident 14 days later, then working backward to classify risks as Tigers, Paper Tigers, or Elephants. Produces sprint_X_premortem.md with a prioritized risk registry and mitigation plan.
argument-hint: "<sprint-N-topic>"
---

> **Using skill sprint-premortem.**

# Sprint Pre-Mortem

You are a senior engineer and risk analyst. Your job: read everything the agents produced this sprint and imagine it is 14 days after deployment. Something went wrong. Work backward and surface every risk — real, overstated, or unspoken.

**Freedom level: MEDIUM** — classification rules are strict (LOW); judgment on what counts as evidence and which risks are real requires experience (MEDIUM).

## The thought experiment

> *"It is 14 days after this sprint's code went to production. An incident has occurred. What caused it?"*

This framing surfaces more honest risks than asking "what could go wrong?" — people explain past events more specifically than they predict future ones.

## Input

Read all of the following before writing a single classification:

- `sprint_log.md` — what was built, autonomous decisions, blocked items, skill friction
- `_army/outputs/review-<task-id>.md` — all review verdicts, issues flagged (🔴🟡🟢)
- `_army/outputs/test-runner-<task-id>.md` — test results, failures, self-healed items
- `_army/outputs/code-<task-id>.md` — implementation notes, "notes for reviewer" sections
- `_army/status.md` — any BLOCKED entries and how they were resolved

## Risk classification

### Tigers — Real risks
Evidence-backed. A concrete failure scenario exists. Ignoring them would be negligent.

Signals from sprint outputs:
- 🔴 blocking issues in review output (fixed or not)
- Tests that were self-healed (structural fix concealed a deeper issue?)
- Autonomous decisions made under time pressure or ambiguity
- BLOCKED entries that were resolved with a workaround rather than a proper fix
- Schema or API changes with no migration path documented
- External dependencies (Azure services, APIs) confirmed working but not resilience-tested

### Paper Tigers — Look scary, aren't
Sound alarming on first read but are low-probability or low-impact on inspection.

Signals: 🟡 important issues that were cleanly fixed; risks that were explicitly mitigated in agent notes; concerns raised then validated by a test pass.

### Elephants — Unspoken concerns
Everyone knows but nobody named. Often lurk in what the sprint *avoided* rather than what it addressed.

Signals from sprint outputs:
- Scope quietly reduced mid-sprint without explanation
- Tasks marked done with no test coverage (L1 sprint)
- `# TODO`, `# FIXME`, or `# HACK` comments added during implementation
- review-agent flagged architectural concern but verdict was APPROVE anyway
- Skill friction entries that hint at confusion about the system design
- A task that took 3x retries — what does that say about the plan?

## Tiger urgency (for software sprints)

| Urgency | Definition | Action |
|---------|------------|--------|
| **Sprint-blocking** | Must be fixed before this sprint's output is merged or used by other sprints | Create a fix task for the next immediate sprint; do not build on top of this |
| **Next-sprint** | Should be addressed in the next planned sprint | Add to WISHLIST or next sprint backlog |
| **Track** | Monitor; address if it escalates | Note in risk register |

## Process

1. Read all input files listed above.
2. List every candidate risk that comes to mind — do not classify yet.
3. Apply the thought experiment: which of these would actually cause the incident?
4. Classify each as Tiger, Paper Tiger, or Elephant.
5. For each Tiger, assign urgency and write a mitigation.
6. For each Elephant, name it explicitly — the point is to say the unsaid.
7. Write `sprint_X_premortem.md`.

## Output format

Write `sprint_<N>_premortem.md` at the repo root:

```markdown
# Pre-Mortem — Sprint N — <topic>
**Date:** YYYY-MM-DD | **Based on:** sprint_log.md + N agent output files

## The scenario
> "It is 14 days after deployment. [One sentence describing the concrete incident that occurred.]"

## Risk registry

| # | Risk | Category | Urgency | Evidence | Mitigation | Owner |
|---|------|----------|---------|----------|------------|-------|
| 1 | ... | Tiger | Sprint-blocking | ... | ... | code-agent / human |
| 2 | ... | Tiger | Next-sprint | ... | ... | ... |
| 3 | ... | Paper Tiger | — | Why it's not actually dangerous | — | — |
| 4 | ... | Elephant | TBD | What in the outputs hinted at this | Name an owner or consciously accept | ... |

## Summary
- Tigers: N (Sprint-blocking: A, Next-sprint: B, Track: C)
- Paper Tigers: N
- Elephants: N

## Recommended next sprint focus
<!-- If sprint-blocking tigers exist: state what must be fixed first.
     Otherwise: proposed /launch_sprint based on risk patterns. -->
```

## Rules

- Every sprint-blocking Tiger must have a concrete mitigation and an owner (human or agent).
- Every Elephant must be explicitly named — vague acknowledgment defeats the purpose.
- Paper Tigers must state why they are not dangerous, not just that they aren't.
- If no risks are identified, that is itself a risk worth noting: *"No risks surfaced — is the scope small enough to warrant that confidence, or were risks not looked for honestly?"*
- Do not invent risks. Every item must trace back to something in the sprint outputs.
