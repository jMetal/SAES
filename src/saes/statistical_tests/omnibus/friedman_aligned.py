"""Friedman aligned-rank test for comparing multiple algorithms."""

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


@register_test(TestName.FRIEDMAN_ALIGNED)
class FriedmanAlignedRankTest(BaseOmnibusTest):
    """Friedman aligned-rank test for non-parametric multi-algorithm comparison.

    Unlike the standard Friedman test, the aligned-rank variant first
    subtracts the instance mean from each observation and then ranks the
    differences globally.  This can improve power when instances have very
    different scales.

    Reference:
        Hodges, J. L. & Lehmann, E. L. (1962). *Rank methods for combination
        of independent experiments in analysis of variance.* Ann. Math.
        Statist. 33(2).
    """

    def run(self, data: pd.DataFrame, *, maximize: bool) -> StatisticalTestResult:
        """Execute the Friedman aligned-rank test.

        Args:
            data: DataFrame where each column is an algorithm and each row
                is a problem instance.
            maximize: If ``True``, higher values are better.

        Returns:
            A :class:`StatisticalTestResult` with the aligned-rank statistic
            and its p-value.

        Raises:
            StatisticalTestError: If the data has fewer than 2 columns or
                is not 2-dimensional.
        """
        values = data.values if isinstance(data, pd.DataFrame) else data

        if values.ndim != 2:
            msg = "Data must be a 2-D array."
            raise StatisticalTestError(msg)

        n_instances, k = values.shape

        if k < 2:
            msg = "Friedman aligned-rank test requires at least 2 algorithms."
            raise StatisticalTestError(msg)

        logger.debug(
            "Running Friedman aligned-rank test: %d instances × %d algorithms",
            n_instances,
            k,
        )

        # Compute per-instance means and aligned differences
        instance_means = np.mean(values, axis=1)
        diff = np.column_stack([values[:, j] - instance_means for j in range(k)])

        # Rank all aligned differences globally
        aligned_ranks = compute_ranks(np.ravel(diff), maximize=maximize)
        aligned_ranks = np.reshape(aligned_ranks, newshape=(n_instances, k), order="F")

        # Compute statistics
        r_hat_i = np.sum(aligned_ranks, axis=1)  # sum per instance
        r_hat_j = np.sum(aligned_ranks, axis=0)  # sum per algorithm

        si = np.sum(r_hat_i**2)
        sj = np.sum(r_hat_j**2)

        a = sj - (k * n_instances**2 / 4.0) * (k * n_instances + 1) ** 2
        b1 = k * n_instances * (k * n_instances + 1) * (2 * k * n_instances + 1) / 6.0
        b2 = si / float(k)

        statistic = ((k - 1) * a) / (b1 - b2)
        p_value = 1.0 - chi2.cdf(statistic, df=k - 1)

        logger.debug("Aligned-rank statistic=%.4f, p-value=%.4e", statistic, p_value)

        return StatisticalTestResult(
            statistic=float(statistic),
            p_value=float(p_value),
            test_name="Friedman Aligned Rank",
        )
