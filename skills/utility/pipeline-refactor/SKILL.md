---
name: pipeline-refactor
description: Manages architectural changes to Python/Azure data pipelines where existing data must be migrated or reprocessed. Covers change classification, impact assessment, cost gate (mandatory before any LLM reprocessing), migration strategy selection (delete+reprocess / patch-in-place / dual-run+compare), code changes, execution, and validation. Use when a schema change, logic change, or structural refactor makes stored data stale or inconsistent with the new pipeline.
argument-hint: "<what changed or what needs to change>"
---

> **Using skill pipeline-refactor.**

# Pipeline Refactor

You are a data pipeline architect. Your job: understand what changed, assess what data is now stale, estimate the cost of fixing it, choose the right migration strategy, execute it safely, and validate the result. You never reprocess data without a cost gate. You never cut over without a validation sample.

**Freedom level: MEDIUM** — change classification and strategy selection follow a fixed decision tree (LOW); judgment on sample size, cost thresholds, and validation criteria (MEDIUM).

## When to use this skill vs `/refactor`

| Situation | Use |
|-----------|-----|
| Internal code cleanup, rename, extract method — behavior unchanged, no stored data affected | `/refactor` (external skill) |
| Schema field added, removed, or renamed in a model that writes to Cosmos / Blob / DB | **This skill** |
| Scoring algorithm, prompt, or extraction logic changed — existing records are now computed differently | **This skill** |
| New pipeline step added that all existing documents must pass through | **This skill** |
| Switching models (e.g. gpt-4o → gpt-4.1) where you want to reprocess for comparison | **This skill** |

---

## Step 1 — Classify the change

Identify which category (or combination) applies:

### A — Schema change
A Pydantic model, dataclass, or Cosmos document structure changed: field added, removed, renamed, or retyped. Existing records in storage are now schema-mismatched with the new code.

Signals: changes to `*_schemas.py`, `settings.py` dataclasses, Cosmos document structure.

### B — Logic change
The computation that produces stored values changed: prompt updated, scoring rules altered, algorithm replaced. Existing records were produced by the old logic and are now incorrect by the new standard.

Signals: changes to `*_prompts.py`, `step_0N_*.py` pipeline steps, scoring functions.

### C — Structural change
New pipeline step, new container, new model added. Existing documents have never been processed by the new component.

Signals: new `step_0N_*.py`, new Cosmos container, new model variant added.

> Multiple categories can apply. A prompt fix (B) that also adds a new output field (A) is both.

---

## Step 2 — Impact assessment

**Read before touching code.** Answer these questions by probing the actual system:

```
1. Which containers / storage locations hold affected data?
2. How many documents exist in each? (point-read or count query)
3. What does the current data look like? (read 1-2 representative records)
4. Which pipeline steps produce data to those containers?
5. If LLM-driven: what is the average token cost per document? (read from existing records or prior run logs)
6. Are there downstream consumers of this data that will break during migration? (other pipeline steps, reports, Dynamics imports)
```

Print a short impact summary before proceeding:
```
Affected: <container/location> — <N> documents
Change type: A / B / C (or combination)
Downstream consumers: <list or "none identified">
Estimated reprocessing cost: <N tokens/doc × N docs × $rate = $estimate> (or "non-LLM, no cost">
```

---

## Step 3 — Cost gate (mandatory for LLM-driven reprocessing)

If the change requires calling an LLM (type B or C involving an LLM step):

**Stop here and present the cost estimate to the user before proceeding.**

Format:
```
Cost gate — reprocessing estimate
  Documents: N
  Avg tokens/doc: N (from existing run logs or sample)
  Models: <model names>
  Estimated total: N tokens × $rate = $X
  At current scale: $X
  At full corpus (if different): $Y

Proceed? This will incur real API costs.
```

Do not proceed to Step 4 until the user explicitly confirms. This is the only mandatory human gate in this skill.

For non-LLM changes (schema patch, field rename, adding a field with a default): no cost gate needed — proceed directly to Step 4.

---

## Step 4 — Choose migration strategy

Select based on the change type and user context:

### Strategy 1: Delete + Reprocess
**When:** Logic changed fundamentally (type B), or schema is incompatible with in-place patching, or you want a clean slate.

**Steps:**
1. Take a backup snapshot (export to Blob or note the container can be recreated from source)
2. Delete all records in the affected container (or drop and recreate the container)
3. Re-run the pipeline step(s) from scratch

**Risk:** Expensive (full token cost). Container is empty during reprocessing — downstream consumers see no data.

**Mitigation:** Use dual-run strategy if downstream consumers cannot tolerate empty data.

---

### Strategy 2: Patch in Place
**When:** Schema-only change (type A) where the new field can be backfilled from existing record values or with a default. No recomputation needed.

**Steps:**
1. Write a migration script that reads each record, adds/renames/removes fields, writes back
2. Run against a 3-doc sample first, inspect output
3. Run at full scale
4. Verify record count and spot-check 3-5 records

**Example (Python/Cosmos):**
```python
for item in container.read_all_items():
    # add new field with default
    item["new_field"] = item.get("old_field", default_value)
    # remove deprecated field
    item.pop("deprecated_field", None)
    container.upsert_item(item)
```

**Risk:** Low cost, but if the script has a bug it corrupts live data. Always test on a sample first.

---

### Strategy 3: Dual-Run + Compare
**When:** Logic changed (type B) and you want to validate quality before cutting over. You run the new pipeline alongside the old results, compare, then delete the old results once satisfied.

**Steps:**
1. Run new pipeline into a **temporary container** (e.g. `ner-gpt4o-v2`) — do not overwrite the current container
2. Compare new vs old results on a sample (5-10 docs): field by field, flag divergences
3. If comparison passes human review: swap containers (rename or update the pointer in code)
4. Delete old container

**Risk:** 2× token cost (old results still exist while new ones are produced). Requires temporary storage. But gives you a rollback path — old container still exists until you delete it.

---

## Step 5 — Code changes

Make code changes **before** touching data:

1. Update schemas (`*_schemas.py`) — all Pydantic models
2. Update pipeline step logic (`step_0N_*.py`) — prompts, functions, scoring
3. Update any downstream consumers that read the stored format
4. Run tests: `pytest tests/ -v` — all tests must pass before migration
5. If tests fail: fix the implementation, not the tests

Do not proceed to Step 6 with failing tests.

---

## Step 6 — Execute migration

Follow the chosen strategy from Step 4.

### Before running at scale:
- Always run on a **3-document sample** first
- Inspect output manually: does the data look correct?
- Check that the pipeline completed without errors
- Verify the record count is as expected

### During execution:
- Log progress: document ID, status, tokens used (if LLM)
- Write a running total to a local file or stdout — do not run silently
- On any error: stop, inspect, do not continue blindly

### Idempotency:
- Re-running should be safe — use upsert, not insert
- Track processed documents so a partial run can resume: write processed IDs to `_migration_progress.jsonl` (gitignored)

---

## Step 7 — Validate

After migration completes:

1. **Count check**: number of records in new state matches expected
2. **Sample check**: read 3-5 records, verify key fields have expected shape
3. **Downstream check**: run the next pipeline step on 1 migrated record to confirm it accepts the new format
4. **Test suite**: run `pytest tests/ -v` — all tests must still pass

Write a short validation summary:
```
Validation
  Records: N expected, N found ✓
  Sample: 3 docs spot-checked — [field X: OK, field Y: OK, new_field: OK]
  Downstream: step_05 accepts new format ✓ / ✗
  Tests: N passed, 0 failed ✓
```

If any check fails: **do not delete old data yet**. Diagnose first.

---

## Step 8 — Cleanup and document

1. Delete migration artifacts (`_migration_progress.jsonl`, temporary containers) once validation passes
2. Write a one-line entry to `_army/status.md` (or the sprint log if running inside a sprint):
   ```
   pipeline-refactor: <change description> — <N docs migrated> — validated ✓
   ```
3. If running in dual-run mode: only delete old container after explicit user confirmation

---

## Constraints

- **Never reprocess at scale without a cost gate confirmation** (Step 3)
- **Never touch data before code changes + tests pass** (Step 5 before Step 6)
- **Never skip the 3-doc sample run** before full-scale execution
- **Never delete old data** until Step 7 validation passes and user confirms (for dual-run)
- If a migration script fails mid-run: stop, report which documents were processed, ask before retrying

## Rollback

If the migration fails and old data needs to be restored:
- Strategy 1 (delete + reprocess): restore from the Blob snapshot taken in Step 4, or re-run the previous pipeline version from source documents
- Strategy 2 (patch in place): restore from a point-in-time backup (Cosmos continuous backup), or re-run previous pipeline version
- Strategy 3 (dual-run): old container was never deleted — simply revert the code pointer and the old container is still live
