"""ANOVA table for algorithm performance comparison."""

from __future__ import annotations

from saes.data.enums import ColumnName
from saes.reporting._formatting import format_cell
from saes.reporting.base import BaseTable
from saes.reporting.registry import TableName, register_table
from saes.statistical_tests import TestName, get_test


@register_table(TableName.ANOVA)
class AnovaTable(BaseTable):
    """Table showing mean/std with ANOVA test significance per instance."""

    @property
    def table_name(self) -> str:
        return "Anova"

    def __repr__(self) -> str:
        return "ANOVA Test Table"

    def compute_table(self) -> None:
        self.compute_base_table()
        if self.mean_median is None:
            return
        self.table = self.mean_median.copy()

        test = get_test(TestName.ANOVA)
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
            # No cast needed due to overloads
            result = test.run(pivot, maximize=self.maximize)
            self.table.loc[instance, "Anova"] = "+" if result.is_significant else "="

    def _create_latex_body(self) -> str:
        body = ""
        for instance in self.instances:
            mm, si, best, second = self.rank_top_two(instance)
            cells = []
            for alg in self.algorithms:
                cells.append(
                    format_cell(mm[alg], si[alg], is_best=(alg == best), is_second=(alg == second))
                )
            anova_val = self.table.loc[instance, "Anova"] if self.table is not None else "?"
            cells.append(str(anova_val))
            body += f"{instance} & " + " & ".join(cells) + " \\\\ \n"
        return body
