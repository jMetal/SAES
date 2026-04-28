# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Migrated project to a modern `src/saes/` library layout for improved package distribution.
- Introduced `uv` for lightning-fast dependency management and reproducible environments, replacing `requirements.txt`.
- Established a modern quality assurance stack using `ruff` (linting/formatting), `mypy` (static type checking), and `pytest` (testing).
- Added `Makefile` to standardize development workflows (`make ci`, `make format`, `make test`).
- Added `CLAUDE.md` for AI-assisted development guidelines and project context.
- Implemented a modular, registry-based architecture for statistical tests (`saes.statistical_tests`), visualizations (`saes.visualization`), and reporting (`saes.reporting`).
- Added central `ThemeConfig` API (`saes.config`) for library-wide plot customization (colors, fonts, grid styles).
- Added `ColumnName` and `TableName` enums for type-safe data access and elimination of magic strings.
- Implemented lazy-loading in all registries to ensure high performance and minimal startup overhead.
- Added automated CI/CD pipeline configurations for testing and release management.

### Changed

- Refactored legacy `SAES/utils/dataframe_processor.py` into a domain-driven `saes.data.processor` module.
- Modernized all reporting tables and plots to utilize the new Enum-based column schema and Theme API.
- Updated all Jupyter notebooks (`SAES_tutorial.ipynb`, `ml_study.ipynb`, etc.) to align with the v2.0 registry-based API.
- Refactored `__init__.py` to serve as a clean entry point with optimized import resolution.

### Removed

- Removed legacy `SAES/` flat directory structure.
- Deleted deprecated configuration files: `requirements.txt`, `requirements-dev.txt`, `environment.yml`, and `.editorconfig`.
- Removed the legacy `SAES.html` module and associated HTML report generation logic.
- Removed outdated GitHub Action workflows (`publish.yml`, `release-on-merge.yml`, `pages.yml`) in favor of modern standard CI.
- Deleted legacy `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` boilerplate.

### Fixed

- Fixed Pareto `FRONT_ND` visualization dimensionality handling and output file naming in the demo script.
- Resolved various linting, formatting, and typing issues across the codebase to ensure 100% CI compliance.

## [Released]

## [1.5.0] - 2025-11-21 (@rorro6787)

### Added

- **Reproducibility support**: Added `seed` parameter to Bayesian statistical tests (`bayesian_sign_test`, `bayesian_signed_rank_test`) for deterministic results
- **Reproducibility support**: Added `seed` parameter to `HistoPlot` class for consistent jitter in histogram generation
- **Multi-platform CI**: Comprehensive GitHub Actions workflow testing on Windows, Linux (Ubuntu), and macOS
- **Smoke tests**: Added automated smoke tests for CLI and API functionality across all platforms
- **Environment files**: Added `requirements.txt`, `requirements-dev.txt`, and `environment.yml` for broader compatibility
- **Headless mode documentation**: Complete documentation and examples for running SAES without display (CI/CD, servers)
- **Headless mode examples**: Python and shell script examples for automated workflows (`examples/headless_mode_example.py`, `examples/headless_cli_example.sh`, `examples/headless_cli_example.bat`)
- **New test suite**: Added `test_bayesian_seed.py` specifically for verifying seed reproducibility
- **Documentation**: New reproducibility documentation page (`docs/usage/reproducibility.rst`) with best practices

### Changed

- Updated `test_bayesian.py` to demonstrate both seed parameter usage and backward compatibility
- Enhanced README with sections on reproducibility and headless mode
- Improved documentation structure to include reproducibility guidance

### Fixed

- Ensured all random operations can be made deterministic for reproducible research

## [1.4.0] - 2025-11-15 (@rorro6787)

### Added

- Comprehensive test suite for Bayesian statistical tests (`bayesian_sign_test`, `bayesian_signed_rank_test`)
- Code of Conduct based on Contributor Covenant v2.1
- `.editorconfig` file for consistent code style across editors
- `.pre-commit-config.yaml` for automated code quality checks (black, flake8, isort)

### Changed

- **BREAKING**: Renamed plot modules to lowercase for Python naming consistency:
  - `SAES.plots.CDplot` → `SAES.plots.cdplot`
  - `SAES.plots.HistoPlot` → `SAES.plots.histoplot`
  - `SAES.plots.Pplot` → `SAES.plots.pplot`
- Migrated from `pip`/`venv` to `uv` for faster, more reliable dependency management
- Reorganized dependencies in `pyproject.toml` into logical groups:
  - Runtime dependencies (core functionality)
  - `[test]`: Testing dependencies
  - `[dev]`: Development tools (black, flake8, mypy, isort, pre-commit)
  - `[docs]`: Documentation generation (Sphinx)
  - `[html]`: HTML notebook generation (papermill, nbconvert)
- Expanded `CONTRIBUTING.md` with detailed setup instructions using `uv`
- Updated `README.md` with `uv` installation instructions
- Improved documentation in `docs/conf.py` to dynamically read version from `version.txt`
- Updated GitHub Actions workflows to use `uv` for dependency installation
- Updated all notebooks to use new lowercase plot module names

### Fixed

- Corrected 'frtom' typo to 'from' in all plot module docstrings (23 instances across 5 files)
- Removed debug code (`if __name__ == "__main__"` block) from `HistoPlot.py`
- Fixed `pyproject.toml` structure (moved `requires-python` to correct location)
- Restored corrupted `boxplot.py` and `violin.py` files

### Documentation

- Populated `CHANGELOG.md` with complete version history from v0.5.1 to v1.3.6
- Replaced generic TODO comment in `apv_procedures.py` with comprehensive module docstring
- Added detailed examples and usage instructions throughout documentation

## [1.3.6] - 2025-03-18 (@rorro6787)

### Added

- HistoPlot visualization for algorithm performance distribution
- Violin plot for enhanced performance distribution visualization

### Fixed

- Various bug fixes and added code comments for better maintainability

## [1.3.5] - 2025-03-13 (@rorro6787)

### Added

- Anova and T-test tables for parametric statistical analysis
- Extra Friedman test variations (aligned-rank, Quade) for non-parametric analysis
- ML notebook example demonstrating library usage with machine learning algorithms
- Comprehensive tests for new features

### Changed

- Mean/median now used as estimators of best and second-best performance in LaTeX tables
- Improved documentation across the entire library
- Updated Bayesian notebook with better examples

### Fixed

- Bug in MeanMedian table show() function

## [1.3.4] - 2025-03-06 (@rorro6787)

### Added

- Frequency graph to the Bayesian posterior plot (Pplot)
- Article references for statistical test implementations

### Fixed

- Fixed dependency issues (v2)
- Fixed tests to accommodate new changes

## [1.3.2] - 2025-03-06 (@rorro6787)

### Changed

- Updated internal dependencies and configurations

## [1.3.1] - 2025-03-05 (@rorro6787)

### Fixed

- Minor bug fixes and improvements

## [1.3.0] - 2025-03-05 (@rorro6787)

### Added

- Bayesian posterior plot (Pplot) for probabilistic algorithm comparison
- HTML module for generating interactive analysis reports

### Changed

- Updated multi-objective fronts notebook
- Updated sphinx documentation

## [1.2.0] - 2025-03-04 (@rorro6787)

### Added

- Reference fronts support in 2D and 3D for multi-objective optimization module
- Parallel coordinates visualization for multi-objective analysis
- Fronts notebook with comprehensive examples

### Changed

- Updated all SAES fstring documentation format

### Fixed

- Bug fixed in pareto_front.py

## [1.1.0] - 2025-02-26 (@rorro6787)

### Changed

- Updated Sphinx documentation to v1.1.0
- Updated README.md with improved examples and instructions

## [1.0.3] - 2025-02-07 (@rorro6787)

### Changed

- Documentation improvements and README updates

## [1.0.2] - 2025-02-06 (@rorro6787)  

### Changed

- Minor improvements and documentation updates

## [1.0.1] - 2025-02-06 (@rorro6787)

### Fixed

- Initial post-release bug fixes

## [1.0.0] - 2025-02-05 (@rorro6787) 

### Added

- First stable release
- Core statistical analysis features (Friedman test, Wilcoxon signed-rank test)
- LaTeX table generation (Median, Friedman, Wilcoxon tables)
- Visualization tools (Boxplot, Critical Distance plot)
- Multi-objective optimization support (Pareto front visualization)
- Command-line interface
- Comprehensive documentation

## [0.6.0] - 2025-02-03 (@rorro6787)

### Added

- Pre-release version with core features
- Initial multi-objective optimization module

## [0.5.1] - 2025-01-21 (@rorro6787)

### Added

- Initial beta release
- Basic statistical testing framework
- CSV data processing utilities
