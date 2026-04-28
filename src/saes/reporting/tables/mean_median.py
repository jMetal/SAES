"""Mean/Median table for algorithm performance comparison."""

from __future__ import annotations

from saes.reporting._formatting import format_cell
from saes.reporting.base import BaseTable
from saes.reporting.registry import TableName, register_table


@register_table(TableName.MEAN_MEDIAN)
class MeanMedianTable(BaseTable):
    """Table showing mean/std or median/IQR per instance and algorithm."""

    @property
    def table_name(self) -> str:
        return "MeanMedian"

    def __repr__(self) -> str:
        if self.normal:
            return "Mean and Standard Deviation Table"
        return "Median and Interquartile Range Table"

    def compute_table(self) -> None:
        self.compute_base_table()
        if self.mean_median is not None:
            self.table = self.mean_median.copy()

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
            row += " & ".join(cells) + " \\\\ \n"
            body += row
        return body
