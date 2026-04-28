"""Holland procedure for adjusted p-value computation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from saes.exceptions import PostHocTestError
from saes.statistical_tests.post_hoc.base import BasePostHocTest


class Holland(BasePostHocTest):
    """Holland procedure for one-vs-all p-value adjustment."""

    def adjust(self, p_values: pd.DataFrame, *, control: int | None = None) -> pd.DataFrame:
        values, algorithms = self._extract_arrays(p_values)

        if control is None:
            msg = "Holland requires a control algorithm."
            raise PostHocTestError(msg)

        k = values.shape[1]
        sorted_idx = np.argsort(values[0, :])

        apvs = np.zeros((k - 1, 1))
        comparisons = []
        for i in range(k - 1):
            comparisons.append(f"{algorithms[control]} vs {algorithms[sorted_idx[i]]}")
            aux = k - 1 - np.arange(i + 1)
            v = np.max(1.0 - (1.0 - values[0, sorted_idx[: (i + 1)]]) ** aux)
            apvs[i, 0] = min(v, 1.0)

        return pd.DataFrame(data=apvs, index=comparisons, columns=["Holland"])
