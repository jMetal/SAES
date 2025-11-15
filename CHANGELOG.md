# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [Released]

## [1.4.0] - 2025-11-15

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

## [1.3.6] - 2025-03-18

### Added
- HistoPlot visualization for algorithm performance distribution
- Violin plot for enhanced performance distribution visualization

### Fixed
- Various bug fixes and added code comments for better maintainability

## [1.3.5] - 2025-03-13

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

## [1.3.4] - 2025-03-06

### Added
- Frequency graph to the Bayesian posterior plot (Pplot)
- Article references for statistical test implementations

### Fixed
- Fixed dependency issues (v2)
- Fixed tests to accommodate new changes

## [1.3.2] - 2025-03-06

### Changed
- Updated internal dependencies and configurations

## [1.3.1] - 2025-03-05

### Fixed
- Minor bug fixes and improvements

## [1.3.0] - 2025-03-05

### Added
- Bayesian posterior plot (Pplot) for probabilistic algorithm comparison
- HTML module for generating interactive analysis reports

### Changed
- Updated multi-objective fronts notebook
- Updated sphinx documentation

## [1.2.0] - 2025-03-04

### Added
- Reference fronts support in 2D and 3D for multi-objective optimization module
- Parallel coordinates visualization for multi-objective analysis
- Fronts notebook with comprehensive examples

### Changed
- Updated all SAES fstring documentation format

### Fixed
- Bug fixed in pareto_front.py

## [1.1.0] - 2025-02-26

### Changed
- Updated Sphinx documentation to v1.1.0
- Updated README.md with improved examples and instructions

## [1.0.3] - 2025-02-07

### Changed
- Documentation improvements and README updates

## [1.0.2] - 2025-02-06

### Changed
- Minor improvements and documentation updates

## [1.0.1] - 2025-02-06

### Fixed
- Initial post-release bug fixes

## [1.0.0] - 2025-02-05

### Added
- First stable release
- Core statistical analysis features (Friedman test, Wilcoxon signed-rank test)
- LaTeX table generation (Median, Friedman, Wilcoxon tables)
- Visualization tools (Boxplot, Critical Distance plot)
- Multi-objective optimization support (Pareto front visualization)
- Command-line interface
- Comprehensive documentation

## [0.6.0] - 2025-02-03

### Added
- Pre-release version with core features
- Initial multi-objective optimization module

## [0.5.1] - 2025-01-21

### Added
- Initial beta release
- Basic statistical testing framework
- CSV data processing utilities

[Unreleased]: https://github.com/jMetal/SAES/compare/v1.3.6...HEAD
[1.3.6]: https://github.com/jMetal/SAES/compare/v1.3.5...v1.3.6
[1.3.5]: https://github.com/jMetal/SAES/compare/v1.3.4...v1.3.5
[1.3.4]: https://github.com/jMetal/SAES/compare/v1.3.2...v1.3.4
[1.3.2]: https://github.com/jMetal/SAES/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/jMetal/SAES/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/jMetal/SAES/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/jMetal/SAES/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/jMetal/SAES/compare/v1.0.3...v1.1.0
[1.0.3]: https://github.com/jMetal/SAES/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/jMetal/SAES/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/jMetal/SAES/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jMetal/SAES/compare/v0.6.0...v1.0.0
[0.6.0]: https://github.com/jMetal/SAES/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/jMetal/SAES/releases/tag/v0.5.1
