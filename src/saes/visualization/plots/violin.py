"""Violin plot visualization for algorithm performance comparison."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from saes.data.enums import ColumnName
from saes.visualization.base import BasePlot
from saes.visualization.registry import PlotName, register_plot


@register_plot(PlotName.VIOLIN)
class Violin(BasePlot):
    """Violin plot comparing algorithm distributions per instance."""

    @property
    def _prefix(self) -> str:
        return "violin"

    def _plot_single(self, data: pd.DataFrame, ax: plt.Axes, instance: str) -> None:
        sns.violinplot(
            data=data,
            x=ColumnName.ALGORITHM,
            y=ColumnName.METRIC_VALUE,
            ax=ax,
            inner="box",
        )

        ax.set_title(
            f"Instance: {instance}",
            fontsize=self.theme.title_fontsize,
            fontweight="bold",
        )
        ax.set_ylabel(self.metric, fontsize=self.theme.label_fontsize, fontweight="bold")
        ax.set_xlabel("")
        ax.grid(axis="y", linestyle="-", alpha=self.theme.grid_alpha)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", bottom=False)
        ax.set_xticklabels(
            ax.get_xticklabels(), rotation=15, fontsize=self.theme.label_fontsize, fontweight="bold"
        )
