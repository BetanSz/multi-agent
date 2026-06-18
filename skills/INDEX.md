# Skills Index

The single source of truth for every skill in this library. If a skill is not listed here, it does not exist.

**Two locations:**
- `skills/` — local skills, version-controlled in this repo
- `.agents/skills/` — external skills resolved from `skills-lock.json` (gitignored; run `npx skills update` to install/refresh)

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

## Agile — `skills/agile/`

| Skill | Path | Description |
|-------|------|-------------|
| backlog-management | `skills/agile/backlog-management/` | GitHub backlog end-to-end: issues, triage, sprint plan, release notes; enforces label taxonomy and DoR |

## AI Tools — `skills/ai-tools/`

| Skill | Path | Description |
|-------|------|-------------|
| prompt-master | `skills/ai-tools/prompt-master/` | Generates optimized prompts for 30+ tools (Claude, GPT, Cursor, Midjourney, …) |
| mcp-builder | `skills/ai-tools/mcp-builder/` | Full guide for building MCP servers (TypeScript preferred, 4-phase process) |
| openrouter | `skills/ai-tools/openrouter/` | OpenRouter integration — unified access to many LLM providers via one API |

## Research — `skills/research/`

| Skill | Path | Description |
|-------|------|-------------|
| deep-research | `skills/research/deep-research/` | o4-mini-deep-research: 10–20 min web-enabled research with prompt enhancement |
| find-skills | `skills/research/find-skills/` | Discovers and installs skills from skills.sh via `npx skills find` |
| fact-checker | `skills/research/fact-checker/` | Verifies claims against sources; flags unsupported assertions |
| decision-toolkit | `skills/research/decision-toolkit/` | Structured decision-making frameworks + cognitive-bias encyclopedia + decision templates |

## Content — `skills/content/`

| Skill | Path | Description |
|-------|------|-------------|
| audio-transcriber | `skills/content/audio-transcriber/` | Transcribe audio files (Whisper and alternatives); install + transcribe scripts |
| humanizer | `skills/content/humanizer/` | Rewrites AI-sounding text into natural human prose |
| frontend-slides | `skills/content/frontend-slides/` | Generates HTML/CSS slide decks with style presets |

## Utility — `skills/utility/`

| Skill | Path | Description |
|-------|------|-------------|
| repo-init | `skills/utility/repo-init/` | Project bootstrapper — folders, conda env, .gitignore, .env.example, CLAUDE.md, pyproject.toml; stack-aware; never overwrites |
| agent-browser | `skills/utility/agent-browser/` | Browser automation agent |
| api-documentation | `skills/utility/api-documentation/` | Document REST APIs in OpenAPI 3.0 — schemas, examples, auth, response codes |
| file-organizer | `skills/utility/file-organizer/` | Organizes files and folders by rules |
| claude-code-commands | `skills/utility/claude-code-commands/` | Loose Claude Code command snippets (`perf-analyze`, `refactor`) — not a SKILL.md skill |
| seloger-scraper | `skills/utility/seloger-scraper/` | SeLoger real-estate scraper (`scraper.py`) — standalone script, not a SKILL.md skill |

---

## External skills — `.agents/skills/` (resolved from `skills-lock.json`)

Not committed. Install/refresh with `npx skills update`. Sources of truth: the lock file + upstream repos. Skills here are **read-only** — never edited (to customize one, "adopt" it: move it into `skills/` and drop it from the lock). Cross-references point at `.agents/skills/<name>/` directly — no bridge symlinks.

| Skill | Source repo |
|-------|-------------|
| architecture-decision-records | wshobson/agents |
| architecture-patterns | wshobson/agents |
| azure-ai · azure-deploy · azure-diagnostics · azure-prepare · azure-storage · azure-validate | microsoft/azure-skills |
| brainstorming · finishing-a-development-branch · receiving-code-review · requesting-code-review · systematic-debugging · verification-before-completion | obra/superpowers |
| diagnose · grill-me · grill-with-docs · improve-codebase-architecture · tdd · to-issues · to-prd | mattpocock/skills |
| performance | addyosmani/web-quality-skills |
| webapp-testing | anthropics/skills |

---

## Managing skills

```bash
npx skills update            # install / refresh all external skills from the lock file
npx skills update <name>     # refresh one
npx skills list              # list installed external skills
npx skills find <query>      # search skills.sh for new skills
```

**Adding a local skill:** create `skills/<category>/<identifier>/SKILL.md`, set frontmatter `name:` equal to the folder name, and add a row here. **Adding an external skill:** `npx skills add <owner/repo>` (writes to `skills-lock.json`), then add a row to the external table.
