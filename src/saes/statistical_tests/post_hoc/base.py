"""Abstract base class for post-hoc APV correction procedures."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class BasePostHocTest(ABC):
    """Abstract base for p-value adjustment (APV) procedures.

    Post-hoc tests adjust the raw p-values from pairwise comparisons
    to control the family-wise error rate when performing multiple
    comparisons.
    """

    @abstractmethod
    def adjust(self, p_values: pd.DataFrame, *, control: int | None = None) -> pd.DataFrame:
        """Compute adjusted p-values.

        Args:
            p_values: DataFrame of raw p-values.
            control: Index of the control algorithm for one-vs-all
                comparisons.  ``None`` for all-vs-all.

        Returns:
            DataFrame with adjusted p-values.
        """

    @staticmethod
    def _extract_arrays(
        p_values: pd.DataFrame | np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Extract numeric values and algorithm names from p-values input.

        Returns:
            Tuple of ``(values_array, algorithm_names)``.
        """
        if isinstance(p_values, pd.DataFrame):
            algorithms = np.asarray(p_values.columns)
            values = p_values.values
        else:
            algorithms = np.array([f"Alg{i}" for i in range(p_values.shape[1])])
            values = p_values
        return values, algorithms
