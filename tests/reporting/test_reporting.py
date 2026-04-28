"""Tests for the reporting module and LaTeX table generation."""

from __future__ import annotations

import pandas as pd
import pytest

from saes.reporting import FriedmanTable, MeanMedianTable


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Algorithm": ["Alg1", "Alg1", "Alg2", "Alg2"],
            "Instance": ["Inst1", "Inst1", "Inst1", "Inst1"],
            "MetricName": ["HV", "HV", "HV", "HV"],
            "MetricValue": [0.9, 0.95, 0.7, 0.75],
            "ExecutionId": [0, 1, 0, 1],
        }
    )


@pytest.fixture
def sample_metrics():
    return pd.DataFrame({"MetricName": ["HV"], "Maximize": [True]})


class TestReporting:
    def test_mean_median_table_computation(self, sample_data, sample_metrics):
        table = MeanMedianTable(sample_data, sample_metrics, "HV")
        table.compute_table()
        assert table.table is not None
        assert "Alg1" in table.table.columns
        assert "Alg2" in table.table.columns

    def test_rank_top_two(self, sample_data, sample_metrics):
        table = MeanMedianTable(sample_data, sample_metrics, "HV")
        table.compute_base_table()
        mm, si, best, second = table.rank_top_two("Inst1")
        assert best == "Alg1"
        assert second == "Alg2"

    def test_friedman_table(self, sample_data, sample_metrics):
        table = FriedmanTable(sample_data, sample_metrics, "HV")
        table.compute_table()
        assert "Friedman" in table.table.columns

    def test_latex_generation_header(self, sample_data, sample_metrics):
        table = MeanMedianTable(sample_data, sample_metrics, "HV")
        table.create_latex_table()
        assert "\\begin{table}" in table.latex_doc
        assert "\\caption{HV." in table.latex_doc
