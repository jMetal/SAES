"""Posterior probability plot for Bayesian algorithm comparison.

Reference:
    Benavoli, A. et al. (2017). *Time for a change: a tutorial for
    comparing multiple classifiers through Bayesian analysis.*
    https://arxiv.org/pdf/1606.04316
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from saes.config import ThemeConfig, default_theme
from saes.data.enums import ColumnName
from saes.data.processor import process_dataframe_metric
from saes.logger import get_logger
from saes.statistical_tests.bayesian import BayesianSignedRankTest, BayesianSignTest
from saes.visualization.registry import PlotName, register_plot

logger = get_logger(__name__)


def _barycentric_to_cartesian(p: np.ndarray) -> np.ndarray:
    """Convert barycentric coordinates to 2-D Cartesian for simplex display."""
    lambda1, lambda2, lambda3 = p.T
    x = 0.1 * lambda1 + 0.5 * lambda2 + 0.9 * lambda3
    y = (0.2 * lambda1 + 1.4 * lambda2 + 0.2 * lambda3) / np.sqrt(3)
    return np.vstack((x, y)).T


def _draw_simplex(
    ax: plt.Axes,
    data: np.ndarray,
    *,
    maximize: bool,
    alg_names: list[str],
    min_points_per_hexbin: int = 2,
    show_colorbar: bool = True,
) -> None:
    """Draw the posterior probability simplex on a given axes."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()

    # Labels depend on maximize direction
    if maximize:
        label_left = f"{alg_names[1]} +"
        label_right = f"{alg_names[0]} +"
    else:
        label_left = f"{alg_names[0]} +"
        label_right = f"{alg_names[1]} +"

    ax.text(x=0.5, y=1.4 / np.sqrt(3) + 0.005, s="no-diff", ha="center", va="bottom", weight="bold")
    ax.text(x=0.35, y=0.175 / np.sqrt(3) - 0.005, s=label_left, ha="right", va="top", weight="bold")
    ax.text(x=0.75, y=0.175 / np.sqrt(3) - 0.005, s=label_right, ha="left", va="top", weight="bold")

    # Convert to 2-D
    sample2d = _barycentric_to_cartesian(data)

    # Plot hexbin
    hb = ax.hexbin(sample2d[:, 0], sample2d[:, 1], mincnt=min_points_per_hexbin, cmap="plasma")

    if show_colorbar:
        cb = plt.colorbar(hb, ax=ax, orientation="vertical", fraction=0.05, pad=0.0, shrink=0.6)
        cb.set_label("Count")

    # Draw simplex boundary (white) and internal divisions (orange)
    sqrt3 = np.sqrt(3)
    for color, pairs in [
        (
            "white",
            [
                ([0.095, 0.505], [0.2 / sqrt3, 1.4 / sqrt3]),
                ([0.505, 0.905], [1.4 / sqrt3, 0.2 / sqrt3]),
                ([0.09, 0.905], [0.2 / sqrt3, 0.2 / sqrt3]),
            ],
        ),
        (
            "orange",
            [
                ([0.5, 0.5], [0.2 / sqrt3, 0.6 / sqrt3]),
                ([0.3, 0.5], [0.8 / sqrt3, 0.6 / sqrt3]),
                ([0.5, 0.7], [0.6 / sqrt3, 0.8 / sqrt3]),
                ([0.1, 0.5], [0.2 / sqrt3, 1.4 / sqrt3]),
                ([0.5, 0.9], [1.4 / sqrt3, 0.2 / sqrt3]),
                ([0.1, 0.9], [0.2 / sqrt3, 0.2 / sqrt3]),
            ],
        ),
    ]:
        for xs, ys in pairs:
            ax.plot(xs, ys, linewidth=3.0, color=color)


@register_plot(PlotName.POSTERIOR)
class PosteriorPlot:
    """Posterior probability simplex plot for Bayesian test results.

    Visualises the Dirichlet posterior samples as a hexbin heatmap
    projected onto a 2-D simplex.

    Args:
        data: Experiment data (DataFrame or CSV path).
        metrics: Metrics metadata (DataFrame or CSV path).
        metric: The metric to visualize.
        bayesian_test: ``"sign"`` or ``"rank"``.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        metrics: pd.DataFrame,
        metric: str,
        bayesian_test: str = "sign",
        theme: ThemeConfig | None = None,
    ) -> None:
        if bayesian_test not in ("sign", "rank"):
            msg = "bayesian_test must be 'sign' or 'rank'."
            raise ValueError(msg)

        self.theme = theme or default_theme

        self.data, self.maximize = process_dataframe_metric(data, metrics, metric)
        self.algorithms = self.data[ColumnName.ALGORITHM].unique()
        self.metric = metric
        self._test_cls = BayesianSignTest if bayesian_test == "sign" else BayesianSignedRankTest

    def save(
        self,
        alg1: str,
        alg2: str,
        output_path: str,
        file_name: str | None = None,
        width: int = 5,
        sample_size: int = 2500,
    ) -> None:
        """Render and save the posterior plot for two algorithms."""
        samples = self._compute_posterior(alg1, alg2, sample_size)
        fig = plt.figure(figsize=(width, width), facecolor="white")
        ax = fig.add_axes((0, 0, 1, 1))
        _draw_simplex(ax, samples, maximize=self.maximize, alg_names=[alg1, alg2])
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"{self.metric}_{alg1}_vs_{alg2}.png"
        plt.savefig(out / fname, bbox_inches="tight")
        plt.close()
        logger.info("PosteriorPlot %s saved to %s", fname, output_path)

    def show(
        self,
        alg1: str,
        alg2: str,
        width: int = 5,
        sample_size: int = 2500,
    ) -> None:
        """Render and display the posterior plot for two algorithms."""
        samples = self._compute_posterior(alg1, alg2, sample_size)
        fig = plt.figure(figsize=(width, width), facecolor="white")
        ax = fig.add_axes((0, 0, 1, 1))
        _draw_simplex(ax, samples, maximize=self.maximize, alg_names=[alg1, alg2])
        plt.show()

    def save_pivot(
        self,
        algorithm: str,
        output_path: str,
        file_name: str | None = None,
        width: int = 30,
        height: int = 15,
        sample_size: int = 2500,
    ) -> None:
        """Render and save the posterior plots of one algorithm vs all others."""
        self._plot_pivot(algorithm, width, height, sample_size)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"{self.metric}_pivot_{algorithm}.png"
        plt.savefig(out / fname, bbox_inches="tight")
        plt.close()
        logger.info("PosteriorPlot %s saved to %s", fname, output_path)

    def show_pivot(
        self,
        algorithm: str,
        width: int = 30,
        height: int = 15,
        sample_size: int = 2500,
    ) -> None:
        """Render and display the posterior plots of one algorithm vs all others."""
        self._plot_pivot(algorithm, width, height, sample_size)
        plt.show()

    def _plot_pivot(self, algorithm: str, width: int, height: int, sample_size: int) -> None:
        others = [a for a in self.algorithms if a != algorithm]
        num_plots = len(others)
        ncols = min(3, num_plots)
        nrows = (num_plots + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))
        flat = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        for idx, other in enumerate(others):
            samples = self._compute_posterior(algorithm, other, sample_size)
            _draw_simplex(
                flat[idx],
                samples,
                maximize=self.maximize,
                alg_names=[algorithm, other],
                show_colorbar=False,
            )

        for i in range(num_plots, len(flat)):
            fig.delaxes(flat[i])

        plt.tight_layout()

    def _compute_posterior(self, alg1: str, alg2: str, sample_size: int) -> np.ndarray:
        """Compute posterior samples across all executions."""
        filtered = self.data[self.data[ColumnName.ALGORITHM].isin([alg1, alg2])]
        exec_min = int(filtered[ColumnName.EXECUTION_ID].min())
        exec_max = int(filtered[ColumnName.EXECUTION_ID].max()) + 1

        test = self._test_cls()
        all_samples: list[np.ndarray] = []

        for i in range(exec_min, exec_max):
            data_i = filtered[filtered[ColumnName.EXECUTION_ID] == i]
            data_i = data_i.pivot(
                index=ColumnName.INSTANCE,
                columns=ColumnName.ALGORITHM,
                values=ColumnName.METRIC_VALUE,
            )
            data_i = data_i[[alg1, alg2]]

            result = test.run(data_i, sample_size=sample_size)
            all_samples.append(result.samples)

        return np.vstack(all_samples) if all_samples else np.empty((0, 3))
