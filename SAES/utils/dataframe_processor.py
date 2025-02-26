from scipy.stats import shapiro
import pandas as pd

def get_metrics(data: pd.DataFrame) -> list:
    """
    Extract the unique metrics from the input data DataFrame.

    Args:
        data (pd.DataFrame): 
            The input DataFrame containing the data to extract metrics from.

    Returns:
        list: 
            A list of unique metric names present in the input data.
    """

    return data["MetricName"].unique()

def check_normality(data: pd.DataFrame) -> bool:
    """
    Check the normality of grouped data in a DataFrame using the Shapiro-Wilk test.
    This function groups the input data by the "Algorithm" and "Instance" columns, 
    and tests the normality of the "MetricValue" column within each group. It returns `False` 
    if any group fails the normality test, and `True` otherwise.
    
    Args:
        data (pd.DataFrame): 
            The input DataFrame containing the data to be tested for normality. Must include columns "Algorithm", "Instance", and "MetricValue".
    
    Returns:
        bool: 
            `True` if all groups pass the Shapiro-Wilk test for normality, `False` if any group fails.
    """

    # Group the data by Algorithm and Instance
    grouped_data = data.groupby(["Algorithm", "Instance"])

    # Perform the Shapiro-Wilk test for normality for each group
    for _, group in grouped_data:
        metric_values = group["MetricValue"]
        if metric_values.max() == metric_values.min() or len(metric_values) < 3: 
            # Identical values imply non-normal distribution
            p_value = 0
        else:
            _, p_value = shapiro(metric_values)
            
        # If any group fails the normality test
        if p_value <= 0.05:
            return False
        
    # If all groups pass the normality test
    return True

def process_dataframe_metric(data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str) -> tuple:
    """
    Processes the given CSV data and metrics to extract and return the data for a specific metric.
    
    Args:
        data (str | pd.DataFrame): 
            Path to CSV file or a DataFrame containing data.

        metrics (str | pd.DataFrame): 
            Path to CSV file or a DataFrame containing metric information.

        metric (str): 
            The specific metric to extract from the data.
    
    Returns:
        pd.DataFrame: 
            A filtered DataFrame containing data for the specified metric.
            
        bool: 
            Whether the metric should be maximized (True) or minimized (False).
    
    Raises:
        ValueError: If the specified metric is not found in the metrics DataFrame.

    Example:
        >>> from SAES.utils.csv_processor import process_csv_metrics
        >>> 
        >>> # Data source
        >>> experimentData = "experimentData.csv"
        >>> 
        >>> # Metrics source
        >>> metrics = "metrics.csv"
        >>> 
        >>> # metric
        >>> metric = "HV"
        >>> 
        >>> df_n, maximize = process_csv_metrics(experimentData, metrics, metric)
    """

    # Load the data DataFrame, either from a CSV file or as an existing DataFrame
    data = pd.read_csv(data, delimiter=",") if isinstance(data, str) else data

    # Load the metrics DataFrame, either from a CSV file or as an existing DataFrame
    metrics = pd.read_csv(metrics, delimiter=",") if isinstance(metrics, str) else metrics

    try:
        # Retrieve the maximize flag (True/False) for the specified metric
        maximize = metrics[metrics["MetricName"] == metric]["Maximize"].values[0]
    
        # Filter the data DataFrame for the rows matching the specified metric
        data = data[data["MetricName"] == metric].reset_index()

        # Return the filtered data and the maximize flag
        return data, maximize
    except Exception as e:
        raise ValueError(f"Metric '{metric}' not found in the metrics DataFrame.") from e
