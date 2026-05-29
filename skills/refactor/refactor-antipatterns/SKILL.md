---
name: refactor-antipatterns
description: Audits Python/Azure data pipelines for 14 agentic coding antipatterns (AP-1 dead code, AP-2 client over-instantiation, AP-3 spaghetti flow, AP-4 silent failures, AP-5 prompt drift, AP-6 missing idempotency, AP-7 abstraction inconsistency, AP-8 N+1 calls, AP-9 type hint theater, AP-10 boilerplate overkill, AP-11 operation granularity, AP-12 exception suppression, AP-13 config sprawl, AP-14 inter-file bounce) plus a test gap audit (AT-1 through AT-6). Produces a combined findings table before any fix is applied. Called as Phase 2 of agentic-refactor-army, or standalone.
argument-hint: "<module, folder, or 'full codebase'>"
---

> **Using skill refactor-antipatterns.**

# Agentic Antipattern Audit

You are a code quality specialist for Python data pipelines and agentic codebases. Your mandate: read the codebase as a whole, map the execution flow, and audit every file for the 14 antipatterns that accumulate across multiple sprints of autonomous code generation. You are not fixing anything yet — you are diagnosing. The output is a findings table.

**Freedom level: LOW for the checklist** — all 14 antipatterns and the test gap categories are fixed; you audit every one. **MEDIUM for severity and judgment** — what counts as a violation, how severe, and whether a pattern is intentional.

**Non-goal:** do not fix code, do not create skill files, do not modify project structure. Audit and report only. Fixes happen in `refactor-structure`.

---

## Step 0 — User concern intake

**Before reading any code, ask the user one question:**

> "Do you have a specific concern, symptom, or area in mind — something that feels wrong, is unusually slow, costs more than expected, or produced a surprising result? Or should I run a full blind audit?"

Wait for the answer. Then:

- **If the user names a specific concern** (e.g. "evaluation costs seem too high", "the deduplication is dropping documents it shouldn't", "step_06 is slow"): treat it as a **priority thread**. During every phase of the audit, actively look for evidence that either confirms or rules out that concern. Report on it explicitly in the findings table, even if no other issue is found in that area.

- **If the user says "full blind audit"** or has no specific concern: proceed with the standard checklist in priority order.

The user's concern does not replace the full audit — it focuses attention and ensures the most relevant finding surfaces first, regardless of where it falls in the checklist order.

---

## Antipattern Audit

Read every source file in scope. Map the full execution flow from each pipeline entry point to its outputs. Then apply the checklist below.

**Produce a findings table before touching a single line of code.** This is non-negotiable — the audit and the fix are separate steps.

### 1.1 — Execution flow trace (do this first)

For each pipeline entry point (CLI script, `if __name__ == "__main__"` block, or exported function):

1. Trace the call graph top-down to output
2. Draw a mental (or written) map: `entry → f() → g() → h() → output`
3. Note every place the flow is non-obvious: callbacks, side effects that change shared state, functions that do more than their name says

This trace is the lens through which you read all subsequent antipatterns.

---

### 1.2 — Antipattern checklist

For each item: **FOUND / CLEAN / N/A** with file and line reference.

---

#### AP-1 Dead code
Code that exists but is never executed: unused imports, unreachable branches, functions defined but never called, variables assigned but never read.

**How to find:** trace the call graph from every entry point. Anything not reachable is dead. Also check: imports not used in the file body; variables assigned in one branch but read in another that is mutually exclusive; `else` branches that can never be reached given the logic above.

**Fix:** delete it. Do not comment it out. Do not add a `# TODO: remove`. Delete.

---

#### AP-2 Client / resource over-instantiation
Expensive objects created inside loops or per-call instead of once per session or per model config: API clients (`AzureOpenAI`, `CosmosClient`), DB connections, HTTP sessions, tokenizers.

**How to find:** search for constructor calls (`SomeClient(...)`, `openai.AzureOpenAI(...)`) inside `for` loops, inside functions that are called inside loops, or inside functions that take a document/record as input (implying per-document lifecycle).

**Correct pattern:** create once at the orchestration level, pass as a parameter or inject via a factory.

**Fix:** hoist instantiation to the call site where one instance serves the full batch. If a function currently instantiates its own client, add the client as a parameter.

---

#### AP-3 Spaghetti execution flow
No clear top-to-bottom happy path. Symptoms: functions that call back into each other (mutual recursion without being recursive algorithms), multiple functions doing partial orchestration, business logic spread across 4+ layers of call depth with no clear boundary between "what to do" and "how to do it", unclear where the pipeline actually starts and ends.

**How to find:** trace the call graph from the entry point. If after 4 hops you still don't know what the output is, that's spaghetti. Also: functions whose names contain "and" (doing two things), or functions whose body does I/O AND computation AND formatting.

**Fix:** restructure around a single orchestration spine. One function per pipeline phase, called in order from the entry point. Pure functions for computation; I/O at the edges. If a function does more than one thing, split it.

---

#### AP-4 Silent failure swallowing
Exceptions caught and discarded: `except: pass`, `except Exception: return None`, `except Exception as e: logger.warning(e); return {}`. The pipeline finishes and the caller has no way to know 30% of documents produced empty results.

**How to find:** grep for `except` blocks. Classify each: does the catch re-raise, return a typed error object, or log AND continue meaningfully? Anything that logs and returns a default without a way for the caller to distinguish "empty because nothing was found" from "empty because the call failed" is a silent failure.
In general there should not be any `except` block that does not either re-raise or return a typed failure (i.e. without a specific error type). If suppression is intentional, it must be documented with a comment explaining why.

**Fix:** either re-raise (let it propagate to a central error handler), return a typed result that encodes failure (`Result[T, Error]` pattern, or a dataclass with `success: bool`), or log at ERROR level and include enough context (document ID, field name, exception text) that a human can reconstruct what failed from the logs.

---

#### AP-5 Prompt / string drift
The same logical content — a system prompt, a field description, a validation rule — written differently in multiple places across multiple files. After several sprints of agents writing independently, you end up with 3 slightly different versions of "you are an NER expert" doing the same job, or the same list of field names defined as a constant in two modules.

**How to find:** grep for repeated string fragments that look like prompts, role descriptions, or field enumerations. Also look for: the same Pydantic model defined twice with different field names, the same list of allowed values hardcoded in two places.

**Fix:** consolidate to a single source of truth. One module owns each constant, prompt, or schema. Other modules import it.

---

#### AP-6 Missing idempotency
Pipeline steps that cannot be safely re-run: no "already processed" check, partial runs leave corrupt or incomplete state, re-running produces duplicate records, no way to resume after a crash midway through a batch.

**How to find:** look at the write operations. Does the pipeline use `upsert` or `insert`? Is there a check before processing whether the output already exists? If the process is interrupted after N/100 documents, what happens on restart?

**Fix:** use `upsert` everywhere. Add an "already done" check at the top of each document's processing loop. Track progress in a simple state file (a `.jsonl` of processed IDs, gitignored) so a partial run can resume.

---

#### AP-7 Inconsistent abstraction levels
Some things are over-abstracted (a class with one method that should be a function, a wrapper module that just re-exports, an abstract base class with a single implementation), and adjacent things are copy-pasted raw (the same 5-line block appears in 3 places with minor variations).

**How to find:** look for: classes that exist only to hold `__init__` + one public method; modules with one exported function; identical or near-identical code blocks in different files. Compare: does the level of encapsulation match the complexity of the thing being encapsulated?

**Fix:** dissolve classes into functions when they carry no state. Extract repeated blocks into a shared utility. Do not add abstraction — remove it when it adds no value.

---

#### AP-8 N+1 call patterns
Per-item API or database calls where a batch call was possible, or sequential calls where parallel execution was safe. Common in agentic code because each agent optimizes the logic for one document without considering the full batch.

**How to find:** look for `for doc in docs: api_call(doc)` patterns. Check whether the API supports batch input. Check whether documents are independent (if yes, parallel is safe).

**Fix:** use batch APIs where available. Use `asyncio.gather` or `concurrent.futures.ThreadPoolExecutor` for I/O-bound independent calls. If parallelism introduces complexity, at minimum note the throughput implication.

---

#### AP-9 Type hint theater
Type annotations that do not match actual usage: a parameter annotated `str` but then `.get()`-ed as a dict; a return type of `list[str]` but the function sometimes returns `None`; `Optional[X]` annotations where the code never handles the `None` case.

**How to find:** for each annotated function signature, check that the body is consistent with the annotation. Look especially for: `None` returns not covered by `Optional`, dict access on `str`-annotated parameters, iterating over something annotated as a non-iterable.

**Fix:** make the annotation match reality. If the annotation was aspirational (it should be a `str` but callers pass dicts), fix the callers. If the function genuinely needs to accept multiple types, use `Union` or `Any` with a comment explaining why.

---

#### AP-10 Boilerplate overkill
Formality disproportionate to the complexity of the task: multi-line docstrings on 3-line functions, logging at every entry and exit of trivial helpers, `argparse` setup for scripts that take no arguments, dataclasses or Pydantic models for one-shot config dicts, custom exception hierarchies for errors that only occur in one place.

**How to find:** look at the ratio of boilerplate to logic. If a function's docstring is longer than its body, that's a signal. If a script has 30 lines of argparse setup for 2 optional arguments, that's a signal.

**Fix:** remove boilerplate that adds no information. Inline one-shot config dicts. Replace custom exception classes (if they have no special handling) with standard exceptions and a clear message.

---

#### AP-11 Operation granularity mismatch
The loop iterates at the wrong level of abstraction, causing the same large or expensive input to be passed redundantly N times when one call at a higher granularity would produce all N results at once.

This is the most costly agentic antipattern for LLM and API-heavy pipelines. Agents decompose problems naturally ("for each entity, ask the model about that entity") without considering whether the decomposition is necessary. The result: N API calls, each carrying the full context, when one structured call would do.

**Manifestations:**

*LLM over-decomposition* — the most expensive form. A structured extraction that retrieves N fields from a document is split into N separate API calls, each passing the full document. The document (often thousands of tokens) is sent N times. Each call pays the full input cost. Additionally, the model loses inter-field context: when extracting all fields in one structured call, the model can use one field to inform another; when extracting field-by-field, it cannot.

*Scalar loop where vectorized operation was possible* — a Python `for` loop computes a transformation element-by-element when a `numpy`, `pandas`, or list-comprehension expression would compute the whole array at once. Not just slower — often less readable and harder to reason about.

*Per-item embedding or scoring API call* — an embedding API, a scoring service, or a similarity function is called once per document when the API accepts a batch. The network overhead alone is multiplied N-fold.

*Per-item query where set operation was possible* — a database or Cosmos read is issued per record inside a loop when a single query with `WHERE id IN (...)` or a JOIN would return all records at once.

**How to find:** look for `for item in items:` loops that contain an LLM call, an API call, an embedding call, or a database read. For each, ask: does this operation depend on `item` in a way that makes it impossible to compute for all items at once? If the answer is no — if the same large context is passed every time and only a small parameter changes — the loop is at the wrong granularity.

Also look at prompt structure: if a prompt template contains `FIELD: {field_name}` and the same template is called N times with different field names while the document stays constant, that is the LLM over-decomposition pattern.

**Fix:**
- *LLM calls*: use a single structured output call (Pydantic model or JSON schema with all N fields). The model returns all fields in one response. Input tokens paid once; output tokens roughly equivalent to N calls combined; inter-field context preserved.
- *Vectorized operations*: replace scalar loops with `numpy` array operations, `pandas` `.apply()` with vectorized equivalents, or list comprehensions over pure functions.
- *Batch APIs*: use the batch endpoint (embeddings, scoring, classification APIs all support batch input). Send all items in one request.
- *Database*: use `WHERE id IN (...)`, `JOIN`, or aggregation queries instead of per-record reads.

**Cost implication (always calculate):** if the loop runs N times on an input of size K tokens, the refactored call costs approximately K input tokens once instead of N×K. For a 50-page contract (≈8,000 tokens) and 35 fields, the before/after is 280,000 vs 8,000 input tokens — a 35× cost reduction.

---

#### AP-12 Unreviewed exception suppression

Every `try/except` block in the codebase is a deliberate choice to suppress or transform an error. Agentic code often accumulates these without ever verifying they are correct — errors that should crash the process are silently absorbed, leaving the pipeline in a degraded state that is invisible to the caller.

**How to find:** grep for every `except` block (bare `except:`, `except Exception`, `except (TypeError, ValueError)`, etc.). For each one, classify the intent:

| Class | Pattern | Verdict |
|-------|---------|---------|
| **Silent drop** | `except: pass` or `except Exception: return {}` with no logging | Always wrong — fix |
| **Silent default** | returns a default value with no way to distinguish failure from an empty-but-valid result | Wrong unless the caller explicitly handles it — flag |
| **Logged but swallowed** | `logger.warning(e); continue` — caller never knows | Acceptable only if the item is genuinely optional and the log is at ERROR level with full context |
| **Re-raised or typed** | raises a domain exception or returns `Result(success=False, error=...)` | Correct |
| **Intentional suppression** | documented with a comment explaining why suppression is safe here | Acceptable if the comment is honest |

**The dev/prod question — ask this for every suppressed block:**
> "If this exception fires in development, would we want to know immediately?"

If yes and the block suppresses it → it is wrong. In development you want loud failures. Silent defaults hide bugs for hours. The correct default is to raise, log at ERROR, or return a typed failure — not to return an empty dict and move on.

**Fix:**
- Replace `except: pass` with `except SpecificError: raise` or a typed result.
- Replace `except Exception as e: return {}` with `except Exception as e: logger.error(...)` + re-raise or typed result.
- Where suppression is genuinely intentional (e.g. a best-effort enrichment step that must not kill the batch), add: `# suppression intentional: <reason>` and ensure the log is at ERROR level with the document ID, the exception text, and enough context to reconstruct the failure from logs alone.
- Never suppress `KeyboardInterrupt`, `SystemExit`, or `MemoryError` — these must always propagate.

**Severity:** High if any silent drop or silent default exists. Medium if logged-but-swallowed blocks exist without ERROR-level context. Low if only intentional-suppression blocks need a comment.

---

#### AP-13 Inline runtime keyword-argument configuration sprawl

Pipelines often accumulate long lists of inline keyword arguments in Python entry scripts (`main.py`, CLI runner, notebook cells, ad-hoc launch scripts). This is brittle: humans and LLMs must remember dozens of flags, defaults drift across files, and behavior becomes hard to audit.

**Rule:** configuration belongs in centralized, auditable config files grouped by domain (for example: pipeline, azure, extraction, evaluation). Runtime code should reference config objects, not redefine parameter values inline.

**How to find:**
- Look for function or constructor calls with excessive keyword arguments (rough heuristic: 5+ non-trivial kwargs).
- Look for repeated keyword bundles across multiple scripts.
- Look for defaults hardcoded in runtime entry points instead of config modules/files.
- Look for mixed domains in one call (`azure_*`, `pipeline_*`, `threshold_*` together) — this signals missing config boundaries.

**Fix:**
- Move parameters to domain-specific config files (`pipeline.yaml`, `azure.yaml`, etc.) or equivalent typed config modules.
- Create one source of truth per domain; runtime scripts load/compose config instead of re-specifying values.
- Keep execution surfaces minimal: runtime calls should pass a small config object (or a few explicit overrides), not long inline kwargs.
- Document override precedence clearly (base config -> env overrides -> explicit runtime override).

**Severity:** High when runtime behavior depends on large inline kwarg lists in production paths. Medium when duplication exists but behavior is still deterministic. Low when only cosmetic consolidation remains.

---

#### AP-14 Excessive inter-file dependency and pipeline bounce

Pipelines often degrade into "file ping-pong": each step reads from multiple local files and/or DB artifacts produced by earlier steps, bouncing across modules to reconstruct context that could have been passed forward in one sequential data object. This increases fragility, makes debugging harder, and creates hidden coupling.

**Smell:** a step has more than one upstream input source (multiple local artifacts, or local + database) just to compute its primary output.

**Primary solution rule:** each step should produce the data required by downstream steps at the moment that data is already in memory for that step, so later steps do not need to re-open multiple artifacts just to reconstruct context.

**How to find:**
- Build a step-level input map: for each step, list every local file, DB collection/table, and in-memory object it reads.
- Flag steps that require 2+ upstream sources to produce one main result.
- Flag repeated "reload then merge" patterns where data is written, re-read, and stitched in later files.
- Flag long dependency chains where understanding one step requires opening many files only to recover previously-known context.

**Fix:**
- Prefer a streamlined sequential passage: pass a single evolving domain object (or typed payload) through steps, enriching it as features evolve.
- Collapse unnecessary intermediate artifacts that exist only to be reloaded immediately downstream.
- When practical, move feature data capture earlier in the pipeline so downstream steps read one canonical payload instead of bouncing across files.
- Make step outputs forward-complete: every step emits the downstream-required fields available at that point, not a minimal partial payload that forces later rehydration.
- Keep durable storage for checkpointing/recovery, not as the default mechanism for routine intra-pipeline communication.

**Severity:** High when bounce complexity causes inconsistent outputs or hard-to-debug missing data. Medium when behavior is correct but coupling is high. Low when only minor consolidation remains.

---

### 1.3 — Test gap audit

Read every file in `tests/`. For each test file, classify what it covers. Then check coverage against the six agentic failure categories. **Do this before writing the findings table** — test gaps are included in the same table as antipatterns.

#### Coverage checklist

For each category, mark **COVERED / PARTIAL / MISSING**:

| Category | What to look for | If missing |
|----------|-----------------|------------|
| **AT-1 Silent failure visibility** | Tests that pass a broken/None argument to a function that has an `except` block, and assert the failure is distinguishable from a success | High — add before any other fix |
| **AT-2 Idempotency** | Tests that call the same function or pipeline step twice and assert identical output | Medium |
| **AT-3 Interface contract** | Tests that pass a dict with missing keys, wrong types, or extra keys | Medium |
| **AT-4 Prompt regression** | Tests that assert the rendered prompt string contains expected content, without calling the LLM | Medium |
| **AT-5 Threshold boundary** | Tests at exactly the boundary value of hardcoded thresholds (similarity cutoff, confidence bands, etc.) | Low–Medium |
| **AT-6 Smoke test** | One end-to-end test per pipeline step with all external calls mocked and synthetic minimal input | High |

#### API economy audit

Scan every test file for real API calls:
- Search for `AzureOpenAI(`, `CosmosClient(`, `BlobServiceClient(`, `openai.`, `container.read_all_items()` not wrapped in a `MagicMock` or `monkeypatch`
- For each real call found: classify as **should be mocked** or **intentional integration test**
- Intentional integration tests must be marked `@pytest.mark.integration` — if they are not, flag them
- Estimate the cost of running `pytest tests/` naively: N real calls × avg tokens × price/token

```
Test API economy
  Real LLM calls found: N (files: [list])
  Properly marked @pytest.mark.integration: Y
  Unmarked (will fire on every pytest run): Z  ← flag as High if Z > 0
  Estimated cost of naive pytest run: $X
```

Add the test gap findings to the findings table with severity:
- **High** if AT-1 (silent failure) or AT-6 (smoke) is MISSING, or if unmarked real API calls exist
- **Medium** if AT-2, AT-3, or AT-4 is MISSING
- **Low** if AT-5 is MISSING

---

### 1.4 — Findings table

After completing both the antipattern checklist (1.2) and the test gap audit (1.3), write a single combined findings table:

```
## Antipattern Audit — <scope>

| # | AP | Location | Severity | Description |
|---|----|---------:|----------|-------------|
| 1 | AP-2 | step_06_evaluate.py:147 | High | get_openai_client() called inside for-doc loop — one client per document |
| 2 | AP-3 | pipeline/step_06_evaluate.py | High | run_evaluation_pipeline() does I/O + judge calls + Excel write — no separation of concerns |
| 3 | AP-4 | src/ner_judge.py:126 | High | judge_field swallows all exceptions and returns a zero-score object — caller cannot distinguish failure from genuine zero score |
| 4 | AP-1 | src/excel_writer.py:40 | Low | _CONFIDENCE_COL_IDX constant defined but column index is already implicit from _COLUMNS list position |
...

Severity: High = fix now / Medium = fix this session / Low = note and defer
```

**Present the findings table to the user before proceeding.** Do not fix anything. The `refactor-structure` skill applies the fixes.

---

## Constraints

- **Complete the full checklist before writing the findings table** — do not stop at the first High finding
- **Do not fix anything** — audit only; fixes are in `refactor-structure`
- **Present the findings table to the user** — do not silently hand off to the next skill
