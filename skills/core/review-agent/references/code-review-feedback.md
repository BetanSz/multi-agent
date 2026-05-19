# Code Review — {{PR title or branch name}}

**Reviewer:** {{name}}
**Date:** {{date}}
**Files reviewed:** {{count}}

## Summary

{{2-3 sentence overview of what was reviewed and the overall quality assessment}}

## Feedback

### 🔴 BLOCKING

- **`{{file}}:{{line}}`** — {{description}}
  ```{{lang}}
  // Current code
  {{bad_code}}
  ```
  **Fix:** {{suggestion}}
  ```{{lang}}
  // Suggested fix
  {{good_code}}
  ```

### 🟡 IMPORTANT

- **`{{file}}:{{line}}`** — {{description}}

### 🟢 SUGGESTIONS

- **`{{file}}`** — {{optional improvement}}

### ✅ WELL DONE

- {{specific positive observation}}

## Verdict

- [ ] ✅ **Approved** — Ready to merge
- [ ] 🟡 **Approved with suggestions** — Minor items to address
- [ ] 🔴 **Changes requested** — Blocking items must be fixed first
