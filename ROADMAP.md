# Roadmap

Deferred work, tracked here instead of as TODO stubs inside skill bodies.

## Agent integration hooks (removed from skill bodies 2026-06-18)

These were aspirational `~~`/TODO notes inside the agent skills. The agents deliberately **never commit, push, or call external systems** today; these are the future wiring:

- **Source control** — `code-agent`: push branch + open draft PR after a task. `review-agent`: post review comments on the PR.
- **CI/CD** — `code-agent`: trigger a CI run and wait for the result before marking a task done.
- **Chat** — `plan-agent`: post the plan summary for async human review. `review-agent`: request human approval before merge.
- **ADRs** — `plan-agent`: read existing ADRs from `docs/adr/` when the project adopts them, and feed them into planning.

## Pass B — stack parameterization (decided: explicit + parameterized)

- Add `stack:` / `cloud:` fields to the sprint-file header (`sprint-army`/`sprint-design` produce them; template documents them).
- `sprint-executor`: replace the hardcoded `azure-*` routing with a generic "domain skills" hook driven by the sprint file, keeping Azure as the default example.
- `code-agent` / `review-agent`: turn the Python/FastAPI-specific conventions into a language profile applied when `stack: python`.
- `refactor-perf`: frame as the Python performance profile (when `stack: python`); leave room for other stacks.

## Local structure (decided 2026-06-18: reference model, 3-tier)

- **Library** = `mutlit-agent` — the only thing an agent loads. `skills/` = your own (edited here, one copy); `.agents/skills/` = externals pulled by `npx skills update` (read-only, gitignored); `skills-lock.json` = the dependency list.
- **Sources** = per-repo clones for exploration only (`git pull` to browse latest); promote keepers into the lock file.
- ✅ Done: removed the `skills/azure-*` bridge symlinks; `sprint-executor` now references `.agents/skills/` directly.
- Optional: group the desktop source clones under a single `sources/` folder.
