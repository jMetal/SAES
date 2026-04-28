"""Tests for the pareto module."""

from __future__ import annotations

import pytest

from saes.pareto import Front2D, Front3D, FrontND


@pytest.fixture
def mock_fronts_dir(tmp_path):
    """Creates a mock directory structure for Pareto fronts."""
    fronts = tmp_path / "fronts"
    fronts.mkdir()

    for alg in ["Alg1", "Alg2"]:
        alg_dir = fronts / alg
        alg_dir.mkdir()
        for inst in ["Inst1", "Inst2"]:
            inst_dir = alg_dir / inst
            inst_dir.mkdir()
            (inst_dir / "MEDIAN_HV_FUN.csv").write_text("0.1,0.2\n0.3,0.4")

    refs = tmp_path / "refs"
    refs.mkdir()
    (refs / "Inst1.2D.csv").write_text("0.0,0.0")
    (refs / "Inst2.2D.csv").write_text("0.0,0.0")

    return fronts, refs


class TestPareto:
    def test_front_2d_initialization(self, mock_fronts_dir):
        fronts, refs = mock_fronts_dir
        plot = Front2D(str(fronts), str(refs), "HV")
        assert "Alg1" in plot.algorithms
        assert "Inst1" in plot.instances
        assert plot.dimensions == 2

    def test_front_3d_initialization(self, mock_fronts_dir):
        fronts, refs = mock_fronts_dir
        plot = Front3D(str(fronts), str(refs), "HV")
        assert plot.dimensions == 3

    def test_front_nd_initialization(self, mock_fronts_dir):
        fronts, refs = mock_fronts_dir
        plot = FrontND(str(fronts), str(refs), "HV", dimensions=4)
        assert plot.dimensions == 4
