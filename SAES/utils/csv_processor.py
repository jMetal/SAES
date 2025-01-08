import pandas as pd
import os
from SAES.utils.statistical_checks import check_normality

def process_csv(data: str | pd.DataFrame, metrics: str | pd.DataFrame) -> dict:
    """
    Processes two CSV or DataFrame inputs: one containing metrics information and the other containing data.
    
    Args:
        data (str | pd.DataFrame): Path to a CSV file or an existing DataFrame containing data.
        metrics (str | pd.DataFrame): Path to a CSV file or an existing DataFrame containing metrics information.
    
    This function loads the metrics and data, and then filters the data based on the metric names,
    storing the filtered data along with a flag indicating whether to maximize the metric.
    """

    # Load the metrics DataFrame, either from a CSV file or as an existing DataFrame
    df_m = pd.read_csv(metrics, delimiter=",") if isinstance(metrics, str) else metrics

    # Load the data DataFrame, either from a CSV file or as an existing DataFrame
    df = pd.read_csv(data, delimiter=",") if isinstance(data, str) else data

    # Initialize an empty dictionary to store the filtered data and the 'Maximize' flag
    data = {}

    # Iterate through each row in the metrics DataFrame
    for _, row in df_m.iterrows():
        # Extract the metric name and the 'Maximize' flag (whether to maximize the metric)
        metric = row["MetricName"]
        maximize = row["Maximize"]

        # Filter the data for the rows where the 'Metric' matches the current metric
        df_n = df[df["MetricName"] == metric].reset_index()

        # Store the filtered data and the 'Maximize' flag in a dictionary
        data[metric] = (df_n, maximize)

    return data

def process_csv_metrics(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str) -> tuple:
    """
    Processes the given CSV data and metrics to extract and return the data for a specific metric.
    
    Parameters:
        data (str | pd.DataFrame): Path to CSV file or a DataFrame containing data.
        metrics (str | pd.DataFrame): Path to CSV file or a DataFrame containing metric information.
        metric (str): The specific metric to extract from the data.
    
    Returns:
        pd.DataFrame: A filtered DataFrame containing data for the specified metric.
        bool: Whether the metric should be maximized (True) or minimized (False).
    
    Raises:
        ValueError: If the specified metric is not found in the metrics DataFrame.
    """

    # Load the metrics DataFrame, either from a CSV file or as an existing DataFrame
    df_m = pd.read_csv(metrics, delimiter=",") if isinstance(metrics, str) else metrics

    # Load the data DataFrame, either from a CSV file or as an existing DataFrame
    df = pd.read_csv(data, delimiter=",") if isinstance(data, str) else data

    try:
        # Retrieve the maximize flag (True/False) for the specified metric
        maximize = df_m[df_m["MetricName"] == metric]["Maximize"].values[0]

        # Filter the data DataFrame for the rows matching the specified metric
        df_n = df[df["MetricName"] == metric].reset_index()

        # Return the filtered data and the maximize flag
        return df_n, maximize
    except Exception as e:
        raise ValueError(f"Metric '{metric}' not found in the metrics DataFrame.") from e

def process_dataframe_basic(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """
    Saves a DataFrame as a CSV file in a 'CSVs' directory.

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame to save.
    metric : str
        Used to name the output CSV file.

    Returns:
    -------
    pd.DataFrame
        The input DataFrame.
    """
    
    # Check if the input & output directories exist, if not create them
    os.makedirs(os.path.join(os.getcwd(), "outputs"), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(), "CSVs"), exist_ok=True)

    # Save the data to a CSV file
    df.to_csv(os.path.join(os.getcwd(), "CSVs", f"data_{metric}.csv"), index=False)

    return df

def process_dataframe_extended(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """
    Processes a CSV DataFrame by grouping data by 'Problem' and 'Algorithm', calculating either the mean or median 
    of the 'MetricValue' column based on normality, and saving the aggregated data and standard deviations as CSV files.
    
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing 'Problem', 'Algorithm', and 'MetricValue' columns.
    - metric (str): The metric name to be included in the saved filenames.
    
    Returns:
    - pd.DataFrame: A pivoted DataFrame with 'Problem' as index and 'Algorithm' as columns, showing aggregated metric values.
    - pd.DataFrame: A pivoted DataFrame showing standard deviations of metric values.
    - str: The aggregation type used ('Mean' or 'Median').
    """

    # Check if the input & output directories exist, if not create them
    os.makedirs(os.path.join(os.getcwd(), "outputs"), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(), "CSVs"), exist_ok=True)

    # Group by 'Problem' and 'Algorithm', then calculate the median or mean of the 'Metric Value' column
    normal = check_normality(df)

    if normal:
        df_agg = df.groupby(['Instance', 'Algorithm'])['MetricValue'].mean().reset_index()
        aggregation_type = "Mean"
    else:
        df_agg = df.groupby(['Instance', 'Algorithm'])['MetricValue'].median().reset_index()
        aggregation_type = "Median"
    
    # Pivot the DataFrame to get 'Problem' as the index and 'Algorithm' as the columns with 'Metric Value' values
    df_agg_pivot = df_agg.pivot(index='Instance', columns='Algorithm', values='MetricValue')

    # Calculate the standard deviation DataFrame 
    df_std = df.groupby(['Instance', 'Algorithm'])['MetricValue'].std().reset_index()
    df_std_pivot = df_std.pivot(index='Instance', columns='Algorithm', values='MetricValue')
    
    # Save the DataFrames to CSV files
    df_agg_pivot.to_csv(os.path.join(os.getcwd(), "CSVs", f"data_{aggregation_type}_{metric}.csv"), index=False)
    df_std_pivot.to_csv(os.path.join(os.getcwd(), "CSVs", f"data_std_{aggregation_type}_{metric}.csv"), index=False)

    # Return the DataFrames and the aggregation type
    return df_agg_pivot, df_std_pivot, aggregation_type

if __name__ == "__main__":
    data = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/data.csv"
    metrics = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/metrics.csv"
    process_csv_metrics(data, metrics, "NHV")