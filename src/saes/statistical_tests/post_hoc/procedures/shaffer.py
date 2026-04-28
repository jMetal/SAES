"""Shaffer procedure for adjusted p-value computation."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import comb as binomial

from saes.exceptions import PostHocTestError
from saes.statistical_tests.post_hoc.base import BasePostHocTest


def _shaffer_true_hypotheses(k: int) -> list[int]:
    """Compute the set of possible numbers of true hypotheses.

    Args:
        k: Number of algorithms being compared.

    Returns:
        Sorted list of possible true hypothesis counts.
    """
    true_set: set[int] = {0}
    if k > 1:
        for j in range(k, 0, -1):
            sub = _shaffer_true_hypotheses(k - j)
            true_set |= {int(binomial(j, 2)) + x for x in sub}
    return sorted(true_set)


class Shaffer(BasePostHocTest):
    """Shaffer procedure for all-vs-all p-value adjustment.

    Uses the logical structure of the hypotheses to improve power
    over simpler methods like Nemenyi.
    """

    def adjust(self, p_values: pd.DataFrame, *, control: int | None = None) -> pd.DataFrame:
        values, algorithms = self._extract_arrays(p_values)

        if values.ndim != 2 or values.shape[0] != values.shape[1]:
            msg = "Shaffer requires a square p-value matrix (all-vs-all)."
            raise PostHocTestError(msg)

        k = values.shape[0]
        m = int(k * (k - 1) / 2)
        s = np.array(_shaffer_true_hypotheses(k)[1:])

        pairs_index = np.triu_indices(k, 1)
        pairs_pvals = values[pairs_index]
        pairs_sorted = np.argsort(pairs_pvals)

        # Compute ti: max number of hypotheses that can be true
        t = np.sort(-np.repeat(s[:-1], (s[1:] - s[:-1]).astype(int)))
        t = np.insert(-t, 0, s[-1])

        apvs = np.zeros((m, 1))
        aux = pairs_pvals[pairs_sorted] * t
        comparisons = []
        for i in range(m):
            row = pairs_index[0][pairs_sorted[i]]
            col = pairs_index[1][pairs_sorted[i]]
            comparisons.append(f"{algorithms[row]} vs {algorithms[col]}")
            v = np.max(aux[: i + 1])
            apvs[i, 0] = min(v, 1.0)

        return pd.DataFrame(data=apvs, index=comparisons, columns=["Shaffer"])
