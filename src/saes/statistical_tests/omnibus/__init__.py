"""Omnibus statistical tests for multi-algorithm comparison."""

from __future__ import annotations

from saes.statistical_tests.omnibus.anova import AnovaTest
from saes.statistical_tests.omnibus.friedman import FriedmanTest
from saes.statistical_tests.omnibus.friedman_aligned import FriedmanAlignedRankTest
from saes.statistical_tests.omnibus.quade import QuadeTest

__all__ = [
    "AnovaTest",
    "FriedmanAlignedRankTest",
    "FriedmanTest",
    "QuadeTest",
]
