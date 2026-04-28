"""Abstract base class for distribution plots."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from saes.config import ThemeConfig, default_theme
from saes.data.enums import ColumnName
from saes.data.processor import process_dataframe_metric
from saes.logger import get_logger

logger = get_logger(__name__)


class BasePlot(ABC):
    """Abstract base for instance-based distribution plots.

    Subclasses implement :meth:`_plot_single` to render a single instance
    on a given matplotlib axes.  All save/show boilerplate is handled here
    via the Template Method pattern.

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
        self.data, self.maximize = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.algorithms: np.ndarray = self.data[ColumnName.ALGORITHM].unique()
        self.instances: np.ndarray = self.data[ColumnName.INSTANCE].unique()
        self.theme = theme or default_theme

    # ── Public API ───────────────────────────────────────────────

    def save_instance(
        self,
        instance: str,
        output_path: str,
        file_name: str | None = None,
        width: int = 8,
    ) -> None:
        """Render a single instance and save to disk."""
        self._plot_instance(instance, width=width)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"{self._prefix}_{self.metric}_{instance}.png"
        plt.savefig(out / fname, bbox_inches="tight")
        plt.close()
        logger.info("%s saved to %s", fname, output_path)

    def save_all_instances(
        self,
        output_path: str,
        file_name: str | None = None,
        width: int = 30,
    ) -> None:
        """Render all instances in a grid and save to disk."""
        self._plot_all_instances(width=width)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"{self._prefix}_{self.metric}_all.png"
        plt.savefig(out / fname, bbox_inches="tight")
        plt.close()
        logger.info("%s saved to %s", fname, output_path)

    def show_instance(self, instance: str, width: int = 8) -> None:
        """Render a single instance and display it."""
        self._plot_instance(instance, width=width)
        plt.show()

    def show_all_instances(self, width: int = 30) -> None:
        """Render all instances in a grid and display it."""
        self._plot_all_instances(width=width)
        plt.show()

    # ── Abstract interface ───────────────────────────────────────

    @property
    @abstractmethod
    def _prefix(self) -> str:
        """File name prefix (e.g. ``"boxplot"``, ``"violin"``)."""

    @abstractmethod
    def _plot_single(self, data: pd.DataFrame, ax: plt.Axes, instance: str) -> None:
        """Render one instance on the given axes.

        Args:
            data: Filtered data for this instance.
            ax: Matplotlib axes to draw on.
            instance: Instance name (for titles).
        """

    # ── Private implementation ───────────────────────────────────

    def _plot_instance(self, instance: str, width: int) -> None:
        fig, ax = plt.subplots(figsize=(width, width * 0.56))
        data_inst = self.data[self.data[ColumnName.INSTANCE] == instance].copy()
        self._plot_single(data_inst, ax, instance)
        plt.tight_layout()

    def _plot_all_instances(self, width: int) -> None:
        instances = self.instances
        n_cols = min(3, len(instances))
        n_rows = int(np.ceil(len(instances) / n_cols))

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(width, width * (n_rows / 4)))
        flat_axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        for i, instance in enumerate(instances):
            data_inst = self.data[self.data[ColumnName.INSTANCE] == instance].copy()
            self._plot_single(data_inst, flat_axes[i], instance)

        # Remove unused subplots
        for j in range(len(instances), len(flat_axes)):
            fig.delaxes(flat_axes[j])

        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.35, hspace=0.45)
