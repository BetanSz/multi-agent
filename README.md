# multi-agent

A skills library for Claude Code built around two autonomous pipelines: the **Agentic Sprint Army** for building features sprint by sprint, and the **Agentic Refactor Army** for cleaning up what several sprints of autonomous code produce.

**Requires:** [Claude Code](https://claude.ai/code) (the CLI / VS Code extension). The slash commands do not work in other tools.

---

## The two pipelines

### `/agentic-army` — Sprint Army

Use this to build things. Each invocation runs one full sprint: design → code → review → test → risk analysis, with a human-in-the-loop gate before agents touch any code.

```
/agentic-army "build an API endpoint that does X"
```

Pipeline:
1. **Brainstorm** — design session, locked decisions
2. **Process interview** — extract requirements, eliminate ambiguity
3. **HITL gate** — verify every prerequisite (credentials, Azure resources, conda env, git state) before agents run
4. **Autonomous execution** — plan-agent → code-agent → review-agent → test-agent, dispatched in dependency order
5. **Sprint report** — full visibility into every agent decision
6. **Pre-mortem** — prospective risk analysis (Tigers / Paper Tigers / Elephants) before merging

Sprint artifacts land in `sprints/sprint_N_<slug>/`.

---

### `/agentic-refactor-army` — Refactor Army

Use this after several sprints have accumulated. Autonomous agents are good at producing working code quickly but tend to accumulate antipatterns over time — unnecessary API calls, redundant client instantiation, spaghetti execution flow, missing validation. Run this periodically to address that.

```
/agentic-refactor-army "path/to/codebase — optional specific concern"
```

Pipeline:
1. **Science audit** (interactive) — reads the codebase and describes precisely what it computes; flags mathematical/logical issues, evaluation gaps, and data flow problems; the user can flag concerns that become priority threads
2. **Superficial refactor** (autonomous) — audits 11 agentic antipatterns and applies fixes that don't change the architecture: client consolidation, prompt string extraction, batching redundant LLM calls, silent failure wrapping
3. **Diff review checkpoint** — one human gate: review what changed, revert anything, confirm before proceeding
4. **Deep architectural refactor** (autonomous) — structural redesign, module boundaries, execution flow; conditional data migration if stored data is affected

Refactor artifacts land in `refactors/refactor_N_<slug>/`.

---

## Recommended workflow

```
sprint 1 → sprint 2 → sprint 3 → /agentic-refactor-army → sprint 4 → sprint 5 → …
```

Run the refactor army every few sprints, or whenever the codebase starts feeling hard to extend. The science audit catches problems that pure code review misses — wrong evaluation metrics, silent data drops, statistical power gaps.

---

## Using in another project

Create `.claude/commands/agentic-army.md` in your project:

```markdown
Read and follow: `../mutlit-agent/skills/core/launch-sprint/SKILL.md`
**Skill path resolution**: all skill paths are relative to `../mutlit-agent/`. Prepend `../mutlit-agent/` to any path that does not start with `/` or `../`.
**Project context**: sprint files and artifacts live in THIS project under `sprints/sprint_N_<slug>/`.
Apply to: $ARGUMENTS
```

And `.claude/commands/agentic-refactor-army.md`:

```markdown
Read and follow: `../mutlit-agent/skills/core/launch-refactor/SKILL.md`
Apply to: $ARGUMENTS
```

Adjust the relative path to `mutlit-agent/` as needed for your folder structure.

---

## Skills catalog

See [skills/INDEX.md](skills/INDEX.md) for the full list.

**Two locations:**
- `skills/` — custom skills, version-controlled here
- `.agents/skills/` — external skills installed via `npx skills` (gitignored, install on each machine)

```bash
npx skills update   # install / update all external skills
```

### Sprint Army internals

| Skill | Description |
|-------|-------------|
| `skills/core/launch-sprint/` | Entry point |
| `skills/core/hitl-analyzer/` | Pre-flight gate — conda env, credentials, Azure resources, git state |
| `skills/core/execute-sprint/` | Autonomous execution engine — DAG dispatch |
| `skills/core/plan-agent/` | Architect: scoping, API design, implementation sequence |
| `skills/core/code-agent/` | Implementation: Pythonic, minimal footprint |
| `skills/core/review-agent/` | 3-mode reviewer: review / fix / architectural-fix-with-test-gate |
| `skills/core/test-generator-agent/` | TDD + 6 agentic failure pattern tests (AT-1 through AT-6) |
| `skills/core/test-runner-agent/` | Runs tests, signals pass/fail, triggers retry |
| `skills/core/sprint-reporter/` | Writes `sprint_N_log.md` after execution |
| `skills/core/sprint-premortem/` | Prospective risk analysis |

### Refactor Army internals

| Skill | Description |
|-------|-------------|
| `skills/core/launch-refactor/` | Entry point |
| `skills/utility/data-science-audit/` | Science audit — pipeline portrait, evaluation soundness, statistical power |
| `skills/utility/pipeline-refactor/` | 11 agentic antipatterns + architectural refactor + data migration |

### Utility

| Skill | Description |
|-------|-------------|
| `skills/utility/repo-init/` | Bootstraps a new project (conda env, .gitignore, CLAUDE.md, pyproject.toml) |

---

## Project structure

```
skills/
  core/           ← sprint and refactor pipeline orchestrators + agents
  utility/        ← repo-init, pipeline-refactor, data-science-audit, …
  research/       ← deep-research, fact-checker
  ai-tools/       ← prompt-master, openrouter, mcp-builder
  content/        ← audio-transcriber, humanizer, frontend-slides, decision-toolkit
  agile/          ← backlog-management
  INDEX.md        ← full skill catalog
.agents/skills/   ← external skills (gitignored — install with npx skills update)
sprints/          ← sprint artifacts from /agentic-army
refactors/        ← refactor artifacts from /agentic-refactor-army
.claude/commands/ ← Claude Code slash command definitions
```
