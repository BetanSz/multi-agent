# Skills Index

Single source of truth for all skills available in this project.

**Two locations:**
- `skills/` — custom skills (this folder, version-controlled)
- `.agents/skills/` — external skills installed via `npx skills` (updatable with `npx skills update`)

---

## Agent Army — Sprint Execution

| Skill | Path | Description |
|-------|------|-------------|
| **agentic-sprint-army** | `skills/sprint/agentic-sprint-army/` | **Main entry point** — `/agentic-sprint-army "description"` runs the full pipeline: brainstorm → interview → HITL → agents → sprint_log |
| **agentic-refactor-army** | `skills/refactor/agentic-refactor-army/` | **Refactor entry point** — `/agentic-refactor-army "path [— concern]"` runs: science audit (interactive) → antipattern + depth refactor (autonomous) → diff review checkpoint → deep architectural refactor (autonomous) → performance optimization (conditional, Phase 4); artifacts in `refactors/refactor_N_<slug>/` |
| **hitl-analyzer** | `skills/sprint/hitl-analyzer/` | **Pre-flight gate** — reads sprint file, verifies every human-required action works before agents start; blocks until 100% confirmed |
| **execute-sprint** | `skills/sprint/sprint-dag-executor/` | **Autonomous execution engine** — reads a confirmed sprint file, builds task DAG, dispatches agents (plan → code → review → test) in order, no human interaction except genuine blockers |
| plan-agent | `skills/sprint/plan-agent/` | Architect specialist: scoping, API design, implementation sequence |
| code-agent | `skills/sprint/code-agent/` | Implementation specialist: Pythonic, efficient, minimal footprint, stays with existing stack |
| review-agent | `skills/sprint/review-agent/` | 3-mode reviewer: review / fix / architectural-fix-with-test-gate — includes performance + best-practice analysis |
| test-generator-agent | `skills/sprint/test-gen-agent/` | L3 sprints: standard TDD tests + 6 agentic failure pattern tests (AT-1 silent failure visibility — break each argument and assert failure is observable; AT-2 idempotency; AT-3 interface contract with wrong dict shapes; AT-4 prompt regression snapshots; AT-5 threshold boundaries; AT-6 smoke). All external calls mocked — zero real API cost. |
| test-runner-agent | `skills/sprint/test-run-agent/` | L2/L3 sprints: runs existing + new tests, signals pass/fail to conductor, triggers code-agent retry on failure |
| **sprint-reporter** | `skills/sprint/sprint-reporter/` | **Post-sprint reporter** — reads all task output files in `sprints/sprint_N_<slug>/` after sprint-dag-executor completes and writes `sprint_N_log.md` with full visibility into agent decisions |
| **sprint-premortem** | `skills/sprint/sprint-premortem/` | **Final step** — prospective hindsight on the sprint's deliverables; classifies risks as Tigers, Paper Tigers, and Elephants; produces `sprint_N_premortem.md` |

---

## Superpowers — Structured development workflow
*Source: [obra/superpowers](https://github.com/obra/superpowers) · installed via `npx skills` · update with `npx skills update`*

| Skill | Path | Description |
|-------|------|-------------|
| using-superpowers | `.agents/skills/using-superpowers/` | Foundational protocol: always invoke skills first, 3-tier instruction hierarchy |
| brainstorming | `.agents/skills/brainstorming/` | Design-first: 9-step process, no implementation until design approved |
| writing-plans | `.agents/skills/writing-plans/` | Creates detailed TDD plans with atomic 2-5 min tasks |
| executing-plans | `.agents/skills/executing-plans/` | Executes plans step by step with safety gates |
| subagent-driven-development | `.agents/skills/subagent-driven-development/` | Fresh subagent per task + 2-stage review (spec then quality) |
| dispatching-parallel-agents | `.agents/skills/dispatching-parallel-agents/` | Delegate independent tasks to concurrent agents |
| using-git-worktrees | `.agents/skills/using-git-worktrees/` | Isolated workspaces for parallel agent work |
| systematic-debugging | `.agents/skills/systematic-debugging/` | Root cause investigation before any fix |
| test-driven-development | `.agents/skills/test-driven-development/` | Red-Green-Refactor, failing test before production code |
| requesting-code-review | `.agents/skills/requesting-code-review/` | Dispatch reviewer subagents with focused context |
| verification-before-completion | `.agents/skills/verification-before-completion/` | No completion claims without fresh verification evidence |
| finishing-a-development-branch | `.agents/skills/finishing-a-development-branch/` | 5-step branch completion: verify, detect env, execute, cleanup |

---

## Automation loop

| Skill | Path | Description |
|-------|------|-------------|
| ralph-loop | `.agents/skills/ralph-loop/` | Agent-driven dev loop: user stories → acceptance criteria → iterative agent verification |

---

## Azure — Microsoft official
*Source: [microsoft/azure-skills](https://github.com/microsoft/azure-skills) · 327K+ installs · installed via `npx skills`*

| Skill | Path | Description |
|-------|------|-------------|
| azure-ai | `.agents/skills/azure-ai/` | Azure AI services: Azure OpenAI, Cognitive Services, ML — patterns and SDK usage |
| azure-deploy | `.agents/skills/azure-deploy/` | Deploy to Azure: App Service, Functions, Container Apps, AKS |
| azure-prepare | `.agents/skills/azure-prepare/` | Azure environment setup: subscriptions, resource groups, CLI auth, prerequisites |
| azure-diagnostics | `.agents/skills/azure-diagnostics/` | Diagnose Azure issues: logs, metrics, alerts, Monitor, Application Insights |
| azure-storage | `.agents/skills/azure-storage/` | Azure Storage: blobs, queues, tables, files — SDK patterns and operations |
| azure-validate | `.agents/skills/azure-validate/` | Validate Azure configurations, policies, naming conventions, and deployments |

---

## Agile

| Skill | Path | Description |
|-------|------|-------------|
| backlog-management | `skills/agile/backlog-management/` | GitHub backlog end-to-end: create issues, triage, sprint plan, release notes — enforces label taxonomy and DoR |

---

## Architecture & Design

| Skill | Path | Description |
|-------|------|-------------|
| architecture-decision-records | `.agents/skills/architecture-decision-records/` | Write and maintain ADRs — 5 templates (MADR, lightweight, Y-statement, deprecation, RFC), lifecycle management |
| architecture-patterns | `.agents/skills/architecture-patterns/` | Clean Architecture, Hexagonal, DDD — Python-first code examples, directory structures, in-memory adapter testing |
| improve-codebase-architecture | `.agents/skills/improve-codebase-architecture/` | Surface architectural friction using depth/seam/leverage language; deepening opportunities with deletion test |

---

## Code Quality

| Skill | Path | Description |
|-------|------|-------------|
| code-review-excellence | `.agents/skills/code-review-excellence/` | Code review methodology — feedback techniques, severity labels, handling disagreements, language-specific patterns |
| receiving-code-review | `.agents/skills/receiving-code-review/` | How to receive review feedback — verify before implementing, technical pushback, no performative agreement |
| superficial-file-refactor | `.agents/skills/superficial-file-refactor/` | Surgical refactoring — 10 code smells with before/after, extract method, type safety, design patterns (external, installed via npx) |
| python-performance-optimization | `.agents/skills/python-performance-optimization/` | Profile and optimize Python — cProfile, memory_profiler, py-spy, list comprehensions, dict lookups, generators |

---

## Research

| Skill | Path | Description |
|-------|------|-------------|
| deep-research | `skills/research/deep-research/` | OpenAI o4-mini-deep-research: 10-20 min web-enabled research with prompt enhancement |
| find-skills | `skills/research/find-skills/` | Discovers and installs skills from skills.sh via `npx skills find` |

---

## AI Tools

| Skill | Path | Description |
|-------|------|-------------|
| prompt-master | `skills/ai-tools/prompt-master/` | Generates optimized prompts for 30+ tools (Claude, GPT, Cursor, Midjourney, etc.) |
| mcp-builder | `skills/ai-tools/mcp-builder/` | Full guide for building MCP servers (TypeScript preferred, 4-phase process) |

---

## Utility

| Skill | Path | Description |
|-------|------|-------------|
| **repo-init** | `skills/utility/repo-init/` | **Project bootstrapper** — folder structure, conda env, .gitignore, .env.example, CLAUDE.md, pyproject.toml; stack-aware (Python/Azure, FastAPI, TS); never overwrites existing files |
| **agentic-antipattern-audit** | `skills/refactor/refactor-antipatterns/` | **14-antipattern audit + test gap report** — AP-1 dead code through AP-14 inter-file bounce; AT-1→AT-6 test gap audit; produces a combined findings table with no code changes. Phase 2 of `agentic-refactor-army`. |
| **architectural-refactor** | `skills/refactor/refactor-structure/` | **Structural redesign** — module depth/seam/deletion-test lens, KISS/DRY principles, code smell catalog; authorized for large-scale changes (dissolve classes, merge files, reroute call graphs). Phase 3 of `agentic-refactor-army`. |
| **data-migration** | `skills/refactor/refactor-data/` | **Data migration protocol** — classify change (schema/logic/structural), impact assessment, cost gate for LLM reprocessing, 3 strategies (delete+reprocess, patch in place, dual-run+compare), 3-doc sample before full scale. Phase 4 of `agentic-refactor-army` (conditional). |
| **deep-scientific-refactor** | `skills/refactor/refactor-science/` | **Scientific review of pipelines and evaluation systems** — senior data scientist persona. Opens with a pipeline portrait: minimal, precise prose description of what the system actually computes, with inline [?] flags on dubious parts; user response collected but audit proceeds fully independently. Then three formal lenses: (1) data flow correctness; (2) evaluation soundness (metric validity, null inflation, circular evaluation, score calibration, threshold justification, baseline, statistical power analysis with N_min formula and cost-to-close); (3) output completeness. Abstracts away from implementation — reads logic, math, and scientific validity only |
| **optimization-refactor** | `skills/refactor/refactor-perf/` | **Python runtime performance audit** — profiles CPU and memory (cProfile, memory_profiler), identifies hot spots, applies targeted optimizations (vectorization, generators, caching, async I/O, data structure substitution). Run after `refactor-structure` when performance is a concern. Phase 6 of `agentic-refactor-army`. |
| agent-browser | `skills/utility/agent-browser/` | Browser automation agent |
| process-interviewer | `skills/sprint/sprint-design/` | Relentless interviewer: extracts complete process before building anything |
| api-documentation | `skills/utility/api-documentation/` | Document REST APIs in OpenAPI 3.0 — schemas, examples, auth, response codes |
| webapp-testing | `.agents/skills/webapp-testing/` | Playwright Python testing for web apps — decision tree, server lifecycle, selector patterns |

---

## How to update external skills

```bash
# Update all installed skills
npx skills update

# Update a specific skill
npx skills update brainstorming

# List all installed skills
npx skills list
```

## How to add a new skill from Bureau projects

Copy the skill folder into the appropriate category under `skills/`, e.g.:
```
skills/
  core/          — orchestration and multi-agent coordination
  research/      — information gathering
  ai-tools/      — AI APIs and model integration
  utility/       — refactoring, optimization, process design, browser
  other/         — domain-specific
```
