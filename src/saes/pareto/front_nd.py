"""N-D Pareto front visualization via parallel coordinates."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from saes.config import ThemeConfig
from saes.pareto.base import BaseFront
from saes.visualization.registry import PlotName, register_plot


@register_plot(PlotName.FRONT_ND)
class FrontND(BaseFront):
    """N-D Pareto front parallel coordinate plots."""

    def __init__(
        self,
        fronts_path: str,
        references_path: str,
        metric: str,
        dimensions: int,
        theme: ThemeConfig | None = None,
    ) -> None:
        super().__init__(fronts_path, references_path, metric, dimensions, theme=theme)

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
            df = pd.read_csv(fp, header=None, names=[f"f{j}" for j in range(self.dimensions)])
            df["Name"] = "Value"
            color = (
                self.theme.pareto_reference_color
                if name == "Reference"
                else self.theme.pareto_point_color
            )
            pd.plotting.parallel_coordinates(
                df, "Name", color=(color,), ax=axes[i], alpha=self.theme.pareto_point_alpha
            )
            axes[i].set_title(name)
            axes[i].get_legend().remove()
        plt.tight_layout()
