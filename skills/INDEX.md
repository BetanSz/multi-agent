# Skills Index

The single source of truth for every skill in this repo. This repo is **the two armies** (sprint + refactor) and their direct support — nothing else. General-purpose skills live elsewhere and are pulled in on demand (see [../ROADMAP.md](../ROADMAP.md)).

**Two locations:**
- `skills/` — local skills, version-controlled in this repo
- `.agents/skills/` — external dependencies resolved from `skills-lock.json` (gitignored; run `npx skills update` to install/refresh)

## Naming convention (so names stop drifting)

One identifier per skill, used **verbatim** in all four slots: folder name = frontmatter `name:` = slash command (entry skills) = every cross-reference. Role is encoded by suffix:

- **`*-army`** — a macro conductor you launch (`/sprint-army`, `/refactor-army`)
- **`*-agent`** — a worker the army dispatches, one job each (`plan-agent`, `code-agent`, …)
- **plain name** — a phase/helper skill named for what it produces (`sprint-design`, `sprint-preflight`, `refactor-science`, …)

---

## Sprint Army — `skills/sprint/`

| Skill | Path | Role | Description |
|-------|------|------|-------------|
| **sprint-army** | `skills/sprint/sprint-army/` | macro | **Entry point** — `/sprint-army "description"` runs the full pipeline: brainstorm → design → preflight → autonomous execution → sprint log → premortem |
| sprint-brainstorm | `skills/sprint/sprint-brainstorm/` | phase | Design session; locks decisions before any build |
| sprint-design | `skills/sprint/sprint-design/` | phase | Relentless interviewer — turns an approved direction into a concrete sprint file (tasks, `depends_on`, quality level) |
| sprint-preflight | `skills/sprint/sprint-preflight/` | phase | Pre-flight HITL gate — verifies every human-required action (env, credentials, Azure, git state) works before agents start; blocks until 100% confirmed |
| sprint-executor | `skills/sprint/sprint-executor/` | engine | Autonomous execution engine — builds the task DAG, dispatches agents (plan → code → review → test) in waves, no human interaction except genuine blockers |
| plan-agent | `skills/sprint/plan-agent/` | agent | Architect: scoping, API design, implementation sequence |
| code-agent | `skills/sprint/code-agent/` | agent | Implementation: Pythonic, efficient, minimal footprint, stays with existing stack; never commits |
| review-agent | `skills/sprint/review-agent/` | agent | 3-mode reviewer: review / fix / architectural-fix-with-test-gate; includes performance + best-practice checks |
| test-gen-agent | `skills/sprint/test-gen-agent/` | agent | L3 sprints: TDD tests + 6 agentic failure-pattern tests (AT-1→AT-6); all external calls mocked |
| test-run-agent | `skills/sprint/test-run-agent/` | agent | L2/L3 sprints: runs existing + new tests, signals pass/fail, triggers code-agent retry on failure |
| sprint-reporter | `skills/sprint/sprint-reporter/` | phase | Reads all task outputs and writes `sprint_N_log.md` — full visibility into agent decisions |
| sprint-premortem | `skills/sprint/sprint-premortem/` | phase | Prospective hindsight on deliverables; classifies risk as Tigers / Paper Tigers / Elephants |

---

## Refactor Army — `skills/refactor/`

| Skill | Path | Role | Description |
|-------|------|------|-------------|
| **refactor-army** | `skills/refactor/refactor-army/` | macro | **Entry point** — `/refactor-army "path [— concern]"`; Sequential or Parallel mode → science audit → antipattern audit → review checkpoint → architectural refactor → data migration (cond.) → test verification → perf optimization (cond.); artifacts in `refactors/refactor_N_<slug>/` |
| refactor-science | `skills/refactor/refactor-science/` | phase | Scientific review — pipeline portrait, data-flow correctness, evaluation soundness (metric validity, null inflation, statistical power), output completeness |
| refactor-antipatterns | `skills/refactor/refactor-antipatterns/` | phase | 14-antipattern audit (AP-1→AP-14) + AT-1→AT-6 test-gap report; findings table only, no code changes |
| refactor-structure | `skills/refactor/refactor-structure/` | phase | Structural redesign — depth/seam/deletion-test lens, KISS/DRY, code-smell catalog; applies fixes |
| refactor-data | `skills/refactor/refactor-data/` | phase | Data-migration protocol — classify change, cost gate for LLM reprocessing, 3 strategies, 3-doc sample before full scale |
| refactor-perf | `skills/refactor/refactor-perf/` | phase | Python runtime performance audit — cProfile/memory_profiler, targeted optimizations (vectorization, generators, caching, async I/O) |

---

## Direct support

| Skill | Path | Description |
|-------|------|-------------|
| repo-init | `skills/utility/repo-init/` | Project bootstrapper — folders, conda env, .gitignore, .env.example, CLAUDE.md, pyproject.toml; stack-aware (Python/Azure); never overwrites. Run before the first sprint. |
| backlog-management | `skills/agile/backlog-management/` | GitHub backlog end-to-end: issues, triage, sprint plan, release notes; enforces label taxonomy and DoR |

---

## External dependencies — `.agents/skills/` (resolved from `skills-lock.json`)

Not committed. Install/refresh with `npx skills update`. Read-only — never edited. The two the armies actually use:

| Skill | Source repo | Used by |
|-------|-------------|---------|
| azure-ai · azure-deploy · azure-diagnostics · azure-prepare · azure-storage · azure-validate | microsoft/azure-skills | `sprint-executor` (Azure tasks) |
| brainstorming | obra/superpowers | `sprint-brainstorm` (visual companion) |

---

## Managing skills (the `npx skills` ≈ git workflow)

| Git | skills.sh equivalent |
|-----|----------------------|
| `git clone <repo>` | `npx skills add <owner/repo[@skill]>` — pull a skill (or all skills from a repo) into `.agents/skills/`, recorded in `skills-lock.json` |
| `git pull` | `npx skills update` — refresh all installed skills to latest from source |
| (list remotes) | `npx skills list` |
| (search GitHub) | `npx skills find <query>` — search skills.sh |

**Adding a local skill:** create `skills/<category>/<identifier>/SKILL.md`, set frontmatter `name:` = folder name, add a row here.
