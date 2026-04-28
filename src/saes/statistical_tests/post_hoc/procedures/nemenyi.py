"""Nemenyi procedure and critical difference computation."""

from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.stats.libqsturng import qsturng

from saes.exceptions import PostHocTestError
from saes.statistical_tests.post_hoc.base import BasePostHocTest


def nemenyi_critical_difference(alpha: float, num_algorithms: int, num_datasets: int) -> float:
    """Compute Nemenyi's Critical Difference (CD) for post-hoc analysis.

    Formula:
        ``CD = q_α / √2 · √(k·(k+1) / (6·n))``

    where *k* = number of algorithms, *n* = number of datasets, and
    *q_α* is the critical value from the Studentized range distribution.

    Args:
        alpha: Significance level.
        num_algorithms: Number of algorithms being compared (*k*).
        num_datasets: Number of datasets/instances (*n*).

    Returns:
        The critical difference value.
    """
    q_alpha = qsturng(p=1 - alpha, r=num_algorithms, v=num_datasets - 1) / np.sqrt(2)
    return float(q_alpha * np.sqrt(num_algorithms * (num_algorithms + 1) / (6.0 * num_datasets)))


class Nemenyi(BasePostHocTest):
    """Nemenyi procedure for all-vs-all p-value adjustment.

    Simply multiplies each p-value by the total number of comparisons
    ``m = k·(k-1)/2`` and caps at 1.0.
    """

    def adjust(self, p_values: pd.DataFrame, *, control: int | None = None) -> pd.DataFrame:
        values, algorithms = self._extract_arrays(p_values)

        if values.ndim != 2 or values.shape[0] != values.shape[1]:
            msg = "Nemenyi requires a square p-value matrix (all-vs-all)."
            raise PostHocTestError(msg)

        k = values.shape[0]
        m = int(k * (k - 1) / 2)

        pairs_index = np.triu_indices(k, 1)
        pairs_pvals = values[pairs_index]
        pairs_sorted = np.argsort(pairs_pvals)

        apvs = np.zeros((m, 1))
        comparisons = []
        for i in range(m):
            row = pairs_index[0][pairs_sorted[i]]
            col = pairs_index[1][pairs_sorted[i]]
            comparisons.append(f"{algorithms[row]} vs {algorithms[col]}")
            apvs[i, 0] = min(pairs_pvals[pairs_sorted[i]] * m, 1.0)

        return pd.DataFrame(data=apvs, index=comparisons, columns=["Nemenyi"])
