"""Friedman rank-sum test for comparing multiple algorithms."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2

from saes.exceptions import StatisticalTestError
from saes.logger import get_logger
from saes.statistical_tests._ranking import compute_ranks
from saes.statistical_tests.base import BaseOmnibusTest, StatisticalTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)


@register_test(TestName.FRIEDMAN)
class FriedmanTest(BaseOmnibusTest):
    """Friedman rank-sum test for non-parametric multi-algorithm comparison.

    The Friedman test is a non-parametric statistical test used to detect
    differences in treatments across multiple groups.  The null hypothesis
    is that all algorithms perform equivalently, implying their average
    ranks should be equal.

    Reference:
        Friedman, M. (1937). *The use of ranks to avoid the assumption of
        normality implicit in the analysis of variance.* JASA 32(200).

    Formula:
        ``χ²_F = (12·n) / (k·(k+1)) · [Σ R̄²_j - k·(k+1)²/4]``

        where *n* = number of instances, *k* = number of algorithms,
        and *R̄_j* = average rank of algorithm *j*.

    See Also:
        https://en.wikipedia.org/wiki/Friedman_test
    """

    def run(self, data: pd.DataFrame, *, maximize: bool) -> StatisticalTestResult:
        """Execute the Friedman test.

        Args:
            data: DataFrame where each column is an algorithm and each row
                is a problem instance.
            maximize: If ``True``, higher values are better.

        Returns:
            A :class:`StatisticalTestResult` with the Friedman statistic
            and its p-value (χ² distribution with *k-1* degrees of freedom).

        Raises:
            StatisticalTestError: If the data has fewer than 2 columns.
        """
        values = data.values if isinstance(data, pd.DataFrame) else data
        n_instances, k = values.shape

        if k < 2:
            msg = "Friedman test requires at least 2 algorithms (columns)."
            raise StatisticalTestError(msg)

        logger.debug("Running Friedman test: %d instances × %d algorithms", n_instances, k)

        # Compute ranks per instance (row)
        ranks = compute_ranks(values, maximize=maximize)
        average_ranks = np.mean(ranks, axis=0)

        # Friedman statistic: χ²_F = 12n/(k(k+1)) * [Σ R̄_j² - k(k+1)²/4]
        sum_avg_ranks_sq = np.sum(average_ranks**2)
        statistic = (
            (12.0 * n_instances) / (k * (k + 1)) * (sum_avg_ranks_sq - k * (k + 1) ** 2 / 4.0)
        )

        p_value = 1.0 - chi2.cdf(statistic, df=k - 1)

        logger.debug("Friedman statistic=%.4f, p-value=%.4e", statistic, p_value)

        return StatisticalTestResult(
            statistic=float(statistic),
            p_value=float(p_value),
            test_name="Friedman",
            metadata={"average_ranks": average_ranks},
        )
