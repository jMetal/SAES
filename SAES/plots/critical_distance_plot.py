import numpy as np
import pandas as pd
from SAES.statistical_tests.non_parametrical import NemenyiCD
from SAES.utils.csv_processor import process_dataframe_extended
from SAES.utils.csv_processor import obtain_list_metrics
from scipy.stats import rankdata
import matplotlib.pyplot as plt
import os

from SAES.logger import get_logger
logger = get_logger(__name__)

def CDplot_metric(data: pd.DataFrame, metric: str, alpha: float = 0.05, higher_is_better: bool = False) -> None:
    """
    Creates a critical distance plot to compare the performance of different algorithms on a specific problem.

    Parameters:
    data (pd.DataFrame): A DataFrame containing the data for a specific problem, with columns for algorithms and performance marks:
    AutoMOPSOD  AutoMOPSORE  AutoMOPSOW  AutoMOPSOZ    NSGAII    OMOPSO     SMPSO
    DTLZ1    0.008063     1.501062    1.204757    2.071152  0.413378  1.000000  0.011571
    DTLZ2    0.004992     0.006439    0.009557    0.007497  0.012612  0.006407  0.006556
    DTLZ3    0.025848     3.991959    1.875400    6.131452  1.155789  3.291164  0.203524
    DTLZ4    0.004965     0.011184    0.031624    0.016845  0.014132  0.007744  0.006859
    DTLZ5    0.004589     0.006358    0.010652    0.006825  0.011919  0.005922  0.005828
    DTLZ6    0.004915     0.004569    1.000000    0.004490  0.944101  0.038736  0.018126
    DTLZ7    0.005071     0.013038    0.031957    0.003955  0.016132  0.013000  0.006951
    RE21     0.006046     0.005378    0.005553    0.005496  0.011490  0.006004  0.006269
    metric (str): The metric to be used for the calculations. It should match the column name in the CSV file.
    alpha (float): The significance level for the critical distance calculation. Default is 0.05.
    higher_is_better (bool): Whether higher metric values are better. Default is False.
    
    Returns:
    None: The function saves the boxplot as a PNG file.
    """

    def _join_alg(avranks, num_alg, cd):
        """
        join_alg returns the set of non significant methods
        """

        # get all pairs
        sets = (-1) * np.ones((num_alg, 2))
        for i in range(num_alg):
            elements = np.where(np.logical_and(avranks - avranks[i] > 0, avranks - avranks[i] < cd))[0]
            if elements.size > 0:
                sets[i, :] = [avranks[i], avranks[elements[-1]]]
        sets = np.delete(sets, np.where(sets[:, 0] < 0)[0], axis=0)

        # group pairs
        group = sets[0, :]
        for i in range(1, sets.shape[0]):
            if sets[i - 1, 1] < sets[i, 1]:
                group = np.vstack((group, sets[i, :]))

        return group
    
    alg_names = data.columns
    data = data.values

    if data.ndim == 2:
        num_dataset, num_alg = data.shape
    else:
        raise ValueError("Initialization ERROR: In CDplot(...) results must be 2-D array")

    # Get the critical difference
    cd = NemenyiCD(alpha, num_alg, num_dataset)

    # Compute ranks. (ranks[i][j] rank of the i-th algorithm on the j-th problem.)
    rranks = rankdata(-data, axis=1) if higher_is_better else rankdata(data, axis=1)

    # Compute for each algorithm the ranking averages.
    avranks = np.transpose(np.mean(rranks, axis=0))
    indices = np.argsort(avranks).astype(np.uint8)
    avranks = avranks[indices]

    # Split algorithms.
    spoint = np.round(num_alg / 2.0).astype(np.uint8)
    leftalg = avranks[:spoint]

    rightalg = avranks[spoint:]
    rows = np.ceil(num_alg / 2.0).astype(np.uint8)

    # Figure settings.
    highest = np.ceil(np.max(avranks)).astype(np.uint8)  # highest shown rank
    lowest = np.floor(np.min(avranks)).astype(np.uint8)  # lowest shown rank
    width = 6  # default figure width (in inches)
    height = 0.575 * (rows + 1)  # figure height

    """
                        FIGURE
      (1,0)
        +-----+---------------------------+-------+
        |     |                           |       |
        |     |                           |       |
        |     |                           |       |
        +-----+---------------------------+-------+ stop
        |     |                           |       |
        |     |                           |       |
        |     |                           |       |
        |     |                           |       |
        |     |                           |       |
        |     |                           |       |
        +-----+---------------------------+-------+ sbottom
        |     |                           |       |
        +-----+---------------------------+-------+
            sleft                       sright     (0,1)
    """

    stop, sbottom, sleft, sright = 0.65, 0.1, 0.15, 0.85

    # main horizontal axis length
    lline = sright - sleft

    # Initialize figure
    fig = plt.figure(figsize=(width, height), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()

    # Main horizontal axis
    ax.hlines(stop, sleft, sright, color="black", linewidth=0.7)
    for xi in range(highest - lowest + 1):
        # Plot mayor ticks
        ax.vlines(
            x=sleft + (lline * xi) / (highest - lowest), ymin=stop, ymax=stop + 0.05, color="black", linewidth=0.7
        )
        # Mayor ticks labels
        ax.text(
            x=sleft + (lline * xi) / (highest - lowest), y=stop + 0.06, s=str(lowest + xi), ha="center", va="bottom"
        )
        # Minor ticks
        if xi < highest - lowest:
            ax.vlines(
                x=sleft + (lline * (xi + 0.5)) / (highest - lowest),
                ymin=stop,
                ymax=stop + 0.025,
                color="black",
                linewidth=0.7,
            )

    # Plot lines/names for left models
    vspace = 0.5 * (stop - sbottom) / (spoint + 1)
    for i in range(spoint):
        ax.vlines(
            x=sleft + (lline * (leftalg[i] - lowest)) / (highest - lowest),
            ymin=sbottom + (spoint - 1 - i) * vspace,
            ymax=stop,
            color="black",
            linewidth=0.7,
        )
        ax.hlines(
            y=sbottom + (spoint - 1 - i) * vspace,
            xmin=sleft,
            xmax=sleft + (lline * (leftalg[i] - lowest)) / (highest - lowest),
            color="black",
            linewidth=0.7,
        )
        ax.text(x=sleft - 0.01, y=sbottom + (spoint - 1 - i) * vspace, s=alg_names[indices][i], ha="right", va="center")

    # Plot lines/names for right models
    vspace = 0.5 * (stop - sbottom) / (num_alg - spoint + 1)
    for i in range(num_alg - spoint):
        ax.vlines(
            x=sleft + (lline * (rightalg[i] - lowest)) / (highest - lowest),
            ymin=sbottom + i * vspace,
            ymax=stop,
            color="black",
            linewidth=0.7,
        )
        ax.hlines(
            y=sbottom + i * vspace,
            xmin=sleft + (lline * (rightalg[i] - lowest)) / (highest - lowest),
            xmax=sright,
            color="black",
            linewidth=0.7,
        )
        ax.text(x=sright + 0.01, y=sbottom + i * vspace, s=alg_names[indices][spoint + i], ha="left", va="center")

    # Plot critical difference rule
    if sleft + (cd * lline) / (highest - lowest) <= sright:
        ax.hlines(y=stop + 0.2, xmin=sleft, xmax=sleft + (cd * lline) / (highest - lowest), linewidth=1.5)
        ax.text(
            x=sleft + 0.5 * (cd * lline) / (highest - lowest), y=stop + 0.21, s="CD=%.3f" % cd, ha="center", va="bottom"
        )
    else:
        ax.text(x=(sleft + sright) / 2, y=stop + 0.2, s="CD=%.3f" % cd, ha="center", va="bottom")

    # Get pair of non-significant methods
    nonsig = _join_alg(avranks, num_alg, cd)
    if nonsig.ndim == 2:
        if nonsig.shape[0] == 2:
            left_lines = np.reshape(nonsig[0, :], (1, 2))
            right_lines = np.reshape(nonsig[1, :], (1, 2))
        else:
            left_lines = nonsig[: np.round(nonsig.shape[0] / 2.0).astype(np.uint8), :]
            right_lines = nonsig[np.round(nonsig.shape[0] / 2.0).astype(np.uint8) :, :]
    else:
        left_lines = np.reshape(nonsig, (1, nonsig.shape[0]))

    # plot from the left
    vspace = 0.5 * (stop - sbottom) / (left_lines.shape[0] + 1)
    for i in range(left_lines.shape[0]):
        ax.hlines(
            y=stop - (i + 1) * vspace,
            xmin=sleft + lline * (left_lines[i, 0] - lowest - 0.025) / (highest - lowest),
            xmax=sleft + lline * (left_lines[i, 1] - lowest + 0.025) / (highest - lowest),
            linewidth=2,
        )

    # plot from the rigth
    if nonsig.ndim == 2:
        vspace = 0.5 * (stop - sbottom) / (left_lines.shape[0])
        for i in range(right_lines.shape[0]):
            ax.hlines(
                y=stop - (i + 1) * vspace,
                xmin=sleft + lline * (right_lines[i, 0] - lowest - 0.025) / (highest - lowest),
                xmax=sleft + lline * (right_lines[i, 1] - lowest + 0.025) / (highest - lowest),
                linewidth=2,
            )

    output_path = os.path.join(os.getcwd(), "outputs", "critical_distance", f"{metric}_cd_plot.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.show()
    logger.warning(f"Critical distance for metric {metric} saved in {output_path}")

def CDplot_csv(data: str | pd.DataFrame, metrics: str | pd.DataFrame):
    """
    Generates CD plots for a list of metrics from the given data.

    Parameters:
    data (str | pd.DataFrame): Data source, either a file path or a pandas DataFrame.
    metrics (str | pd.DataFrame): Metric names or a DataFrame containing metrics.

    The function processes the data and metrics, aggregates the information, 
    and calls CDplot_metric for each metric to generate the corresponding plots.
    """

    # Obtain the list of metrics from the provided input
    list_metrics = obtain_list_metrics(metrics)
    
    # Iterate through each metric in the list
    for metric in list_metrics:
        # Process the dataframe to aggregate data for the given metric
        df_agg_pivot, _, _, maximize = process_dataframe_extended(data, metric, metrics)
        
        # Call the function to generate the CD plot for the current metric
        CDplot_metric(df_agg_pivot, metric, higher_is_better=maximize)

if __name__ == "__main__":
    data = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/data.csv"
    metrics = "/home/khaosdev/algorithm-benchmark-toolkit/notebooks/metrics.csv"
    CDplot_csv(data, metrics)