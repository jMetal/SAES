"""Tests for the Nemenyi critical difference function."""

from __future__ import annotations

import pytest

from saes.statistical_tests.post_hoc import nemenyi_critical_difference


class TestNemenyiCD:
    def test_known_value(self):
        cd = nemenyi_critical_difference(0.05, 5, 2)
        assert cd == pytest.approx(41.45, abs=1.0)

    def test_more_datasets_smaller_cd(self):
        cd_small = nemenyi_critical_difference(0.05, 5, 10)
        cd_large = nemenyi_critical_difference(0.05, 5, 50)
        assert cd_large < cd_small

    def test_more_algorithms_larger_cd(self):
        cd_few = nemenyi_critical_difference(0.05, 3, 10)
        cd_many = nemenyi_critical_difference(0.05, 10, 10)
        assert cd_many > cd_few
