"""Tests for Bayesian statistical tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from saes.exceptions import ConfigurationError, StatisticalTestError
from saes.statistical_tests import TestName, get_test
from saes.statistical_tests.base import BayesianTestResult


@pytest.fixture
def data_a_better():
    return pd.DataFrame(
        {
            "Algorithm_A": [0.9, 0.85, 0.95, 0.9, 0.92, 0.88, 0.91, 0.89],
            "Algorithm_B": [0.5, 0.6, 0.55, 0.58, 0.52, 0.54, 0.56, 0.57],
        }
    )


@pytest.fixture
def data_equivalent():
    return pd.DataFrame(
        {
            "Algorithm_A": [0.5, 0.6, 0.7, 0.55, 0.65],
            "Algorithm_B": [0.5, 0.6, 0.7, 0.55, 0.65],
        }
    )


class TestBayesianSignTest:
    def test_basic(self, data_a_better):
        result = get_test(TestName.BAYESIAN_SIGN).run(data_a_better, seed=42)
        assert isinstance(result, BayesianTestResult)
        assert result.probabilities.shape == (3,)
        np.testing.assert_allclose(result.probabilities.sum(), 1.0, atol=1e-5)

    def test_a_better(self, data_a_better):
        result = get_test(TestName.BAYESIAN_SIGN).run(data_a_better, sample_size=5000, seed=42)
        assert result.probabilities[2] > 0.5

    def test_equivalent(self, data_equivalent):
        result = get_test(TestName.BAYESIAN_SIGN).run(data_equivalent, sample_size=5000, seed=42)
        assert result.probabilities[1] > result.probabilities[0]
        assert result.probabilities[1] > result.probabilities[2]

    def test_invalid_prior_strength(self, data_a_better):
        with pytest.raises(ConfigurationError):
            get_test(TestName.BAYESIAN_SIGN).run(data_a_better, prior_strength=0)

    def test_invalid_prior_place(self, data_a_better):
        with pytest.raises(ConfigurationError):
            get_test(TestName.BAYESIAN_SIGN).run(data_a_better, prior_place="invalid")

    def test_wrong_columns(self):
        bad = pd.DataFrame({"A": [1], "B": [2], "C": [3]})
        with pytest.raises(StatisticalTestError):
            get_test(TestName.BAYESIAN_SIGN).run(bad)

    def test_reproducibility(self, data_a_better):
        r1 = get_test(TestName.BAYESIAN_SIGN).run(data_a_better, seed=42)
        r2 = get_test(TestName.BAYESIAN_SIGN).run(data_a_better, seed=42)
        np.testing.assert_array_almost_equal(r1.probabilities, r2.probabilities)


class TestBayesianSignedRank:
    def test_basic(self, data_a_better):
        result = get_test(TestName.BAYESIAN_SIGNED_RANK).run(
            data_a_better, sample_size=500, seed=42
        )
        assert isinstance(result, BayesianTestResult)
        assert result.probabilities.shape == (3,)
        np.testing.assert_allclose(result.probabilities.sum(), 1.0, atol=1e-5)

    def test_a_better(self, data_a_better):
        result = get_test(TestName.BAYESIAN_SIGNED_RANK).run(
            data_a_better, sample_size=500, seed=42
        )
        assert result.probabilities[2] > 0.5

    def test_invalid_prior_strength(self, data_a_better):
        with pytest.raises(ConfigurationError):
            get_test(TestName.BAYESIAN_SIGNED_RANK).run(data_a_better, prior_strength=-1)

    def test_invalid_prior_place(self, data_a_better):
        with pytest.raises(ConfigurationError):
            get_test(TestName.BAYESIAN_SIGNED_RANK).run(data_a_better, prior_place="invalid")

    def test_wrong_columns(self):
        bad = pd.DataFrame({"A": [1], "B": [2], "C": [3]})
        with pytest.raises(StatisticalTestError):
            get_test(TestName.BAYESIAN_SIGNED_RANK).run(bad)
