# Skills Index

Single source of truth for all skills available in this project.

**Two locations:**
- `skills/` — custom skills (this folder, version-controlled)
- `.agents/skills/` — external skills installed via `npx skills` (updatable with `npx skills update`)

---

## Core — Multi-agent orchestration

| Skill | Path | Description |
|-------|------|-------------|
| **launch-sprint** | `skills/core/launch-sprint/` | **Main entry point** — `/launch_sprint "description"` runs the full pipeline: brainstorm → interview → HITL → agents → sprint_log |
| **hitl-analyzer** | `skills/core/hitl-analyzer/` | **Pre-flight gate** — reads sprint file, verifies every human-required action works before agents start; blocks until 100% confirmed |
| **execute-sprint** | `skills/core/execute-sprint/` | **Autonomous execution engine** — reads a confirmed sprint file, builds task DAG, dispatches agents (plan → code → review → test) in order, no human interaction except genuine blockers |
| orchestrate | `skills/core/orchestrate/` | Decompose task → assign agents → coordinate pipeline |
| plan-agent | `skills/core/plan-agent/` | Architect specialist: scoping, API design, implementation sequence |
| code-agent | `skills/core/code-agent/` | Implementation specialist: Pythonic, efficient, minimal footprint, stays with existing stack |
| review-agent | `skills/core/review-agent/` | 3-mode reviewer: review / fix / architectural-fix-with-test-gate — includes performance + best-practice analysis |
| test-generator-agent | `skills/core/test-generator-agent/` | L3 sprints: writes failing tests for new features before implementation is verified (TDD protocol) |
| test-runner-agent | `skills/core/test-runner-agent/` | L2/L3 sprints: runs existing + new tests, signals pass/fail to conductor, triggers code-agent retry on failure |
| spawn-agent | `skills/core/spawn-agent/` | Activates a focused agent with role + task + isolated context |
| synthesize | `skills/core/synthesize/` | Merges all agent outputs into the final deliverable |
| **sprint-reporter** | `skills/core/sprint-reporter/` | **Post-sprint reporter** — reads all `_army/outputs/` files after execute-sprint completes and writes `sprint_log.md` with full visibility into agent decisions |

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

## Research

| Skill | Path | Description |
|-------|------|-------------|
| deep-research | `skills/research/deep-research/` | OpenAI o4-mini-deep-research: 10-20 min web-enabled research with prompt enhancement |
| fact-checker | `skills/research/fact-checker/` | Systematic claim verification with TRUE/MOSTLY TRUE/FALSE rating scale |
| find-skills | `skills/research/find-skills/` | Discovers and installs skills from skills.sh via `npx skills find` |

---

## AI Tools

| Skill | Path | Description |
|-------|------|-------------|
| prompt-master | `skills/ai-tools/prompt-master/` | Generates optimized prompts for 30+ tools (Claude, GPT, Cursor, Midjourney, etc.) |
| openrouter | `skills/ai-tools/openrouter/` | Unified API for 400+ models with fallbacks, auto-routing, and streaming |
| mcp-builder | `skills/ai-tools/mcp-builder/` | Full guide for building MCP servers (TypeScript preferred, 4-phase process) |

---

## Content

| Skill | Path | Description |
|-------|------|-------------|
| audio-transcriber | `skills/content/audio-transcriber/` | Audio → Markdown via Faster-Whisper, generates meeting minutes |
| humanizer | `skills/content/humanizer/` | Removes 24 AI writing patterns, adds voice and personality |
| frontend-slides | `skills/content/frontend-slides/` | HTML presentations from scratch or PPTX conversion, zero dependencies |
| decision-toolkit | `skills/content/decision-toolkit/` | 9-step decision framework with HTML/MD/PDF output |

---

## Utility

| Skill | Path | Description |
|-------|------|-------------|
| file-organizer | `skills/utility/file-organizer/` | Intelligent folder cleanup, duplicate detection, suggests structure |
| agent-browser | `skills/utility/agent-browser/` | Browser automation agent |
| process-interviewer | `skills/utility/process-interviewer/` | Relentless interviewer: extracts complete process before building anything |

---

## Other — OpenClaw cherry-picks

### openclaw-dev
| Skill | Path | Description |
|-------|------|-------------|
| coding-agent | `skills/other/openclaw-dev/coding-agent/` | General coding agent skill |
| skill-creator | `skills/other/openclaw-dev/skill-creator/` | Meta-skill: creates new skills |
| github | `skills/other/openclaw-dev/github/` | GitHub operations |
| gh-issues | `skills/other/openclaw-dev/gh-issues/` | GitHub issue management |
| summarize | `skills/other/openclaw-dev/summarize/` | Content summarization |
| nano-pdf | `skills/other/openclaw-dev/nano-pdf/` | PDF reading and processing |
| session-logs | `skills/other/openclaw-dev/session-logs/` | Agent session logging |
| model-usage | `skills/other/openclaw-dev/model-usage/` | AI model usage tracking |
| gemini | `skills/other/openclaw-dev/gemini/` | Google Gemini integration |

### openclaw-productivity
| Skill | Path | Description |
|-------|------|-------------|
| notion | `skills/other/openclaw-productivity/notion/` | Notion workspace operations |
| obsidian | `skills/other/openclaw-productivity/obsidian/` | Obsidian vault operations |
| taskflow | `skills/other/openclaw-productivity/taskflow/` | Task management workflow |
| taskflow-inbox-triage | `skills/other/openclaw-productivity/taskflow-inbox-triage/` | Inbox triage automation |
| trello | `skills/other/openclaw-productivity/trello/` | Trello board operations |
| canvas | `skills/other/openclaw-productivity/canvas/` | Canvas/diagram creation |
| tmux | `skills/other/openclaw-productivity/tmux/` | Terminal multiplexer control |

### openclaw-communication
| Skill | Path | Description |
|-------|------|-------------|
| slack | `skills/other/openclaw-communication/slack/` | Slack messaging and channels |
| discord | `skills/other/openclaw-communication/discord/` | Discord bot interactions |

### openclaw-maintenance
| Skill | Path | Description |
|-------|------|-------------|
| openclaw-pr-maintainer | `skills/other/openclaw-maintenance/openclaw-pr-maintainer/` | PR and issue triage |
| openclaw-testing | `skills/other/openclaw-maintenance/openclaw-testing/` | Test selection and CI debugging |
| openclaw-docs | `skills/other/openclaw-maintenance/openclaw-docs/` | Documentation writing |
| openclaw-debugging | `skills/other/openclaw-maintenance/openclaw-debugging/` | Model/provider behavior debugging |
| codex-review | `skills/other/openclaw-maintenance/codex-review/` | Code review closeout |
| security-triage | `skills/other/openclaw-maintenance/security-triage/` | Security vulnerability triage |

### openclaw-extensions
| Skill | Path | Description |
|-------|------|-------------|
| browser-automation | `skills/other/openclaw-extensions/browser-automation/` | Browser control and web automation |
| wiki-maintainer | `skills/other/openclaw-extensions/wiki-maintainer/` | Wiki/knowledge base maintenance |
| tavily | `skills/other/openclaw-extensions/tavily/` | Tavily web search integration |
| prose | `skills/other/openclaw-extensions/prose/` | Open-prose language for agent workflows |

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
  content/       — writing, media, presentations
  utility/       — file ops, process design, browser
  other/         — domain-specific (openclaw-*)
```
