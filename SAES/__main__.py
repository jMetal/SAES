import argparse

from SAES.latex_generation.stats_table import MeanMedian
from SAES.latex_generation.stats_table import Friedman
from SAES.latex_generation.stats_table import WilcoxonPivot
from SAES.latex_generation.stats_table import Wilcoxon

from SAES.plots.boxplot import Boxplot
from SAES.plots.CDplot import CDplot

from SAES.multiobjective.pareto_front import Front2D
from SAES.multiobjective.pareto_front import Front3D
from SAES.multiobjective.pareto_front import FrontND

def main():
    # Create the argument parser object
    parser = argparse.ArgumentParser(description='SAES: Statistical Analysis of Empirical Studies')

    # Create a mutually exclusive group for the main options (only one of these can be selected at a time)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ls', action='store_true', help='Generate a LaTeX skeleton for the paper')
    group.add_argument('-bp', action='store_true', help='Generate a boxplot for the paper')
    group.add_argument('-cdp', action='store_true', help='Generate a critical distance plot for the paper')
    group.add_argument('-fr', action='store_true', help='Generate a the Pareto Fronts for the paper')

    # Add the required arguments: paths to dataset and metrics CSV files
    parser.add_argument('-ds', required=True, type=str, help='Path to the dataset csv')
    parser.add_argument('-ms', required=True, type=str, help='Path to the metrics csv')
    parser.add_argument('-pf', required=False, type=str, help='Path to the Pareto Fronts csv. Works only for --fr')
    parser.add_argument('-r', required=False, type=str, help='Path to the Pareto Fronts references csv. Works only for --fr')

    # Add optional arguments for more specific settings
    parser.add_argument('-m', type=str, help='Specify the metric to be used to generate the results. Works for the three features')
    parser.add_argument('-i', type=str, help='Specify the instance to be used to generate the results. Works only for --bp')
    parser.add_argument(
        '-s', 
        type=str, 
        choices=['mean_median', 'friedman', 'wilcoxon', 'wilcoxon_pivot'],
        help='Specify the type of LaTeX report to be generated (works only for --ls)'
    )
    parser.add_argument('-op', type=str, help='Specify the output path for the generated files. Works for the three features')
    parser.add_argument('-g', action='store_true', help='Choose to generate all the boxplots for a specific metric in grid format. Works only for --bp')
    parser.add_argument('-d', type=str, help='Choose the number of dimensions for the Pareto Fronts. Works only for --fr')

    # Parse the command-line arguments
    args = parser.parse_args()

    BOXPLOT = args.bp
    LATEX = args.ls
    CDPLOT = args.cdp
    FRONT = args.fr

    DATA = args.ds
    METRICS = args.ms
    PFRONTS = args.pf
    REFERENCES = args.r

    METRIC = args.m
    TABLE = args.s
    INSTANCE = args.i
    OUTPUT = args.op
    GRID = args.g
    DIMENSIONS = args.d

    # Boxplot generation
    if BOXPLOT:
        boxplot = Boxplot(DATA, METRICS, METRIC)
        if METRIC and GRID and not INSTANCE:
            boxplot.save_all_instances(OUTPUT)
        elif METRIC and not GRID and INSTANCE:
            boxplot.save_instance(INSTANCE, OUTPUT)
        else:
            parser.error("Please specify a metric and an instance to generate the boxplot")
    # LaTeX report generation
    elif LATEX:
        if TABLE and METRIC:
            if TABLE == 'mean_median':
                MeanMedian(DATA, METRICS, METRIC).save(OUTPUT)
            elif TABLE == 'friedman':
                Friedman(DATA, METRICS, METRIC).save(OUTPUT)
            elif TABLE == 'wilcoxon_pivot':
                WilcoxonPivot(DATA, METRICS, METRIC).save(OUTPUT)
            elif TABLE == 'wilcoxon':
                Wilcoxon(DATA, METRICS, METRIC).save(OUTPUT)
            else:
                parser.error("Please specify a valid type of LaTeX report to be generated")
        else:
            parser.error("Please specify the type of LaTeX report to be generated")
    # Critical Distance Plot generation
    elif CDPLOT:
        cdplot = CDplot(DATA, METRICS, METRIC)
        if METRIC:
            cdplot.save(OUTPUT)
        else:
            parser.error("Please specify a metric to generate the critical distance plot")
    # Pareto Fronts generation
    elif FRONT:
        if PFRONTS and REFERENCES and INSTANCE and METRIC:
            if DIMENSIONS == '2':
                Front2D(PFRONTS, REFERENCES, METRIC).save(INSTANCE, OUTPUT)
            elif DIMENSIONS == '3':
                Front3D(PFRONTS, REFERENCES, METRIC).save(INSTANCE, OUTPUT)
            else:
                FrontND(PFRONTS, REFERENCES, METRIC, DIMENSIONS).save(INSTANCE, OUTPUT)
        else:
            parser.error("Please specify the paths to the Pareto Fronts and References CSV files")
    else:
        parser.error("Please specify one of the main options")

if __name__ == "__main__":
    main()