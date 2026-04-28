"""Enumerations for standardizing data column names."""

from __future__ import annotations

from enum import StrEnum


class ColumnName(StrEnum):
    """Standard column names used in SAES data structures."""

    ALGORITHM = "Algorithm"
    INSTANCE = "Instance"
    METRIC_VALUE = "MetricValue"
    METRIC_NAME = "MetricName"
    EXECUTION_ID = "ExecutionId"
    MAXIMIZE = "Maximize"
