import pandas as pd
from scipy.stats import shapiro

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
        bool: `True` if all groups pass the Shapiro-Wilk test for normality, `False` if any group fails.
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
