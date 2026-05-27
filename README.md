# multi-agent

A skills library for Claude Code built around two autonomous pipelines: the **Agentic Sprint Army** for building features sprint by sprint, and the **Agentic Refactor Army** for cleaning up what several sprints of autonomous code produce.

**Requires:** [Claude Code](https://claude.ai/code) (the CLI / VS Code extension). The slash commands do not work in other tools.

---

## The two pipelines

### `/agentic-sprint-army` — Sprint Army

Use this to build things. Each invocation runs one full sprint: design → code → review → test → risk analysis, with a human-in-the-loop gate before agents touch any code.

```
/agentic-sprint-army "build an API endpoint that does X"
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
1. **Science audit** (interactive) — reads the codebase and describes precisely what it computes; flags mathematical/logical issues, evaluation gaps, and data flow problems
2. **Antipattern audit** (autonomous) — audits 14 agentic antipatterns and produces a findings table; no code changes yet
3. **Findings review checkpoint** — one human gate: review findings, exclude anything, then confirm before fixes begin
4. **Architectural refactor** (autonomous) — structural redesign, module boundaries, execution flow
5. **Data migration** (conditional) — if stored data schemas were affected
6. **Test verification** (autonomous) — full suite green, AT-1→AT-6 gaps closed
7. **Performance optimization** (conditional) — profiling + targeted fixes when cost/latency was flagged

Refactor artifacts land in `refactors/refactor_N_<slug>/`.

---

## Recommended workflow

```
sprint 1 → sprint 2 → sprint 3 → /agentic-refactor-army → sprint 4 → sprint 5 → …
```

Run the refactor army every few sprints, or whenever the codebase starts feeling hard to extend. The science audit catches problems that pure code review misses — wrong evaluation metrics, silent data drops, statistical power gaps.

---

## Using in another project

Create `.claude/commands/agentic-sprint-army.md` in your project:

```markdown
Read and follow: `../mutlit-agent/skills/sprint/agentic-sprint-army/SKILL.md`
**Skill path resolution**: all skill paths are relative to `../mutlit-agent/`. Prepend `../mutlit-agent/` to any path that does not start with `/` or `../`.
**Project context**: sprint files and artifacts live in THIS project under `sprints/sprint_N_<slug>/`.
Apply to: $ARGUMENTS
```

And `.claude/commands/agentic-refactor-army.md`:

```markdown
Read and follow: `../mutlit-agent/skills/refactor/agentic-refactor-army/SKILL.md`
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
| `skills/sprint/agentic-sprint-army/` | Entry point |
| `skills/sprint/hitl-analyzer/` | Pre-flight gate — conda env, credentials, Azure resources, git state |
| `skills/sprint/sprint-dag-executor/` | Autonomous execution engine — DAG dispatch |
| `skills/sprint/plan-agent/` | Architect: scoping, API design, implementation sequence |
| `skills/sprint/code-agent/` | Implementation: Pythonic, minimal footprint |
| `skills/sprint/review-agent/` | 3-mode reviewer: review / fix / architectural-fix-with-test-gate |
| `skills/sprint/test-gen-agent/` | TDD + 6 agentic failure pattern tests (AT-1 through AT-6) |
| `skills/sprint/test-run-agent/` | Runs tests, signals pass/fail, triggers retry |
| `skills/sprint/sprint-reporter/` | Writes `sprint_N_log.md` after execution |
| `skills/sprint/sprint-premortem/` | Prospective risk analysis |

### Refactor Army internals

| Skill | Description |
|-------|-------------|
| `skills/refactor/agentic-refactor-army/` | Entry point |
| `skills/refactor/refactor-science/` | Science audit — pipeline portrait, evaluation soundness, statistical power |
| `skills/refactor/refactor-antipatterns/` | 14 agentic antipatterns + test gap audit (AT-1→AT-6) — findings table only |
| `skills/refactor/refactor-structure/` | Depth/seam lens, KISS/DRY, code smells — applies all fixes |
| `skills/refactor/refactor-data/` | Cost gate + 3 migration strategies for schema/logic changes |
| `skills/refactor/refactor-perf/` | CPU/memory profiling + targeted Python optimizations |

### Utility

| Skill | Description |
|-------|-------------|
| `skills/utility/repo-init/` | Bootstraps a new project (conda env, .gitignore, CLAUDE.md, pyproject.toml) |

---

## Project structure

```
skills/
  core/           ← sprint and refactor pipeline orchestrators + agents
  utility/        ← repo-init, deep-pipeline-refactor, deep-scientific-refactor, …
  research/       ← deep-research, fact-checker
  ai-tools/       ← prompt-master, openrouter, mcp-builder
  content/        ← audio-transcriber, humanizer, frontend-slides, decision-toolkit
  agile/          ← backlog-management
  INDEX.md        ← full skill catalog
.agents/skills/   ← external skills (gitignored — install with npx skills update)
sprints/          ← sprint artifacts from /agentic-sprint-army
refactors/        ← refactor artifacts from /agentic-refactor-army
.claude/commands/ ← Claude Code slash command definitions
```
