# Software X Compliance

SAES meets all Software X publication requirements.

## 1. Deterministic Seeds ✅

Bayesian tests support `seed` parameter for reproducibility:

```python
from SAES.statistical_tests.bayesian import bayesian_sign_test
result, _ = bayesian_sign_test(data, sample_size=1000, seed=42)
```

## 2. Multi-Platform CI ✅

`.github/workflows/multi-platform-test.yml` tests on:
- Ubuntu, Windows, macOS
- Python 3.10, 3.11, 3.12

## 3. Smoke Tests ✅

Run comprehensive smoke tests (10 tests) - fully automated:

```bash
chmod +x examples/smoke_test.sh
./examples/smoke_test.sh
```

The script automatically:
- Creates virtual environment if needed
- Installs dependencies
- Runs all tests in headless mode

**Tests cover:**
- **LaTeX tables** (4): Mean/Median, Friedman, Wilcoxon pivot, Wilcoxon pairwise
- **Plots** (3): Boxplot single, Boxplot grid, Critical distance
- **Statistical APIs** (3): Bayesian tests with seeds, Plot classes

## 4. Environment Files ✅

Multiple installation options:

```bash
# Option 1: Requirements file
pip install -r requirements.txt

# Option 2: Conda
conda env create -f environment.yml
conda activate saes

# Option 3: Auto-install (smoke test does this)
./examples/smoke_test.sh
```

Files provided:
- `requirements.txt` - Core dependencies
- `requirements-dev.txt` - Development dependencies  
- `environment.yml` - Conda environment

## 5. Headless Mode ✅

For CI/CD and server environments:

```bash
export MPLBACKEND=Agg
python -m SAES -ls -ds data.csv -ms metrics.csv -m HV -s friedman -op output.tex
```

The smoke test script runs in headless mode by default.

## Quick Start

```bash
# Clone and test
git clone https://github.com/jMetal/SAES.git
cd SAES
chmod +x examples/smoke_test.sh
./examples/smoke_test.sh
```

## Verification

```bash
# Smoke tests (automated setup)
./examples/smoke_test.sh

# Unit tests
python -m unittest discover tests
```

## Branch

Feature branch: `feature/software-x-requirements`  
Ready for merge (not merged yet, as requested)
