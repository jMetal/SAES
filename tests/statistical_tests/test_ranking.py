"""Tests for ranking utilities."""

from __future__ import annotations

import numpy as np

from saes.statistical_tests._ranking import compute_ranks


class TestComputeRanks:
    def test_ascending_simple(self):
        data = np.array([3.0, 1.0, 2.0])
        ranks = compute_ranks(data, maximize=False)
        np.testing.assert_array_equal(ranks, [3.0, 1.0, 2.0])

    def test_descending_simple(self):
        data = np.array([3.0, 1.0, 2.0])
        ranks = compute_ranks(data, maximize=True)
        np.testing.assert_array_equal(ranks, [1.0, 3.0, 2.0])

    def test_ties_averaged(self):
        data = np.array([1.0, 2.0, 2.0, 4.0])
        ranks = compute_ranks(data, maximize=False)
        np.testing.assert_array_equal(ranks, [1.0, 2.5, 2.5, 4.0])

    def test_2d_rows_ranked_independently(self):
        data = np.array([[3.0, 1.0, 2.0], [1.0, 2.0, 3.0]])
        ranks = compute_ranks(data, maximize=False)
        np.testing.assert_array_equal(ranks[0], [3.0, 1.0, 2.0])
        np.testing.assert_array_equal(ranks[1], [1.0, 2.0, 3.0])

    def test_all_equal(self):
        data = np.array([5.0, 5.0, 5.0])
        ranks = compute_ranks(data, maximize=False)
        np.testing.assert_array_equal(ranks, [2.0, 2.0, 2.0])
