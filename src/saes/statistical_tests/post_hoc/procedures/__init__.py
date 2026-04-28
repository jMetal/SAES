"""Post-hoc APV correction procedures."""

from __future__ import annotations

from saes.statistical_tests.post_hoc.procedures.bonferroni import BonferroniDunn
from saes.statistical_tests.post_hoc.procedures.finner import Finner
from saes.statistical_tests.post_hoc.procedures.hochberg import Hochberg
from saes.statistical_tests.post_hoc.procedures.holland import Holland
from saes.statistical_tests.post_hoc.procedures.holm import Holm
from saes.statistical_tests.post_hoc.procedures.li import Li
from saes.statistical_tests.post_hoc.procedures.nemenyi import Nemenyi
from saes.statistical_tests.post_hoc.procedures.shaffer import Shaffer

__all__ = [
    "BonferroniDunn",
    "Finner",
    "Hochberg",
    "Holland",
    "Holm",
    "Li",
    "Nemenyi",
    "Shaffer",
]
