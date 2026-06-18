# Skills Map & Dedupe Plan

_Goal: turn four overlapping folders into one coherent library that can power a controlled software-building loop._

Scanned on 2026-06-14 across the four mounted folders. Hashes (md5) were used to confirm true duplicates rather than guessing from names.

---

## 1. The four sources at a glance

| Folder | What it really is | Role | Keep as… |
|---|---|---|---|
| **`mutlit-agent`** | Your own aggregator: categorized local skills **+** a `skills-lock.json` that symlinks skills from 6 GitHub repos | The hub / integration point | **Canonical library** |
| **`skills/`** | A flat dump of 16 skills. 5 are byte-identical to ones already in `mutlit-agent`; ~11 are unique utilities | Raw source, partly already absorbed | Harvest, then retire |
| **`matt_skills`** | A full clone of `mattpocock/skills` (29 skills). `mutlit-agent` already pulls 7 of them via the lock file | Upstream source repo | Upstream mirror, not a parallel library |
| **`spec-kit`** | GitHub's Spec-Driven Development **framework** (not skills) — a command set + templates | Process layer, separate kind of thing | Keep separate; wrap what you use |

**Key fact that simplifies everything:** `mutlit-agent` is not a peer of the other three — it already _consumes_ them. Its `skills-lock.json` symlinks `diagnose`, `grill-me`, `grill-with-docs`, `improve-codebase-architecture`, `tdd`, `to-issues`, `to-prd` straight from `mattpocock/skills`, plus skills from `obra/superpowers`, `microsoft/azure-skills`, `wshobson/agents`, `addyosmani/web-quality-skills`, and `anthropics/skills`. So the consolidation isn't "merge four equals" — it's "promote the hub, harvest the rest into it."

---

## 2. Full inventory

### mutlit-agent — local skills (your own work)

| Category | Skills |
|---|---|
| `agile` | backlog-management |
| `ai-tools` | mcp-builder, prompt-master |
| `research` | deep-research, find-skills |
| `utility` | agent-browser, api-documentation, repo-init |
| `sprint` (multi-agent system) | sprint-army _(entry)_, sprint-executor _(DAG engine)_, plan-agent, code-agent, review-agent, test-gen-agent, test-run-agent, hitl-analyzer _(pre-flight gate)_, sprint-brainstorm, sprint-design, sprint-premortem, sprint-reporter |
| `refactor` (multi-agent system) | refactor-army _(entry)_, refactor-antipatterns, refactor-data, refactor-perf, refactor-science, refactor-structure |

### mutlit-agent — symlinked from GitHub (via skills-lock.json)

| Source repo | Skills |
|---|---|
| `mattpocock/skills` | diagnose, grill-me, grill-with-docs, improve-codebase-architecture, tdd, to-issues, to-prd |
| `obra/superpowers` | brainstorming, systematic-debugging, verification-before-completion, finishing-a-development-branch, receiving-code-review, requesting-code-review |
| `microsoft/azure-skills` | azure-ai, azure-deploy, azure-diagnostics, azure-prepare, azure-storage, azure-validate |
| `wshobson/agents` | architecture-decision-records, architecture-patterns |
| `addyosmani/web-quality-skills` | performance |
| `anthropics/skills` | webapp-testing |

### skills/ (flat collection)

agent-browser, audio-transcriber, claude-code-commands, decision-toolkit, deep-research, fact-checker, file-organizer, find-skills, frontend-slides, humanizer, mcp-builder, multi-agent-army _(a 6-skill plugin: orchestrate/spawn-agent/plan-agent/code-agent/review-agent/synthesize)_, openrouter, process-interviewer, prompt-master, seloger-scraper.

### matt_skills (mattpocock/skills)

| Group | Skills |
|---|---|
| engineering | diagnose, grill-with-docs, improve-codebase-architecture, prototype, tdd, to-issues, to-prd, triage, zoom-out, setup-matt-pocock-skills |
| productivity | grill-me, handoff, teach, write-a-skill, caveman |
| misc | git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit |
| personal | edit-article, obsidian-vault |
| in-progress | review, writing-beats, writing-fragments, writing-shape |
| deprecated | design-an-interface, qa, request-refactor-plan, ubiquitous-language |

### spec-kit (framework, not skills)

Command set: `/constitution` → `/specify` → `/clarify` → `/plan` → `/tasks` → `/analyze` → `/implement`, plus `/checklist` and `/taskstoissues`. Ships matching templates (spec, plan, tasks, constitution, checklist) and bash/powershell scripts.

---

## 3. Overlap map

**A. Exact duplicates — byte-identical (`skills/` ↔ `mutlit-agent`).** Safe to delete from `skills/`.

| Skill | In skills/ | In mutlit-agent |
|---|---|---|
| agent-browser | ✓ | utility/ |
| deep-research | ✓ | research/ |
| find-skills | ✓ | research/ |
| mcp-builder | ✓ | ai-tools/ |
| prompt-master | ✓ | ai-tools/ |

**B. Source-level duplicates (`matt_skills` ↔ `mutlit-agent` symlinks).** `mutlit-agent` already references these 7 from the same upstream repo, so the standalone clone is redundant _for these_: diagnose, grill-me, grill-with-docs, improve-codebase-architecture, tdd, to-issues, to-prd.

**C. Semantic duplicates — same job, different implementation.** Pick one each.

| Concept | Candidates |
|---|---|
| "Interview me into a complete plan" | `skills/process-interviewer` vs `mutlit-agent/sprint/sprint-design` vs `matt_skills/grill-me` |
| Multi-agent plan→code→review pipeline | `skills/multi-agent-army` vs `mutlit-agent/sprint/*` (your sprint army is the evolved version) |
| Architecture improvement | `matt_skills/improve-codebase-architecture` vs `wshobson/architecture-patterns` (symlinked) |

**D. Unique — only here, worth keeping.**

- **`skills/` uniques (~11):** audio-transcriber, claude-code-commands, decision-toolkit, fact-checker, file-organizer, frontend-slides, humanizer, openrouter, process-interviewer, seloger-scraper, multi-agent-army.
- **`matt_skills` uniques (not yet symlinked):** prototype, zoom-out, triage, handoff, teach, write-a-skill, caveman, plus the misc/personal/in-progress sets.
- **`mutlit-agent` uniques:** the entire sprint & refactor armies, backlog-management, api-documentation, repo-init, and all the azure/obra/wshobson symlinks.

---

## 4. Consolidation plan

The principle: **one canonical library (`mutlit-agent`), one source of truth for "what skill exists" (`skills-lock.json`), everything else either folds in or becomes a clearly-labelled upstream mirror.**

**Step 1 — Promote `mutlit-agent` to _the_ library.** It already has the category structure and the lock file. Nothing else becomes a place you "also look for skills."

**Step 2 — Harvest `skills/`, then retire it.**
Delete the 5 exact duplicates (group A). Move the ~11 uniques into `mutlit-agent` under sensible categories — most are general-purpose, so a new `utility/` or `general/` bucket fits (audio-transcriber, file-organizer, fact-checker, humanizer, frontend-slides, decision-toolkit, openrouter, seloger-scraper, claude-code-commands). Decide the two semantic clashes (process-interviewer vs sprint-design; multi-agent-army vs your sprint army) before moving. Once emptied, the `skills/` folder goes away.

**Step 3 — Demote `matt_skills` to upstream mirror.** Don't maintain it as a second library. For the missing high-value engineering skills you'll want in the loop — `prototype`, `zoom-out`, `triage`, `handoff` — add them to `skills-lock.json` so they're symlinked like the other 7, instead of living in a separate folder you have to remember. Keep the clone only as the local checkout the lock file resolves against.

**Step 4 — Keep `spec-kit` as a separate _process_ layer.** It isn't skills and shouldn't be flattened into the library. Either reference its commands as-is, or wrap the three you'll actually use (`/specify`, `/plan`, `/tasks`) as thin skills so they sit beside the others in `mutlit-agent`. Note that spec-kit's `/taskstoissues` and Matt's `to-issues` solve the same hand-off problem — choose one bridge into your issue tracker.

**Step 5 — Single index.** `mutlit-agent/skills/INDEX.md` already exists; after the moves, regenerate it so it lists every skill with one-line descriptions and its category. That index becomes the only map you (or an agent) consult.

**End state:** `mutlit-agent` = the library; `matt_skills` = upstream checkout behind the lock file; `skills/` = deleted; `spec-kit` = an adjacent process toolkit you pull 2–3 commands from.

---

## 5. What this sets up for the loop (next phase)

Once consolidated, the software-building loop has a clean palette to draw from, sitting on a control→automation gradient:

1. **Frame** (spec-kit): `/specify` → `/clarify` → `/plan` — heavy upfront rigor on _what_ to build.
2. **Slice** (Matt): `to-prd` → `to-issues` / spec-kit `/tasks` — break into grabbable vertical slices.
3. **Build, controlled** (Matt): `tdd` → `diagnose`, with `grill-me` / `zoom-out` as gates that keep _you_ in control.
4. **Delegate, when safe** (your army): hand a fully-specified, low-risk batch to `sprint-army` / `sprint-executor`, gated by `hitl-analyzer` (the human checkpoint).
5. **Verify** (obra/Matt): `review` / `verification-before-completion` / `requesting-code-review` before merge.

The tension to resolve in the design is exactly your phrase — _"controlled manner."_ Spec-kit and your army are the automation-heavy ends; Matt's skills are the control-heavy core. The loop keeps the inner cycle Matt-style and only escalates to the army for well-specified work behind a human gate.

> This document covers the **map + dedupe** you asked for first. The loop design in §5 is a sketch to be expanded next.
