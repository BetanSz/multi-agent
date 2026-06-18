---
name: perf-analyze
description: Analyze an application for performance bottlenecks — runtime, memory, database queries, API calls, and rendering. Produces a prioritized list of issues with concrete fixes, not just observations.
argument-hint: "<file, folder, or 'full'> [layer: backend|frontend|db|all]"
---

# /perf-analyze

Find what's actually slow, why, and what to do about it. Every finding includes severity, root cause, and a concrete fix.

## Phase 1 — Instrument before guessing

Never guess at bottlenecks. First:
1. Run the app and identify the slow path (which endpoint, which screen, which operation)
2. If profiling tools are available, run them and read the output
3. If no profiler, add timing logs around suspected areas and run
4. Only move to Phase 2 once you have data, not hypotheses

## Phase 2 — Systematic scan by layer

Work through each layer relevant to the codebase:

### Backend / compute
- N+1 loops: any loop that makes a DB call, API call, or file read on each iteration
- Synchronous blocking I/O in async code (missing `await`, blocking the event loop)
- Repeated expensive computations that could be cached or memoized
- Unbounded operations (no pagination, no limit on result sets)
- Unnecessary serialization/deserialization in hot paths

### Database
- Missing indexes on columns used in WHERE, JOIN, ORDER BY
- SELECT * where only 2-3 columns are needed
- N+1 queries (ORM lazy loading in loops)
- Queries inside loops that could be batched with IN or a JOIN
- Missing query result caching for stable data

### API / network
- Sequential API calls that could be parallelized (`Promise.all` / `asyncio.gather`)
- Oversized payloads (returning full objects when only IDs are needed)
- Missing HTTP caching headers on stable responses
- Chatty APIs (10 small calls that could be 1 batched call)

### Frontend / perceived latency
The user's experience of speed matters as much as actual speed. Check:
- Time to first meaningful interaction — is anything blocking the initial render unnecessarily?
- Optimistic UI — are writes reflected immediately in the UI before the server confirms?
- Loading states — does the user have feedback within 100ms of any action?
- Waterfall requests — are assets or data fetches chained when they could be parallel?
- Bundle size — is there code being loaded on the critical path that isn't needed until later?

### File reads per interaction
Every time a user performs an action, check what files or static resources are being read from disk or fetched:
- Config files, translation files, schema files — are these read on every request or loaded once at startup and cached?
- Any `fs.readFile`, `open()`, or equivalent in a hot path → should be read once and kept in memory
- Template or prompt files loaded per call → cache after first read
- If a file hasn't changed since last read, it should never be re-read — use a module-level or application-level cache with an appropriate invalidation strategy

### API calls per session — count and architecture
Instrument or manually trace how many external API calls a typical user session generates:
1. **Count** — log or inspect network requests for a representative user journey; identify the total
2. **Classify** — which calls are load-bearing (user would notice if removed) vs. speculative or redundant?
3. **Deduplicate** — the same data fetched multiple times in one session should be cached after the first fetch
4. **Batch** — multiple calls to the same service that could be combined into one (e.g. fetching 10 user records one by one vs. a single batch endpoint)
5. **Architecture question** — if the call count is high, ask whether a different pattern would structurally reduce it:
   - Server-side aggregation (backend fetches and combines, frontend makes one call)
   - GraphQL or composite endpoints instead of REST chatter
   - Subscriptions/webhooks instead of polling
   - Local cache with background sync instead of fetch-on-every-render

Report the before/after call count as a concrete metric, not just a qualitative improvement.

### Frontend / rendering
- Re-renders triggered by reference inequality (new object/array created on each render)
- Missing memoization on expensive derived values
- Blocking the main thread with heavy computation (should be a web worker)
- Layout thrashing (reading then writing DOM in a loop)
- Unoptimized assets (images, unminified bundles, missing code splitting)

### Memory
- Objects accumulated in memory and never released (event listeners, timers, closures)
- Large data loaded fully into memory when streaming would work
- Caches with no eviction policy (unbounded growth)

## Output format

```
## Performance analysis: <scope>

### Findings

| # | Severity | Layer | Issue | Location | Fix |
|---|----------|-------|-------|----------|-----|
| 1 | CRITICAL | DB | N+1 query in user listing | `users.service.ts:87` | Batch with single JOIN query |
| 2 | HIGH | Backend | Unparallelized API calls | `dashboard.ts:34` | Wrap in Promise.all |
| 3 | MEDIUM | Frontend | Object recreated on every render | `Table.tsx:12` | Memoize with useMemo |

### Fix #1 — <issue title>
**Root cause:** <why it's slow>
**Before:** <code snippet>
**After:** <code snippet>
**Expected impact:** <e.g. "reduces N queries to 1 per request">

### Fix #2 ...
```

Implement fixes in severity order. After each fix, re-run the profiler or timing measurement to confirm improvement before moving to the next.

## Severity definitions

- **CRITICAL** — causes timeouts, crashes, or O(n²)+ behavior under real load
- **HIGH** — measurable latency impact (>100ms) on the main user path
- **MEDIUM** — latency impact on secondary paths, or memory growth over time
- **LOW** — good practice, minor gain, worth doing but not urgent

## What NOT to do

- Do not micro-optimize (bit twiddling, loop unrolling) before fixing architectural issues
- Do not add caching before understanding why something is slow
- Do not parallelize operations that have side-effect dependencies
- Do not change behavior while optimizing — performance work is not a refactor opportunity
