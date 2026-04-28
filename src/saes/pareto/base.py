"""Abstract base class for Pareto front visualization."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import matplotlib.pyplot as plt

from saes.config import ThemeConfig, default_theme
from saes.logger import get_logger

logger = get_logger(__name__)


class BaseFront(ABC):
    """Abstract base for Pareto front plots.

    Args:
        fronts_path: Path to the folder containing algorithm fronts.
        references_path: Path to the folder containing reference fronts.
        metric: The quality indicator metric name.
        dimensions: Number of objectives (2, 3, or N).
    """

    def __init__(
        self,
        fronts_path: str,
        references_path: str,
        metric: str,
        dimensions: int,
        theme: ThemeConfig | None = None,
    ) -> None:
        self.theme = theme or default_theme
        fp = Path(fronts_path)
        if not fp.is_dir():
            msg = f"Fronts path '{fronts_path}' not found or is not a directory."
            raise FileNotFoundError(msg)

        self.fronts_path = fp
        self.references_path = Path(references_path)
        self.metric = metric
        self.dimensions = dimensions

        self.algorithms = sorted(
            d.name for d in fp.iterdir() if d.is_dir() and d != self.references_path
        )

        first_alg = fp / self.algorithms[0]
        self.instances = sorted(d.name for d in first_alg.iterdir() if d.is_dir())

    def save(
        self, instance: str, output_path: str, file_name: str | None = None, median: bool = True
    ) -> None:
        """Generate and save a Pareto front plot."""
        median_best = "MEDIAN" if median else "BEST"
        front_paths = [
            self.fronts_path / alg / instance / f"{median_best}_{self.metric}_FUN.csv"
            for alg in self.algorithms
        ]
        self._front(front_paths, instance)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"front_all_{instance}_{self.metric}_{median_best}.png"
        plt.savefig(out / fname, bbox_inches="tight")
        logger.info("Front %s saved to %s", fname, output_path)
        plt.close()

    def show(self, instance: str, median: bool = True) -> None:
        """Generate and display a Pareto front plot."""
        median_best = "MEDIAN" if median else "BEST"
        front_paths = [
            self.fronts_path / alg / instance / f"{median_best}_{self.metric}_FUN.csv"
            for alg in self.algorithms
        ]
        self._front(front_paths, instance)
        plt.show()

    @abstractmethod
    def _front(self, front_paths: list[Path], instance: str) -> None:
        """Render the Pareto front plot."""
