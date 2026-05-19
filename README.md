# multi-agent

Unified skills repository and multi-agent workflow system.

## Structure

```
.agents/skills/       ← external skills (installed via npx skills, updatable)
skills/               ← custom skills (version-controlled)
  ├── INDEX.md        ← master catalog of all skills
  ├── core/           ← multi-agent orchestration (orchestrate, plan-agent, code-agent, review-agent, spawn-agent, synthesize)
  ├── research/       ← deep-research, fact-checker, find-skills
  ├── ai-tools/       ← prompt-master, openrouter, mcp-builder
  ├── content/        ← audio-transcriber, humanizer, frontend-slides, decision-toolkit
  ├── utility/        ← file-organizer, agent-browser, process-interviewer
  └── other/          ← cherry-picked openclaw skills (dev, productivity, communication, maintenance, extensions)
```

## Update external skills

```bash
npx skills update
```

## Add a new skill from skills.sh

```bash
npx skills add <owner/repo> --skill <skill-name>
```

## Browse all skills

See [skills/INDEX.md](skills/INDEX.md) for the full catalog.
