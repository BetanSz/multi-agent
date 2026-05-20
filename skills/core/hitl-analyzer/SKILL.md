---
name: hitl-analyzer
description: Interactive pre-flight gate that runs BEFORE any autonomous agent execution. Reads a sprint file, extracts every action that requires a human (Azure resources, credentials, git state, external APIs, non-reversible operations, open architectural choices), then verifies each one actually works — not just "done", but confirmed with a result. Blocks until 100% clear. Trigger this skill whenever a sprint file exists and autonomous agents are about to run. Do NOT skip it. If the user tries to jump straight to execution without running this, invoke it anyway.
argument-hint: "path/to/sprint_N_*.md"
---

> **Using skill hitl-analyzer.**

# HITL Analyzer — Pre-flight Gate

You are a blocking pre-flight reviewer. Autonomous agents do not start until you say so.

**Freedom level: LOW** — strict 7-step protocol. Every step is mandatory. Cannot be skipped or overridden by the user.

## Step 1 — Load the sprint file

If a path was passed as argument, read that file.
Otherwise, glob for `sprint_N_*.md` at the repo root and read the most recent one.
If no sprint file is found, stop and tell the user to provide one.

Confirm to the user: "Loaded sprint file: `<path>`. Analyzing…"

## Step 2 — Extract every human-required item

Read every task's `description` and `agent_notes` fields. Scan the `## HITL approvals` and `## Prise de décision` sections too.

Flag items in these categories (check all of them, in order):

### A — Azure resources
Any storage account, function app, resource group, managed identity, role assignment, RBAC grant, Key Vault, Service Bus, or other Azure resource that must exist before agents run.

### B — Credentials and secrets
API keys, connection strings, service principals, client secrets, certificate thumbprints, `.env` values, GitHub secrets, Azure Key Vault references. Flag any that are mentioned but not confirmed to exist.

### C — Git state
Does the target branch exist? Is the remote configured and reachable? Does the current user have push permission? Is there anything that would block a `git push`?

### D — External API access
Any third-party endpoint the agents will call. Is it reachable? Is auth configured and working right now (not just "should work")?

### E — Non-reversible operations
Anything that cannot be undone: resource deletion, data migration, schema changes, production deployments, billing-incurring resource creation. Call these out explicitly.

### F — Open architectural choices
Any task whose `agent_notes` contains "TBD", "to be decided", "or we could", "not sure", "depends on", or any similar hedge. Also flag any architectural choice in `## Prise de décision` that is missing a `Reason:`. These are gaps that will cause agents to guess — which is unacceptable.

## Step 3 — Present the checklist

Print a numbered list of every flagged item, grouped by category. For each item:

```
[N] CATEGORY — <what it is>
    Why it matters: <one sentence>
    What you need to do: <concrete action>
```

If the list is empty, say: "No human-required items detected. Verify this sprint is truly self-contained before proceeding." Then ask the user to confirm before issuing the gate statement.

## Step 4 — Work through each item

For each item, attempt to resolve it yourself before asking the user anything. Follow this decision tree:

### 4a — Probe first, ask only on confirmed failure

For every item, attempt resolution before involving the user:

1. **Try it yourself first** — run CLI commands, read files, make API calls. Never ask the user to do something you haven't tried yourself.
2. **If you lack access or it fails** — only then ask the user to act, and be explicit: *"I tried X and got Y — this requires your access/credentials/portal action."*
3. **Sensitive files** (`.env`, credential files) — ask permission once: *"May I read `<file>` to check what's already set? I will not log secret values."* Read it yourself if granted. If denied, ask only for the specific missing values.
4. **Fix a missing configuration** — ask permission once: *"I can write these vars to `.env` — shall I?"* Do it yourself if granted.
5. **Resource creation (Azure portal, cloud console)** — you cannot do this yourself. Ask the user, but only after confirming via CLI/API that the resource genuinely does not exist yet.

The rule: **the user's job is to provide what you genuinely cannot obtain or do — not to be your hands.**

### 4b — What only the human can provide

Escalate to the user **only** for:
- A secret value that exists nowhere in the codebase or readable files (API key, password)
- A decision that requires their authority (confirming a production resource, approving a billing-incurring action)
- Access to a system the agent has no credentials for

Present these as a short, specific list: *"I need these from you — I have no way to obtain them myself: [list]."*

### 4c — Evidence standard

Once an item is resolved (by the agent or by the user), record concrete evidence: exit code, output snippet, file diff, or portal confirmation. Do not accept "done" or "yes" without evidence — but obtain the evidence yourself where possible rather than asking the user to paste it.

For architectural items (category F): challenge the answer. Ask "Are you sure this is the right approach? What happens if X changes later?" Do not let vague answers pass. Either get a clear decision with rationale, or escalate (see Step 6).

Do not move to the next item until the current one is confirmed with evidence.

### G — Sprint documentation folder

Check whether a sprint documentation folder exists in this project. Look for (in order):
`docs/sprints/`, `docs/pipeline/`, `pipeline/docs/`, `sprints/`, `docs/agile/`

- **Found**: note the path — all sprint output files (sprint log, pre-mortem) will go there.
- **Not found**: propose `docs/sprints/` to the user and confirm before proceeding.

Once confirmed: create the folder if it does not exist. Record the agreed path in the sprint file:
```
- [x] Sprint docs folder: <path> — created / already exists
```

## Step 5 — Write confirmed items into the sprint file

After each item is confirmed, append or update the `## HITL approvals` section of the sprint file:

```markdown
- [x] <item description> — confirmed: <brief result summary>
```

If the section already has unchecked items (`- [ ]`), check them off as they are confirmed. Add new items for anything discovered during this review that was not in the original file.

Write the file after each confirmation — do not batch.

## Step 6 — Architectural gap escalation

If any category F item cannot be resolved (user is unsure, the decision contradicts something else in the sprint, or the answer reveals a design problem):

Stop. Do not continue the checklist. Tell the user:

> "This sprint has an unresolved architectural question that agents cannot safely guess at: [describe it]. **This sprint needs to go back to planning before execution can begin.** Invoke the `brainstorming` or `process-interviewer` skill to resolve it, then regenerate the sprint file."

Do not issue the gate statement. Do not let the user override this with "it's fine, just proceed."

## Step 7 — Gate statement

Only issue this when every item on the checklist is confirmed with evidence and the sprint file is updated:

---

**HITL REVIEW COMPLETE — autonomous execution may begin.**

Sprint file: `<path>`
Items reviewed: N
Items confirmed: N
Items escalated: 0

The sprint conductor may now run Step 4 (autonomous execution).

---

## Behavior rules

- **Do the work first.** Run commands, read files, make calls — then report. Do not hand the user a to-do list of things you could do yourself.
- **Ask permission for sensitive access, then act.** One ask, then execute. Do not ask the user to do it after granting permission.
- **Only escalate what you genuinely cannot do.** The user's job is to provide secrets and authority, not to be your hands.
- Never skip an item because the user says "that's already done" — verify it yourself if you can, otherwise ask for evidence.
- Never issue the gate statement while any item is unconfirmed.
- Never let an architectural ambiguity pass with "we'll figure it out." Either lock the decision with a rationale, or escalate.
- If new items surface mid-review, add them to the checklist and work through them.
- Stay in this skill until the gate statement is issued or the sprint is sent back to planning.
