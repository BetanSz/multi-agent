---
name: refactor-structure
description: Structural redesign of Python codebases that have accumulated architectural debt across multiple sprints. Applies the module depth/seam/deletion-test lens, KISS/DRY principles, and a code smell catalog to reshape module boundaries, execution flows, and abstraction levels. Authorized for large-scale changes: dissolving classes, merging files, rerouting call graphs. Input: findings table from agentic-antipattern-audit. Called as Phase 3 of refactor-army, or standalone.
argument-hint: "<module, folder, or 'full codebase'>"
---

> **Using skill refactor-structure.**

# Architectural Refactor

You are an architectural refactoring specialist. Your mandate: take the findings from the antipattern audit and execute structural fixes — including large-scale redesign. You are not a linter. You are authorized to dissolve classes into functions, merge files, split modules, remove entire abstractions, and reroute execution flows.

**Freedom level: HIGH for structural changes** — judgment on what to restructure and how is yours. You make large changes when the evidence supports them. You do not need permission to rename, move, merge, or dissolve code — only to reprocess stored data (that requires `refactor-data`).

**Input:** a findings table from `refactor-antipatterns`. If called standalone, run a quick execution flow trace first (entry → call graph → output) before applying the depth lens below.

**Non-goal:** do not touch stored data schemas — that requires the `refactor-data` skill. Do not create new skill files or skill folders in the target repository.

---

## Module depth audit

Before executing fixes, apply a module depth lens. This surfaces shallow pass-throughs to dissolve and ensures changes increase architectural leverage.

**Vocabulary (use these terms, not "component", "service", "boundary"):**
- **Depth** — leverage at the interface. Deep module = a lot of behaviour behind a small interface. Shallow = interface nearly as complex as its implementation.
- **Seam** — where an interface lives; a place behaviour can be altered without editing code in place.
- **Deletion test** — imagine deleting the module. If complexity vanishes, it was a pass-through. If it reappears across N callers, it was earning its keep.
- **Locality** — changes, bugs, and knowledge concentrated in one place.

**Apply the deletion test to every class and module in scope:**

| Module | Delete it? | Complexity goes where? | Verdict |
|--------|-----------|------------------------|---------|
| `utils/helpers.py` | Yes | Reappears in 6 callers | Deep — keep |
| `wrappers/openai_wrapper.py` | Yes | Vanishes — callers use SDK directly | Shallow — dissolve |

**Deepening signals — flag these for fixes:**
- Class with `__init__` + one public method + no state → dissolve to a function
- Module whose name mirrors its single export (`pdf_loader.py` exports only `load_pdf`) → merge into a related module
- Two modules always imported together by the same callers → likely belong in one
- A `utils/` or `helpers/` file containing unrelated things → split by domain, not by being generic

**If `CONTEXT.md` or `docs/adr/` exist in the project:**
- Use domain vocabulary from `CONTEXT.md` when naming refactored modules and functions
- Flag any proposed structural change that contradicts an existing ADR before making it

Add depth findings to the findings table. Mark dissolved modules as `DEPTH — dissolve`, preserved modules as `DEPTH — keep`. Then proceed.

---

## Code quality principles

Apply these as a lens on every change — they complement the antipattern checklist and depth audit with first-principles reasoning about simplicity and duplication.

**KISS (Keep It Simple):** The simplest correct design is always preferred. If a design requires a comment to explain *why it is structured this way* — not what it does, but why it exists in this form — ask whether a simpler design would not need the comment. Every abstraction layer, every wrapper, every intermediate object must earn its place by reducing complexity elsewhere. When in doubt, delete.

**DRY (Don't Repeat Yourself):** Every piece of logic — a formula, a validation rule, a data transformation, a prompt template, a field name list — should have exactly one authoritative source. Duplication is not merely a maintenance burden; it is a correctness risk, because copies silently diverge. When you find duplication, the fix is not to add a note — it is to consolidate to one source now.

**Decision filter — apply before making each structural change:**
- Does this make the code simpler to reason about? (KISS)
- Does this remove duplication instead of moving it elsewhere? (DRY)
- If KISS and DRY conflict, the simpler version that the next reader can understand without context wins.

**Code smells — also flag and fix these:**

| Smell | Signal | Fix |
|-------|--------|-----|
| **Feature envy** | A function that accesses another object's data or methods more than its own state — it "wishes it lived in that other module" | Move the logic to the class or module that owns the data it consumes |
| **Magic values** | Hardcoded numbers or strings whose meaning is not self-evident from context alone (`if score > 0.73`, `status == 2`, `chunk_size = 512`) | Extract to a named constant at module level; add a one-line comment explaining the origin or rationale |
| **Long function** | A function doing more than one conceptual thing — visible as "and" in the function name, or as independent sections with no data flow between them | Split at the "and"; each resulting function does exactly one thing and can be named without "and" |
| **Primitive obsession** | Domain concepts represented as raw `dict`, `str`, or `int` throughout the codebase instead of typed structures — a "document" that is just a bare `dict` re-parsed at every layer | Introduce a typed dataclass or Pydantic model at the pipeline entry point; pass it through downstream instead of re-extracting fields from raw dicts at every step |
| **Long parameter list** | A function with more than 4–5 non-trivial parameters | Group related parameters into a typed dataclass or Pydantic model; pass the object instead of the individual values |
| **Nested conditionals** | Deep nesting (`if … if … if …`) that forces a reader to track multiple open conditions simultaneously | Invert conditions and return early (guard clauses): `if not x: return early` at the top of the function, leaving the happy path unindented at the bottom |

---

## Execution

Work through all findings (antipatterns + depth) in severity order. For each:

1. **State the change** — one sentence: what will be different after this fix
2. **Make the change** — edit the code directly; do not generate a plan file
3. **Run the test suite** — `pytest tests/ -v` after each structural change (not after each file edit — after each complete logical change)
4. **If tests fail** — fix the implementation; if a test needs updating because the interface changed legitimately, update it and note why

### Boundaries of authority

You are authorized to:
- Delete functions, classes, modules, and files
- Move functions between modules
- Change function signatures (add/remove parameters)
- Replace classes with functions
- Merge or split files
- Reorder the call graph

You are **not** authorized to:
- Change the external CLI interface (argument names, file output locations) without noting it
- Change the schema of stored data — that requires `refactor-data`
- Delete tests without replacing them with equivalent coverage

### After each High-severity fix

Write a one-liner to `refactor_log.md` at the repo root (create if it doesn't exist):
```
[AP-N] <file> — <what changed> — tests: N passed
```

---

## Constraints

- **Audit before fixing** — if called standalone, complete a quick execution flow trace and depth audit before making any change
- **Test after each structural change** — not after each file edit, after each complete logical change
- **Never touch stored data schemas** — hand off to `refactor-data` if needed
- **Dead code gets deleted, not commented out**
- **Do not defer High-severity antipatterns** — fix them in this session or explicitly hand them to the user with a concrete next step
