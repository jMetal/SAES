"""Reporting module — LaTeX table generation with registry architecture.

Usage::

    from saes.reporting import MeanMedianTable, FriedmanTable

    table = MeanMedianTable(data, metrics, "HV")
    table.save(output_path)
"""

from __future__ import annotations

from saes.reporting.base import BaseTable
from saes.reporting.tables.anova import AnovaTable
from saes.reporting.tables.friedman import FriedmanPValuesTable, FriedmanTable
from saes.reporting.tables.mean_median import MeanMedianTable
from saes.reporting.tables.t_test import TTestPivotTable, TTestTable
from saes.reporting.tables.wilcoxon import WilcoxonPivotTable, WilcoxonTable

__all__ = [
    "AnovaTable",
    "BaseTable",
    "FriedmanPValuesTable",
    "FriedmanTable",
    "MeanMedianTable",
    "TTestPivotTable",
    "TTestTable",
    "WilcoxonPivotTable",
    "WilcoxonTable",
]
