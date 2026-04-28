"""Paired t-test for pairwise algorithm comparison."""

from __future__ import annotations

import pandas as pd
from scipy import stats

from saes.logger import get_logger
from saes.statistical_tests.base import BasePairwiseTest, PairwiseTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)


@register_test(TestName.T_TEST)
class TTestPairwise(BasePairwiseTest):
    """Paired t-test for parametric pairwise algorithm comparison.

    Uses the related-samples t-test (``scipy.stats.ttest_rel``) to compare
    two algorithms.  Assumes the paired differences are approximately
    normally distributed.
    """

    def run(
        self,
        data: pd.DataFrame,
        *,
        maximize: bool,
        alpha: float = 0.05,
    ) -> PairwiseTestResult:
        """Execute the paired t-test.

        Args:
            data: DataFrame with exactly two columns representing the
                performance of two algorithms across instances.
            maximize: If ``True``, higher values are better.
            alpha: Significance level.

        Returns:
            A :class:`PairwiseTestResult` with verdict ``"+"``, ``"-"``,
            or ``"="``.
        """
        columns = list(data.columns)
        col_a, col_b = columns[0], columns[1]

        mean_a = data[col_a].mean()
        mean_b = data[col_b].mean()

        _, p_value = stats.ttest_rel(data[col_a], data[col_b])
        p_value = float(p_value)

        if p_value <= alpha:
            if maximize:
                verdict = "+" if mean_a > mean_b else "-"
            else:
                verdict = "+" if mean_a <= mean_b else "-"
        else:
            verdict = "="

        logger.debug(
            "T-test %s vs %s: p=%.4e, verdict=%s",
            col_a,
            col_b,
            p_value,
            verdict,
        )

        return PairwiseTestResult(
            verdict=verdict,
            p_value=p_value,
            test_name="T-Test",
        )
