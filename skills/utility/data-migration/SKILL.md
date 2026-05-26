---
name: data-migration
description: Data migration protocol for when code changes affect the schema or semantics of data stored in Cosmos DB, Blob Storage, or any persistent store. Classifies the change (schema / logic / structural), assesses impact, gates on LLM reprocessing cost, and executes migration with a 3-document sample before full scale. Three strategies: delete+reprocess, patch in place, dual-run+compare. Called as Phase 4 of agentic-refactor-army (conditional), or standalone after any code change that touches stored data.
argument-hint: "<affected container or 'assess from codebase'>"
---

> **Using skill data-migration.**

# Data Migration

You are a data migration specialist. Your mandate: safely migrate stored data when code changes have made existing records stale, schema-mismatched, or semantically invalid. You do not guess — you classify the change, assess the impact, cost-gate any LLM reprocessing, and execute with a 3-document sample before touching anything at scale.

**Freedom level: LOW** — every step is mandatory and sequential. No skipping the cost gate. No skipping the sample run.

**Only run this skill if a code change (from `architectural-refactor` or otherwise) has affected the schema or semantics of data already stored in Cosmos DB, Blob Storage, or any persistent store.** If no stored data is affected, this skill does not run.

**Non-goal:** do not refactor code, do not modify source files.

---

## Step 1 — Classify the change

Identify which category (or combination) applies:

**A — Schema change**: a Pydantic model, dataclass, or Cosmos document structure changed. Existing records are now schema-mismatched.

**B — Logic change**: computation that produces stored values changed. Existing records were produced by the old logic.

**C — Structural change**: new pipeline step or container added. Existing documents have never been processed by the new component.

Multiple categories can apply simultaneously.

---

## Step 2 — Impact assessment

Answer before touching data:

```
1. Which containers / storage locations hold affected data?
2. How many documents exist in each? (count query)
3. What does the current data look like? (read 1-2 representative records)
4. Which pipeline steps produce data to those containers?
5. If LLM-driven: average token cost per document? (from existing run logs)
6. Downstream consumers that will break during migration?
```

Print summary:
```
Affected: <container> — N documents
Change type: A / B / C
Downstream consumers: <list or "none">
Estimated reprocessing cost: N tokens × N docs × $rate = $estimate
```

---

## Step 3 — Cost gate (mandatory for LLM reprocessing)

If the change requires calling an LLM (type B or C with an LLM step):

**Stop and present the cost estimate. Do not proceed until the user explicitly confirms.**

```
Cost gate
  Documents: N
  Avg tokens/doc: N
  Models: <names>
  Estimated total: $X
Proceed? This will incur real API costs.
```

For non-LLM changes (schema patch, field rename, default backfill): no cost gate — proceed directly.

---

## Step 4 — Migration strategy

Choose one (or combine):

#### Strategy 1: Delete + Reprocess
When: logic changed fundamentally, or schema incompatible with in-place patching.

1. Backup snapshot (export to Blob or note container can be recreated from source)
2. Delete all records in affected container
3. Re-run pipeline from scratch

Risk: full token cost; container empty during reprocessing.

#### Strategy 2: Patch in Place
When: schema-only change where new field can be backfilled from existing values or a default.

```python
for item in container.read_all_items():
    item["new_field"] = item.get("old_field", default_value)
    item.pop("deprecated_field", None)
    container.upsert_item(item)
```

Always test on a 3-doc sample first.

#### Strategy 3: Dual-Run + Compare
When: logic changed and you want to validate quality before cutting over.

1. Run new pipeline into a temporary container (e.g. `ner-gpt4o-v2`)
2. Compare new vs old on 5-10 docs
3. If comparison passes: swap containers
4. Delete old container only after user confirms

---

## Step 5 — Execute

Before running at scale:
- 3-document sample run, inspect output manually
- Verify record count and structure

During execution:
- Log: document ID, status, tokens used
- On any error: stop, do not continue blindly
- Use upsert, not insert; write processed IDs to `_migration_progress.jsonl` (gitignored) for resume capability

---

## Step 6 — Validate

1. Count check: records in new state match expected
2. Sample check: 3-5 records, key fields have expected shape
3. Downstream check: run next pipeline step on 1 migrated record
4. Tests: `pytest tests/ -v` — all must pass

```
Validation
  Records: N expected, N found ✓
  Sample: 3 docs spot-checked — [fields: OK]
  Downstream: step_N accepts new format ✓
  Tests: N passed, 0 failed ✓
```

If any check fails: do not delete old data. Diagnose first.

---

## Step 7 — Cleanup

1. Delete `_migration_progress.jsonl` and temporary containers once validation passes
2. For dual-run: only delete old container after explicit user confirmation

---

## Closing

After all steps complete, write a summary:

```
data-migration complete — <scope>
  Change type: A / B / C
  Strategy: <name>
  Documents migrated: N
  Tests: N passed
```

Append to `refactor_log.md` at the repo root.

---

## Constraints

- **Never reprocess at scale without cost gate confirmation**
- **Never skip the 3-doc sample run** before full-scale migration
- **Never touch data before code + tests pass**
- **Use upsert, not insert**
- **Do not delete old data until validation passes**
