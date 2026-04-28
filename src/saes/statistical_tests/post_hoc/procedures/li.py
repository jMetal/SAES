"""Li procedure for adjusted p-value computation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from saes.exceptions import PostHocTestError
from saes.statistical_tests.post_hoc.base import BasePostHocTest


class Li(BasePostHocTest):
    """Li procedure for one-vs-all p-value adjustment."""

    def adjust(self, p_values: pd.DataFrame, *, control: int | None = None) -> pd.DataFrame:
        values, algorithms = self._extract_arrays(p_values)

        if control is None:
            msg = "Li requires a control algorithm."
            raise PostHocTestError(msg)

        k = values.shape[1]
        sorted_idx = np.argsort(values[0, :])

        apvs = np.zeros((k - 1, 1))
        comparisons = []
        for i in range(k - 1):
            comparisons.append(f"{algorithms[control]} vs {algorithms[sorted_idx[i]]}")
            p_second_largest = values[0, sorted_idx[-2]]
            p_i = values[0, sorted_idx[i]]
            apvs[i, 0] = min(p_second_largest, p_i / (p_i + 1.0 - p_second_largest))

        return pd.DataFrame(data=apvs, index=comparisons, columns=["Li"])
