"""SAES: Statistical Analysis and Evaluation for Software.

A library for robust statistical comparison of algorithm performance.
"""

from __future__ import annotations

from saes.config import ThemeConfig, default_theme
from saes.data.enums import ColumnName
from saes.exceptions import DataLoadError, SAESException, StatisticalTestError
from saes.logger import get_logger
from saes.reporting.registry import TableName, get_table
from saes.statistical_tests import TestName, get_test
from saes.visualization import PlotName, get_plot

__all__ = [
    "SAESException",
    "DataLoadError",
    "StatisticalTestError",
    "get_logger",
    "get_test",
    "TestName",
    "get_plot",
    "PlotName",
    "get_table",
    "TableName",
    "ThemeConfig",
    "default_theme",
    "ColumnName",
]
