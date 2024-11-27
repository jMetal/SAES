import pandas as pd
import numpy as np
from scipy.stats import rankdata, chi2
from csv_processor import process_csv_extended
from scipy.stats import rankdata
# from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu

def friedman_test(csv_path: str, descending=True) -> pd.DataFrame:
    """Performs Friedman's rank sum test to compare the performance of multiple algorithms across multiple problems.

    The Friedman test is a non-parametric statistical test used to detect differences in treatments (or algorithms) across multiple groups. The null hypothesis is that all algorithms perform equivalently, which implies their average ranks should be equal. The test is particularly useful when the data does not meet the assumptions of parametric tests like ANOVA.

    Example:
    Suppose we have the following performance results of three algorithms (A, B, and C) across five problems:
    
    Algorithm A | Algorithm B | Algorithm C
    ----------------------------------------
    0.9         | 0.8         | 0.8
    0.85        | 0.75        | 0.8
    0.95        | 0.85        | 0.9
    0.8         | 0.85        | 0.88
    0.92        | 0.87        | 0.91

    In this case, the null hypothesis is that the performance of the algorithms is the same across all problems.

    :param data: A 2D array or DataFrame containing the performance results. Each row represents the performance of different algorithms on a problem, and each column represents a different algorithm. For example, data.shape should be (n, k), where n is the number of problems, and k is the number of algorithms.
    :param descending: A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.

    :return: A pandas DataFrame containing the Friedman statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.

    :raises ValueError: If the input data is not a 2D array or DataFrame, or if the number of algorithms (columns) is less than 2.

    :note: The null hypothesis is that all algorithms are equivalent, i.e., their average ranks are equal. A low p-value indicates a significant difference between the algorithms' performances.
    
    :seealso: `scipy.stats.chi2` for chi-square distribution functions.
    """

    data, _, _ = process_csv_extended(csv_path)

    # Initial Checking
    if isinstance(data, pd.DataFrame):
        data = data.values

    if data.ndim != 2:
        raise ValueError("Initialization ERROR: Data must have two dimensions.")
    
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
    """Performs the Wilcoxon signed-rank test to compare the performance of two algorithms across multiple problems.

    The Wilcoxon signed-rank test is a non-parametric statistical test used to compare the performance of two algorithms on multiple problems. The null hypothesis is that the algorithms perform equivalently, which implies their average ranks are equal.

    Example:
    Suppose we have the following performance results of two algorithms (A and B) across five problems:
    
    Algorithm A | Algorithm B
    --------------------------
    0.9         | 0.8
    0.85        | 0.75
    0.95        | 0.85
    0.8         | 0.85
    0.92        | 0.87

    In this case, the null hypothesis is that the performance of the two algorithms is the same across all problems.

    :param data: A DataFrame containing the performance results. Each row represents the performance of both algorithms on a problem. The DataFrame should have two columns, one for each algorithm.

    :return: A pandas DataFrame containing the Wilcoxon statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.

    :raises ValueError: If the input data is not a DataFrame, or if the number of columns is not equal to 2.

    :note: The null hypothesis is that the two algorithms are equivalent, i.e., their average ranks are equal. A low p-value indicates a significant difference between the algorithms' performances.
    
    :seealso: `scipy.stats.rankdata` for ranking data.
    """

    """
    # we create a new test dataframe
    data = {
        "Algorithm A": [456, 564, 54, 554, 54, 51, 1, 12, 45, 5, 456, 564, 54, 554, 54, 51, 1, 12, 45, 5, 456, 564, 54, 554, 54, 51, 1, 12, 45, 5],
        "Algorithm B": [65, 87, 456, 564, 456, 564, 564, 6, 4, 564, 65, 87, 456, 564, 456, 564, 564, 6, 4, 564, 65, 87, 456, 564, 456, 564, 564, 6, 4, 564]
    }

    data = pd.DataFrame(data)
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
    