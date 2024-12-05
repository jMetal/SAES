import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
    plt.savefig(f"outputs/boxplots/{metric}/{problem_name}.png")

def __generate_boxplots(df: pd.DataFrame, metric: str) -> None:
    """
    Generates boxplots for all problems in the given CSV file.

    Parameters:
    df (pd.Dataframe): The DataFrame containing the data to be plotted.
    metric (str): The metric to be used for the calculations. It should match the column name in the CSV file.

    Returns:
    None: The function creates a series of boxplots, one for each unique problem in the CSV file.
    """

    # Get a list of unique problems in the dataset
    problems = df["Problem"].unique()
    
    # Ensure the output directory for boxplots exists
    if not os.path.exists(f"outputs/boxplots/{metric}"):
        os.makedirs(f"outputs/boxplots/{metric}")

    # Create a boxplot for each problem
    for problem in problems:        
        # Create and save the boxplot for the current problem
        create_boxplot_for_problem(df, problem, metric)

def generate_boxplots_from_csv(data: str | pd.DataFrame, metrics: str | pd.DataFrame):
    """
    Generates boxplots for all problems in the given CSV file dividing them by the metric.

    Parameters:
    data (pd.DataFrame | str): The DataFrame or CSV file containing the data to be plotted.
    metrics (pd.DataFrame | str): The DataFrame or CSV file containing the metrics to be used for plotting.
    """
    
    # Load the metrics DataFrame, either from a CSV file or as an existing DataFrame
    df_m = pd.read_csv(metrics, delimiter=",") if isinstance(metrics, str) else metrics

    # Load the data DataFrame, either from a CSV file or as an existing DataFrame
    df = pd.read_csv(data, delimiter=",") if isinstance(data, str) else data

    # Iterate through each row in the metrics DataFrame
    for _, row in df_m.iterrows():
        # Get the metric and whether it should be sorted in descending order
        metric = row["Metric"]

        # Filter the data for the rows where the 'Metric' matches the current metric
        df_n = df[df["Metric"] == metric].reset_index()

        # Call the helper function to create a LaTeX table for the current metric
        __generate_boxplots(df_n, metric)
