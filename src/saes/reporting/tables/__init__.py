"""Reporting table implementations."""

from __future__ import annotations

from saes.reporting.tables.anova import AnovaTable
from saes.reporting.tables.friedman import FriedmanPValuesTable, FriedmanTable
from saes.reporting.tables.mean_median import MeanMedianTable
from saes.reporting.tables.t_test import TTestPivotTable, TTestTable
from saes.reporting.tables.wilcoxon import WilcoxonPivotTable, WilcoxonTable

__all__ = [
    "AnovaTable",
    "FriedmanPValuesTable",
    "FriedmanTable",
    "MeanMedianTable",
    "TTestPivotTable",
    "TTestTable",
    "WilcoxonPivotTable",
    "WilcoxonTable",
]
