"""Wilcoxon signed-rank test for pairwise algorithm comparison."""

from __future__ import annotations

import warnings

import pandas as pd
from scipy.stats import wilcoxon as scipy_wilcoxon

from saes.logger import get_logger
from saes.statistical_tests.base import BasePairwiseTest, PairwiseTestResult
from saes.statistical_tests.registry import TestName, register_test

logger = get_logger(__name__)


@register_test(TestName.WILCOXON)
class WilcoxonTest(BasePairwiseTest):
    """Wilcoxon signed-rank test for non-parametric pairwise comparison.

    Compares the performance of two algorithms across multiple instances.
    The null hypothesis is that the two algorithms perform equivalently.

    Reference:
        Wilcoxon, F. (1945). *Individual comparisons by ranking methods.*
        Biometrics Bulletin 1(6), 80–83.

    See Also:
        https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test
    """

    def run(
        self,
        data: pd.DataFrame,
        *,
        maximize: bool,
        alpha: float = 0.05,
    ) -> PairwiseTestResult:
        """Execute the Wilcoxon signed-rank test.

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

        median_a = data[col_a].median()
        median_b = data[col_b].median()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            _, p_value = scipy_wilcoxon(data[col_a], data[col_b])

        p_value = float(p_value)

        if p_value <= alpha:
            if maximize:
                verdict = "+" if median_a > median_b else "-"
            else:
                verdict = "+" if median_a <= median_b else "-"
        else:
            verdict = "="

        logger.debug(
            "Wilcoxon %s vs %s: p=%.4e, verdict=%s",
            col_a,
            col_b,
            p_value,
            verdict,
        )

        return PairwiseTestResult(
            verdict=verdict,
            p_value=p_value,
            test_name="Wilcoxon",
        )
