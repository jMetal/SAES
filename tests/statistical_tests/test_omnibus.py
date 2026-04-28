"""Tests for omnibus statistical tests (Friedman, ANOVA, Quade)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from scipy.stats import friedmanchisquare

from saes.exceptions import StatisticalTestError
from saes.statistical_tests import TestName, get_test
from saes.statistical_tests.base import StatisticalTestResult


@pytest.fixture
def multi_algorithm_data():
    """DataFrame with 5 instances × 3 algorithms."""
    return pd.DataFrame(
        {
            "Algorithm A": [0.9, 0.85, 0.95, 0.8, 0.92],
            "Algorithm B": [0.8, 0.75, 0.85, 0.85, 0.87],
            "Algorithm C": [0.7, 0.65, 0.75, 0.78, 0.80],
        }
    )


@pytest.fixture
def two_algorithm_data():
    return pd.DataFrame(
        {
            "Algorithm A": [0.9, 0.85, 0.95, 0.8, 0.92],
            "Algorithm B": [0.8, 0.75, 0.85, 0.85, 0.87],
        }
    )


class TestFriedman:
    def test_returns_statistical_result(self, multi_algorithm_data):
        test = get_test(TestName.FRIEDMAN)
        result = test.run(multi_algorithm_data, maximize=True)
        assert isinstance(result, StatisticalTestResult)
        assert result.test_name == "Friedman"

    def test_statistic_positive(self, multi_algorithm_data):
        result = get_test(TestName.FRIEDMAN).run(multi_algorithm_data, maximize=True)
        assert result.statistic > 0

    def test_p_value_in_range(self, multi_algorithm_data):
        result = get_test(TestName.FRIEDMAN).run(multi_algorithm_data, maximize=True)
        assert 0 <= result.p_value <= 1

    def test_to_dataframe(self, multi_algorithm_data):
        result = get_test(TestName.FRIEDMAN).run(multi_algorithm_data, maximize=True)
        df = result.to_dataframe()
        assert "Results" in df.columns
        assert "Friedman stat" in df.index

    def test_raises_on_single_column(self):
        data = pd.DataFrame({"A": [1, 2, 3]})
        with pytest.raises(StatisticalTestError):
            get_test(TestName.FRIEDMAN).run(data, maximize=True)

    def test_validates_against_scipy(self, multi_algorithm_data):
        """Validate our Friedman statistic against scipy's implementation."""
        # scipy uses ascending ranks, so we use maximize=False
        result = get_test(TestName.FRIEDMAN).run(multi_algorithm_data, maximize=False)
        scipy_stat, scipy_p = friedmanchisquare(
            multi_algorithm_data["Algorithm A"],
            multi_algorithm_data["Algorithm B"],
            multi_algorithm_data["Algorithm C"],
        )
        np.testing.assert_allclose(result.statistic, scipy_stat, rtol=0.05)
        np.testing.assert_allclose(result.p_value, scipy_p, rtol=0.05)

    def test_average_ranks_in_metadata(self, multi_algorithm_data):
        result = get_test(TestName.FRIEDMAN).run(multi_algorithm_data, maximize=True)
        assert "average_ranks" in result.metadata
        assert len(result.metadata["average_ranks"]) == 3


class TestFriedmanAligned:
    def test_returns_result(self, multi_algorithm_data):
        result = get_test(TestName.FRIEDMAN_ALIGNED).run(multi_algorithm_data, maximize=True)
        assert isinstance(result, StatisticalTestResult)
        assert result.statistic > 0
        assert 0 <= result.p_value <= 1

    def test_raises_on_single_column(self):
        data = pd.DataFrame({"A": [1, 2, 3]})
        with pytest.raises(StatisticalTestError):
            get_test(TestName.FRIEDMAN_ALIGNED).run(data, maximize=True)


class TestQuade:
    def test_returns_result(self, multi_algorithm_data):
        result = get_test(TestName.QUADE).run(multi_algorithm_data, maximize=True)
        assert isinstance(result, StatisticalTestResult)
        assert result.statistic > 0
        assert 0 <= result.p_value <= 1

    def test_raises_on_single_column(self):
        data = pd.DataFrame({"A": [1, 2, 3]})
        with pytest.raises(StatisticalTestError):
            get_test(TestName.QUADE).run(data, maximize=True)


class TestAnova:
    def test_returns_result(self, multi_algorithm_data):
        result = get_test(TestName.ANOVA).run(multi_algorithm_data, maximize=True)
        assert isinstance(result, StatisticalTestResult)
        assert result.statistic > 0
        assert 0 <= result.p_value <= 1

    def test_raises_on_single_column(self):
        data = pd.DataFrame({"A": [1, 2, 3]})
        with pytest.raises(StatisticalTestError):
            get_test(TestName.ANOVA).run(data, maximize=True)
