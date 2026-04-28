"""Quade test for comparing multiple algorithms."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.stats import f as f_dist

from saes.exceptions import StatisticalTestError
from saes.logger import get_logger
from saes.statistical_tests._ranking import compute_ranks
from saes.statistical_tests.base import BaseOmnibusTest, StatisticalTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)


@register_test(TestName.QUADE)
class QuadeTest(BaseOmnibusTest):
    """Quade test for non-parametric multi-algorithm comparison.

    The Quade test weights each instance by the range of its observations,
    giving more influence to instances where the algorithms differ most.
    The test statistic follows an *F*-distribution under the null hypothesis.

    Reference:
        Quade, D. (1979). *Using weighted rankings in the analysis of
        complete blocks with additive block effects.* JASA 74(367).
    """

    def run(self, data: pd.DataFrame, *, maximize: bool) -> StatisticalTestResult:
        """Execute the Quade test.

        Args:
            data: DataFrame where each column is an algorithm and each row
                is a problem instance.
            maximize: If ``True``, higher values are better.

        Returns:
            A :class:`StatisticalTestResult` with the Quade *F*-statistic
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
            msg = "Quade test requires at least 2 algorithms."
            raise StatisticalTestError(msg)

        logger.debug("Running Quade test: %d instances × %d algorithms", n_instances, k)

        # Rank within each instance
        data_ranks = compute_ranks(values, maximize=maximize)

        # Rank the ranges of each instance
        problem_range = np.max(values, axis=1) - np.min(values, axis=1)
        problem_rank = compute_ranks(problem_range, maximize=maximize)

        # Weighted ranks
        s_stat = np.zeros((n_instances, k))
        for i in range(n_instances):
            s_stat[i, :] = problem_rank[i] * (data_ranks[i, :] - 0.5 * (k + 1))

        s_alg = np.sum(s_stat, axis=0)

        # Quade F-statistic
        a = np.sum(s_stat**2)
        b = np.sum(s_alg**2) / float(n_instances)

        if a == b:
            statistic = float(np.inf)
            p_value = (1.0 / math.factorial(k)) ** (n_instances - 1)
        else:
            statistic = float((n_instances - 1.0) * b / (a - b))
            p_value = float(1.0 - f_dist.cdf(statistic, k - 1, (k - 1) * (n_instances - 1)))

        logger.debug("Quade F-statistic=%.4f, p-value=%.4e", statistic, p_value)

        return StatisticalTestResult(
            statistic=statistic,
            p_value=p_value,
            test_name="Quade",
        )
