"""Data processing utilities for SAES experiment data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import shapiro

from saes.data.enums import ColumnName
from saes.exceptions import DataLoadError


def get_metrics(data: pd.DataFrame) -> list:
    """Extract unique metric names from the input data.

    Args:
        data: DataFrame containing an ``"MetricName"`` column.

    Returns:
        List of unique metric names.
    """
    return list(data[ColumnName.METRIC_NAME].unique())


def check_normality(data: pd.DataFrame) -> bool:
    """Check normality of grouped data using the Shapiro-Wilk test.

    Groups by ``"Algorithm"`` and ``"Instance"`` columns and tests the
    ``"MetricValue"`` column within each group.

    Args:
        data: DataFrame with columns ``"Algorithm"``, ``"Instance"``,
            and ``"MetricValue"``.

    Returns:
        ``True`` if all groups pass the Shapiro-Wilk test at α = 0.05.
    """
    grouped = data.groupby([ColumnName.ALGORITHM, ColumnName.INSTANCE])

    for _, group in grouped:
        values = group[ColumnName.METRIC_VALUE]
        if values.max() == values.min() or len(values) < 3:
            p_value = 0.0
        else:
            _, p_value = shapiro(values)

        if p_value <= 0.05:
            return False

    return True


def process_dataframe_metric(
    data: str | pd.DataFrame,
    metrics: str | pd.DataFrame,
    metric: str,
) -> tuple[pd.DataFrame, bool]:
    """Load and filter data for a specific metric.

    Args:
        data: Path to CSV file or DataFrame containing experiment data.
        metrics: Path to CSV file or DataFrame containing metric metadata.
        metric: The metric name to filter for.

    Returns:
        Tuple of ``(filtered_data, maximize)`` where *maximize* indicates
        whether higher values are better.

    Raises:
        DataLoadError: If the metric is not found.
    """
    df = pd.read_csv(data) if isinstance(data, (str, Path)) else data
    mf = pd.read_csv(metrics) if isinstance(metrics, (str, Path)) else metrics

    try:
        maximize = bool(mf[mf[ColumnName.METRIC_NAME] == metric][ColumnName.MAXIMIZE].values[0])
        filtered = df[df[ColumnName.METRIC_NAME] == metric].reset_index()
        return filtered, maximize
    except (IndexError, KeyError) as e:
        msg = f"Metric '{metric}' not found in the metrics DataFrame."
        raise DataLoadError(msg) from e
