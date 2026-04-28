"""Histogram plot visualization for algorithm performance comparison."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from saes.data.enums import ColumnName
from saes.visualization.base import BasePlot
from saes.visualization.registry import PlotName, register_plot


@register_plot(PlotName.HISTOGRAM)
class Histogram(BasePlot):
    """Histogram with KDE comparing algorithm distributions per instance."""

    @property
    def _prefix(self) -> str:
        return "histogram"

    def _plot_single(self, data: pd.DataFrame, ax: plt.Axes, instance: str) -> None:
        for algorithm in self.algorithms:
            alg_data = data[data[ColumnName.ALGORITHM] == algorithm].copy()

            # Avoid issues with identical values (seaborn KDE fails)
            if alg_data[ColumnName.METRIC_VALUE].nunique() <= 1:
                alg_data = alg_data.copy()
                alg_data.loc[:, ColumnName.METRIC_VALUE] = alg_data[
                    ColumnName.METRIC_VALUE
                ] + np.random.uniform(1e-5, 2e-5, size=len(alg_data))

            sns.histplot(
                alg_data[ColumnName.METRIC_VALUE],
                kde=True,
                label=algorithm,
                element="bars",
                ax=ax,
            )

        ax.legend()
        ax.set_title(f"Instance: {instance}", fontsize=self.theme.title_fontsize, fontweight="bold")
        ax.set_ylabel("Frequency", fontsize=self.theme.label_fontsize, fontweight="bold")
        ax.set_xlabel(self.metric, fontsize=self.theme.label_fontsize, fontweight="bold")
        ax.grid(axis="y", linestyle="-", alpha=self.theme.grid_alpha)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", bottom=False)
