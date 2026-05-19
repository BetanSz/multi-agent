---
name: backlog-management
description: Manage a GitHub backlog end-to-end — create structured issues, triage and prioritize, plan sprints from a Projects board, and generate release notes. Enforces a consistent label taxonomy and Definition of Ready.
argument-hint: "create issue | triage | sprint plan | release notes"
---

> **Using skill backlog-management.**

# Backlog Management

Manage a GitHub backlog end-to-end: write structured issues, triage and prioritize, plan sprints from a GitHub Projects v2 board, and generate release notes from closed issues and merged PRs.

**Freedom level: MEDIUM** — enforces label taxonomy and DoR strictly (LOW); formats and prioritizes using judgment (MEDIUM).

## Operations

Specify the operation you want:

- `create issue` — Generate a complete, well-structured GitHub issue from a feature description
- `triage` — Review open issues, suggest labels and priorities
- `sprint plan` — Build a sprint backlog from a GitHub Projects v2 board
- `release notes` — Generate release notes for a milestone or date range

## Label Convention

Enforce this taxonomy. Create these labels in the target repo before use:

| Label | Purpose |
|-------|---------|
| `type:feature` | New functionality |
| `type:bug` | Defect or regression |
| `type:chore` | Maintenance, refactoring, configuration |
| `type:debt` | Technical debt reduction |
| `priority:high` | Must be in the next sprint |
| `priority:medium` | Important but can wait one sprint |
| `priority:low` | Nice to have |
| `status:ready` | Definition of Ready met — sprint-eligible |
| `status:blocked` | Cannot proceed — dependency or decision needed |
| `status:in-progress` | Actively being worked on |

## Story Sizing

Use Fibonacci story points: **1, 2, 3, 5, 8, 13**

- Issues > 8 points **must** be split before sprint planning
- Sizing is added as a label: `size:1`, `size:2`, `size:3`, `size:5`, `size:8`, `size:13`

## Definition of Ready (DoR)

An issue is sprint-eligible when:
- [ ] User story statement written ("As a … I want … so that …")
- [ ] At least 3 acceptance criteria in Given/When/Then format
- [ ] Size estimate assigned
- [ ] Dependencies identified and linked
- [ ] No blocking labels (`status:blocked`)

## Templates

See `references/` for ready-to-use starting points:
- `github-issue.md` — Full issue template (user story + acceptance criteria + DoR)
- `sprint-plan.md` — Sprint planning summary table
- `release-notes.md` — Release notes structure (technical + business versions)
