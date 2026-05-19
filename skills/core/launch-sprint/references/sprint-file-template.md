# Sprint File Template

This is the contract between any calling project and the launch-sprint system. Any project that generates a sprint file must follow this structure. The conductor reads this file to execute the sprint.

## Template

```markdown
# Sprint N — <topic>

**Goal:** One-paragraph description of what this sprint builds.
**Date:** YYYY-MM-DD
**Quality level:** L1 | L2 | L3

---

## Tasks

- id: task-1
  description: What exactly this task does
  depends_on: []
  agent_notes: Any context the agent needs (files to touch, APIs to call, etc.)

- id: task-2
  description: ...
  depends_on: [task-1]
  agent_notes: ...

## HITL approvals

Actions the agents may perform without interrupting. Must be confirmed by user before execution starts.

- [ ] Create Azure Storage Account "name" in resource group "rg-xxx"
- [ ] Grant role "Contributor" to service principal "xxx" on resource group "rg-xxx"
- [ ] ...

## Prise de décision

Architectural and scope decisions locked before execution. Agents must not re-open these.

- Decision: ...
  Reason: ...

## Outputs

> Filled by agents after execution.

## WISHLIST

> Deferred ideas for future sprints — proposed by agents or human.
```

## Quality levels

| Level | Contract |
|-------|----------|
| **L1** | Feature built. LLM + human test after execution. No automated test requirement. |
| **L2** | Feature built. All pre-existing tests pass. No new tests written. |
| **L3** | New tests defined upfront (TDD-light). All new + existing tests pass before sprint is declared complete. |

## Rules for calling projects

- The sprint file must be placed at the root of the workspace Claude Code is running in, OR the path must be passed explicitly to the conductor
- All `depends_on` values must reference valid task `id` fields in the same file
- HITL approvals must be confirmed by the human before the conductor starts Step 4
- The `Prise de décision` section must not be left empty — even if it just says "No architectural constraints identified"
