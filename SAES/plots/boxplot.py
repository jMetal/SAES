import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from SAES.utils.csv_processor import process_csv
from SAES.utils.csv_processor import process_csv_metrics

from SAES.logger import get_logger
logger = get_logger(__name__)

def __boxplot_instance_metric(df_m: pd.DataFrame, instance_name: str, metric: str, show: bool = False) -> None:
    """
    Creates a boxplot comparing different algorithms performance on a given instance.

    Args:
        df_m (pd.DataFrame):
            A DataFrame containing the data for a specific instance, with columns for algorithms and performance marks.
        
        instance_name (str):
            The name of the instance for which the boxplot is being created.
        
        metric (str): 
            The metric to be used for the calculations. It should match the column name in the CSV file.
        
        show (bool):
            A flag to indicate whether the plot should be displayed or not. Default is False.

    Returns:
        None: The function saves the boxplot as a PNG file.
    """

    # Filter the data for the current instance
    df_instance = df_m[df_m["Instance"] == instance_name]
     
    # Set the figure size for the plot
    plt.figure(figsize=(10, 6))  

    # Create the boxplot with Seaborn
    sns.boxplot(
        x='Algorithm', y='MetricValue', data=df_instance, 
        boxprops=dict(facecolor=(0, 0, 1, 0.3), edgecolor="darkblue", linewidth=1.5),  # Customization for the box
        whiskerprops=dict(color="darkblue", linewidth=1.5),  # Customization for the whiskers
        capprops=dict(color="darkblue", linewidth=1.5),  # Customization for the caps
        medianprops=dict(color="red", linewidth=1.5),  # Customization for the median line
        flierprops=dict(marker='o', color='red', markersize=5, alpha=0.8)  # Customization for the outliers    
    )

    # Set title and labels
    plt.title(f'Comparison of Algorithms for {instance_name} for {metric}', fontsize=16, weight='bold', pad=20)
    plt.ylabel('Performance', fontsize=12, weight='bold')

    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=15, fontsize=10, weight='bold')
    plt.yticks(fontsize=10, weight='bold')

    # Add gridlines along the y-axis
    plt.grid(axis='y', linestyle='-', alpha=0.7)

    # Remove the top, right, left, and bottom borders from the plot
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # Remove the x-axis ticks to avoid vertical lines under the boxplots and hide the x-axis label
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.gca().set_xlabel('')

    # Adjust the layout for better spacing
    plt.tight_layout()

    # Show or close the plot
    if show:
        plt.show()
    else:
        # Save the plot as a PNG image
        plt.savefig(os.path.join(os.getcwd(), "outputs", "boxplots", metric, f"{instance_name}.png"))
        plt.close()

def boxplot(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, instance_name: str, show: bool = False) -> str:
    """
    Generates a boxplot comparing different algorithms performance on a given instance for a specific metric.

    Args:
        data (pd.DataFrame | str):
            The DataFrame or CSV file containing the data to be plotted.
        
        metrics (pd.DataFrame | str):
            The DataFrame or CSV file containing the metrics to be used for plotting.
        
        metric (str):
            The metric to be used for the calculations. It should match the column name in the CSV file.
        
        instance_name (str):
            The name of the instance for which the boxplot is being created.

        show (bool):
            A flag to indicate whether the plot should be displayed or saved in disk. Default is False.
    
    Returns:
        str: The path to the directory containing the generated boxplot or a message indicating that the plot was displayed.

    Example:
        >>> from SAES.plots.boxplot import boxplot
        >>> 
        >>> # Data source
        >>> experimentData = "swarmIntelligence.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # Metric to analyze
        >>> metric = "HV"
        >>> 
        >>> # Instance to analyze
        >>> instance_name = "ZDT1"
        >>> 
        >>> # Show the boxplot instead of saving it on disk
        >>> output_dir = boxplot(data, metrics, metric, instance_name, show=True)
        >>> print(output_dir)
        Boxplot displayed
    """

    # Process the input data and metrics
    df_m, _ = process_csv_metrics(data, metrics, metric)

    # Create the output directory for the boxplots
    output_dir = os.path.join(os.getcwd(), "outputs", "boxplots", metric)

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # If a specific instance was provided, create and save the boxplot for that instance
    __boxplot_instance_metric(df_m, instance_name, metric, show=show)

    if show:
        return "Boxplot displayed"

    # Log the successful generation of the boxplot
    logger.info(f"Boxplots for metric {metric} saved to {output_dir}")
    return output_dir+f"{instance_name}.png"

def boxplot_all_instances(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str) -> str:
    """
    Generates boxplots for all algorithms in the given CSV file for a specific metric.

    Args:
        data (pd.DataFrame | str):
            The DataFrame or CSV file containing the data to be plotted.
        
        metrics (pd.DataFrame | str):
            The DataFrame or CSV file containing the metrics to be used for plotting.
        
        metric (str):
            The metric to be used for the calculations. It should match the column name in the CSV file.
            
    Returns:
        str: The path to the directory containing the generated boxplots.

    Example:
        >>> from SAES.plots.boxplot import boxplot_all_instances
        >>> 
        >>> # Data source
        >>> experimentData = "swarmIntelligence.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # Metric to analyze
        >>> metric = "HV"
        >>> 
        >>> # Save the boxplots on disk
        >>> output_dir = boxplot_all_instances(data, metrics, metric)
        >>> print(output_dir)
        Boxplots for metric HV saved to {output_dir}
        {output_dir}
    """

    # Process the input data and metrics
    df_m, _ = process_csv_metrics(data, metrics, metric)

    # Create the output directory for the boxplots
    output_dir = os.path.join(os.getcwd(), "outputs", "boxplots", metric)

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate boxplots for the current metric
    for instance in df_m["Instance"].unique():
        # Create and save the boxplot for the current instance
        __boxplot_instance_metric(df_m, instance, metric)

    logger.info(f"Boxplots for metric {metric} saved to {output_dir}")
    return output_dir

def boxplots_all_metrics_instances(data: str | pd.DataFrame, metrics: str | pd.DataFrame) -> str:
    """
    Generates boxplots for all instances in the given CSV file for all metrics.

    Args:
        data (pd.DataFrame | str): 
            The DataFrame or CSV file containing the data to be plotted.

        metrics (pd.DataFrame | str): 
            The DataFrame or CSV file containing the metrics to be used for plotting.
        
    Returns:
        str: The path to the directory containing the generated boxplots.

    Example:
        >>> from SAES.plots.boxplot import boxplots_all_metrics_instances
        >>> 
        >>> # Data source
        >>> experimentData = "swarmIntelligence.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # Save the boxplots on disk
        >>> output_dir = boxplots_all_metrics_instances(data, metrics)
        >>> print(output_dir)
        Boxplots for metric HV saved to {output_dir}
        {output_dir}
    """

    # Process the input data and metrics
    df_m = process_csv(data, metrics)

    # Create the output directory for the boxplots
    output_dir = os.path.join(os.getcwd(), "outputs", "boxplots")

    # Process the input data and metrics
    for metric, (df_m, _) in df_m.items():
        # Create the output directory for the current metric
        os.makedirs(os.path.join(output_dir, metric), exist_ok=True)

        # Generate boxplots for the current metric
        for instance in df_m["Instance"].unique():
            # Create and save the boxplot for the current instance
            __boxplot_instance_metric(df_m, instance, metric)

        logger.info(f"Boxplots for metric {metric} saved to {os.path.join(output_dir, metric)}")

    return output_dir
