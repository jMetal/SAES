# CLAUDE.md — SAES

> This file is read automatically by Claude, Antigravity, and any AI assistant that opens this repository.
> It defines the project identity, architecture, and non-negotiable conventions.

## Project Identity

**What**: Python library designed to analyze and compare the performance of different algorithms across multiple problems using non-parametric statistical tests.

**Goal**: Provide researchers and practitioners with an easy-to-use library to conduct robust statistical comparisons of empirical studies, particularly in the fields of optimization, machine learning, and artificial intelligence.

**How it works**: The library reads dataset and metric CSV files to generate LaTeX statistical tables (Mean-Median, Friedman, Wilcoxon), Boxplots, Critical Distance (CD) plots, and visualizes Pareto fronts (2D, 3D, ND) for multi-objective optimization results.

---

## Tech Stack — Non-Negotiable

| Layer | Technology | Version Constraint |
|-------|------------|-------------------|
| Runtime | Python | `>= 3.10` |
| Package Manager | `uv` | Latest |
| Data | `pandas` + `numpy` | `>= 1.3.0` / `< 2.0` |
| Plotting | `matplotlib` + `seaborn` | `== 3.9.2` / `>= 0.11.0` |
| Stats | `scipy` + `scikit-posthocs`| `>= 1.7.0` / `== 0.10.0` |
| Linter / Formatter | `ruff` | `>= 0.8` |
| Type Checker | `mypy` | `>= 1.13`, strict mode |
| Testing | `pytest` | `>= 8.0` |

---

## Project Structure

```
├── src/saes/                      # Main library package
│   ├── statistical_tests/         # Non-parametric tests (Friedman, Wilcoxon, etc.)
│   ├── latex_generation/          # Exporters for generating LaTeX tables
│   ├── plots/                     # CDplots, Boxplots
│   ├── multiobjective/            # Pareto front evaluations and visualizations
│   ├── utils/                     # Helpers
│   ├── exceptions.py              # Custom exception hierarchy
│   ├── logger.py                  # Standardized logging
│   └── __init__.py                # Public Python API
├── tests/                         # pytest test suite
├── scripts/
│   └── release_stamp.py           # Release automation
├── .github/workflows/             # CI (tests.yml) and release (release.yml)
├── .agents/rules/                 # Antigravity agent rules
├── CHANGELOG.md                   # Release history (auto-stamped on merge)
├── version.txt                    # Current version (X.Y.Z)
└── Makefile                       # Development commands (make help for full list)
```

---

## Code Conventions — Mandatory

### Python General

- Every module starts with `from __future__ import annotations`.
- All public functions, methods, and classes **must** have type hints.
- Use modern Python 3.10+ syntax: `X | Y` unions, `match` statements where appropriate.
- Maximum line length: **100 characters**.
- Use `pathlib.Path` — never `os.path`.
- Use `f-strings` — never `.format()` or `%`.

### Library Design Principles

- **Library-first**: All functionality is exposed as Python API.
- **Modularity**: Separation of concerns between calculation, table generation, and plotting.

### Import Conventions

```python
# ✅ DO — use the public API
from saes import generate_cdplot, compute_friedman

# ❌ NEVER — import from private/internal modules directly
from saes.utils.math import _internal_calc
```

---

## Testing

- Framework: `pytest` with fixtures — no `unittest.TestCase`.
- File pattern: `tests/test_<module>.py`.
- Run: `uv run pytest tests/ -v`.

---

## Quality Gates

All checks must pass before any commit. **As an agent, you MUST run this command before finishing your task**:

```bash
export PATH=$PATH:/opt/homebrew/bin && make format && make ci
```

> [!IMPORTANT]
> Always run the above command to verify the entire pipeline (format + lint + type-check + tests) before reporting completion. Never skip the formatting step.

---

## Error Handling

- Never catch bare `Exception` without re-raising or logging.
- Include context in all error messages.
- Use custom exceptions in `src/saes/exceptions.py`.

---

## Git & Collaboration

- Commit messages: conventional commits — `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
- All PRs must pass CI (lint + type-check + tests).
- Never edit `version.txt` manually — it is managed by the release automation.

### Branching Workflow (Mandatory)

- **Always create branches with `make branch`** — this ensures the correct prefix for the version bump.
- Branch prefixes determine the version bump on merge:
  - `feat/*` → minor bump (default)
  - `fix/*`, `patch/*`, `hotfix/*` → patch bump
  - `major/*` → major bump

### Changelog

- When working on a branch, add entries under `## [Unreleased]` in `CHANGELOG.md`.
- On merge to `main`, `scripts/release_stamp.py` automatically stamps and bumps the version.

### Makefile Commands

```bash
make help             # Show all available targets
make branch           # Create a new branch (interactive, recommended)
make version          # Show current version from version.txt
make release-dry-run  # Preview release stamp without modifying files
make release-stamp    # Stamp changelog and bump version (used by CI)
```
