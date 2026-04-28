"""Tests for pairwise statistical tests (Wilcoxon, T-test)."""

from __future__ import annotations

import pandas as pd
import pytest

from saes.statistical_tests import TestName, get_test
from saes.statistical_tests.base import PairwiseTestResult


@pytest.fixture
def equal_data():
    return pd.DataFrame({"Algorithm A": [0.5, 0.6, 0.7], "Algorithm B": [0.5, 0.6, 0.7]})


@pytest.fixture
def different_data():
    return pd.DataFrame(
        {
            "Algorithm A": [0.9, 0.85, 0.95, 0.9, 0.85, 0.95],
            "Algorithm B": [0.1, 0.2, 0.3, 0.1, 0.2, 0.3],
        }
    )


class TestWilcoxon:
    def test_equal_data_returns_eq(self, equal_data):
        result = get_test(TestName.WILCOXON).run(equal_data, maximize=True)
        assert isinstance(result, PairwiseTestResult)
        assert result.verdict == "="

    def test_different_data_returns_verdict(self, different_data):
        result = get_test(TestName.WILCOXON).run(different_data, maximize=True)
        assert result.verdict in ["+", "-"]

    def test_p_value_in_range(self, different_data):
        result = get_test(TestName.WILCOXON).run(different_data, maximize=True)
        assert 0 <= result.p_value <= 1


class TestTTest:
    def test_equal_data_returns_eq(self, equal_data):
        result = get_test(TestName.T_TEST).run(equal_data, maximize=True)
        assert result.verdict == "="

    def test_different_data_returns_verdict(self, different_data):
        result = get_test(TestName.T_TEST).run(different_data, maximize=True)
        assert result.verdict in ["+", "-"]

    def test_p_value_in_range(self, different_data):
        result = get_test(TestName.T_TEST).run(different_data, maximize=True)
        assert 0 <= result.p_value <= 1
