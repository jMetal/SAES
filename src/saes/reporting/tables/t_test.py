"""T-test tables for pairwise algorithm comparison."""

from __future__ import annotations

import pandas as pd

from saes.data.enums import ColumnName
from saes.reporting._formatting import format_cell
from saes.reporting.base import BaseTable
from saes.reporting.registry import TableName, register_table
from saes.statistical_tests import TestName, get_test


@register_table(TableName.T_TEST)
class TTestTable(BaseTable):
    """Table with mean/std and t-test significance per instance."""

    @property
    def table_name(self) -> str:
        return "TTest"

    def __repr__(self) -> str:
        return "T-Test Table"

    def compute_table(self) -> None:
        self.compute_base_table()
        if self.mean_median is None:
            return
        self.table = self.mean_median.copy()

        test = get_test(TestName.T_TEST)
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
            # Test first vs second algorithm if possible
            alg_cols = list(pivot.columns[:2])
            if len(alg_cols) < 2:
                self.table.loc[instance, "T-Test"] = "?"
                continue

            # No cast needed due to overloads
            result = test.run(pivot[alg_cols], maximize=self.maximize)
            self.table.loc[instance, "T-Test"] = result.verdict

    def _create_latex_body(self) -> str:
        body = ""
        for instance in self.instances:
            mm, si, best, second = self.rank_top_two(instance)
            cells = []
            for alg in self.algorithms:
                cells.append(
                    format_cell(mm[alg], si[alg], is_best=(alg == best), is_second=(alg == second))
                )
            ttest_val = self.table.loc[instance, "T-Test"] if self.table is not None else "?"
            cells.append(str(ttest_val))
            body += f"{instance} & " + " & ".join(cells) + " \\\\ \n"
        return body


@register_table(TableName.T_TEST_PIVOT)
class TTestPivotTable(BaseTable):
    """Pivot table: one algorithm vs all others with t-test verdicts."""

    def __init__(
        self,
        data: str | pd.DataFrame,
        metrics: str | pd.DataFrame,
        metric: str,
        pivot_algorithm: str | None = None,
        normal: bool = False,
    ) -> None:
        super().__init__(data, metrics, metric, normal=normal)
        self.pivot_algorithm = pivot_algorithm or str(self.algorithms[0])

    @property
    def table_name(self) -> str:
        return "TTestPivot"

    def __repr__(self) -> str:
        return f"T-Test Pivot Table ({self.pivot_algorithm} vs all)"

    def compute_table(self) -> None:
        self.compute_base_table()
        others = [a for a in self.algorithms if a != self.pivot_algorithm]
        self.table = pd.DataFrame(index=self.instances, columns=others)

        test = get_test(TestName.T_TEST)
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
            for other in others:
                if self.pivot_algorithm in pivot.columns and other in pivot.columns:
                    # No cast needed due to overloads
                    result = test.run(pivot[[self.pivot_algorithm, other]], maximize=self.maximize)
                    self.table.loc[instance, other] = result.verdict
                else:
                    self.table.loc[instance, other] = "?"

    def _create_latex_body(self) -> str:
        body = ""
        if self.table is not None:
            for instance in self.instances:
                cells = [str(self.table.loc[instance, col]) for col in self.table.columns]
                body += f"{instance} & " + " & ".join(cells) + " \\\\ \n"
        return body
