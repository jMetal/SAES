import pandas as pd
import numpy as np

# Scientific article reference: https://arxiv.org/pdf/1606.04316

def bayesian_sign_test(data: pd.DataFrame, 
                       rope_limits=[-0.01, 0.01], 
                       prior_strength=0.5, 
                       prior_place="rope", 
                       sample_size=5000) -> tuple:
    """
    Performs the Bayesian sign test to compare the performance of two algorithms across multiple instances.
    The Bayesian sign test is a non-parametric statistical test used to compare the performance of two algorithms on multiple instances. The null hypothesis is that the algorithms perform equivalently, which implies their average ranks are equal.

    Args:
        data (pd.DataFrame): 
            An (n x 2) array or DataFrame contaning the results. In data, each column represents an algorithm and, and each row an instance. Importante to take into accoun that all this dataframe stores the information of 1 execution pair algorithm-instance.
                - Example:
            +----------+-------------+-------------+
            |          | Algorithm A | Algorithm B |
            +----------+=============+=============+
            |  Inst1   | 0.008063    | 1.501062    |
            +----------+-------------+-------------+
            |  Inst2   | 0.004992    | 0.006439    |
            +----------+-------------+-------------+
            |  ...     | ...         | ...         |
            +----------+-------------+-------------+
            |  Instn   | 0.871175    | 0.3505      |
            +----------+-------------+-------------+

        rope_limits (list):
            Limits of the practical equivalence. Default is [-0.01, 0.01].
        
        prior_strength (float):
            Value of the prior strength. Default is 0.5.

        prior_place (str):
            Place of the pseudo-observation z_0. Default is "rope".

        sample_size (int):
            Total number of random_search samples generated. Default is 5000.
        
    Returns:
        tuple: A tuple containing the posterior probabilities and the samples drawn from the Dirichlet process. List of posterior probabilities:
            - Pr(algorith_1 < algorithm_2)
            - Pr(algorithm_1 equiv algorithm_2)
            - Pr(algorithm_1 > algorithm_2)
    """

    if prior_strength <= 0:
        raise ValueError("Initialization ERROR. prior_strength mustb be a positive float")

    if prior_place not in ["left", "rope", "right"]:
        raise ValueError("Initialization ERROR. Incorrect value fro prior_place")
    
    if type(data) == pd.DataFrame:
        data = data.values

    if data.shape[1] == 2:
        sample1, sample2 = data[:, 0], data[:, 1]
        n = data.shape[0]
    else:
        raise ValueError("Initialization ERROR. Incorrect number of dimensions for axis 1")

    # Compute the differences
    Z = sample1 - sample2

    # Compute the number of pairs diff > right_limit
    Nright = sum(Z > rope_limits[1])

    # Compute the number of pairs diff < right_lelft
    Nleft = sum(Z < rope_limits[0])

    # Compute the number of pairs diff in rope_limits
    Nequiv = n - Nright - Nleft

    # Parameters of the Dirichlet distribution
    alpha = np.array([Nleft, Nequiv, Nright], dtype=float) + 1e-6
    alpha[["left", "rope", "right"].index(prior_place)] += prior_strength

    # Simulate dirichlet process
    Dprocess = np.random.dirichlet(alpha, sample_size)

    # Compute posterior probabilities
    winner_id = np.argmax(Dprocess, axis=1)
    win_left = sum(winner_id == 0)
    win_rifht = sum(winner_id == 2)
    win_rope = sample_size - win_left - win_rifht

    return np.array([win_left, win_rope, win_rifht]) / float(sample_size), Dprocess

def bayesian_signed_rank_test(data, 
                              rope_limits=[-0.01, 0.01], 
                              prior_strength=1.0, 
                              prior_place="rope", 
                              sample_size=1000) -> tuple:
    """
    Performs the Bayesian version of the signed rank test to compare the performance of two algorithms across multiple instances.
    The Bayesian sign test is a non-parametric statistical test used to compare the performance of two algorithms on multiple instances. The null hypothesis is that the algorithms perform equivalently, which implies their average ranks are equal.

    Args:
        data (pd.DataFrame): 
            An (n x 2) array or DataFrame contaning the results. In data, each column represents an algorithm and, and each row an instance. Importante to take into accoun that all this dataframe stores the information of 1 execution pair algorithm-instance.
                - Example:
            +----------+-------------+-------------+
            |          | Algorithm A | Algorithm B |
            +----------+=============+=============+
            |  Inst1   | 0.008063    | 1.501062    |
            +----------+-------------+-------------+
            |  Inst2   | 0.004992    | 0.006439    |
            +----------+-------------+-------------+
            |  ...     | ...         | ...         |
            +----------+-------------+-------------+
            |  Instn   | 0.871175    | 0.3505      |
            +----------+-------------+-------------+

        rope_limits (list):
            Limits of the practical equivalence. Default is [-0.01, 0.01].
        
        prior_strength (float):
            Value of the prior strength. Default is 0.5.

        prior_place (str):
            Place of the pseudo-observation z_0. Default is "rope".

        sample_size (int):
            Total number of random_search samples generated. Default is 5000.
        
    Returns:
        tuple: A tuple containing the posterior probabilities and the samples drawn from the Dirichlet process. List of posterior probabilities:
            - Pr(algorith_1 < algorithm_2)
            - Pr(algorithm_1 equiv algorithm_2)
            - Pr(algorithm_1 > algorithm_2)
    """

    def weights(n, s):
        alpha = np.ones(n + 1)
        alpha[0] = s
        return np.random.dirichlet(alpha, 1)[0]

    if prior_strength <= 0:
        raise ValueError("Initialization ERROR. prior_strength must be a positive float")

    if prior_place not in ["left", "rope", "right"]:
        raise ValueError("Initialization ERROR. Incorrect value for prior_place")
    
    if type(data) == pd.DataFrame:
        data = data.values

    if data.shape[1] == 2:
        sample1, sample2 = data[:, 0], data[:, 1]
        n = data.shape[0]
    else:
        raise ValueError("Initialization ERROR. Incorrect number of dimensions for axis 1")

    # Compute the differences
    Z = sample1 - sample2
    Z0 = [-float("Inf"), 0.0, float("Inf")][["left", "rope", "right"].index(prior_place)]
    Z = np.concatenate(([Z0], Z), axis=None)

    # Compute the the probabilities that the mean difference of accuracy is in the interval (−Inf, left), [left, right], or (ringth, Inf).
    Dprocess = np.zeros((sample_size, 3))
    for mc in range(sample_size):
        W = weights(n, prior_strength)
        for i in range(n + 1):
            for j in range(i, n + 1):
                aux = Z[i] + Z[j]
                sumval = 2 * (W[i] * W[j]) if i != j else (W[i] * W[j])
                if aux < 2 * rope_limits[0]:
                    Dprocess[mc, 0] += sumval
                elif aux > 2 * rope_limits[1]:
                    Dprocess[mc, 2] += sumval
                else:
                    Dprocess[mc, 1] += sumval

    # Compute posterior probabilities
    winner_id = np.argmax(Dprocess, axis=1)
    win_left = sum(winner_id == 0)
    win_rifht = sum(winner_id == 2)
    win_rope = sample_size - win_left - win_rifht

    # Return the posterior probabilities
    return np.array([win_left, win_rope, win_rifht]) / float(sample_size), Dprocess
