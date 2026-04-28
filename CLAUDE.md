# CLAUDE.md — SAES

> This file is read automatically by Claude, Antigravity, and any AI assistant that opens this repository.
> It defines the project identity, architecture, and non-negotiable conventions.

## Project Identity

**What**: Python library designed to analyze and compare the performance of different algorithms across multiple problems using non-parametric statistical tests.

**Goal**: Provide researchers and practitioners with an easy-to-use library to conduct robust statistical comparisons of empirical studies, particularly in the fields of optimization, machine learning, and artificial intelligence.

**How it works**: The library uses a registry-based architecture to provide statistical tests (Friedman, Wilcoxon, Bayesian), visualization (CDPlots, Boxplots), and reporting (LaTeX tables). It also visualizes Pareto fronts (2D, 3D, ND).

---

## Tech Stack — Non-Negotiable

| Layer | Technology | Version Constraint |
|-------|------------|-------------------|
| Runtime | Python | `>= 3.12` |
| Package Manager | `uv` | Latest |
| Data | `pandas` + `numpy` | `>= 2.0` |
| Plotting | `matplotlib` + `seaborn` | Latest |
| Stats | `scipy` + `statsmodels`| Latest |
| Linter / Formatter | `ruff` | `>= 0.8` |
| Type Checker | `mypy` | `>= 1.13` |
| Testing | `pytest` | `>= 8.0` |

---

## Project Structure

```
├── src/saes/                      # Main library package
│   ├── statistical_tests/         # Registry-based tests (Omnibus, Pairwise, Bayesian)
│   ├── visualization/             # Plotting (Boxplot, CDPlot, Posterior, etc.)
│   ├── reporting/                 # LaTeX table generators (MeanMedian, Friedman, etc.)
│   ├── pareto/                    # Pareto front visualizations (2D, 3D, ND)
│   ├── utils/                     # Shared processing utilities
│   ├── exceptions.py              # Custom exception hierarchy
│   ├── logger.py                  # Rich-based standardized logging
│   └── __init__.py                # Public Python API
├── tests/                         # pytest test suite (test_*.py)
├── scripts/
│   └── release_stamp.py           # Release automation
├── .github/workflows/             # CI/CD pipelines
├── CHANGELOG.md                   # Release history
├── version.txt                    # Current version
└── Makefile                       # Development commands
```

---

## Code Conventions — Mandatory

### Python General

- Every module starts with `from __future__ import annotations`.
- All public functions, methods, and classes **must** have type hints.
- Use modern Python 3.12+ syntax: `X | Y` unions, `match` statements.
- Maximum line length: **100 characters**.
- Use `pathlib.Path` — never `os.path`.
- Use `f-strings` — never `.format()` or `%`.

### Registry Pattern

The library uses a decorator-based registry for tests and plots.
- Register: `@register_test(TestName.FRIEDMAN)`
- Instantiate: `get_test(TestName.FRIEDMAN)` or `get_plot(PlotName.BOXPLOT, ...)`

### Import Conventions

```python
# ✅ DO — use the public API
from saes import get_test, TestName, get_plot, PlotName

# ❌ NEVER — import from private/internal modules directly
from saes.statistical_tests.omnibus.friedman import FriedmanTest
```

---

## Testing

- Framework: `pytest` with fixtures.
- File pattern: `tests/**/test_*.py`.
- Run: `uv run pytest tests/ -v`.

---

## Quality Gates

All checks must pass before any commit. **As an agent, you MUST run this command before finishing your task**:

```bash
make ci
```

---

## Git & Collaboration

- Commit messages: conventional commits — `feat:`, `fix:`, etc.
- Branching: Always use `make branch` to create new feature/fix branches.
- Versioning: Managed automatically via `scripts/release_stamp.py` on merge.
