import argparse

from SAES.latex_generation import latex_skeleton as ls
from SAES.plots import boxplot as bp
from SAES.plots import critical_distance_plot as cdp

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

    # Boxplot generation
    if args.bp:
        # Ensure that the required argument '-m' is provided if '-i' is specified
        if args.i and not args.m:
            parser.error("The argument '-i/--instance' requires '-m/--metric' to be specified.")
        # Generate boxplot for all instances if only the metric is provided
        elif args.m and not args.i:
            if args.g:
                bp.boxplot_all_instances_grid(args.ds, args.ms, args.m, output_path=args.op)
            else:
                bp.boxplot_all_instances(args.ds, args.ms, args.m, output_path=args.op)
        # Generate boxplot for a specific instance and metric
        elif args.m and args.i:
            bp.boxplot(args.ds, args.ms, args.m, args.i, output_path=args.op)
        # Generate boxplots for all metrics and instances
        else:
            bp.boxplots_all_metrics_instances(args.ds, args.ms, output_path=args.op)
    # LaTeX report generation
    elif args.ls:
        if args.m:
            # Generate LaTeX report for a specific metric
            if args.s:
                ls.latex_selected(args.ds, args.ms, args.m, args.s, output_path=args.op)
            else:
                ls.latex(args.ds, args.ms, args.m, output_path=args.op)
        else:
            # Generate LaTeX report for all metrics
            ls.latex_all_metrics(args.ds, args.ms, output_path=args.op)
    # Critical Distance Plot generation
    elif args.cdp:
        if args.m:
            # Generate critical distance plot for a specific metric
            cdp.CDplot(args.ds, args.ms, args.m, output_path=args.op)
        else:
            # Generate critical distance plot for all metrics
            cdp.CDplot_all_metrics(args.ds, args.ms, output_path=args.op)
    # Default case: Generate all reports and plots
    else:
        # Generate boxplots for all metrics and instances
        bp.boxplots_all_metrics_instances(args.ds, args.ms, output_path=args.op)

        # Generate LaTeX report for all metrics
        ls.latex_all_metrics(args.ds, args.ms, output_path=args.op)
        
        # Generate critical distance plot for all metrics
        cdp.CDplot_all_metrics(args.ds, args.ms, output_path=args.op)

if __name__ == "__main__":
    main()