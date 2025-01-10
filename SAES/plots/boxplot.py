import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from SAES.utils.csv_processor import process_csv
from SAES.utils.csv_processor import process_csv_metrics

from SAES.logger import get_logger
logger = get_logger(__name__)

def __boxplot_problem_metric(df: pd.DataFrame, problem_name: str, metric: str) -> None:
    """
    Creates a boxplot comparing different algorithms performance on a given problem.

    Args:
        df (pd.DataFrame):
            A DataFrame containing the data for a specific problem, with columns for algorithms and performance marks.
        
        problem_name (str):
            The name of the problem for which the boxplot is being created.
        
        metric (str): 
            The metric to be used for the calculations. It should match the column name in the CSV file.

    Returns:
        None: The function saves the boxplot as a PNG file.
    """

    # Filter the data for the current problem
    df_problem = df[df["Instance"] == problem_name]
     
    # Set the figure size for the plot
    plt.figure(figsize=(10, 6))  

    # Create the boxplot with Seaborn
    sns.boxplot(
        x='Algorithm', y='MetricValue', data=df_problem, 
        boxprops=dict(facecolor=(0, 0, 1, 0.3), edgecolor="darkblue", linewidth=1.5),  # Customization for the box
        whiskerprops=dict(color="darkblue", linewidth=1.5),  # Customization for the whiskers
        capprops=dict(color="darkblue", linewidth=1.5),  # Customization for the caps
        medianprops=dict(color="red", linewidth=1.5),  # Customization for the median line
        flierprops=dict(marker='o', color='red', markersize=5, alpha=0.8)  # Customization for the outliers    
    )

    # Set title and labels
    plt.title(f'Comparison of Algorithms for {problem_name} for {metric}', fontsize=16, weight='bold', pad=20)
    plt.ylabel('Performance (Mark)', fontsize=12)

    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=15, fontsize=10)

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

    # Save the plot as a PNG image
    plt.savefig(os.path.join(os.getcwd(), "outputs", "boxplots", metric, f"{problem_name}.png"))
    
    # Close the plot to free up memory
    plt.close()

def boxplot_csv_metric(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, problem: str = None) -> None:
    """
    Generates boxplots for all algorithms in the given CSV file for a specific metric.

    Args:
        data (pd.DataFrame | str):
            The DataFrame or CSV file containing the data to be plotted.
        
        metrics (pd.DataFrame | str):
            The DataFrame or CSV file containing the metrics to be used for plotting.
        
        metric (str):
            The metric to be used for the calculations. It should match the column name in the CSV file.
        
        problem (str):
            The name of the problem for which the boxplot is being created. If None, boxplots for all problems are generated.
    
    Returns:
        None: The function saves the boxplot as a PNG file.
    """

    # Process the input data and metrics
    df_m, _ = process_csv_metrics(data, metrics, metric)

    # Generate boxplots for the current metric
    os.makedirs(os.path.join(os.getcwd(), "outputs", "boxplots", metric), exist_ok=True)

    # Check if a specific problem was provided
    if problem is None:
        # Generate boxplots for the current metric
        for instance in df_m["Instance"].unique():
            # Create and save the boxplot for the current problem
            __boxplot_problem_metric(df_m, instance, metric)
    else:
        # If a specific problem was provided, create and save the boxplot for that problem
        __boxplot_problem_metric(df_m, problem, metric)

    logger.warning(f"Boxplots for metric {metric} saved to {os.path.join(os.getcwd(), 'outputs', 'boxplots', metric)}")

def boxplots_csv(data: str | pd.DataFrame, metrics: str | pd.DataFrame) -> None:
    """
    Generates boxplots for all problems in the given CSV file dividing them by the metric.

    Args:
        data (pd.DataFrame | str): 
            The DataFrame or CSV file containing the data to be plotted.

        metrics (pd.DataFrame | str): 
            The DataFrame or CSV file containing the metrics to be used for plotting.
        
    Returns:
        None: The function saves the critical distance plot as a PNG file.
    """

    # Process the input data and metrics
    data = process_csv(data, metrics)

    # Process the input data and metrics
    for metric, (df_m, _) in data.items():
        # Generate boxplots for the current metric
        os.makedirs(os.path.join(os.getcwd(), "outputs", "boxplots", metric), exist_ok=True)

        # Generate boxplots for the current metric
        for problem in df_m["Instance"].unique():
            # Create and save the boxplot for the current problem
            __boxplot_problem_metric(df_m, problem, metric)

        logger.warning(f"Boxplots for metric {metric} saved to {os.path.join(os.getcwd(), 'outputs', 'boxplots', metric)}")
