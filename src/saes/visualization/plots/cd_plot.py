"""Critical Difference (CD) plot for non-parametric multi-algorithm comparison.

Reference:
    Demšar, J. (2006). *Statistical Comparisons of Classifiers over
    Multiple Data Sets.* JMLR 7, 1–30.
    https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import rankdata

from saes.config import ThemeConfig, default_theme
from saes.data.enums import ColumnName
from saes.data.processor import process_dataframe_metric
from saes.logger import get_logger
from saes.statistical_tests.post_hoc import nemenyi_critical_difference
from saes.visualization.registry import PlotName, register_plot

logger = get_logger(__name__)


@register_plot(PlotName.CD_PLOT)
class CDPlot:
    """Critical Difference plot comparing algorithm average ranks.

    Unlike distribution plots (boxplot, violin), this is a standalone
    statistical visualisation that does not extend :class:`BasePlot`.

    Args:
        data: Experiment data (DataFrame or CSV path).
        metrics: Metrics metadata (DataFrame or CSV path).
        metric: The metric to visualize.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        metrics: pd.DataFrame,
        metric: str,
        theme: ThemeConfig | None = None,
    ) -> None:
        processed_data, maximize = process_dataframe_metric(data, metrics, metric)
        self.theme = theme or default_theme

        # Build a mean-median table: instances × algorithms
        table = (
            processed_data.groupby([ColumnName.INSTANCE, ColumnName.ALGORITHM])[
                ColumnName.METRIC_VALUE
            ]
            .median()
            .unstack()
        )

        self.table = table
        self.maximize = maximize
        self.metric = metric

    def save(self, output_path: str, file_name: str | None = None, width: int = 9) -> None:
        """Render and save the CD plot."""
        self._plot(width=width)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"cdplot_{self.metric}.png"
        plt.savefig(out / fname, bbox_inches="tight")
        plt.close()
        logger.info("CDplot %s saved to %s", fname, output_path)

    def show(self, width: int = 9) -> None:
        """Render and display the CD plot."""
        self._plot(width=width)
        plt.show()

    # ── Private implementation ───────────────────────────────────

    def _plot(self, width: int, alpha: float = 0.05) -> None:
        """Create the critical difference plot."""
        alg_names = np.array(self.table.columns)
        data = self.table.values
        num_dataset, num_alg = data.shape

        # Get the critical difference
        cd = nemenyi_critical_difference(alpha, num_alg, num_dataset)

        # Compute ranks
        rranks = rankdata(-data, axis=1) if self.maximize else rankdata(data, axis=1)
        avranks = np.mean(rranks, axis=0)
        indices = np.argsort(avranks).astype(np.uint8)
        avranks = avranks[indices]

        # Split algorithms into left and right halves
        spoint = int(np.round(num_alg / 2.0))
        leftalg = avranks[:spoint]
        rightalg = avranks[spoint:]
        rows = int(np.ceil(num_alg / 2.0))

        # Figure settings
        highest = int(np.ceil(np.max(avranks)))
        lowest = int(np.floor(np.min(avranks)))

        height = width * (0.8625 * (rows + 1) / 9)
        stop, sbottom, sleft, sright = 0.65, 0.1, 0.15, 0.85
        lline = sright - sleft

        fig = plt.figure(figsize=(width, height), facecolor="white")
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()

        # Main horizontal axis
        ax.hlines(stop, sleft, sright, color="black", linewidth=3)
        for xi in range(highest - lowest + 1):
            ax.vlines(
                x=sleft + (lline * xi) / (highest - lowest),
                ymin=stop,
                ymax=stop + 0.05,
                color="black",
                linewidth=2,
            )
            ax.text(
                x=sleft + (lline * xi) / (highest - lowest),
                y=stop + 0.06,
                s=str(lowest + xi),
                ha="center",
                va="bottom",
            )
            if xi < highest - lowest:
                ax.vlines(
                    x=sleft + (lline * (xi + 0.5)) / (highest - lowest),
                    ymin=stop,
                    ymax=stop + 0.025,
                    color="black",
                    linewidth=0.7,
                )

        # Left models
        vspace = 0.5 * (stop - sbottom) / (spoint + 1)
        for i in range(spoint):
            x_pos = sleft + (lline * (leftalg[i] - lowest)) / (highest - lowest)
            ax.vlines(
                x=x_pos,
                ymin=sbottom + (spoint - 1 - i) * vspace,
                ymax=stop,
                color="red",
                linewidth=1,
            )
            ax.hlines(
                y=sbottom + (spoint - 1 - i) * vspace,
                xmin=sleft,
                xmax=x_pos,
                color="red",
                linewidth=1,
            )
            ax.text(
                x=sleft - 0.01,
                y=sbottom + (spoint - 1 - i) * vspace,
                s=f"$\\mathbf{{{alg_names[indices][i]}}}$",
                ha="right",
                va="center",
            )

        # Right models
        vspace = 0.5 * (stop - sbottom) / (num_alg - spoint + 1)
        for i in range(num_alg - spoint):
            x_pos = sleft + (lline * (rightalg[i] - lowest)) / (highest - lowest)
            ax.vlines(x=x_pos, ymin=sbottom + i * vspace, ymax=stop, color="green", linewidth=1)
            ax.hlines(y=sbottom + i * vspace, xmin=x_pos, xmax=sright, color="green", linewidth=1)
            ax.text(
                x=sright + 0.01,
                y=sbottom + i * vspace,
                s=f"$\\mathbf{{{alg_names[indices][spoint + i]}}}$",
                ha="left",
                va="center",
            )

        # Critical difference ruler
        cd_width = (cd * lline) / (highest - lowest)
        if sleft + cd_width <= sright:
            ax.hlines(y=stop + 0.2, xmin=sleft, xmax=sleft + cd_width, linewidth=1.5)
            ax.text(
                x=sleft + 0.5 * cd_width,
                y=stop + 0.21,
                s=f"CD={cd:.3f}",
                ha="center",
                va="bottom",
            )
        else:
            ax.text(
                x=(sleft + sright) / 2,
                y=stop + 0.2,
                s=f"$\\mathbf{{CD={cd:.3f}}}$",
                ha="center",
                va="bottom",
            )

        # Non-significant cliques
        nonsig = self._join_alg(avranks, num_alg, cd)
        if nonsig.size > 0:
            if nonsig.ndim == 1:
                nonsig = nonsig.reshape(1, -1)

            half = int(np.round(nonsig.shape[0] / 2.0))
            left_lines = nonsig[:half, :]

            if nonsig.shape[0] >= 2:
                right_lines = nonsig[half:, :]
            else:
                right_lines = np.array([]).reshape(0, 2)

            vspace = 0.5 * (stop - sbottom) / (left_lines.shape[0] + 1)
            for i in range(left_lines.shape[0]):
                ax.hlines(
                    y=stop - (i + 1) * vspace,
                    xmin=sleft + lline * (left_lines[i, 0] - lowest - 0.025) / (highest - lowest),
                    xmax=sleft + lline * (left_lines[i, 1] - lowest + 0.025) / (highest - lowest),
                    linewidth=2,
                )

            if right_lines.shape[0] > 0:
                vspace = 0.5 * (stop - sbottom) / (left_lines.shape[0])
                for i in range(right_lines.shape[0]):
                    ax.hlines(
                        y=stop - (i + 1) * vspace,
                        xmin=sleft
                        + lline * (right_lines[i, 0] - lowest - 0.025) / (highest - lowest),
                        xmax=sleft
                        + lline * (right_lines[i, 1] - lowest + 0.025) / (highest - lowest),
                        linewidth=2,
                    )

    @staticmethod
    def _join_alg(avranks: np.ndarray, num_alg: int, cd: float) -> np.ndarray:
        """Compute sets of non-significantly different methods."""
        sets = -np.ones((num_alg, 2))
        for i in range(num_alg):
            elements = np.where(
                np.logical_and(avranks - avranks[i] > 0, avranks - avranks[i] < cd)
            )[0]
            if elements.size > 0:
                sets[i, :] = [avranks[i], avranks[elements[-1]]]

        sets = np.delete(sets, np.where(sets[:, 0] < 0)[0], axis=0)
        if sets.size == 0:
            return sets

        group = sets[0, :]
        for i in range(1, sets.shape[0]):
            if sets[i - 1, 1] < sets[i, 1]:
                group = np.vstack((group, sets[i, :]))

        return group
