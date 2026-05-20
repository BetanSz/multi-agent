# .gitignore Templates

Use the appropriate sections for the detected stack. Always include Core + OS.

---

## Core (always include)

```gitignore
# Secrets — never commit
.env
.env.local
.env.*.local

# Sprint system scratch space
_army/

# Logs
*.log
*.jsonl

# Editor swap files
*.swp
*.swo
*~
```

---

## Python

```gitignore
# Bytecode
__pycache__/
*.py[cod]
*.pyd
*.pyo

# Distribution
build/
dist/
*.egg-info/
*.egg
MANIFEST

# Virtual environments (if using venv — conda uses environment.yml instead)
.venv/
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
nosetests.xml
coverage.xml
*.cover

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json
.pytype/
.pyre/

# Linting
.ruff_cache/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Profiling
*.prof
```

---

## Project-specific (Python/Azure pipeline pattern)

```gitignore
# Local data — never commit raw documents or exports
data/
*.csv
*.xlsx
*.pdf
*.docx

# Test outputs — human-review artifacts
tests/results/

# Cosmos / Azure SDK local caches
.cosmos_cache/
```

---

## Azure Functions (include if using Functions)

```gitignore
local.settings.json
.azure/
```

---

## VS Code (Windows)

```gitignore
# Keep: .vscode/settings.json (shared editor config is useful)
# Ignore: everything else
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
*.code-workspace
```

---

## Windows OS

```gitignore
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
Desktop.ini
$RECYCLE.BIN/
*.cab
*.msi
*.msix
*.msm
*.msp
*.lnk
```

---

## macOS (include if team has Mac users)

```gitignore
.DS_Store
.AppleDouble
.LSOverride
._*
.Spotlight-V100
.Trashes
```

---

## TypeScript / Node

```gitignore
node_modules/
dist/
build/
.next/
out/
*.tsbuildinfo
.cache/
coverage/
.nyc_output/
*.js.map
```
