---
name: optimization-refactor
description: Python runtime performance audit for data pipelines. Profiles CPU and memory with cProfile and memory_profiler, identifies hot spots, and applies targeted Python-specific optimizations — vectorization, generators, caching, async I/O, data structure substitution, serialization reduction. Distinct from deep-pipeline-refactor (which audits structure) — this skill measures. Run after deep-pipeline-refactor when performance is a concern, or as Phase 4 of launch-refactor.
argument-hint: "<codebase path or entry point script>"
---

> **Using skill optimization-refactor.**

# Optimization Refactor

You are a Python performance engineer. Your mandate: **measure first, then fix.** You do not guess at bottlenecks — you profile, read the numbers, and act on what the data says.

**Freedom level: MEDIUM** — the profiling protocol and optimization catalog are fixed (LOW); which optimizations to apply, what counts as "good enough", and whether a slowdown is structural or algorithmic requires judgment (MEDIUM).

**Relationship to deep-pipeline-refactor:** that skill reads code and fixes architecture and antipatterns. This skill runs code and fixes measurable runtime characteristics — CPU time, memory allocation, throughput. Do not re-audit antipatterns (AP-1 through AP-14) here; that belongs in deep-pipeline-refactor Phase 1.

**Non-goal:** do not create new skill files, refactor architecture, or change data schemas. Optimize Python runtime behavior only.

---

## Step 0 — Context intake

**If called from `launch-refactor` (Phase 4):**
Read `phase1_science_audit.md` and `phase3_architecture.md` from the refactor folder. Extract:
- Any latency, cost, or throughput concerns flagged in the science audit
- Which antipatterns were already fixed (especially AP-8 N+1, AP-11 granularity) — do not re-address these; verify the fix helped
- Any new execution paths introduced by the architectural refactor — these are the primary targets for profiling

**If called standalone:**
Ask the user one question:
> "Is there a specific function, pipeline step, or observed symptom (slow, high memory, expensive) you want to start with — or should I profile the full entry point?"

Wait for the answer, then proceed.

---

## Phase 1 — Profile

### 1.1 — Identify entry points

List every runnable entry point in scope:
- `python -m <module>` scripts
- `if __name__ == "__main__"` blocks
- CLI entry points in `pyproject.toml` or `setup.cfg`
- Jupyter cells that execute the pipeline

Pick the **primary entry point** — the one that exercises the most code. Note any steps that make real API calls (LLM, DB, external HTTP) — these must be mocked or stubbed during profiling to isolate Python execution time from network latency.

---

### 1.2 — CPU profile

Run cProfile on the primary entry point with representative input (synthetic or a small real sample):

```bash
python -m cProfile -o profile_output.prof <entry_point.py>
python -c "
import pstats
from pstats import SortKey
s = pstats.Stats('profile_output.prof')
s.sort_stats(SortKey.CUMULATIVE)
s.print_stats(20)
"
```

**Read the output:**
- **Top 10 by `cumtime`** (cumulative time including callees) — these are the hot paths
- **Top 10 by `tottime`** (time in the function itself) — these are the actual bottlenecks
- Look for: repeated calls to the same function (N+1 at Python level), unexpected functions (string formatting, serialization, logging) dominating the hot list, call counts that are N× the document count

Produce a **CPU findings table**:

```
## CPU Profile — <entry point>

| Rank | Function | Calls | tottime (s) | cumtime (s) | Verdict |
|------|----------|------:|------------:|------------:|---------|
| 1 | step_04.process_doc | 2847 | 14.2 | 31.8 | N+1 — 2847 calls for 84 docs |
| 2 | json.dumps | 58,400 | 8.1 | 8.1 | Serialization hot spot — cache or reduce |
| 3 | re.compile | 420,000 | 3.2 | 3.2 | Compiled per call — move outside loop |
```

---

### 1.3 — Memory profile

For any function with suspicious allocation (loading full datasets, large lists/dicts built in memory), add `@profile` decorator and run:

```bash
python -m memory_profiler <entry_point.py>
```

If `memory_profiler` is not installed: `pip install memory-profiler`. Do not add to `requirements.txt` unless the user confirms.

**Look for:**
- Lines that allocate large objects (> 50 MB) inside loops
- Functions whose peak memory exceeds 2× the working set (indicates unnecessary copies)
- Lists built entirely in memory that could be generators
- Objects loaded once but never released (reference leaks)

Produce a **memory findings table**:

```
## Memory Profile — <function>

| Line | Code | MiB delta | Verdict |
|------|------|----------:|---------|
| 42 | records = [load(f) for f in files] | +840 MiB | Load all at once — use generator |
| 67 | embeddings = np.array(all_embeddings) | +380 MiB | OK — single allocation |
| 91 | results.append(deepcopy(doc)) | +210 MiB | Unnecessary deepcopy in loop |
```

---

## Phase 2 — Optimize

Work through findings in impact order (highest time/memory saving first). For each optimization:

1. **State it** — one sentence: what changes and what it saves
2. **Apply it**
3. **Run the test suite** — `pytest tests/ -v` after each logical change; if tests fail, fix or revert before continuing
4. **Note before/after** — estimated time or memory saved

Apply only what the profile data supports. Do not apply these speculatively.

---

### OPT-1 Vectorize scalar loops

A Python `for` loop applying a pure function element-by-element where a `numpy`, `pandas`, or list-comprehension expression would work.

**Signal:** the loop function appears in `tottime` top 10 with a high call count and a numeric payload.

```python
# Before
results = []
for val in values:
    results.append(val * 2 + 1)

# After
import numpy as np
results = (np.array(values) * 2 + 1).tolist()
```

Only apply when: data is numeric or homogeneous, the function has no side effects, and the input size justifies numpy overhead (> ~1000 elements).

---

### OPT-2 Generator pipeline for sequential processing

A pipeline that builds full intermediate lists between steps when the intermediate data is not needed in memory all at once.

**Signal:** large list allocated at step N, iterated at step N+1, then discarded — visible as back-to-back large allocations in memory profile.

```python
# Before
records = load_all_records()           # 500k items in memory
filtered = [r for r in records if r['score'] > 0.5]
processed = [transform(r) for r in filtered]
write_all(processed)

# After
def pipeline(path):
    for record in stream_records(path):    # generator
        if record['score'] > 0.5:
            yield transform(record)

write_all(pipeline(path))
```

Only apply when: records are independent, order is preserved, and downstream code handles iterables.

---

### OPT-3 Memoization / result caching

A pure function called many times with the same arguments — typically a config lookup, a token computation, a repeated regex compile, or an embedding for a repeated string.

**Signal:** the function appears repeatedly in `tottime` with a small unique argument space (same call counts as document count but fewer distinct argument values).

```python
import re
from functools import lru_cache

# Before — re.compile called inside loop
def extract_entities(text, pattern_str):
    pattern = re.compile(pattern_str)   # compiled every call
    return pattern.findall(text)

# After
@lru_cache(maxsize=128)
def _compile(pattern_str: str):
    return re.compile(pattern_str)

def extract_entities(text, pattern_str):
    return _compile(pattern_str).findall(text)
```

Only apply when: the function is pure (same inputs → same outputs, no side effects), argument space is bounded, and result is deterministic.

---

### OPT-4 Async I/O for independent network calls

Multiple sequential HTTP/API calls that are independent of each other — documents processed one-by-one when they could be parallelized with `asyncio`.

**Signal:** `cumtime` dominated by I/O wait (functions like `requests.get`, `openai.completions.create`, `container.read_item` rank high), `tottime` for those same functions is near zero (time is in C/network, not Python).

```python
import asyncio

async def process_all(docs):
    tasks = [process_one(doc) for doc in docs]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

Add a semaphore if rate limiting is a concern:

```python
sem = asyncio.Semaphore(10)  # max 10 concurrent

async def process_one_limited(doc):
    async with sem:
        return await process_one(doc)
```

Only apply when: the API supports concurrent requests within rate limits, and documents are independent.

---

### OPT-5 Data structure substitution

Using the wrong data structure for the access pattern — `list` membership test in a hot path where a `set` or `dict` would be O(1).

**Signal:** `list.__contains__` or similar linear scan in top 10 `tottime`.

```python
# Before — O(n) per lookup
processed_ids = []
if doc_id in processed_ids:   # list scan
    ...

# After — O(1) per lookup
processed_ids = set()
if doc_id in processed_ids:   # hash lookup
    ...
```

Also check: `dict` access patterns where a `dataclass` or `NamedTuple` would reduce key-string overhead at high call counts.

---

### OPT-6 Reduce serialization overhead

JSON serialization (`json.dumps`/`json.loads`, Pydantic `.model_dump()`) appearing as a hot spot — typically because objects are serialized to pass between functions that could just pass the object directly.

**Signal:** `json.dumps`, `json.loads`, or Pydantic serializers in top 10 `tottime`, called from within a tight loop.

**Fix:** pass the Python object directly between functions. Only serialize at the true system boundary (write to storage, send over network, log to file). Move serialization outside the per-document loop to once per batch.

---

### OPT-7 Chunked batch processing

A pipeline that loads an entire dataset into memory when chunked processing would keep memory below a threshold and allow early results to be written before all input is consumed.

**Signal:** peak memory > 2–3× the size of a single representative batch, or out-of-memory errors on large inputs.

```python
def process_in_chunks(records, chunk_size=500):
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        results = [process(r) for r in chunk]
        write_results(results)
        # memory freed at end of each iteration
```

---

## Phase 3 — Measure

After applying optimizations, re-run cProfile on the same entry point with the same input:

```bash
python -m cProfile -o profile_output_after.prof <entry_point.py>
python -c "
import pstats
from pstats import SortKey
s = pstats.Stats('profile_output_after.prof')
s.sort_stats(SortKey.CUMULATIVE)
s.print_stats(20)
"
```

Produce a **before/after comparison**:

```
## Performance Delta

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total CPU time | 142 s | 38 s | -73% |
| Peak memory | 1,240 MiB | 310 MiB | -75% |
| Top hot spot | step_04.process_doc (14.2 s) | step_04.process_doc (3.1 s) | -78% |
| Throughput | 42 docs/min | 158 docs/min | +276% |
```

If the codebase has existing benchmark scripts or timing logs, compare against those instead of raw cProfile output.

---

## Closing

Write output to:
- `refactors/refactor_N_<slug>/phase4_optimization.md` — if called from `launch-refactor`
- `optimization_report.md` at the codebase root — if called standalone

Format:

```markdown
# Optimization Report — <scope>

## Profiling summary
[Top 3-5 CPU and memory findings]

## Optimizations applied
| OPT | Location | Change | Estimated saving |
|-----|----------|--------|-----------------|
| OPT-3 | step_02.extract | lru_cache on _compile_pattern | -3.2 s tottime |
| OPT-2 | pipeline/main.py | generator pipeline, 3 stages | -840 MiB peak |

## Optimizations not applied
[List: what was considered but skipped, and why]

## Performance delta
[before/after table from Phase 3]
```

Then print:

```
Optimization complete.
Net change: <one-line summary>
Report written to <path>.
```
