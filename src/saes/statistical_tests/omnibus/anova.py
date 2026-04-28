"""ANOVA (Analysis of Variance) test for comparing multiple algorithms."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from saes.exceptions import StatisticalTestError
from saes.logger import get_logger
from saes.statistical_tests.base import BaseOmnibusTest, StatisticalTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)


@register_test(TestName.ANOVA)
class AnovaTest(BaseOmnibusTest):
    """One-way ANOVA test for parametric multi-algorithm comparison.

    ANOVA tests whether the means of *k* groups differ significantly.
    It assumes that the data in each group is normally distributed and
    has equal variance.

    Note:
        For non-normal data, prefer a non-parametric alternative such as
        :class:`~saes.statistical_tests.omnibus.friedman.FriedmanTest`.
    """

    def run(self, data: pd.DataFrame, *, maximize: bool) -> StatisticalTestResult:
        """Execute the one-way ANOVA test.

        Args:
            data: DataFrame where each column is an algorithm and each row
                is a problem instance.
            maximize: Unused for ANOVA (kept for interface consistency).

        Returns:
            A :class:`StatisticalTestResult` with the *F*-statistic and
            its p-value.

        Raises:
            StatisticalTestError: If the data has fewer than 2 columns.
        """
        values = data.values if isinstance(data, pd.DataFrame) else data

        _, k = values.shape
        if k < 2:
            msg = "ANOVA test requires at least 2 algorithms (columns)."
            raise StatisticalTestError(msg)

        logger.debug("Running ANOVA test with %d algorithms", k)

        # scipy's f_oneway expects each group as a separate argument
        groups = [values[:, j] for j in range(k)]
        f_statistic, p_value = stats.f_oneway(*groups)

        # Handle NaN results (e.g., identical data)
        f_statistic = float(np.nan_to_num(f_statistic, nan=0.0))
        p_value = float(np.nan_to_num(p_value, nan=1.0))

        logger.debug("ANOVA F-statistic=%.4f, p-value=%.4e", f_statistic, p_value)

        return StatisticalTestResult(
            statistic=f_statistic,
            p_value=p_value,
            test_name="ANOVA",
        )
