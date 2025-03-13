import scipy.stats as stats
import pandas as pd
import numpy as np

def t_test(data: pd.DataFrame, maximize: bool):
    """
    Perform the T-Test signed-rank test to compare two algorithms.

    Args:
        data (pd.DataFrame):
            A DataFrame containing the performance results. Each row represents the performance of both algorithms on a instance. The DataFrame should have two columns, one for each algorithm.
                - Example:
            +-------+-------------+-------------+
            |   0   | Algorithm A | Algorithm B |
            +-------+=============+=============+
            |   1   | 0.008063    | 1.501062    |
            +-------+-------------+-------------+
            |   2   | 0.004992    | 0.006439    |
            +-------+-------------+-------------+
            | ...   | ...         | ...         |
            +-------+-------------+-------------+
            |  30   | 0.871175    | 0.3505      |
            +-------+-------------+-------------+
            
        maximize (bool):
            A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.

    Returns:
        str: A string indicating the result of the T-Test test. The result can be one of the following:
            - "+" if Algorithm A outperforms Algorithm B.
            - "-" if Algorithm B outperforms Algorithm A.
            - "=" if both algorithms perform
    """

    mean_a = data["Algorithm A"].mean()
    mean_b = data["Algorithm B"].mean()

    # Perform the T-Test signed-rank test
    _, p_value = stats.ttest_rel(data["Algorithm A"], data["Algorithm B"])

    # Determine the result based on the p-value
    alpha = 0.05
    if p_value <= alpha:
        if maximize:
            return "+" if mean_a > mean_b else "-"
        else:
            return "+" if mean_a <= mean_b else "-"
    
    return "="

def anova(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform the ANOVA test to compare the performance of multiple algorithms.

    Args:
        data (pd.DataFrame): 
            A 2D array or DataFrame containing the performance results. Each row represents the performance of different algorithms on a instance, and each column represents a different algorithm. For example, data.shape should be (n, k), where n is the number of instances, and k is the number of algorithms.
                - Example:
                    +----------+-------------+-------------+-------------+-------------+
                    |          | Algorithm A | Algorithm B | Algorithm C | Algorithm D |
                    +==========+=============+=============+=============+=============+
                    |    0     | 0.008063    | 1.501062    | 1.204757    | 2.071152    | 
                    +----------+-------------+-------------+-------------+-------------+
                    |    1     | 0.004992    | 0.006439    | 0.009557    | 0.007497    | 
                    +----------+-------------+-------------+-------------+-------------+
                    | ...      | ...         | ...         | ...         | ...         | 
                    +----------+-------------+-------------+-------------+-------------+
                    |    30    | 0.871175    | 0.3505      | 0.546       | 0.5345      | 
                    +----------+-------------+-------------+-------------+-------------+
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the Friedman statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.
            - Example:
                +--------------------+------------+
                | Anova-stat         | p-value    |
                +===================-+============+
                | 12.34              | 0.0001     |
                +--------------------+------------+
    """

    # Initial Checking
    if isinstance(data, pd.DataFrame):
        data = data.values

    _, k = data.shape
    if k < 2:
        raise ValueError("Initialization ERROR: The data must have at least two columns.")
    
    f_statistic, p_value = stats.f_oneway(*data)

    return pd.DataFrame(
        data=np.array([f_statistic, p_value]),
        index=["Anova-stat", "p-value"],
        columns=["Results"]
    )
