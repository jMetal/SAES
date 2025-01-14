import pandas as pd
import numpy as np
from scipy.stats import rankdata, chi2
from scipy.stats import mannwhitneyu
from statsmodels.stats.libqsturng import qsturng

def friedman_test(data: pd.DataFrame, descending: bool) -> pd.DataFrame:
    """
    Performs Friedman's rank sum test to compare the performance of multiple algorithms across multiple instances.
    The Friedman test is a non-parametric statistical test used to detect differences in treatments (or algorithms) across multiple groups. The null hypothesis is that all algorithms perform equivalently, which implies their average ranks should be equal. The test is particularly useful when the data does not meet the assumptions of parametric tests like ANOVA.

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
        
        descending (bool):
            A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the Friedman statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.
            - Example:
                +--------------------+------------+
                | Friedman-statistic | p-value    |
                +===================-+============+
                | 12.34              | 0.0001     |
                +--------------------+------------+
    """

    # Initial Checking
    if isinstance(data, pd.DataFrame):
        data = data.values

    n_samples, k = data.shape
    if k < 2:
        raise ValueError("Initialization ERROR: The data must have at least two columns.")

    # Compute ranks, in the order specified by the descending parameter
    ranks = rankdata(-data, axis=1) if descending else rankdata(data, axis=1)

    # Calculate average ranks for each algorithm (column)
    average_ranks = np.mean(ranks, axis=0)

    # Compute the Friedman statistic
    rank_sum_squared = np.sum(average_ranks**2)
    friedman_stat = (12 * n_samples) / (k * (k + 1)) * (rank_sum_squared - (k * (k + 1)**2) / 4)

    # Calculate the p-value using the chi-squared distribution
    p_value = 1.0 - chi2.cdf(friedman_stat, df=(k - 1))

    # Return the result as a DataFrame
    return pd.DataFrame(
        data=np.array([friedman_stat, p_value]),
        index=["Friedman-statistic", "p-value"],
        columns=["Results"]
    )

def wilcoxon_test(data: pd.DataFrame):
    """
    Performs the Wilcoxon signed-rank test to compare the performance of two algorithms across multiple instances.
    The Wilcoxon signed-rank test is a non-parametric statistical test used to compare the performance of two algorithms on multiple instances. The null hypothesis is that the algorithms perform equivalently, which implies their average ranks are equal.

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

    Returns:
        str: A string indicating the result of the Wilcoxon test. The result can be one of the following:
            - "+" if Algorithm A outperforms Algorithm B.
            - "-" if Algorithm B outperforms Algorithm A.
            - "=" if both algorithms perform
    """

    median_a = data["Algorithm A"].median()
    median_b = data["Algorithm B"].median()

    # Realizar el test de Wilcoxon
    _, p_value = mannwhitneyu(data["Algorithm A"], data["Algorithm B"])

    # Interpretar el resultado
    alpha = 0.05
    if p_value <= alpha:
        return "+" if median_a > median_b else "-"
    else:
        return "="

def NemenyiCD(alpha: float, num_alg: int, num_dataset: int) -> float:
    """
    Computes Nemenyi's Critical Difference (CD) for post-hoc analysis. The formula for CD is:
        CD = q_alpha * sqrt(num_alg * (num_alg + 1) / (6 * num_prob))

    Args:
        alpha (float):
            The significance level for the critical difference calculation.
        
        num_alg (int):
            The number of algorithms being compared.
        
        num_dataset (int):
            The number of datasets/instances used for comparison.
    
    Returns:
        float: The critical difference value for Nemenyi's
    """

    # get critical value
    q_alpha = qsturng(p=1 - alpha, r=num_alg, v=num_alg * (num_dataset - 1)) / np.sqrt(2)

    # compute the critical difference
    return q_alpha * np.sqrt(num_alg * (num_alg + 1) / (6.0 * num_dataset))
