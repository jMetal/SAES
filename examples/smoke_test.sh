#!/bin/bash
# SAES Comprehensive Smoke Tests
# Self-contained: Sets up environment and runs all tests

set -e

echo "=== SAES Smoke Tests ==="
echo ""

# Setup virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if ! python -c "import SAES" 2>/dev/null; then
    echo "Installing SAES..."
    pip install -q -e ".[test]"
    echo "✓ SAES installed"
else
    echo "✓ SAES already installed"
fi

# Set headless mode
export MPLBACKEND=Agg
mkdir -p /tmp/saes_smoke_tests

echo ""
echo "Running tests..."
echo ""

DATA="tests/test_data/swarmIntelligence.csv"
METRICS="tests/test_data/multiobjectiveMetrics.csv"

# LaTeX Tables (4 types)
echo "[1/10] LaTeX: Mean/Median table"
python -m SAES -ls -ds $DATA -ms $METRICS -m HV -s mean_median -op /tmp/saes_smoke_tests/mean_median.tex

echo "[2/10] LaTeX: Friedman test table"
python -m SAES -ls -ds $DATA -ms $METRICS -m HV -s friedman -op /tmp/saes_smoke_tests/friedman.tex

echo "[3/10] LaTeX: Wilcoxon pivot table"
python -m SAES -ls -ds $DATA -ms $METRICS -m HV -s wilcoxon_pivot -op /tmp/saes_smoke_tests/wilcoxon_pivot.tex

echo "[4/10] LaTeX: Wilcoxon pairwise table"
python -m SAES -ls -ds $DATA -ms $METRICS -m HV -s wilcoxon -op /tmp/saes_smoke_tests/wilcoxon.tex

# Plots (3 types)
echo "[5/10] Plot: Boxplot (single instance)"
python -m SAES -bp -ds $DATA -ms $METRICS -m HV -i DTLZ1 -op /tmp/saes_smoke_tests/boxplot.png

echo "[6/10] Plot: Boxplot (all instances grid)"
python -m SAES -bp -ds $DATA -ms $METRICS -m HV -g -op /tmp/saes_smoke_tests/boxplot_grid.png

echo "[7/10] Plot: Critical distance plot"
python -m SAES -cdp -ds $DATA -ms $METRICS -m HV -op /tmp/saes_smoke_tests/cdplot.png

# Statistical Tests API (3 tests)
echo "[8/10] API: Bayesian sign test (with seed)"
python -c "
from SAES.statistical_tests.bayesian import bayesian_sign_test
import pandas as pd, numpy as np
data = pd.DataFrame({'A': [0.9,0.85,0.95,0.9,0.92], 'B': [0.5,0.6,0.55,0.58,0.52]})
r1, _ = bayesian_sign_test(data, sample_size=1000, seed=42)
r2, _ = bayesian_sign_test(data, sample_size=1000, seed=42)
np.testing.assert_array_almost_equal(r1, r2, decimal=10)
"

echo "[9/10] API: Bayesian signed rank test (with seed)"
python -c "
from SAES.statistical_tests.bayesian import bayesian_signed_rank_test
import pandas as pd, numpy as np
data = pd.DataFrame({'A': [0.9,0.85,0.95,0.9,0.92], 'B': [0.5,0.6,0.55,0.58,0.52]})
r1, _ = bayesian_signed_rank_test(data, sample_size=500, seed=123)
r2, _ = bayesian_signed_rank_test(data, sample_size=500, seed=123)
np.testing.assert_array_almost_equal(r1, r2, decimal=10)
"

echo "[10/10] API: Plot classes initialization"
python -c "
from SAES.plots.histoplot import HistoPlot
from SAES.plots.violin import Violin
from SAES.plots.boxplot import Boxplot
from SAES.plots.cdplot import CDplot
import pandas as pd
data = pd.read_csv('$DATA')
metrics = pd.read_csv('$METRICS')
histoplot = HistoPlot(data, metrics, 'HV')
violin = Violin(data, metrics, 'HV')
boxplot = Boxplot(data, metrics, 'HV')
cdplot = CDplot(data, metrics, 'HV')
"

echo ""
echo "✓ All 10 smoke tests passed!"
echo "  Tests cover: LaTeX tables (4), Plots (3), Statistical APIs (3)"
echo "  Output directory: /tmp/saes_smoke_tests/"
ls -lh /tmp/saes_smoke_tests/ 2>/dev/null | tail -n +2 | wc -l | xargs echo "  Files created:"
