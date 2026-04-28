"""Tests for the visualization registry and plot classes."""

from __future__ import annotations

import pandas as pd
import pytest

from saes.visualization import PlotName, get_plot
from saes.visualization.base import BasePlot
from saes.visualization.plots.boxplot import Boxplot
from saes.visualization.plots.cd_plot import CDPlot
from saes.visualization.plots.histogram import Histogram
from saes.visualization.plots.posterior import PosteriorPlot
from saes.visualization.plots.violin import Violin


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Algorithm": ["Alg1", "Alg1", "Alg2", "Alg2"],
            "Instance": ["Inst1", "Inst2", "Inst1", "Inst2"],
            "MetricName": ["HV", "HV", "HV", "HV"],
            "MetricValue": [0.9, 0.8, 0.7, 0.6],
            "ExecutionId": [0, 0, 0, 0],
        }
    )


@pytest.fixture
def sample_metrics():
    return pd.DataFrame({"MetricName": ["HV"], "Maximize": [True]})


class TestVisualizationRegistry:
    def test_get_boxplot(self, sample_data, sample_metrics):
        plot = get_plot(PlotName.BOXPLOT, data=sample_data, metrics=sample_metrics, metric="HV")
        assert isinstance(plot, Boxplot)
        assert isinstance(plot, BasePlot)

    def test_get_violin(self, sample_data, sample_metrics):
        plot = get_plot(PlotName.VIOLIN, data=sample_data, metrics=sample_metrics, metric="HV")
        assert isinstance(plot, Violin)

    def test_get_histogram(self, sample_data, sample_metrics):
        plot = get_plot(PlotName.HISTOGRAM, data=sample_data, metrics=sample_metrics, metric="HV")
        assert isinstance(plot, Histogram)

    def test_get_cd_plot(self, sample_data, sample_metrics):
        plot = get_plot(PlotName.CD_PLOT, data=sample_data, metrics=sample_metrics, metric="HV")
        assert isinstance(plot, CDPlot)

    def test_get_posterior(self, sample_data, sample_metrics):
        plot = get_plot(PlotName.POSTERIOR, data=sample_data, metrics=sample_metrics, metric="HV")
        assert isinstance(plot, PosteriorPlot)
