import argparse

from SAES.latex_generation.stats_table import MeanMedian
from SAES.latex_generation.stats_table import Friedman
from SAES.latex_generation.stats_table import WilcoxonPivot
from SAES.latex_generation.stats_table import Wilcoxon

from SAES.plots.boxplot import Boxplot
from SAES.plots.CDplot import CDplot
from SAES.utils.dataframe_processor import get_metrics

def main():
    # Create the argument parser object
    parser = argparse.ArgumentParser(description='SAES: Statistical Analysis of Empirical Studies')

    # Create a mutually exclusive group for the main options (only one of these can be selected at a time)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ls', action='store_true', help='Generate a LaTeX skeleton for the paper')
    group.add_argument('-bp', action='store_true', help='Generate a boxplot for the paper')
    group.add_argument('-cdp', action='store_true', help='Generate a critical distance plot for the paper')
    group.add_argument('-all', action='store_true', help='Generate all the plots and reports from the dataset')

    # Add the required arguments: paths to dataset and metrics CSV files
    parser.add_argument('-ds', required=True, type=str, help='Path to the dataset csv')
    parser.add_argument('-ms', required=True, type=str, help='Path to the metrics csv')

    # Add optional arguments for more specific settings
    parser.add_argument('-m', type=str, help='Specify the metric to be used to generate the results. Works for the three features')
    parser.add_argument('-i', type=str, help='Specify the instance to be used to generate the results. Works only for --bp')
    parser.add_argument('-s', type=str, help='Specify the type of LaTeX report to be generated. Works only for --ls')
    parser.add_argument('-op', type=str, help='Specify the output path for the generated files. Works for the three features')
    parser.add_argument('-g', action='store_true', help='Choose to generate all the boxplots for a specific metric in grid format. Works only for --bp')

    # Parse the command-line arguments
    args = parser.parse_args()
    metrics = get_metrics(args.ms)

    # Boxplot generation
    if args.bp:
        boxplot = Boxplot(args.ds, args.ms, args.m)
        # Ensure that the required argument '-m' is provided if '-i' is specified
        if args.i and not args.m:
            parser.error("The argument '-i/--instance' requires '-m/--metric' to be specified.")
        # Generate boxplot for all instances if only the metric is provided
        elif args.m and not args.i:
            if args.g:
                boxplot.save_all_instances(args.op)
            else:
                for instance in boxplot.instances:
                    boxplot.save_instance(instance, args.op)
        # Generate boxplot for a specific instance and metric
        elif args.m and args.i:
            boxplot.save_instance(args.i, args.op)
        # Generate boxplots for all metrics and instances
        else:
            for metric in metrics:
                boxplot = Boxplot(args.ds, args.ms, metric)
                for instance in boxplot.instances:
                    boxplot.save_instance(instance, args.op)
    
    # LaTeX report generation
    elif args.ls:
        if args.m:
            MeanMedian(args.ds, args.ms, args.m).save(args.op)
            Friedman(args.ds, args.ms, args.m).save(args.op)
            WilcoxonPivot(args.ds, args.ms, args.m).save(args.op)
            Wilcoxon(args.ds, args.ms, args.m).save(args.op)
        else:
            for metric in metrics:
                MeanMedian(args.ds, args.ms, metric).save(args.op)
                Friedman(args.ds, args.ms, metric).save(args.op)
                WilcoxonPivot(args.ds, args.ms, metric).save(args.op)
                Wilcoxon(args.ds, args.ms, metric).save(args.op)
            
    # Critical Distance Plot generation
    elif args.cdp:
        cdplot = CDplot(args.ds, args.ms, args.m)
        if args.m:
            # Generate critical distance plot for a specific metric
            cdplot.save(args.op)
        else:
            # Generate critical distance plot for all metrics
            for metric in metrics:
                cdplot = CDplot(args.ds, args.ms, metric)
                cdplot.save(args.op)

if __name__ == "__main__":
    main()