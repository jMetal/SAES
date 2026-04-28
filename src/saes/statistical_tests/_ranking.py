"""Internal ranking utilities for statistical tests."""

from __future__ import annotations

import numpy as np


def compute_ranks(data: np.ndarray, *, maximize: bool) -> np.ndarray:
    """Compute tied ranks for each row of a 2-D array.

    For each row, elements are ranked starting at 1. Ties receive the
    average of the ranks they would span.  When ``maximize=True`` the
    *largest* value gets rank 1 (descending); otherwise the *smallest*
    value gets rank 1 (ascending).

    Args:
        data: Array of shape ``(n_instances, k_algorithms)`` or ``(k,)``.
        maximize: If ``True``, rank in descending order (best = highest).

    Returns:
        Array of the same shape containing the ranks.

    Raises:
        ValueError: If *data* has more than 2 dimensions.
    """
    if data.ndim == 1:
        return _rank_1d(data, maximize=maximize)
    if data.ndim == 2:
        ranks = np.empty_like(data, dtype=float)
        for i in range(data.shape[0]):
            ranks[i, :] = _rank_1d(data[i, :], maximize=maximize)
        return ranks
    msg = f"Expected 1-D or 2-D array, got {data.ndim}-D"
    raise ValueError(msg)


def _rank_1d(row: np.ndarray, *, maximize: bool) -> np.ndarray:
    """Rank a single 1-D array with tied-rank averaging.

    Sorts ascending (``maximize=False``) or descending (``maximize=True``)
    and assigns average ranks to tied values.
    """
    n = row.size
    # Negate for descending sort when maximize=True
    values = -row if maximize else row.copy()

    # argsort gives the indices that would sort the array
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(n, dtype=float)

    i = 0
    while i < n:
        j = i
        # Find the end of the group of tied values
        while j < n - 1 and values[order[j]] == values[order[j + 1]]:
            j += 1
        # Average rank for the tied group (1-indexed)
        avg_rank = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1

    return ranks
