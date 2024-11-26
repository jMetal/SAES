import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_boxplot_for_problem(df_problem: pd.DataFrame, problem_name: str) -> None:
    """
    Creates a boxplot comparing different algorithms performance on a given problem.

    Parameters:
    df_problem (pd.DataFrame): A DataFrame containing the data for a specific problem,
                               with columns for algorithms and performance marks.
    problem_name (str): The name of the problem for which the boxplot is being created.

    Returns:
    None: The function saves the boxplot as a PNG file.
    """

    # Set the figure size for the plot
    plt.figure(figsize=(10, 6))  

    # Create the boxplot with Seaborn
    sns.boxplot(
        x='Algorithm', y='Mark', data=df_problem, 
        boxprops=dict(facecolor=(0, 0, 1, 0.3), edgecolor="darkblue", linewidth=1.5),  # Customization for the box
        whiskerprops=dict(color="darkblue", linewidth=1.5),  # Customization for the whiskers
        capprops=dict(color="darkblue", linewidth=1.5),  # Customization for the caps
        medianprops=dict(color="red", linewidth=1.5),  # Customization for the median line
        flierprops=dict(marker='o', color='red', markersize=5, alpha=0.8)  # Customization for the outliers    
    )

    # Set title and labels
    plt.title(f'Comparison of Algorithms for {problem_name}', fontsize=16, weight='bold', pad=20)
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
    plt.savefig(f"outputs/boxplots/boxplot_{problem_name}.png")

def generate_boxplots_from_csv(csv_path: str) -> None:
    """
    Generates boxplots for all problems in the given CSV file.

    Parameters:
    csv_path (str): The path to the CSV file containing problem, algorithm, and performance data.

    Returns:
    None: The function creates a series of boxplots, one for each unique problem in the CSV file.
    """
    
    # Load the CSV data into a DataFrame
    df_data = pd.read_csv(csv_path, delimiter=",")

    # Get a list of unique problems in the dataset
    problems = df_data["Problem"].unique()
    
    # Ensure the output directory for boxplots exists
    if not os.path.exists("outputs/boxplots"):
        os.makedirs("outputs/boxplots")

    # Create a boxplot for each problem
    for problem in problems:
        # Filter the data for the current problem
        df_problem = df_data[df_data["Problem"] == problem]
        
        # Create and save the boxplot for the current problem
        create_boxplot_for_problem(df_problem, problem)
