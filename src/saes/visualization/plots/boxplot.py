"""Boxplot visualization for algorithm performance comparison."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from saes.data.enums import ColumnName
from saes.visualization.base import BasePlot
from saes.visualization.registry import PlotName, register_plot


@register_plot(PlotName.BOXPLOT)
class Boxplot(BasePlot):
    """Boxplot comparing algorithm distributions per instance."""

    @property
    def _prefix(self) -> str:
        return "boxplot"

    def _plot_single(self, data: pd.DataFrame, ax: plt.Axes, instance: str) -> None:
        algorithms = self.algorithms
        plot_data = [
            data[data[ColumnName.ALGORITHM] == alg][ColumnName.METRIC_VALUE].values
            for alg in algorithms
        ]

        bp = ax.boxplot(plot_data, patch_artist=True)

        # Style the boxes
        for patch in bp["boxes"]:
            patch.set_facecolor(self.theme.primary_color)
            patch.set_edgecolor(self.theme.edge_color)

        ax.set_xticklabels(
            algorithms, rotation=15, fontsize=self.theme.label_fontsize, fontweight="bold"
        )
        ax.set_title(
            f"Instance: {instance}",
            fontsize=self.theme.title_fontsize,
            fontweight="bold",
        )
        ax.set_ylabel(self.metric, fontsize=self.theme.label_fontsize, fontweight="bold")
        ax.grid(axis="y", linestyle="-", alpha=self.theme.grid_alpha)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", bottom=False)
