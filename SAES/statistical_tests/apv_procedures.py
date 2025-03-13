import numpy as np
import pandas as pd

from SAES.statistical_tests.non_parametrical import _ranks
from scipy.stats import rankdata, mannwhitneyu, chi2, binom, f, norm

def friedman_ph_test(data: pd.DataFrame, maximize: bool, control=None, apv_procedure=None) -> pd.DataFrame:
    """Friedman post-hoc test.

    :param data: An (n x 2) array or DataFrame contaning the results. In data, each column represents an algorithm and, and each row a problem.
    :param control: optional int or string. Default None. Index or Name of the control algorithm. If control = None all FriedmanPosHocTest considers all possible comparisons among algorithms.
    :param apv_procedure: optional string. Default None.
        Name of the procedure for computing adjusted p-values. If apv_procedure
        is None, adjusted p-value are not computed, else the values are computed
        according to the specified procedure:
        For 1 vs all comparisons.
            {'Bonferroni', 'Holm', 'Hochberg', 'Holland', 'Finner', 'Li'}
        For all vs all coparisons.
            {'Shaffer', 'Holm', 'Nemenyi'}

    :return z_values: Test statistic.
    :return p_values: The p-value according to the Studentized range distribution.
    """

    # Initial Checking
    if type(data) == pd.DataFrame:
        algorithms = data.columns
        data = data.values
    elif type(data) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(data.shape[1])])

    if control is None:
        index = algorithms
    elif type(control) == int:
        index = [algorithms[control]]
    else:
        index = [control]

    if data.ndim == 2:
        n_samples, k = data.shape
    else:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")
    if k < 2:
        raise ValueError("Initialization Error. Incorrect number of dimensions for axis 1.")

    if control is not None:
        if type(control) == int and control >= data.shape[1]:
            raise ValueError("Initialization ERROR. control is out of bounds")
        if type(control) == str and control not in algorithms:
            raise ValueError("Initialization ERROR. %s is not a column name of data" % control)

    if apv_procedure is not None:
        if apv_procedure not in [
            "Bonferroni",
            "Holm",
            "Hochberg",
            "Hommel",
            "Holland",
            "Finner",
            "Li",
            "Shaffer",
            "Nemenyi",
        ]:
            raise ValueError("Initialization ERROR. Incorrect value for APVprocedure.")

    # Compute ranks.
    datarank = _ranks(data, maximize)
    # Compute for each algorithm the ranking average.
    avranks = np.mean(datarank, axis=0)

    # Compute z-values
    aux = np.sqrt((k * (k + 1)) / (6.0 * n_samples))

    if control is None:
        z = np.zeros((k, k))
        for i in range(k):
            for j in range(i + 1, k):
                z[i, j] = abs(avranks[i] - avranks[j]) / aux
        z += z.T
    else:
        if type(control) == str:
            control = int(np.where(algorithms == control)[0])
        z = np.zeros((1, k))
        for j in range(k):
            z[0, j] = abs(avranks[control] - avranks[j]) / aux

    # Compute associated p-value
    p_value = 2 * (1.0 - norm.cdf(z))

    pvalues_df = pd.DataFrame(data=p_value, index=index, columns=algorithms)
    zvalues_df = pd.DataFrame(data=z, index=index, columns=algorithms)

    if apv_procedure is None:
        return zvalues_df, pvalues_df
    else:
        if apv_procedure == "Bonferroni":
            ap_vs_df = bonferroni_dunn(pvalues_df, control=control)
        elif apv_procedure == "Holm":
            ap_vs_df = holm(pvalues_df, control=control)
        elif apv_procedure == "Hochberg":
            ap_vs_df = hochberg(pvalues_df, control=control)
        elif apv_procedure == "Holland":
            ap_vs_df = holland(pvalues_df, control=control)
        elif apv_procedure == "Finner":
            ap_vs_df = finner(pvalues_df, control=control)
        elif apv_procedure == "Li":
            ap_vs_df = li(pvalues_df, control=control)
        elif apv_procedure == "Shaffer":
            ap_vs_df = shaffer(pvalues_df)
        elif apv_procedure == "Nemenyi":
            ap_vs_df = nemenyi(pvalues_df)

        return zvalues_df, pvalues_df, ap_vs_df


def friedman_aligned_ph_test(data: pd.DataFrame, maximize: bool, control=None, apv_procedure=None) -> pd.DataFrame:
    """Friedman Aligned Ranks post-hoc test.

    :param data: An (n x 2) array or DataFrame contaning the results. In data, each column represents an algorithm and, and each row a problem.
    :param control: optional int or string. Default None. Index or Name of the control algorithm. If control = None all FriedmanPosHocTest considers all possible comparisons among algorithms.
    :param apv_procedure: optional string. Default None.
        Name of the procedure for computing adjusted p-values. If apv_procedure
        is None, adjusted p-value are not computed, else the values are computed
        according to the specified procedure:
        For 1 vs all comparisons.
            {'Bonferroni', 'Holm', 'Hochberg', 'Holland', 'Finner', 'Li'}
        For all vs all coparisons.
            {'Shaffer', 'Holm', 'Nemenyi'}

    :return z_values: Test statistic.
    :return p_values: The p-value according to the Studentized range distribution.
    """

    # Initial Checking
    if type(data) == pd.DataFrame:
        algorithms = data.columns
        data = data.values
    elif type(data) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(data.shape[1])])

    if control is None:
        index = algorithms
    elif type(control) == int:
        index = [algorithms[control]]
    else:
        index = [control]

    if data.ndim == 2:
        n_samples, k = data.shape
    else:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")
    if k < 2:
        raise ValueError("Initialization Error. Incorrect number of dimensions for axis 1.")

    if control is not None:
        if type(control) == int and control >= data.shape[1]:
            raise ValueError("Initialization ERROR. control is out of bounds")
        if type(control) == str and control not in algorithms:
            raise ValueError("Initialization ERROR. %s is not a column name of data" % control)

    # Compute the average value achieved by all algorithms in each problem
    problemmean = np.mean(data, axis=1)
    # Compute the difference between control an data
    diff = np.zeros((n_samples, k))
    for j in range(k):
        diff[:, j] = data[:, j] - problemmean

    alignedRanks = _ranks(np.ravel(diff), maximize)
    alignedRanks = np.reshape(alignedRanks, newshape=(n_samples, k))

    # Average ranks
    avranks = np.mean(alignedRanks, axis=0)

    # Compute test statistics
    aux = 1.0 / np.sqrt(k * (n_samples + 1) / 6.0)
    if control is None:
        z = np.zeros((k, k))
        for i in range(k):
            for j in range(i + 1, k):
                z[i, j] = abs(avranks[i] - avranks[j]) * aux
        z += z.T
    else:
        if type(control) == str:
            control = int(np.where(algorithms == control)[0])
        z = np.zeros((1, k))
        for j in range(k):
            z[0, j] = abs(avranks[control] - avranks[j]) * aux

    # Compute associated p-value
    p_value = 2 * (1.0 - norm.cdf(z))

    pvalues_df = pd.DataFrame(data=p_value, index=index, columns=algorithms)
    zvalues_df = pd.DataFrame(data=z, index=index, columns=algorithms)

    if apv_procedure is None:
        return zvalues_df, pvalues_df
    else:
        if apv_procedure == "Bonferroni":
            ap_vs_df = bonferroni_dunn(pvalues_df, control=control)
        elif apv_procedure == "Holm":
            ap_vs_df = holm(pvalues_df, control=control)
        elif apv_procedure == "Hochberg":
            ap_vs_df = hochberg(pvalues_df, control=control)
        elif apv_procedure == "Holland":
            ap_vs_df = holland(pvalues_df, control=control)
        elif apv_procedure == "Finner":
            ap_vs_df = finner(pvalues_df, control=control)
        elif apv_procedure == "Li":
            ap_vs_df = li(pvalues_df, control=control)
        elif apv_procedure == "Shaffer":
            ap_vs_df = shaffer(pvalues_df)
        elif apv_procedure == "Nemenyi":
            ap_vs_df = nemenyi(pvalues_df)

        return zvalues_df, pvalues_df, ap_vs_df


def quade_ph_test(data: pd.DataFrame, maximize: bool, control=None, apv_procedure=None) -> pd.DataFrame:
    """Quade post-hoc test.

    :param data: An (n x 2) array or DataFrame contaning the results. In data, each column represents an algorithm and, and each row a problem.
    :param control: optional int or string. Default None. Index or Name of the control algorithm. If control = None all FriedmanPosHocTest considers all possible comparisons among algorithms.
    :param apv_procedure: optional string. Default None.
        Name of the procedure for computing adjusted p-values. If apv_procedure
        is None, adjusted p-value are not computed, else the values are computed
        according to the specified procedure:
        For 1 vs all comparisons.
            {'Bonferroni', 'Holm', 'Hochberg', 'Holland', 'Finner', 'Li'}
        For all vs all coparisons.
            {'Shaffer', 'Holm', 'Nemenyi'}

    :return z_values: Test statistic.
    :return p_values: The p-value according to the Studentized range distribution.
    """

    # Initial Checking
    if type(data) == pd.DataFrame:
        algorithms = data.columns
        data = data.values
    elif type(data) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(data.shape[1])])

    if control is None:
        index = algorithms
    elif type(control) == int:
        index = [algorithms[control]]
    else:
        index = [control]

    if data.ndim == 2:
        n_samples, k = data.shape
    else:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")
    if k < 2:
        raise ValueError("Initialization Error. Incorrect number of dimensions for axis 1.")

    if control is not None:
        if type(control) == int and control >= data.shape[1]:
            raise ValueError("Initialization ERROR. control is out of bounds")
        if type(control) == str and control not in algorithms:
            raise ValueError("Initialization ERROR. %s is not a column name of data" % control)

    # Compute ranks.
    datarank = _ranks(data, maximize)
    # Compute the range of each problem
    problemRange = np.max(data, axis=1) - np.min(data, axis=1)
    # Compute problem rank
    problemRank = _ranks(problemRange, maximize)

    # Compute average rakings
    W = np.zeros((n_samples, k))
    for i in range(n_samples):
        W[i, :] = problemRank[i] * datarank[i, :]
    avranks = 2 * np.sum(W, axis=0) / (n_samples * (n_samples + 1))
    # Compute test statistics
    aux = 1.0 / np.sqrt(k * (k + 1) * (2 * n_samples + 1) * (k - 1) / (18.0 * n_samples * (n_samples + 1)))
    if control is None:
        z = np.zeros((k, k))
        for i in range(k):
            for j in range(i + 1, k):
                z[i, j] = abs(avranks[i] - avranks[j]) * aux
        z += z.T
    else:
        if type(control) == str:
            control = int(np.where(algorithms == control)[0])
        z = np.zeros((1, k))
        for j in range(k):
            z[0, j] = abs(avranks[control] - avranks[j]) * aux

    # Compute associated p-value
    p_value = 2 * (1.0 - norm.cdf(z))

    pvalues_df = pd.DataFrame(data=p_value, index=index, columns=algorithms)
    zvalues_df = pd.DataFrame(data=z, index=index, columns=algorithms)

    if apv_procedure is None:
        return zvalues_df, pvalues_df
    else:
        if apv_procedure == "Bonferroni":
            ap_vs_df = bonferroni_dunn(pvalues_df, control=control)
        elif apv_procedure == "Holm":
            ap_vs_df = holm(pvalues_df, control=control)
        elif apv_procedure == "Hochberg":
            ap_vs_df = hochberg(pvalues_df, control=control)
        elif apv_procedure == "Holland":
            ap_vs_df = holland(pvalues_df, control=control)
        elif apv_procedure == "Finner":
            ap_vs_df = finner(pvalues_df, control=control)
        elif apv_procedure == "Li":
            ap_vs_df = li(pvalues_df, control=control)
        elif apv_procedure == "Shaffer":
            ap_vs_df = shaffer(pvalues_df)
        elif apv_procedure == "Nemenyi":
            ap_vs_df = nemenyi(pvalues_df)

        return zvalues_df, pvalues_df, ap_vs_df
    
def bonferroni_dunn(p_values, control):
    """
    Bonferroni-Dunn's procedure for the adjusted p-value computation.

    Parameters:
    -----------
    p_values: 2-D array or DataFrame containing the p-values obtained from a ranking test.
    control: int or string. Index or Name of the control algorithm.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if type(control) == str:
        control = int(np.where(algorithms == control)[0])
    if control is None:
        raise ValueError("Initialization ERROR. Incorrect value for control.")

    k = p_values.shape[1]

    # sort p-values p(0) <= p(1) <= ... <= p(k-1)
    argsorted_pvals = np.argsort(p_values[0, :])

    APVs = np.zeros((k - 1, 1))
    comparison = []
    for i in range(k - 1):
        comparison.append(algorithms[control] + " vs " + algorithms[argsorted_pvals[i]])
        APVs[i, 0] = np.min([(k - 1) * p_values[0, argsorted_pvals[i]], 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Bonferroni"])


def holland(p_values, control):
    """
    Holland's procedure for the adjusted p-value computation.

    Parameters:
    -----------
    p_values: 2-D array or DataFrame containing the p-values obtained from a ranking test.
    control: int or string. Index or Name of the control algorithm.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if type(control) == str:
        control = int(np.where(algorithms == control)[0])
    if control is None:
        raise ValueError("Initialization ERROR. Incorrect value for control.")

    # --------------------------------------------------------------------------
    # ------------------------------- Procedure --------------------------------
    # --------------------------------------------------------------------------
    k = p_values.shape[1]

    # sort p-values p(0) <= p(1) <= ... <= p(k-1)
    argsorted_pvals = np.argsort(p_values[0, :])

    APVs = np.zeros((k - 1, 1))
    comparison = []
    for i in range(k - 1):
        comparison.append(algorithms[control] + " vs " + algorithms[argsorted_pvals[i]])
        aux = k - 1 - np.arange(i + 1)
        v = np.max(1 - (1 - p_values[0, argsorted_pvals[: (i + 1)]]) ** aux)
        APVs[i, 0] = np.min([v, 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Holland"])


def finner(p_values, control):
    """
    Finner's procedure for the adjusted p-value computation.

    Parameters:
    -----------
    p_values: 2-D array or DataFrame containing the p-values obtained from a ranking test.
    control: int or string. Index or Name of the control algorithm.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if type(control) == str:
        control = int(np.where(algorithms == control)[0])
    if control is None:
        raise ValueError("Initialization ERROR. Incorrect value for control.")

    k = p_values.shape[1]

    # sort p-values p(0) <= p(1) <= ... <= p(k-1)
    argsorted_pvals = np.argsort(p_values[0, :])

    APVs = np.zeros((k - 1, 1))
    comparison = []
    for i in range(k - 1):
        comparison.append(algorithms[control] + " vs " + algorithms[argsorted_pvals[i]])
        aux = float(k - 1) / (np.arange(i + 1) + 1)
        v = np.max(1 - (1 - p_values[0, argsorted_pvals[: (i + 1)]]) ** aux)
        APVs[i, 0] = np.min([v, 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Finner"])


def hochberg(p_values, control):
    """
    Hochberg's procedure for the adjusted p-value computation.

    Parameters:
    -----------
    p_values: 2-D array or DataFrame containing the p-values obtained from a ranking test.
    control: int or string. Index or Name of the control algorithm.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if type(control) == str:
        control = int(np.where(algorithms == control)[0])
    if control is None:
        raise ValueError("Initialization ERROR. Incorrect value for control.")

    k = p_values.shape[1]

    # sort p-values p(0) <= p(1) <= ... <= p(k-1)
    argsorted_pvals = np.argsort(p_values[0, :])

    APVs = np.zeros((k - 1, 1))
    comparison = []
    for i in range(k - 1):
        comparison.append(algorithms[control] + " vs " + algorithms[argsorted_pvals[i]])
        aux = np.arange(k, i, -1).astype(np.uint8)
        v = np.max(p_values[0, argsorted_pvals[aux - 1]] * (k - aux))
        APVs[i, 0] = np.min([v, 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Hochberg"])


def li(p_values, control):
    """
    Li's procedure for the adjusted p-value computation.

    Parameters:
    -----------
    p_values: 2-D array or DataFrame containing the p-values obtained from a ranking test.
    control: optional int or string. Default None
        Index or Name of the control algorithm. If control is provided, control vs all
        comparisons are considered, else all vs all.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if type(control) == str:
        control = int(np.where(algorithms == control)[0])
    if control is None:
        raise ValueError("Initialization ERROR. Incorrect value for control.")

    k = p_values.shape[1]

    # sort p-values p(0) <= p(1) <= ... <= p(k-1)
    argsorted_pvals = np.argsort(p_values[0, :])

    APVs = np.zeros((k - 1, 1))
    comparison = []
    for i in range(k - 1):
        comparison.append(algorithms[control] + " vs " + algorithms[argsorted_pvals[i]])
        APVs[i, 0] = np.min(
            [
                p_values[0, argsorted_pvals[-2]],
                p_values[0, argsorted_pvals[i]]
                / (p_values[0, argsorted_pvals[i]] + 1 - p_values[0, argsorted_pvals[-2]]),
            ]
        )
    return pd.DataFrame(data=APVs, index=comparison, columns=["Li"])


def holm(p_values, control=None):
    """
    Holm's procedure for the adjusted p-value computation.

    Parameters:
    -----------
    p_values: 2-D array or DataFrame containing the p-values obtained from a ranking test.
    control: optional int or string. Default None
        Index or Name of the control algorithm. If control is provided, control vs all
        comparisons are considered, else all vs all.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if type(control) == str:
        control = int(np.where(algorithms == control)[0])

    if type(control) == int:
        k = p_values.shape[1]

        # sort p-values p(0) <= p(1) <= ... <= p(k-1)
        argsorted_pvals = np.argsort(p_values[0, :])

        APVs = np.zeros((k - 1, 1))
        comparison = []
        for i in range(k - 1):
            aux = k - 1 - np.arange(i + 1)
            comparison.append(algorithms[control] + " vs " + algorithms[argsorted_pvals[i]])
            v = np.max(aux * p_values[0, argsorted_pvals[: (i + 1)]])
            APVs[i, 0] = np.min([v, 1])

    elif control is None:
        k = p_values.shape[1]
        m = int((k * (k - 1)) / 2.0)

        # sort p-values p(0) <= p(1) <= ... <= p(m-1)
        pairs_index = np.triu_indices(k, 1)
        pairs_pvals = p_values[pairs_index]
        pairs_sorted = np.argsort(pairs_pvals)

        APVs = np.zeros((m, 1))
        aux = pairs_pvals[pairs_sorted] * (m - np.arange(m))
        comparison = []
        for i in range(m):
            row = pairs_index[0][pairs_sorted[i]]
            col = pairs_index[1][pairs_sorted[i]]
            comparison.append(algorithms[row] + " vs " + algorithms[col])
            v = np.max(aux[: i + 1])
            APVs[i, 0] = np.min([v, 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Holm"])


def shaffer(p_values):
    """
    Shaffer's procedure for adjusted p_value ccmputation.

    Parameters:
    -----------
    data: 2-D array or DataFrame containing the p-values.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    def S(k):
        """
        Computes the set of possible numbers of true hoypotheses.

        Parameters:
        -----------
        k: int
            number of algorithms being compared.

        Returns
        ----------
        TrueSet : array-like
            Set of true hypotheses.
        """

        from scipy.special import binom as binomial

        TrueHset = [0]
        if k > 1:
            for j in np.arange(k, 0, -1, dtype=int):
                TrueHset = list(set(TrueHset) | set([binomial(j, 2) + x for x in S(k - j)]))
        return TrueHset

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if p_values.ndim != 2:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")
    elif p_values.shape[0] != p_values.shape[1]:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")

    # define parameters
    k = p_values.shape[0]
    m = int(k * (k - 1) / 2.0)
    s = np.array(S(k)[1:])

    # sort p-values p(0) <= p(1) <= ... <= p(m-1)
    pairs_index = np.triu_indices(k, 1)
    pairs_pvals = p_values[pairs_index]
    pairs_sorted = np.argsort(pairs_pvals)

    # compute ti: max number of hypotheses that can be true given that any
    # (i-1) hypotheses are false.
    t = np.sort(-np.repeat(s[:-1], (s[1:] - s[:-1]).astype(np.uint8)))
    t = np.insert(-t, 0, s[-1])

    # Adjust p-values
    APVs = np.zeros((m, 1))
    aux = pairs_pvals[pairs_sorted] * t
    comparison = []
    for i in range(m):
        row = pairs_index[0][pairs_sorted[i]]
        col = pairs_index[1][pairs_sorted[i]]
        comparison.append(algorithms[row] + " vs " + algorithms[col])
        v = np.max(aux[: i + 1])
        APVs[i, 0] = np.min([v, 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Shaffer"])


def nemenyi(p_values):
    """
    Nemenyi's procedure for adjusted p_value computation.

    Parameters:
    -----------
    data: 2-D array or DataFrame containing the p-values.

    Returns:
    --------
    APVs: DataFrame containing the adjusted p-values.
    """

    # Initial Checking
    if type(p_values) == pd.DataFrame:
        algorithms = p_values.columns
        p_values = p_values.values
    elif type(p_values) == np.ndarray:
        algorithms = np.array(["Alg%d" % alg for alg in range(p_values.shape[1])])

    if p_values.ndim != 2:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")
    elif p_values.shape[0] != p_values.shape[1]:
        raise ValueError("Initialization ERROR. Incorrect number of array dimensions.")

    # define parameters
    k = p_values.shape[0]
    m = int(k * (k - 1) / 2.0)

    # sort p-values p(0) <= p(1) <= ... <= p(m-1)
    pairs_index = np.triu_indices(k, 1)
    pairs_pvals = p_values[pairs_index]
    pairs_sorted = np.argsort(pairs_pvals)

    # Adjust p-values
    APVs = np.zeros((m, 1))
    comparison = []
    for i in range(m):
        row = pairs_index[0][pairs_sorted[i]]
        col = pairs_index[1][pairs_sorted[i]]
        comparison.append(algorithms[row] + " vs " + algorithms[col])
        APVs[i, 0] = np.min([pairs_pvals[pairs_sorted[i]] * m, 1])
    return pd.DataFrame(data=APVs, index=comparison, columns=["Nemenyi"])
