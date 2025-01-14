from enum import Enum

class TableTypes(Enum):
    MEDIAN = "median"
    FRIEDMAN = "friedman"
    WILCOXON_PIVOT = "wilcoxon_pivot"
    WILCOXON = "wilcoxon"
