"""Abstract base class for all LaTeX statistical tables."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from saes.data.enums import ColumnName
from saes.data.processor import check_normality, process_dataframe_metric
from saes.logger import get_logger
from saes.reporting._formatting import latex_document_footer, latex_document_header

logger = get_logger(__name__)


def _highlight_max(table: pd.DataFrame) -> list[str]:
    """Highlight the maximum value in each row."""
    is_max = table[:-1] == table[:-1].max()
    return [*["background-color: green" if v else "" for v in is_max], ""]


def _highlight_min(table: pd.DataFrame) -> list[str]:
    """Highlight the minimum value in each row."""
    is_min = table[:-1] == table[:-1].min()
    return [*["background-color: green" if v else "" for v in is_min], ""]


class BaseTable(ABC):
    """Abstract base class for generating LaTeX statistical tables.

    Handles data loading, mean/median/IQR computation, and the common
    LaTeX document wrapping.  Subclasses implement the specific table
    body via :meth:`compute_table` and :meth:`_create_latex_body`.

    Args:
        data: Experiment data (DataFrame or CSV path).
        metrics: Metrics metadata (DataFrame or CSV path).
        metric: The metric to use.
        normal: If ``True``, use mean/std instead of median/IQR.
    """

    def __init__(
        self,
        data: str | pd.DataFrame,
        metrics: str | pd.DataFrame,
        metric: str,
        normal: bool = False,
    ) -> None:
        self.data, self.maximize = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.normality = check_normality(self.data)
        self.normal = normal
        self.algorithms: np.ndarray = self.data[ColumnName.ALGORITHM].unique()
        self.instances: np.ndarray = self.data[ColumnName.INSTANCE].unique()

        self.mean_median: pd.DataFrame | None = None
        self.std_iqr: pd.DataFrame | None = None
        self.table: pd.DataFrame | None = None
        self.latex_doc: str = ""

    # ── Public API ───────────────────────────────────────────────

    def save(
        self,
        output_path: str,
        file_name: str | None = None,
        sideways: bool = False,
    ) -> None:
        """Generate LaTeX and save to file."""
        self.create_latex_table(sideways=sideways)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)
        fname = file_name or f"{self.table_name}_{self.metric}.tex"
        (out / fname).write_text(self.latex_doc)
        logger.info("%s table saved to %s", fname, output_path)

    def create_latex_table(self, sideways: bool = False) -> None:
        """Build the full LaTeX document string."""
        self.compute_table()
        doc = latex_document_header()
        doc += "\\begin{sidewaystable}" if sideways else "\\begin{table}[H]"
        doc += self._latex_table_header()
        doc += self._create_latex_body()
        doc += self._latex_table_footer(sideways)
        doc += latex_document_footer()
        self.latex_doc = doc

    def show(self) -> Any:
        """Display the table in a Jupyter notebook."""
        self.compute_table()
        if self.table is None:
            msg = "Table not computed."
            raise RuntimeError(msg)
        highlight_fn = _highlight_max if self.maximize else _highlight_min
        # Use type: ignore for pandas styler which has complex generic types
        styled = self.table.style.apply(highlight_fn, axis=1)  # type: ignore
        styled.format(dict.fromkeys(self.table.select_dtypes(include=["number"]).columns, "{:.4e}"))
        return styled

    # ── Base table computation ───────────────────────────────────

    def compute_base_table(self) -> None:
        """Compute mean/median and std/IQR grouped by instance × algorithm."""
        if self.normal:
            g1 = self.data.groupby([ColumnName.INSTANCE, ColumnName.ALGORITHM])[
                ColumnName.METRIC_VALUE
            ]
            df1 = g1.agg(["mean", "std"])
            self.mean_median = df1["mean"].unstack()
            self.std_iqr = df1["std"].unstack()
        else:
            g2 = self.data.groupby([ColumnName.INSTANCE, ColumnName.ALGORITHM])[
                ColumnName.METRIC_VALUE
            ]
            df2 = g2.agg(
                median="median",
                Q1=lambda x: x.quantile(0.25),
                Q3=lambda x: x.quantile(0.75),
            )
            self.mean_median = df2["median"].unstack()
            self.std_iqr = (df2["Q3"] - df2["Q1"]).unstack()

        if self.mean_median is not None:
            self.mean_median = self.mean_median[self.algorithms].reindex(self.instances)
            self.mean_median.index.name = None
            self.mean_median.columns.name = None

        if self.std_iqr is not None:
            self.std_iqr = self.std_iqr[self.algorithms].reindex(self.instances)
            self.std_iqr.index.name = None
            self.std_iqr.columns.name = None

    def rank_top_two(self, instance: str) -> tuple:
        """Return the first and second best algorithms for a given instance."""
        if self.mean_median is None or self.std_iqr is None:
            msg = "Call compute_base_table() first."
            raise RuntimeError(msg)

        mm = self.mean_median.loc[instance]
        si = self.std_iqr.loc[instance]

        if self.maximize:
            best = mm.idxmax()
            second = mm.drop(best).idxmax()
        else:
            best = mm.idxmin()
            second = mm.drop(best).idxmin()

        if mm[best] == mm[second]:
            best = si.idxmin()
            second = si.drop(best).idxmin()

        return mm, si, best, second

    # ── Abstract interface ───────────────────────────────────────

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Short name used for file names."""

    @abstractmethod
    def compute_table(self) -> None:
        """Compute the specific table data."""

    @abstractmethod
    def _create_latex_body(self) -> str:
        """Generate the LaTeX table body rows."""

    # ── LaTeX helpers ────────────────────────────────────────────

    def _latex_table_header(self) -> str:
        """Generate the LaTeX tabular header."""
        cols = "|".join(["c"] * (len(self.algorithms) - 1)) + "c"
        header = f"""
        \\\\
        \\caption{{{self.metric}. {self!r}}}
        \\vspace{{1mm}}
        \\centering
        \\begin{{scriptsize}}
        \\begin{{tabular}}{{l|{cols}}}
        \\hline
        & {" & ".join(self.algorithms)} \\\\ \\hline
        """
        return header

    @staticmethod
    def _latex_table_footer(sideways: bool) -> str:
        """Generate the LaTeX tabular footer."""
        footer = """
        \\end{tabular}
        \\end{scriptsize}
        """
        footer += "\\end{sidewaystable}" if sideways else "\\end{table}"
        return footer
