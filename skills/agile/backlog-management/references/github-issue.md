# GitHub Issue Template

> Use this template when creating a new issue from a user story. Fill in all sections before marking the issue as `status:ready`.

---

## User Story

As a **[specific user role]**, I want **[specific action]**, so that **[measurable business outcome]**.

> ⚠️ Avoid generic roles like "user" or "admin". Use specific roles: "authenticated consultant", "project manager", "anonymous visitor".

---

## Description

<!-- 3–5 sentences explaining the context: what problem this solves, what the current gap is, and why it matters now. -->

---

## Acceptance Criteria

### Scenario 1 — Happy path

```
Given [the user is in a valid state]
When  [the user performs the action]
Then  [the expected result occurs]
```

### Scenario 2 — Edge case

```
Given [a boundary condition]
When  [the user performs the action]
Then  [the system handles it gracefully]
```

### Scenario 3 — Error / negative case

```
Given [an invalid state or input]
When  [the user performs the action]
Then  [the system shows a clear error or falls back safely]
```

---

## Technical Notes

- **API changes**: <!-- e.g., POST /api/v1/items — new endpoint -->
- **Data model changes**: <!-- e.g., new column `is_archived BOOLEAN` on `items` table -->
- **Non-functional requirements**: <!-- performance, security, accessibility -->
- **Dependencies**: <!-- #123, #456 — must be merged first -->

---

## Definition of Ready

- [ ] User story statement written
- [ ] At least 3 acceptance criteria defined (happy path, edge case, error case)
- [ ] Technical notes complete
- [ ] Size estimate assigned (`size:X` label)
- [ ] Dependencies identified and linked
- [ ] Team has enough context to start without further clarification

---

## Labels

<!-- Assign from the standard taxonomy before moving to sprint -->

- `type:` — feature / bug / chore / debt
- `priority:` — high / medium / low
- `size:` — 1 / 2 / 3 / 5 / 8 / 13
- `status:ready` (once DoR checklist is complete)
