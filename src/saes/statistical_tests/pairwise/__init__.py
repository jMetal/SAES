"""Pairwise statistical tests for two-algorithm comparison."""

from __future__ import annotations

from saes.statistical_tests.pairwise.t_test import TTestPairwise
from saes.statistical_tests.pairwise.wilcoxon import WilcoxonTest

__all__ = [
    "TTestPairwise",
    "WilcoxonTest",
]
