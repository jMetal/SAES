"""Tests for the statistical test registry and base classes."""

from __future__ import annotations

import pytest

from saes.exceptions import ConfigurationError
from saes.statistical_tests import TestName, get_test
from saes.statistical_tests.base import BaseOmnibusTest, BasePairwiseTest
from saes.statistical_tests.bayesian import BayesianSignedRankTest, BayesianSignTest
from saes.statistical_tests.omnibus import AnovaTest, FriedmanTest, QuadeTest
from saes.statistical_tests.pairwise import TTestPairwise, WilcoxonTest


class TestRegistry:
    """Tests for the test registry pattern."""

    def test_get_test_friedman(self):
        test = get_test(TestName.FRIEDMAN)
        assert isinstance(test, FriedmanTest)
        assert isinstance(test, BaseOmnibusTest)

    def test_get_test_wilcoxon(self):
        test = get_test(TestName.WILCOXON)
        assert isinstance(test, WilcoxonTest)
        assert isinstance(test, BasePairwiseTest)

    def test_get_test_anova(self):
        test = get_test(TestName.ANOVA)
        assert isinstance(test, AnovaTest)

    def test_get_test_quade(self):
        test = get_test(TestName.QUADE)
        assert isinstance(test, QuadeTest)

    def test_get_test_t_test(self):
        test = get_test(TestName.T_TEST)
        assert isinstance(test, TTestPairwise)

    def test_get_test_bayesian_sign(self):
        test = get_test(TestName.BAYESIAN_SIGN)
        assert isinstance(test, BayesianSignTest)

    def test_get_test_bayesian_signed_rank(self):
        test = get_test(TestName.BAYESIAN_SIGNED_RANK)
        assert isinstance(test, BayesianSignedRankTest)

    def test_get_test_unknown_raises(self):
        with pytest.raises(ConfigurationError, match="Unknown test"):
            get_test("nonexistent_test")

    def test_get_test_case_insensitive(self):
        test = get_test("FRIEDMAN")
        assert isinstance(test, FriedmanTest)
