"""Friedman table for algorithm performance comparison."""

from __future__ import annotations

import pandas as pd

from saes.data.enums import ColumnName
from saes.logger import get_logger
from saes.reporting._formatting import format_cell
from saes.reporting.base import BaseTable
from saes.reporting.registry import TableName, register_table
from saes.statistical_tests import TestName, get_test

logger = get_logger(__name__)

_FRIEDMAN_VARIANTS = {
    "base": TestName.FRIEDMAN,
    "aligned": TestName.FRIEDMAN_ALIGNED,
    "quade": TestName.QUADE,
}


@register_table(TableName.FRIEDMAN)
class FriedmanTable(BaseTable):
    """Table showing median/IQR with Friedman test significance per instance."""

    def __init__(
        self,
        data: str | pd.DataFrame,
        metrics: str | pd.DataFrame,
        metric: str,
        normal: bool = False,
        friedman_test: str = "base",
    ) -> None:
        super().__init__(data, metrics, metric, normal=normal)
        if friedman_test not in _FRIEDMAN_VARIANTS:
            msg = f"friedman_test must be one of {list(_FRIEDMAN_VARIANTS.keys())}"
            raise ValueError(msg)
        self._test_name = _FRIEDMAN_VARIANTS[friedman_test]

    @property
    def table_name(self) -> str:
        return "Friedman"

    def __repr__(self) -> str:
        return "Friedman Test Table"

    def compute_table(self) -> None:
        if self.normal:
            logger.warning("Friedman test is only applicable for non-normal data.")
            return

        self.compute_base_table()
        if self.mean_median is None:
            return
        self.table = self.mean_median.copy()

        test = get_test(self._test_name)
        if self.table is None:
            return

        for instance in self.instances:
            inst_data = self.data[self.data[ColumnName.INSTANCE] == instance]
            pivot = (
                inst_data.pivot(
                    index=ColumnName.EXECUTION_ID,
                    columns=ColumnName.ALGORITHM,
                    values=ColumnName.METRIC_VALUE,
                )
                .reset_index()
                .drop(columns=ColumnName.EXECUTION_ID)
            )
            from typing import cast

            from saes.statistical_tests.base import BaseOmnibusTest

            result = cast(BaseOmnibusTest, test).run(pivot, maximize=self.maximize)
            self.table.loc[instance, "Friedman"] = "+" if result.is_significant else "="

    def _create_latex_body(self) -> str:
        body = ""
        for instance in self.instances:
            mm, si, best, second = self.rank_top_two(instance)
            row = f"{instance} & "
            cells = []
            for alg in self.algorithms:
                cells.append(
                    format_cell(mm[alg], si[alg], is_best=(alg == best), is_second=(alg == second))
                )
            friedman_val = self.table.loc[instance, "Friedman"] if self.table is not None else "?"
            cells.append(str(friedman_val))
            row += " & ".join(cells) + " \\\\ \n"
            body += row
        return body


@register_table(TableName.FRIEDMAN_P_VALUES)
class FriedmanPValuesTable(BaseTable):
    """Table showing Friedman p-values per instance."""

    def __init__(
        self,
        data: str | pd.DataFrame,
        metrics: str | pd.DataFrame,
        metric: str,
        friedman_test: str = "base",
    ) -> None:
        super().__init__(data, metrics, metric, normal=False)
        if friedman_test not in _FRIEDMAN_VARIANTS:
            msg = f"friedman_test must be one of {list(_FRIEDMAN_VARIANTS.keys())}"
            raise ValueError(msg)
        self._test_name = _FRIEDMAN_VARIANTS[friedman_test]

    @property
    def table_name(self) -> str:
        return "FriedmanPValues"

    def __repr__(self) -> str:
        return "Friedman P-Values Table"

    def compute_table(self) -> None:
        self.compute_base_table()
        self.table = pd.DataFrame(index=self.instances, columns=["Statistic", "p-value"])

        test = get_test(self._test_name)
        if self.table is None:
            return

        for instance in self.instances:
            inst_data = self.data[self.data[ColumnName.INSTANCE] == instance]
            pivot = (
                inst_data.pivot(
                    index=ColumnName.EXECUTION_ID,
                    columns=ColumnName.ALGORITHM,
                    values=ColumnName.METRIC_VALUE,
                )
                .reset_index()
                .drop(columns=ColumnName.EXECUTION_ID)
            )
            from typing import cast

            from saes.statistical_tests.base import BaseOmnibusTest

            result = cast(BaseOmnibusTest, test).run(pivot, maximize=self.maximize)
            self.table.loc[instance, "Statistic"] = f"{result.statistic:.4e}"
            self.table.loc[instance, "p-value"] = f"{result.p_value:.4e}"

    def _create_latex_body(self) -> str:
        body = ""
        if self.table is not None:
            for instance in self.instances:
                stat = self.table.loc[instance, "Statistic"]
                pval = self.table.loc[instance, "p-value"]
                body += f"{instance} & {stat} & {pval} \\\\ \n"
        return body
