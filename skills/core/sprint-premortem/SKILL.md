---
name: sprint-premortem
description: Runs after sprint-reporter. Does a static analysis of the codebase produced this sprint against the project's stated objectives — not a sprint log summary. Reads key source files, data schemas, and 1-2 output samples. Applies prospective hindsight (Tiger / Paper Tiger / Elephant) to surface risks before they hit production. Produces sprint_N_premortem.md. Never runs code or tests.
argument-hint: "<sprint-N-topic>"
---

> **Using skill sprint-premortem.**

# Sprint Pre-Mortem

You are a senior engineer doing a pre-mortem. Your primary job is a **static analysis of the current codebase against the project's stated objectives** — not a summary of what happened during the sprint. Read the code that was written, understand what it actually does, and ask: *"Will this achieve the goal? What is most likely to fail in the next 14 days of real use?"*

**Freedom level: MEDIUM** — classification rules are strict (LOW); judgment on what counts as evidence and which risks are real requires experience (MEDIUM).

**Never run code. Never run tests. Never read entire datasets.** This is a reading exercise, not an execution exercise.

## The thought experiment

**First, read the project documentation** to establish what success looks like. Look for `README.md`, `CLAUDE.md`, `docs/objectives.md`, or equivalent. Identify the project's primary objective in one sentence — what is the system ultimately supposed to produce, for whom, and at what quality bar?

Then construct the scenario from that objective:

> *"It is 14 days after this sprint's output is being used. The project's stated objective — [X] — has failed. [Describe the most probable failure mode: the downstream system rejected the output, the data was wrong in a way that caused a business error, the quality bar was not met, the pipeline silently produced incorrect results.] What in this sprint's code caused it?"*

The scenario must be specific to this project's goal, not a generic production incident. "Something went wrong" is not a scenario — "the Dynamics import rejected 20% of records because project codes were hallucinated" is.

This framing forces you to read the implementation against what actually matters, not what the sprint tried to do.

## Input — what to read

### Primary (always read)
- **Project documentation** (`README.md`, `CLAUDE.md`, `docs/objectives.md`, or equivalent) — the overarching project goal; derive the pre-mortem scenario from this
- **The sprint file** (`sprint_N_<topic>.md`) — this sprint's scope, locked decisions, and constraints
- **Every source file produced or modified this sprint** — read the actual code and schemas
- **Data model / schema files** referenced in agent_notes — understand the shape of data being produced

### Secondary (bounded — read the minimum that gives concrete evidence)
- **1–2 sample output files or records** (e.g. 1 Cosmos document, 1 generated JSON) — enough to see what the code actually produces, not enough to read the whole dataset
- **`sprints/sprint_N_<slug>/sprint_N_log.md`** — autonomous decisions, bugs encountered, blocked items
- **`sprints/sprint_N_<slug>/task_*_review.md`** — review verdicts, 🔴🟡🟢 flags
- **`sprints/sprint_N_<slug>/status.md`** — BLOCKED entries and workaround resolutions

### Never read
- Entire collections, databases, or directories of output files
- All test results (scan the summary line only)
- Duplicate content — if you've already read the source, don't re-read a generated copy of it

**Token discipline**: if you find yourself reading more than 3-4 data sample files, stop — you are not doing static analysis, you are doing a data audit. The pre-mortem answers "is the code correct?" not "is every record correct?"

## Risk classification

### Tigers — Real risks
Evidence-backed. A concrete failure scenario exists in the code or data. Ignoring them would be negligent.

Signals from the codebase:
- A function that does not validate its inputs at a system boundary (user input, API response, DB read)
- Business logic that handles only the happy path — no fallback, no error case
- A schema field typed loosely (`str`) where the downstream consumer needs a specific format (number, date, code pattern)
- Two code paths that should produce consistent results but could diverge (e.g. two models extracting the same field differently, no reconciliation logic)
- An external dependency (API, service, container) assumed always available with no degradation path
- A cost or scale assumption that was never calculated (e.g. per-document token consumption × corpus size)

Also check sprint log signals: 🔴 blocking issues (fixed or not), BLOCKED entries resolved via workaround, autonomous decisions made under ambiguity.

### Paper Tigers — Look scary, aren't
Sound alarming on first read but are low-probability or low-impact on inspection.

Signals: 🟡 important issues that were cleanly fixed; risks that were explicitly mitigated in the code or prompts; concerns raised then validated by a test or sample output.

### Elephants — Unspoken concerns
The code works for what was tested. Something adjacent was never addressed and nobody named it.

Signals from the codebase and sprint log:
- The test corpus covers only one contract type / one scenario / one model
- `# TODO`, `# FIXME`, or `# HACK` comments left in production code
- A field or output goes from LLM → storage with no normalization or validation (raw string that downstream systems need to parse)
- The goal says "for downstream system X" but no check was made that the output format matches what X actually accepts
- Scope quietly reduced mid-sprint (a whole contract type, a model variant, a validation step dropped)
- A task that required 3x retries — what does that say about the underlying design?

## Tiger urgency (for software sprints)

| Urgency | Definition | Action |
|---------|------------|--------|
| **Sprint-blocking** | Must be fixed before this sprint's output is merged or used by other sprints | Create a fix task for the next immediate sprint; do not build on top of this |
| **Next-sprint** | Should be addressed in the next planned sprint | Add to WISHLIST or next sprint backlog |
| **Track** | Monitor; address if it escalates | Note in risk register |

## Process

1. Read the sprint file — internalize the goal and locked decisions.
2. Read every source file and schema produced this sprint — understand what the code actually does, not what it was supposed to do.
3. Read 1-2 sample outputs or records — does the code produce what the goal requires?
4. Read the sprint log (secondary) — note bugs, autonomous decisions, and workarounds.
5. List every candidate risk — do not classify yet. Ground each one in something you actually read.
6. Apply the thought experiment: which of these would actually cause the incident?
7. Classify each as Tiger, Paper Tiger, or Elephant.
8. For each Tiger, assign urgency and write a concrete mitigation.
9. For each Elephant, name it explicitly — the point is to say the unsaid.
10. Write `sprints/sprint_N_<slug>/sprint_N_premortem.md`.

## Output format

Write `sprints/sprint_N_<slug>/sprint_N_premortem.md`:

```markdown
# Pre-Mortem — Sprint N — <topic>
**Date:** YYYY-MM-DD | **Based on:** codebase + sprint_N_log.md + N agent output files

## Project objective
> "[One sentence from the project documentation describing what this system is ultimately supposed to produce and for whom.]"

## The scenario
> "It is 14 days after deployment. The objective above has failed: [one sentence describing the most probable concrete failure — specific to this project's goal, not a generic incident]."

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
     Otherwise: proposed /agentic-army based on risk patterns. -->
```

## Rules

- Every sprint-blocking Tiger must have a concrete mitigation and an owner (human or agent).
- Every Elephant must be explicitly named — vague acknowledgment defeats the purpose.
- Paper Tigers must state why they are not dangerous, not just that they aren't.
- If no risks are identified, that is itself a risk worth noting: *"No risks surfaced — is the scope small enough to warrant that confidence, or were risks not looked for honestly?"*
- Do not invent risks. Every item must trace back to something in the sprint outputs.
