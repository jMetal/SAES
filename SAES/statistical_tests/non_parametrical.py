from statsmodels.stats.libqsturng import qsturng
from scipy.stats import wilcoxon as wx
from scipy.stats import chi2, f
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Article reference: https://www.statology.org/friedman-test-python/
# Wikipedia reference: https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test

def _ranks(data: np.array, maximize: bool):
    """Computes the rank of the elements in data."""

    # Set sorting order: ascending if maximize is False, descending if True
    s = 0 if (maximize is False) else 1

    # Handle case for 2D arrays
    if data.ndim == 2:
        # Initialize ranks with ones
        ranks = np.ones(data.shape)

        # Iterate over each row
        for i in range(data.shape[0]):
            # Sort data in the desired order and extract unique values, their indices, and repetitions
            values, indices, rep = np.unique(
                (-1) ** s * np.sort((-1) ** s * data[i, :]),
                return_index=True,
                return_counts=True,
            )

            # Assign ranks to each element in the row
            for j in range(data.shape[1]):
                # ranks[i, j] += indices[values == data[i, j]] + 0.5 * (rep[values == data[i, j]] - 1)
                ranks[i, j] += indices[values == data[i, j]].item() + 0.5 * (rep[values == data[i, j]].item() - 1)
        return ranks
    
    # Handle case for 1D arrays
    elif data.ndim == 1:
        # Initialize ranks with ones
        ranks = np.ones((data.size,))

        # Sort data in the desired order and extract unique values, their indices, and repetitions
        values, indices, rep = np.unique(
            (-1) ** s * np.sort((-1) ** s * data),
            return_index=True,
            return_counts=True,
        )

        # Assign ranks to each element
        for i in range(data.size):
            # ranks[i] += indices[values == data[i]] + 0.5 * (rep[values == data[i]] - 1)
            ranks[i] += indices[values == data[i]].item() + 0.5 * (rep[values == data[i]].item() - 1)

        return ranks

def friedman(data: pd.DataFrame, maximize: bool) -> pd.DataFrame:
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
        
        maximize (bool):
            A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the Friedman statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.
            - Example:
                +--------------------+------------+
                | Friedman-stat      | p-value    |
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

    # Compute ranks, in the order specified by the maximize parameter
    # ranks = rankdata(-data, axis=1) if maximize else rankdata(data, axis=1)
    ranks = _ranks(data, maximize)

    # Calculate average ranks for each algorithm (column)
    average_ranks = np.mean(ranks, axis=0)

    # Compute the Friedman statistic
    rank_sum_squared = np.sum(n_samples * (average_ranks**2))
    friedman_stat = (12 * n_samples) / (k * (k + 1)) * (rank_sum_squared - (k * (k + 1)**2) / 4)

    # Calculate the p-value using the chi-squared distribution
    p_value = 1.0 - chi2.cdf(friedman_stat, df=(k - 1))

    # Return the result as a DataFrame
    return pd.DataFrame(
        data=np.array([friedman_stat, p_value]),
        index=["Friedman-stat", "p-value"],
        columns=["Results"]
    )

def friedman_aligned_rank(data: pd.DataFrame, maximize: bool) -> pd.DataFrame:
    """
    Performs the Friedman aligned rank test to compare the performance of multiple algorithms across multiple instances.

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
        
        maximize (bool):
            A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the Friedman statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.
            - Example:
                +--------------------+------------+
                | Aligned Rank stat  | p-value    |
                +===================-+============+
                | 12.34              | 0.0001     |
                +--------------------+------------+
    """

    # Initial Checking
    if type(data) == pd.DataFrame:
        data = data.values

    # Ensure the data has the correct dimensions
    if data.ndim == 2:
        n_samples, k = data.shape
    else:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions")
    if k < 2:
        raise ValueError("Initialization Error. Incorrect number of dimensions for axis 1.")

    # Compute control values (average performance per instance)
    control = np.mean(data, axis=1)

    # Compute the difference between each algorithm's performance and the control
    diff = [data[:, j] - control for j in range(data.shape[1])]
    
    # Compute ranks of the aligned differences
    alignedRanks = _ranks(np.ravel(diff), maximize)
    alignedRanks = np.reshape(alignedRanks, newshape=(n_samples, k), order="F")

    # Compute sum of aligned ranks per instance and per algorithm
    Rhat_i = np.sum(alignedRanks, axis=1)
    Rhat_j = np.sum(alignedRanks, axis=0)

    # Compute statistical components
    si, sj = np.sum(Rhat_i**2), np.sum(Rhat_j**2)
    A = sj - (k * n_samples**2 / 4.0) * (k * n_samples + 1) ** 2
    B1 = k * n_samples * (k * n_samples + 1) * (2 * k * n_samples + 1) / 6.0
    B2 = si / float(k)

    # Compute the Friedman aligned rank statistic
    alignedRanks_stat = ((k - 1) * A) / (B1 - B2)

    # Calculate the p-value using the chi-squared distribution
    p_value = 1 - chi2.cdf(alignedRanks_stat, df=k - 1)

    # Return the result as a DataFrame
    return pd.DataFrame(
        data=np.array([alignedRanks_stat, p_value]), 
        index=["Aligned Rank stat", "p-value"], 
        columns=["Results"]
    )

def quade(data: pd.DataFrame, maximize: bool) -> pd.DataFrame:
    """
    Performs the Quade test to compare the performance of multiple algorithms across multiple instances.

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
        
        maximize (bool):
            A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the Friedman statistic and the corresponding p-value. The result can be used to determine whether there are significant differences between the algorithms.
            - Example:
                +--------------------+------------+
                | Quade Test stat    | p-value    |
                +===================-+============+
                | 12.34              | 0.0001     |
                +--------------------+------------+
    """

    # Initial Checking
    if type(data) == pd.DataFrame:
        data = data.values

    # Ensure the data has the correct dimensions
    if data.ndim == 2:
        n_samples, k = data.shape
    else:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions")
    if k < 2:
        raise ValueError("Initialization Error. Incorrect number of dimensions for axis 1.")

    # Compute ranks, in the order specified by the maximize parameter
    datarank = _ranks(data, maximize)

    # Compute the rank of the range of each problem
    problemRange = np.max(data, axis=1) - np.min(data, axis=1)
    problemRank = _ranks(problemRange, maximize)

    # Compute S_stat: weight of each observation within the problem, adjusted to reflect the significance of the problem when it appears.
    S_stat = np.zeros((n_samples, k))
    for i in range(n_samples):
        S_stat[i, :] = problemRank[i] * (datarank[i, :] - 0.5 * (k + 1))

    # Compute the sum of the ranks for each algorithm
    Salg = np.sum(S_stat, axis=0)

    # Compute Fq (Quade Test statistic) and associated p_value
    A = np.sum(S_stat**2)
    B = np.sum(Salg**2) / float(n_samples)

    # Compute the Quade test statistic and p-value
    if A == B:
        Fq = np.Inf
        p_value = (1 / (np.math.factorial(k))) ** (n_samples - 1)

    # Compute the Quade test statistic and p-value
    else:
        Fq = (n_samples - 1.0) * B / (A - B)
        p_value = 1 - f.cdf(Fq, k - 1, (k - 1) * (n_samples - 1))

    # Return the result as a DataFrame
    return pd.DataFrame(data=np.array([Fq, p_value]), 
                        index=["Quade Test stat", "p-value"], 
                        columns=["Results"])

def wilcoxon(data: pd.DataFrame, maximize: bool):
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
            
        maximize (bool):
            A boolean indicating whether to rank the data in descending order. If True, the algorithm with the highest performance will receive the lowest rank (i.e., rank 1). If False, the algorithm with the lowest performance will receive the lowest rank. Default is True.

    Returns:
        str: A string indicating the result of the Wilcoxon test. The result can be one of the following:
            - "+" if Algorithm A outperforms Algorithm B.
            - "-" if Algorithm B outperforms Algorithm A.
            - "=" if both algorithms perform
    """

    median_a = data["Algorithm A"].median()
    median_b = data["Algorithm B"].median()

    # Perform the Wilcoxon signed-rank test
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        _, p_value = wx(data["Algorithm A"], data["Algorithm B"])

    # Determine the result based on the p-value
    alpha = 0.05
    if p_value <= alpha:
        if maximize:
            return "+" if median_a > median_b else "-"
        else:
            return "+" if median_a <= median_b else "-"
    
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
        float: 
            The critical difference value for Nemenyi's
    """

    # Get critical value
    q_alpha = qsturng(p=1 - alpha, r=num_alg, v=num_dataset - 1) / np.sqrt(2)

    # Compute the critical difference
    return q_alpha * np.sqrt(num_alg * (num_alg + 1) / (6.0 * num_dataset))
