from SAES.statistical_tests.non_parametrical import NemenyiCD
from SAES.latex_generation.stats_table import MeanMedian
from SAES.logger import get_logger

from scipy.stats import rankdata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Scientific article reference: https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf

class CDplot:
    """
    Class to generate a critical difference plot to compare the performance of different algorithms on multiple instances.

    Attributes:
        table (pd.DataFrame):
            A pandas DataFrame containing the performance results of different algorithms across multiple instances.

        metric (str):
            The metric to be used for comparison.

        logger (Logger):
            A logger object to record and display log messages.

    Methods:
        __init__(data: pd.DataFrame, metrics: pd.DataFrame, metric: str):
            Initializes the CDplot object with the given data, metrics, and metric.
        
        save(output_path: str):
            Generates a critical difference plot and saves it to the specified output path.

        show():
            Generates a critical difference plot and displays it.
    """

    def __init__(self, data: pd.DataFrame, metrics: pd.DataFrame, metric: str) -> None:
        """
        Initializes the CDplot object with the given data, metrics, and metric.

        Args:
            data (pd.DataFrame):
                A pandas DataFrame containing the performance results of different algorithms across multiple instances.
            
            metrics (pd.DataFrame):
                A pandas DataFrame containing the metric information.
            
            metric (str):
                The metric to be used for comparison.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.CDplot import CDplot
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> cd_plot = CDplot(data, metrics, metric)
        """

        mean_median = MeanMedian(data, metrics, metric)
        mean_median.compute_table()

        self.table, self.maximize = mean_median.table, mean_median.maximize
        self.metric = metric
        self.logger = get_logger(__name__)

    def save(self, output_path: str, file_name: str = None, width: int = 9) -> None:
        """
        Generates a critical difference plot and saves it to the specified output path.

        Args: 
            output_path (str):
                The path where the CDplot image will be saved.
            
            file_name (str):
                The name of the file to be saved. If not provided, the file will be saved as "cdplot_{metric}.png".

            width (int):
                The width of the CDplot image.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.CDplot import CDplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> cd_plot = CDplot(data, metrics, metric)
            >>> cd_plot.save(os.getcwd())
        """

        self._plot(width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"cdplot_{self.metric}.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"CDplot {file_name} saved to {output_path}")

    def show(self, width: int = 9) -> None:
        """
        Generates a critical difference plot and displays it.

        Args:
            width (int):
                The width of the CDplot image.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.CDplot import CDplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> cd_plot = CDplot(data, metrics, metric)
            >>> cd_plot.show()
        """

        self._plot(width=width)
        plt.show()

    def _plot(self, width: int, alpha: float = 0.05) -> None:
        """Creates a critical distance plot to compare the performance of different algorithms on the different instances."""

        def _join_alg(avranks, num_alg, cd):
            """join_alg returns the set of non significant methods."""

            # get all pairs
            sets = (-1) * np.ones((num_alg, 2))
            for i in range(num_alg):
                elements = np.where(np.logical_and(avranks - avranks[i] > 0, avranks - avranks[i] < cd))[0]
                if elements.size > 0:
                    sets[i, :] = [avranks[i], avranks[elements[-1]]]
            sets = np.delete(sets, np.where(sets[:, 0] < 0)[0], axis=0)
            if sets.size == 0:
                return sets
            
            # group pairs
            group = sets[0, :]
            for i in range(1, sets.shape[0]):
                if sets[i - 1, 1] < sets[i, 1]:
                    group = np.vstack((group, sets[i, :]))

            return group
        
        alg_names = self.table.columns
        data = self.table.values

        if data.ndim == 2:
            num_dataset, num_alg = data.shape
        else:
            raise ValueError("Initialization ERROR: In CDplot(...) results must be 2-D array")

        # Get the critical difference
        cd = NemenyiCD(alpha, num_alg, num_dataset)

        # Compute ranks. (ranks[i][j] rank of the i-th algorithm on the j-th Instance.)
        rranks = rankdata(-data, axis=1) if self.maximize else rankdata(data, axis=1)

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

        # Compute figure size
        height = width * (0.8625 * (rows + 1) / 9)

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
        ax.hlines(stop, sleft, sright, color="black", linewidth=3)
        for xi in range(highest - lowest + 1):
            # Plot mayor ticks
            ax.vlines(
                x=sleft + (lline * xi) / (highest - lowest), ymin=stop, ymax=stop + 0.05, color="black", linewidth=2
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
                color="red",
                linewidth=1,
            )
            ax.hlines(
                y=sbottom + (spoint - 1 - i) * vspace,
                xmin=sleft,
                xmax=sleft + (lline * (leftalg[i] - lowest)) / (highest - lowest),
                color="red",
                linewidth=1,
            )
            ax.text(x=sleft - 0.01, y=sbottom + (spoint - 1 - i) * vspace, s=f"$\\mathbf{{{alg_names[indices][i]}}}$", ha="right", va="center")

        # Plot lines/names for right models
        vspace = 0.5 * (stop - sbottom) / (num_alg - spoint + 1)
        for i in range(num_alg - spoint):
            ax.vlines(
                x=sleft + (lline * (rightalg[i] - lowest)) / (highest - lowest),
                ymin=sbottom + i * vspace,
                ymax=stop,
                color="green",
                linewidth=1,
            )
            ax.hlines(
                y=sbottom + i * vspace,
                xmin=sleft + (lline * (rightalg[i] - lowest)) / (highest - lowest),
                xmax=sright,
                color="green",
                linewidth=1,
            )
            ax.text(x=sright + 0.01, y=sbottom + i * vspace, s=f"$\\mathbf{{{alg_names[indices][spoint+i]}}}$", ha="left", va="center")

        # Plot critical difference rule
        if sleft + (cd * lline) / (highest - lowest) <= sright:
            ax.hlines(y=stop + 0.2, xmin=sleft, xmax=sleft + (cd * lline) / (highest - lowest), linewidth=1.5)
            ax.text(
                x=sleft + 0.5 * (cd * lline) / (highest - lowest), y=stop + 0.21, s="CD=%.3f" % cd, ha="center", va="bottom"
            )
        else:
            ax.text(x=(sleft + sright) / 2, y=stop + 0.2, s=f"$\\mathbf{{CD={cd:.3f}}}$", ha="center", va="bottom")

        # Get pair of non-significant methods
        nonsig = _join_alg(avranks, num_alg, cd)
        if nonsig.size == 0:  # No pairs to process
            left_lines = np.array([])  # Initialize as empty array
            right_lines = np.array([])  # Initialize as empty array
        elif nonsig.ndim == 2:
            if nonsig.shape[0] == 2:
                left_lines = np.reshape(nonsig[0, :], (1, 2))
                right_lines = np.reshape(nonsig[1, :], (1, 2))
            else:
                left_lines = nonsig[: np.round(nonsig.shape[0] / 2.0).astype(np.uint8), :]
                right_lines = nonsig[np.round(nonsig.shape[0] / 2.0).astype(np.uint8) :, :]
        else:
            left_lines = np.reshape(nonsig, (1, nonsig.shape[0]))

        if nonsig.size > 0:
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
