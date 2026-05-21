# multi-agent

A skills library and autonomous sprint execution system for Claude Code. Type `/agentic-army "description"` to run a full design-to-code sprint — brainstorming, human-in-the-loop review, then multi-agent execution with no further interruptions.

**Requires:** [Claude Code](https://claude.ai/code) (the CLI / VS Code extension). The slash commands do not work in other tools.

---

## Quick start

```
/agentic-army "build an API endpoint that does X"
```

This runs the full pipeline:

1. **Brainstorm** — design session, locked decisions
2. **Process interview** — extract requirements, eliminate ambiguity
3. **HITL gate** — verify every human-required prerequisite (credentials, Azure resources, git state) before any agent touches code
4. **Autonomous execution** — plan-agent → code-agent → review-agent → test-agent, dispatched in dependency order
5. **Sprint report** — full visibility into every agent decision
6. **Pre-mortem** — prospective risk analysis before merging

Sprint artifacts land in `sprints/sprint_N_<slug>/`.

---

## Using in another project

Create `.claude/commands/agentic-army.md` in your project:

```markdown
Read and follow: `../mutlit-agent/skills/core/launch-sprint/SKILL.md`
**Skill path resolution**: all skill paths are relative to `../mutlit-agent/`. Prepend `../mutlit-agent/` to any path that does not start with `/` or `../`.
**Project context**: sprint files and artifacts live in THIS project under `sprints/sprint_N_<slug>/`.
Apply to: $ARGUMENTS
```

Adjust the relative path to `mutlit-agent/` as needed.

---

## Skills catalog

See [skills/INDEX.md](skills/INDEX.md) for the full list.

**Two locations:**
- `skills/` — custom skills, version-controlled here
- `.agents/skills/` — external skills installed via `npx skills` (gitignored, install on each machine)

### Install external skills

```bash
npx skills update
```

This installs or updates all external skills (brainstorming, architecture patterns, refactor, azure-*, etc.).

### Core sprint pipeline

| Skill | Description |
|-------|-------------|
| `skills/core/launch-sprint/` | Entry point — orchestrates the full pipeline |
| `skills/core/hitl-analyzer/` | Pre-flight gate — blocks until every prerequisite is confirmed |
| `skills/core/execute-sprint/` | Autonomous execution engine — dispatches agents in DAG order |
| `skills/core/plan-agent/` | Architect: scoping, API design, implementation sequence |
| `skills/core/code-agent/` | Implementation: Pythonic, minimal footprint |
| `skills/core/review-agent/` | 3-mode reviewer: review / fix / architectural-fix-with-test-gate |
| `skills/core/test-generator-agent/` | TDD + 6 agentic failure pattern tests (AT-1 through AT-6) |
| `skills/core/test-runner-agent/` | Runs tests, signals pass/fail, triggers retry |
| `skills/core/sprint-reporter/` | Writes `sprint_N_log.md` after execution |
| `skills/core/sprint-premortem/` | Prospective risk analysis — Tigers / Paper Tigers / Elephants |

### Utility

| Skill | Description |
|-------|-------------|
| `skills/utility/repo-init/` | Bootstraps a new project (conda env, .gitignore, CLAUDE.md, folder structure) |
| `skills/utility/pipeline-refactor/` | Agentic antipattern audit (11 patterns) + architectural refactor + data migration |
| `skills/utility/data-science-audit/` | Scientific review of pipeline logic and evaluation methodology |

---

## Project structure

```
skills/
  core/           ← sprint pipeline agents
  utility/        ← repo-init, pipeline-refactor, data-science-audit, …
  research/       ← deep-research, fact-checker
  ai-tools/       ← prompt-master, openrouter, mcp-builder
  content/        ← audio-transcriber, humanizer, frontend-slides, decision-toolkit
  agile/          ← backlog-management
  INDEX.md        ← full skill catalog
.agents/skills/   ← external skills (gitignored — install with npx skills update)
sprints/          ← sprint files produced by /agentic-army
.claude/commands/ ← Claude Code slash command definitions
```
