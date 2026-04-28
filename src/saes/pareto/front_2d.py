"""2-D Pareto front visualization."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from saes.config import ThemeConfig
from saes.pareto.base import BaseFront
from saes.visualization.registry import PlotName, register_plot


@register_plot(PlotName.FRONT_2D)
class Front2D(BaseFront):
    """2-D Pareto front scatter plots."""

    def __init__(
        self, fronts_path: str, references_path: str, metric: str, theme: ThemeConfig | None = None
    ) -> None:
        super().__init__(fronts_path, references_path, metric, 2, theme=theme)

    def _front(self, front_paths: list[Path], instance: str) -> None:
        ref_path = self.references_path / f"{instance}.{self.dimensions}D.csv"
        all_paths = [ref_path, *front_paths]
        all_names = ["Reference", *self.algorithms]
        num_plots = len(all_paths)
        rows = int(num_plots**0.5)
        cols = (num_plots + rows - 1) // rows

        _, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 6))
        axes = axes.flatten()

        for i, (fp, name) in enumerate(zip(all_paths, all_names, strict=False)):
            if not fp.exists():
                msg = f"Front {fp} not found"
                raise FileNotFoundError(msg)
            df = pd.read_csv(fp, header=None)
            color = (
                self.theme.pareto_reference_color
                if name == "Reference"
                else self.theme.pareto_point_color
            )
            axes[i].scatter(df[0], df[1], alpha=self.theme.pareto_point_alpha, color=color)
            axes[i].spines["top"].set_visible(False)
            axes[i].spines["right"].set_visible(False)
            axes[i].tick_params(axis="both", which="both", length=0)
            axes[i].set_title(name, pad=20)
            axes[i].grid(True, alpha=0.3)
        plt.tight_layout()
