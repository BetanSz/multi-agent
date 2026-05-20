---
name: repo-init
description: Bootstraps a new project repository — proposes and creates the folder structure, virtual environment (conda by default), .gitignore, .env.example, CLAUDE.md, pyproject.toml, and docs/sprints/ layout. Stack-aware (Python/Azure pipeline, FastAPI, TypeScript). Probes what already exists and only creates what is missing. Use at the start of a new project before the first sprint.
argument-hint: '"project name and one-line description"'
---

> **Using skill repo-init.**

# Repo Init

You are a project bootstrapper. Your job: ask the right questions, probe what already exists, then create a professional project structure so the first sprint starts from a clean foundation — not from a blank folder.

**Freedom level: MEDIUM** — folder structure and file content follow opinionated templates; stack detection and naming decisions require judgment.

## Step 1 — Understand the project

Ask (or infer from the argument if already clear):

1. **Project name** — will become the conda env name and the repo name
2. **Stack** — choose the closest match:
   - `python-azure-pipeline` — Python pipeline with Azure services (Cosmos, Storage, OpenAI, DI)
   - `python-fastapi` — FastAPI backend with Azure auth
   - `python-script` — simple Python scripts / notebooks, no web framework
   - `typescript-node` — Node.js / TypeScript project
3. **Azure services in scope** — which of: Cosmos DB, Blob Storage, Azure OpenAI, Document Intelligence, Key Vault, Functions, Service Bus (used to seed .env.example and CLAUDE.md)
4. **Python version** — default: 3.11

If the argument contains enough to infer all four, skip the questions.

## Step 2 — Probe what already exists

Before creating anything, check:

```
- Is git already initialized? (look for .git/)
- Does environment.yml already exist?
- Does .gitignore already exist?
- Does CLAUDE.md already exist?
- Does src/ or any standard folder already exist?
- Does docs/sprints/ already exist?
```

For each item that already exists: **do not overwrite it**. Report what was found and skip creation. Only create what is missing.

## Step 3 — Propose the structure

Print the proposed structure before creating anything. For `python-azure-pipeline`:

```
<project-name>/
├── src/                        # core library: settings, clients, schemas
│   └── __init__.py
├── pipeline/                   # numbered steps: step_01_*.py, step_02_*.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── results/                # gitignored — human-review outputs
├── sprints/                    # one sub-folder per sprint: sprint_N_<topic>/
├── scripts/                    # one-off utility scripts
├── data/                       # gitignored — local raw data
├── .env                        # gitignored — secrets
├── .env.example                # committed — template with var names, no values
├── environment.yml             # conda environment definition
├── pyproject.toml              # project metadata + pytest + linting config
├── CLAUDE.md                   # context file for Claude Code
└── README.md
```

For `python-fastapi`, add:
```
├── app/
│   ├── routers/
│   ├── models/
│   ├── dependencies.py
│   └── main.py
```
(replace `pipeline/` and `src/` with the FastAPI layout)

For `python-script`, simplify:
```
├── scripts/
├── notebooks/                  # gitignore checkpoints
├── data/
├── tests/
├── docs/sprints/
```

For `typescript-node`, adapt accordingly (see reference below).

Confirm with the user before creating. A quick "looks good" is sufficient — do not require exhaustive approval.

## Step 4 — Create files

### 4.1 — Folder structure

Create all directories (including empty `__init__.py` where needed for Python packages).

### 4.2 — environment.yml (conda)

```yaml
name: <project-name>
channels:
  - conda-forge
  - defaults
dependencies:
  - python=<version>
  - pip
  - pip:
    - -r requirements.txt
```

Instructions for user (print after creating):
```
conda env create -f environment.yml
conda activate <project-name>
```

### 4.3 — pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "<project-name>"
version = "0.1.0"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v"

[tool.ruff]
line-length = 100
target-version = "py311"
```

### 4.4 — .gitignore

Write a comprehensive `.gitignore` for the detected stack. See `references/gitignore-templates.md` for the full templates.

Always include these sections regardless of stack:
- **Python**: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `.pytest_cache/`, `*.egg-info/`, `dist/`, `build/`, `.mypy_cache/`, `.ruff_cache/`
- **Environment**: `.env`, `.env.local`, `.env.*.local` — never commit secrets
- **Project-specific**: `data/`, `tests/results/`, `*.log`, `*.jsonl`
- **Conda**: no files to gitignore from conda itself (env is defined by `environment.yml`)
- **VS Code** (Windows): `.vscode/` except `.vscode/settings.json` if it contains useful shared config
- **Windows**: `Thumbs.db`, `Desktop.ini`, `$RECYCLE.BIN/`
- **macOS**: `.DS_Store`, `.AppleDouble`
- **Jupyter**: `.ipynb_checkpoints/`
- **Azure Functions** (if in scope): `local.settings.json`

### 4.5 — .env.example

Generate based on the Azure services selected in Step 1.

```bash
# Azure OpenAI (francecentral)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AZURE_OPENAI_DEPLOYMENT=

# Azure AI Foundry (swedencentral) — optional
AZURE_FOUNDRY_ENDPOINT=
AZURE_FOUNDRY_KEY=
AZURE_FOUNDRY_DEPLOYMENT=

# Cosmos DB
AZURE_COSMOS_ENDPOINT=
AZURE_COSMOS_KEY=
AZURE_COSMOS_DATABASE=

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=

# Azure Document Intelligence
AZURE_DI_ENDPOINT=
AZURE_DI_KEY=
```

Include only the services selected. Add a comment block at the top:
```bash
# Copy this file to .env and fill in values.
# .env is gitignored — never commit it.
```

### 4.6 — CLAUDE.md

```markdown
# <Project Name>

## What this project does
<one paragraph from the user's description>

## Stack
- Python <version> (conda env: <project-name>)
- [Azure services in scope]

## Key commands
```bash
# Activate environment
conda activate <project-name>

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run a pipeline step
python pipeline/step_01_*.py
```

## Project structure
[paste the folder structure from Step 3]

## Environment setup
Copy `.env.example` → `.env` and fill in values.
All Azure credentials go in `.env` — never commit it.

## Sprint system
Sprint files live in `docs/sprints/`.
Run `/launch_sprint "description"` to start a new sprint.
```

### 4.7 — README.md skeleton

```markdown
# <Project Name>

<one-line description>

## Setup
```bash
conda env create -f environment.yml
conda activate <project-name>
pip install -r requirements.txt
cp .env.example .env   # fill in credentials
```

## Usage
[TODO]

## Architecture
[TODO]
```

### 4.8 — tests/conftest.py skeleton

```python
import pytest

# Add project root to sys.path so imports work without installation
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### 4.9 — Git init (if not already initialized)

```bash
git init
git add .
git commit -m "chore: initial project scaffold"
```

Do not run git init if `.git/` already exists.

## Step 5 — Summary

After creating all files, print:

```
Project initialized: <project-name>

Created:
  ✓ Folder structure
  ✓ environment.yml     → conda env create -f environment.yml
  ✓ pyproject.toml      → pytest config, ruff config
  ✓ .gitignore          → <N> rules covering Python, VS Code, Windows, Azure
  ✓ .env.example        → <N> variables (fill in .env)
  ✓ CLAUDE.md           → project context for Claude Code
  ✓ README.md           → skeleton
  ✓ tests/conftest.py   → sys.path setup
  ✓ sprints/            → sprint folders go here (sprint_N_<topic>/)
  [✓ git init + initial commit]

Skipped (already existed):
  [list]

Next step: fill in .env, then run /launch_sprint "Sprint 1 — <first feature>"
```

## Constraints

- Never overwrite an existing file — only create what is missing.
- Never commit `.env` — verify it is in `.gitignore` before any git operation.
- If git is already initialized and has uncommitted changes, do not run `git commit` — warn the user instead.
- For the conda env name: use the project name with hyphens, lowercase (e.g. `helexia-poc`).
