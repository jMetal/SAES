import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from SAES.utils.csv_processor import process_csv

from SAES.logger import get_logger
logger = get_logger(__name__)

def create_boxplot_for_problem(csv: str | pd.DataFrame, problem_name: str, metric: str) -> None:
    """
    Creates a boxplot comparing different algorithms performance on a given problem.

    Parameters:
    df_problem (pd.DataFrame): A DataFrame containing the data for a specific problem, with columns for algorithms and performance marks.
    problem_name (str): The name of the problem for which the boxplot is being created.
    metric (str): The metric to be used for the calculations. It should match the column name in the CSV file.

    Returns:
    None: The function saves the boxplot as a PNG file.
    """
    # Load the data from the CSV file
    df = pd.read_csv(csv, delimiter=",") if isinstance(csv, str) else csv

    # Filter the data for the current problem
    df_problem = df[df["Problem"] == problem_name]
     
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

def generate_boxplots_from_csv(data: str | pd.DataFrame, metrics: str | pd.DataFrame):
    """
    Generates boxplots for all problems in the given CSV file dividing them by the metric.

    Parameters:
    data (pd.DataFrame | str): The DataFrame or CSV file containing the data to be plotted.
    metrics (pd.DataFrame | str): The DataFrame or CSV file containing the metrics to be used for plotting.
    """

    # Process the input data and metrics
    data = process_csv(data, metrics)

    # Process the input data and metrics
    for metric, (df_m, _) in data.items():
        # Generate boxplots for the current metric
        os.makedirs(os.path.join(os.getcwd(), "outputs", "boxplots", metric), exist_ok=True)

        # Generate boxplots for the current metric
        for problem in df_m["Problem"].unique():
            # Create and save the boxplot for the current problem
            create_boxplot_for_problem(df_m, problem, metric)

        logger.warning(f"Boxplots for metric {metric} saved to {os.path.join(os.getcwd(), 'outputs', 'boxplots', metric)}")

if __name__ == "__main__":
    data = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/data.csv"
    metrics = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/metrics.csv"

    data2 = "/home/khaosdev/algorithm-benchmark-toolkit/examples/data.csv"
    metrics2 = "/home/khaosdev/algorithm-benchmark-toolkit/examples/metrics.csv"
    generate_boxplots_from_csv(data, metrics)