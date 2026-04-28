"""
Demonstration script for SAES library features.
This script uses all major components: tests, tables, plots, and pareto visualizations.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from saes import (
    ColumnName,
    PlotName,
    TableName,
    TestName,
    ThemeConfig,
    get_plot,
    get_table,
    get_test,
)
from saes.logger import get_logger

logger = get_logger(__name__)

# Paths
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "tests" / "test_data"
OUTPUT_DIR = ROOT / "demo_output"

DATA_CSV = DATA_DIR / "swarmIntelligence.csv"
METRICS_CSV = DATA_DIR / "multiobjectiveMetrics.csv"
FRONTS_DIR = DATA_DIR / "fronts"
REFS_DIR = DATA_DIR / "references"


def main():
    # Cleanup previous output
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    logger.info("Starting SAES Full Feature Demonstration")

    # Load data
    data = pd.read_csv(DATA_CSV)
    metric = "HV"

    # Define a custom Theme to show off the API
    custom_theme = ThemeConfig(
        primary_color="violet",
        secondary_color="magenta",
        edge_color="black",
        title_fontsize=16,
        label_fontsize=12,
        grid_alpha=0.3,
    )

    # 1. Statistical Tests
    logger.info("--- 1. Statistical Tests ---")
    # Get a pivot of data for one instance
    inst_data = data[
        (data[ColumnName.INSTANCE] == "ZDT1") & (data[ColumnName.METRIC_NAME] == metric)
    ]
    pivot = inst_data.pivot(
        index=ColumnName.EXECUTION_ID, columns=ColumnName.ALGORITHM, values=ColumnName.METRIC_VALUE
    )

    # Omnibus
    friedman = get_test(TestName.FRIEDMAN)
    res_f = friedman.run(pivot, maximize=True)
    logger.info("Friedman significant: %s (p=%.4e)", res_f.is_significant, res_f.p_value)

    anova = get_test(TestName.ANOVA)
    res_a = anova.run(pivot, maximize=True)
    logger.info("ANOVA significant: %s (p=%.4e)", res_a.is_significant, res_a.p_value)

    # Pairwise (Using NSGAII and OMOPSO)
    wilcoxon = get_test(TestName.WILCOXON)
    res_w = wilcoxon.run(pivot[["NSGAII", "OMOPSO"]], maximize=True)
    logger.info("Wilcoxon verdict: %s", res_w.verdict)

    # Bayesian
    bayesian = get_test(TestName.BAYESIAN_SIGN)
    res_b = bayesian.run(pivot[["NSGAII", "OMOPSO"]])
    logger.info("Bayesian probabilities: %s", res_b.probabilities)

    # 2. Reporting (LaTeX Tables)
    logger.info("--- 2. Reporting Tables ---")
    tables_out = OUTPUT_DIR / "tables"

    get_table(TableName.MEAN_MEDIAN, DATA_CSV, METRICS_CSV, metric).save(str(tables_out))
    get_table(TableName.FRIEDMAN, DATA_CSV, METRICS_CSV, metric).save(str(tables_out))
    get_table(TableName.FRIEDMAN_P_VALUES, DATA_CSV, METRICS_CSV, metric).save(str(tables_out))
    get_table(TableName.ANOVA, DATA_CSV, METRICS_CSV, metric).save(str(tables_out))
    get_table(TableName.WILCOXON, DATA_CSV, METRICS_CSV, metric).save(str(tables_out))
    get_table(
        TableName.WILCOXON_PIVOT, DATA_CSV, METRICS_CSV, metric, pivot_algorithm="NSGAII"
    ).save(str(tables_out))
    get_table(TableName.T_TEST, DATA_CSV, METRICS_CSV, metric).save(str(tables_out))
    get_table(TableName.T_TEST_PIVOT, DATA_CSV, METRICS_CSV, metric, pivot_algorithm="NSGAII").save(
        str(tables_out)
    )

    # 3. Visualization (Plots)
    logger.info("--- 3. Visualization Plots ---")
    plots_out = OUTPUT_DIR / "plots"

    get_plot(
        PlotName.BOXPLOT, DATA_CSV, METRICS_CSV, metric, theme=custom_theme
    ).save_all_instances(str(plots_out))
    get_plot(PlotName.VIOLIN, DATA_CSV, METRICS_CSV, metric, theme=custom_theme).save_all_instances(
        str(plots_out)
    )
    get_plot(
        PlotName.HISTOGRAM, DATA_CSV, METRICS_CSV, metric, theme=custom_theme
    ).save_all_instances(str(plots_out))
    get_plot(PlotName.CD_PLOT, DATA_CSV, METRICS_CSV, metric, theme=custom_theme).save(
        str(plots_out)
    )
    get_plot(PlotName.POSTERIOR, DATA_CSV, METRICS_CSV, metric, theme=custom_theme).save(
        "NSGAII", "OMOPSO", str(plots_out)
    )

    # 4. Pareto Fronts
    logger.info("--- 4. Pareto Fronts ---")
    pareto_out = OUTPUT_DIR / "pareto"

    # Using DTLZ1 as it has 2D, 3D, and 4D files in references
    get_plot(PlotName.FRONT_2D, str(FRONTS_DIR), str(REFS_DIR), metric, theme=custom_theme).save(
        "DTLZ1", output_path=str(pareto_out), file_name="front_2d_DTLZ1_HV_MEDIAN.png"
    )
    get_plot(PlotName.FRONT_3D, str(FRONTS_DIR), str(REFS_DIR), metric, theme=custom_theme).save(
        "DTLZ1", output_path=str(pareto_out), file_name="front_3d_DTLZ1_HV_MEDIAN.png"
    )
    get_plot(
        PlotName.FRONT_ND, str(FRONTS_DIR), str(REFS_DIR), metric, dimensions=3, theme=custom_theme
    ).save("DTLZ1", output_path=str(pareto_out), file_name="front_nd_DTLZ1_HV_MEDIAN.png")

    logger.info("SAES Demonstration Completed. Results in %s", OUTPUT_DIR)


if __name__ == "__main__":
    main()
