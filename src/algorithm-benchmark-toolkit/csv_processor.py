import pandas as pd
import os

def process_csv(file_path: str, delimiter: str = ",", median: bool = True, extra: bool = False) -> pd.DataFrame:
    """
    Reads a CSV file and processes the data to generate statistical metrics like median, mean, standard deviation,
    and interquartile range (IQR) for each problem and algorithm. It returns pivoted DataFrames with these metrics.

    :param file_path: str
        The path to the CSV file to be processed.
        
    :param delimiter: str, default ","
        The delimiter used in the CSV file. By default, it is a comma.
        
    :param median: bool, default True
        If True, the median of the 'Mark' column is calculated for each combination of 'Problem' and 'Algorithm'.
        If False, the mean of the 'Mark' column is calculated instead.
        
    :param extra: bool, default False
        If True, additional metrics such as standard deviation and interquartile range (IQR) are also calculated 
        and returned in the result. These metrics are calculated for each combination of 'Problem' and 'Algorithm'.
        
    :return: tuple of pandas.DataFrame
        - df_pivot: DataFrame with the median or mean 'Mark' values, indexed by 'Problem' and columns for each 'Algorithm'.
        - df_std_pivot (optional): DataFrame with standard deviation values, if extra=True, indexed by 'Problem' and columns for each 'Algorithm'.
        - df_iqr_pivot (optional): DataFrame with interquartile range values, if extra=True, indexed by 'Problem' and columns for each 'Algorithm'.
        
    :raises FileNotFoundError: If the provided file_path does not exist.
    :raises ValueError: If the CSV file does not contain the expected columns ('Problem', 'Algorithm', 'Mark').
    """
    
    # Check if the input & output directories exist, if not create them
    if not os.path.exists("outputs"):
        os.mkdir("outputs")
    if not os.path.exists("CSVs"):
        os.mkdir("CSVs")

    # Read the CSV file into a pandas DataFrame using the specified delimiter
    df = pd.read_csv(file_path, delimiter=delimiter)
    df.to_csv(f"CSVs/{file_path.split('/')[-1]}", index=False)

    # Group by 'Problem' and 'Algorithm', then calculate the median or mean of the 'Mark' column
    if median:
        df_metric = df.groupby(['Problem', 'Algorithm'])['Mark'].median().reset_index()
    else:
        df_metric = df.groupby(['Problem', 'Algorithm'])['Mark'].mean().reset_index()
    
    # Pivot the DataFrame to get 'Problem' as the index and 'Algorithm' as the columns with 'Mark' values
    df_pivot = df_metric.pivot(index='Problem', columns='Algorithm', values='Mark')

    # If extra is True, calculate the standard deviation and interquartile range (IQR)
    df_std_pivot = None
    if extra:
        # Calculate the standard deviation of 'Mark' for each 'Problem' and 'Algorithm'
        df_std = df.groupby(['Problem', 'Algorithm'])['Mark'].std().reset_index()

        # Pivot the standard deviation and IQR DataFrames to match the 'Problem' index and 'Algorithm' columns
        df_std_pivot = df_std.pivot(index='Problem', columns='Algorithm', values='Mark')

    # Return the pivoted DataFrame with the requested metrics
    return df_pivot, df_std_pivot


