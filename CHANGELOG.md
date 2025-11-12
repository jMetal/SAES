# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Corrected 'frtom' typo to 'from' in all plot module docstrings (23 instances across 5 files)

## [Released]

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
