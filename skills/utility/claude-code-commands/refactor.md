---
name: refactor
description: Systematically refactor code for clarity, maintainability, and correctness. Reads the target file(s), identifies issues, applies changes, and verifies nothing breaks. Scope is always explicit — no changes outside the files specified.
argument-hint: "<file or folder path> [focus: duplication|naming|complexity|all]"
---

# /refactor

Refactor code without changing behavior. Every change is traceable, scoped, and verified.

## Rules before touching anything

1. Read the file(s) fully before writing a single change
2. Run existing tests first — if they fail before you start, stop and report
3. Make one category of change at a time (don't mix renaming with restructuring)
4. Never change behavior — refactor only
5. Re-run tests after each category of change

## Core principle — readability is not optional

Simpler, clearer code is always preferred over clever code, as long as performance and correctness are preserved. When in doubt, choose the version a new team member can understand in 30 seconds.

**Intermediate variables and constants are your friend.** A well-named intermediate variable costs nothing at runtime and can turn an unreadable expression into self-documenting code:

```ts
// hard to read
if (user.roles.includes('admin') && Date.now() - user.lastLogin < 86400000 && !user.suspended) { ... }

// clear
const isAdmin = user.roles.includes('admin');
const loggedInRecently = Date.now() - user.lastLogin < MS_PER_DAY;
const isActive = !user.suspended;
if (isAdmin && loggedInRecently && isActive) { ... }
```

Use intermediate variables freely when they:
- Name the intent of an expression (not just repeat it)
- Break a long boolean condition into readable parts
- Make a multi-step computation follow like a sentence
- Replace a comment that explained what the code does

## What to look for (in priority order)

### 0. Readability first
Before looking for structural issues, ask: can I understand what this code does in one read?
- Expressions that require mental parsing → introduce named intermediates
- Conditions with 3+ clauses → split into named booleans
- Chained method calls longer than 3 steps → break into named steps
- Comments that say *what* the code does (not *why*) → the code itself should say what, the comment should say why

### 1. Duplication
- Repeated logic that should be a shared function
- Copy-pasted blocks with minor variations → parameterize
- Identical conditions checked in multiple places

### 2. Complexity
- Functions doing more than one thing → split them
- Deeply nested conditionals (>3 levels) → early returns or extracted predicates
- Long functions (>40 lines) → extract cohesive sub-functions
- Magic numbers/strings → named constants

### 3. Naming
- Variable names that don't say what the value is (`data`, `result`, `temp`, `x`)
- Functions named by implementation not intent (`processData` → `calculateMonthlyTotal`)
- Misleading names (name says one thing, code does another)
- Inconsistent naming conventions within the same file

### 4. Structure
- Dead code (unreachable branches, unused imports, unused variables)
- Unnecessary abstraction (indirection that adds complexity without value)
- Missing or wrong error handling (silent failures, swallowed exceptions)
- Overly defensive code that obscures the happy path

## Output format

After each category of changes:
```
## Refactor: <category>

### Changes made
- `file.ts:42` — extracted `calculateTotal()` from inline loop (was 12 lines)
- `file.ts:87` — renamed `d` → `dueDate`

### Why
<one sentence per change explaining the intent>

### Tests
<result of running tests>
```

## When to stop

- If tests fail after a change → revert that change, report it, continue with others
- If a refactor would require changing the public API or behavior → flag it, don't do it
- If the code has no tests → warn the user before making structural changes

## What NOT to do

- Do not add new features
- Do not change function signatures visible to callers without explicit approval
- Do not reformat code style (that's a linter/formatter job)
- Do not refactor files not listed in the arguments
