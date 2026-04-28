"""Holm procedure for adjusted p-value computation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from saes.statistical_tests.post_hoc.base import BasePostHocTest


class Holm(BasePostHocTest):
    """Holm step-down procedure for p-value adjustment.

    Supports both one-vs-all (with ``control``) and all-vs-all
    (without ``control``) comparisons.
    """

    def adjust(self, p_values: pd.DataFrame, *, control: int | None = None) -> pd.DataFrame:
        values, algorithms = self._extract_arrays(p_values)

        if isinstance(control, int):
            return self._one_vs_all(values, algorithms, control)
        return self._all_vs_all(values, algorithms)

    @staticmethod
    def _one_vs_all(values: np.ndarray, algorithms: np.ndarray, control: int) -> pd.DataFrame:
        k = values.shape[1]
        sorted_idx = np.argsort(values[0, :])

        apvs = np.zeros((k - 1, 1))
        comparisons = []
        for i in range(k - 1):
            aux = k - 1 - np.arange(i + 1)
            comparisons.append(f"{algorithms[control]} vs {algorithms[sorted_idx[i]]}")
            v = np.max(aux * values[0, sorted_idx[: (i + 1)]])
            apvs[i, 0] = min(float(v), 1.0)

        return pd.DataFrame(data=apvs, index=comparisons, columns=["Holm"])

    @staticmethod
    def _all_vs_all(values: np.ndarray, algorithms: np.ndarray) -> pd.DataFrame:
        k = values.shape[1]
        m = int(k * (k - 1) / 2)

        pairs_index = np.triu_indices(k, 1)
        pairs_pvals = values[pairs_index]
        pairs_sorted = np.argsort(pairs_pvals)

        apvs = np.zeros((m, 1))
        aux = pairs_pvals[pairs_sorted] * (m - np.arange(m))
        comparisons = []
        for i in range(m):
            row = pairs_index[0][pairs_sorted[i]]
            col = pairs_index[1][pairs_sorted[i]]
            comparisons.append(f"{algorithms[row]} vs {algorithms[col]}")
            v = np.max(aux[: i + 1])
            apvs[i, 0] = min(float(v), 1.0)

        return pd.DataFrame(data=apvs, index=comparisons, columns=["Holm"])
