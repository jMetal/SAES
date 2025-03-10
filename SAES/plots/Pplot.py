from SAES.statistical_tests.bayesian import bayesian_sign_test, bayesian_signed_rank_test
from SAES.utils.dataframe_processor import process_dataframe_metric
from SAES.logger import get_logger

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Scientific article reference: https://arxiv.org/pdf/1606.04316

class Pplot:
    """
    Class to generate plots for the posterior distribution of a Bayesian statistical test.
    
    Attributes:
        data (pd.DataFrame):
            A pandas DataFrame containing the performance results of different algorithms across multiple instances.
        
        maximize (bool):
            A boolean indicating whether the metric is higher is better.

        algorithms (np.array):
            An array containing the names of the algorithms under evaluation.

        metric (str):
            The metric to be used for comparison

        logger (Logger):
            A logger object to record and display log messages.
    
    Methods:
        plot(alg1: str, alg2: str, width: int = 5) -> None:
            Plots the posterior distribution of the Bayesian statistical test between two algorithms.
        
        save(alg1: str, alg2: str, output_path: str, file_name: str = None, width: int = 5) -> None:
            Saves the posterior distribution of the Bayesian statistical test between two algorithms to a file.

        plot_pivot(algorithm: str, width: int = 30) -> None:
            Plots the posterior distribution of the Bayesian statistical test between an algorithm and all other algorithms.

        save_pivot(algorithm: str, output_path: str, file_name: str = None, width: int = 30) -> None:
            Saves the posterior distribution of the Bayesian statistical test between an algorithm and all other algorithms to a file.
    """

    def __init__(self, data: pd.DataFrame, metrics: pd.DataFrame, metric: str, bayesian_test: str = "sign") -> None:
        """
        Initializes the Pplot object with the given data, metrics, and metric.

        Args:
            data (pd.DataFrame):
                A pandas DataFrame containing the performance results of different algorithms across multiple instances.
            
            metrics (pd.DataFrame):
                A pandas DataFrame containing the metric information.
            
            metric (str):
                The metric to be used for comparison.

            bayesian_test (str):
                The type of Bayesian test to be performed. Default is "sign". List of available tests:
                    - "sign": Bayesian sign test.
                    - "rank": Bayesian rank test.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.Pplot import Pplot
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> pplot = Pplot(data, metrics, metric)
        """

        if bayesian_test not in ["sign", "rank"]:
            raise ValueError("Invalid Bayesian test type. Please choose between 'sign' and 'rank'.")
        
        self.data, self.maximize = process_dataframe_metric(data, metrics, metric)
        self.algorithms = self.data['Algorithm'].unique()
        self.metric = metric
        self.bayesian_test = bayesian_test
        self.logger = get_logger(__name__)

    def save(self, alg1, alg2, output_path: str, file_name: str = None, width: int = 5, sample_size: int = 2500) -> None:
        """
        Saves the posterior distribution of the Bayesian statistical test between two algorithms to a file.

        Args:
            alg1 (str):
                The name of the first algorithm.
            
            alg2 (str):
                The name of the second algorithm.

            output_path (str):
                The path where the file will be saved.
            
            file_name (str):
                The name of the file. Default is None.

            width (int):
                The width of the figure. Default is 5.

            sample_size (int):
                Total number of random_search samples generated. Default is 2500.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.Pplot import Pplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> pplot = Pplot(data, metrics, metric)
            >>> pplot.save("NSGAII", "OMOPSO", os.getcwd())
        """

        posterior_probabilities = self._obtain_posterior_probabilities(alg1, alg2, sample_size)
        self._plot(posterior_probabilities, width, alg_names=[alg1, alg2])
        file_name = file_name if file_name else f"{self.metric}_{alg1}_vs_{alg2}.png"
        plt.savefig(f"{output_path}/{file_name}", bbox_inches="tight")
        self.logger.info(f"Pplot {file_name} saved to {output_path}")
        plt.close()

    def show(self, alg1: str, alg2: str, width: int = 5, sample_size: int = 2500) -> None:
        """
        Plots the posterior distribution of the Bayesian statistical test between two algorithms.

        Args:
            alg1 (str):
                The name of the first algorithm.
            
            alg2 (str):
                The name of the second algorithm.

            width (int):
                The width of the figure. Default is 5.

            sample_size (int):
                Total number of random_search samples generated. Default is 2500.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.Pplot import Pplot
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> pplot = Pplot(data, metrics, metric)
            >>> pplot.plot("NSGAII", "OMOPSO")
        """

        posterior_probabilities = self._obtain_posterior_probabilities(alg1, alg2, sample_size)
        self._plot(posterior_probabilities, width, alg_names=[alg1, alg2])
        plt.show()

    def save_pivot(self, algorithm: str, output_path: str, file_name: str = None, 
                   width: int = 30, 
                   heigth: int = 15, 
                   sample_size: int = 2500) -> None:
        """
        Saves the posterior distribution of the Bayesian statistical test between an algorithm and all other algorithms to a file.

        Args:
            algorithm (str):
                The name of the algorithm.
            
            output_path (str):
                The path where the file will be saved.
            
            file_name (str):
                The name of the file. Default is None.

            width (int):
                The width of the figure. Default is 30.

            heigth (int):
                The heigth of the figure. Default is 15.

            sample_size (int):
                Total number of random_search samples generated. Default is 2500.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.Pplot import Pplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> pplot = Pplot(data, metrics, metric)
            >>> pplot.save_pivot("NSGAII", os.getcwd())
        """

        self._plot_pivot(algorithm, width, heigth, sample_size)
        file_name = file_name if file_name else f"{self.metric}_pivot_{algorithm}.png"
        plt.savefig(f"{output_path}/{file_name}", bbox_inches="tight") 
        self.logger.info(f"Pplot {file_name} saved to {output_path}")
        plt.close()

    def show_pivot(self, algorithm: str, width: int = 30, heigth: int = 15, sample_size: int = 2500) -> None:
        """
        Plots the posterior distribution of the Bayesian statistical test between an algorithm and all other algorithms.

        Args:
            algorithm (str):
                The name of the algorithm.

            width (int):
                The width of the figure. Default is 30.

            heigth (int):
                The heigth of the figure. Default is 15.

            sample_size (int):
                Total number of random_search samples generated. Default is 2500.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.Pplot import Pplot
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> pplot = Pplot(data, metrics, metric)
            >>> pplot.plot_pivot("NSGAII")
        """

        self._plot_pivot(algorithm, width, heigth, sample_size)
        plt.show()

    def _plot_pivot(self, algorithm: str, width: int, heigth: int, sample_size: int) -> None:
        """Plots the posterior distribution of the Bayesian statistical test between an algorithm and all other algorithms."""

        # Filter out the specified algorithm from the list of algorithms
        algorithms = self.algorithms[self.algorithms != algorithm]
        column_combinations = [(algorithm, algorithm_i) for algorithm_i in algorithms]
        num_plots = len(column_combinations)
        
        # Define the number of columns and calculate the required number of rows for the grid
        ncols = 3 if num_plots >= 3 else num_plots
        nrows = (num_plots + ncols - 1) // ncols 
        
        # Create subplots with the specified grid size
        fig, axes = plt.subplots(nrows, ncols, figsize=(width, heigth))
        
        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]

        # Loop through the algorithm combinations and plot the posterior probabilities
        for idx, (alg1, alg2) in enumerate(column_combinations):
            posterior_probabilities = self._obtain_posterior_probabilities(alg1, alg2, sample_size=sample_size)
            self._plot_grid(posterior_probabilities, ax=axes[idx], alg_names=[alg1, alg2])
        
        # Remove any empty subplots if the number of combinations is less than the number of available axes
        for i in range(num_plots, len(axes)):
            fig.delaxes(axes[i])

        # Adjust the layout to avoid overlap between subplots
        plt.tight_layout()

    def _plot(self,
              data: np.array,
              width: int,
              min_points_per_hexbin: int = 2,
              alg_names: list = None) -> None:
        """
        Plots the sample from posterior distribution of a Bayesian statistical test.
        Args:
            data (np.array):
                An (n x 3) array or DataFrame contaning the probabilities. It is the result array after vstacking the results of the Bayesian sign test over multiple executions of the same pair of algorithms-instance.

            width (int):
                The width of the figure.

            min_points_per_hexbin (int):
                The minimum number of points in each hexbin. Default is 2.

            alg_names (list):
                Names of the algorithms under evaluation. Default is None.

        Returns:
            None
        """

        if data.ndim == 2:
            _, ncol = data.shape
            if ncol != 3:
                raise ValueError("Initialization ERROR. Incorrect number of dimensions in axis 1.")
        else:
            raise ValueError("Initialization ERROR. Incorrect number of dimensions for sample")

        def transform(p):
            lambda1, lambda2, lambda3 = p.T
            x = 0.1 * lambda1 + 0.5 * lambda2 + 0.9 * lambda3
            y = (0.2 * lambda1 + 1.4 * lambda2 + 0.2 * lambda3) / np.sqrt(3)
            return np.vstack((x, y)).T

        # Initialize figure
        fig = plt.figure(figsize=(width, width), facecolor="white")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()

        # Plot text
        if self.maximize:
            ax.text(x=0.5, y=1.4 / np.sqrt(3) + 0.005, s="no-diff", ha="center", va="bottom", weight='bold')
            ax.text(x=0.35, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[1] + " +", ha="right", va="top", weight='bold')
            ax.text(x=0.75, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[0] + " +", ha="left", va="top", weight='bold')
        else:
            ax.text(x=0.5, y=1.4 / np.sqrt(3) + 0.005, s="no-diff", ha="center", va="bottom", weight='bold')
            ax.text(x=0.35, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[0] + " +", ha="right", va="top", weight='bold')
            ax.text(x=0.75, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[1] + " +", ha="left", va="top", weight='bold')

        # Conversion between barycentric and Cartesian coordinates
        sample2d = np.zeros((data.shape[0], 2))
        for p in range(data.shape[0]):
            sample2d[p, :] = transform(data[p, :])

        # Plot projected points
        hb = ax.hexbin(sample2d[:, 0], sample2d[:, 1], mincnt=min_points_per_hexbin, cmap=plt.cm.plasma)

        # Add colorbar to the plot for better visualization
        cb = fig.colorbar(hb, ax=ax, orientation="vertical", fraction=0.05, pad=0.0, shrink=0.6)
        cb.set_label("Count")

        ax.plot([0.095, 0.505], [0.2 / np.sqrt(3), 1.4 / np.sqrt(3)], linewidth=3.0, color="white")
        ax.plot([0.505, 0.905], [1.4 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="white")
        ax.plot([0.09, 0.905], [0.2 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="white")
        ax.plot([0.5, 0.5], [0.2 / np.sqrt(3), 0.6 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.3, 0.5], [0.8 / np.sqrt(3), 0.6 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.5, 0.7], [0.6 / np.sqrt(3), 0.8 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.1, 0.5], [0.2 / np.sqrt(3), 1.4 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.5, 0.9], [1.4 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.1, 0.9], [0.2 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="orange")

    def _plot_grid(self,
                   data: np.array,
                   ax: plt.Axes,
                   min_points_per_hexbin: int = 2,
                   alg_names: list = None) -> None:
        """Plots the sample from posterior distribution of a Bayesian statistical test in a grid."""

        if data.ndim == 2:
            _, ncol = data.shape
            if ncol != 3:
                raise ValueError("Initialization ERROR. Incorrect number of dimensions in axis 1.")
        else:
            raise ValueError("Initialization ERROR. Incorrect number of dimensions for sample")

        def transform(p):
            lambda1, lambda2, lambda3 = p.T
            x = 0.1 * lambda1 + 0.5 * lambda2 + 0.9 * lambda3
            y = (0.2 * lambda1 + 1.4 * lambda2 + 0.2 * lambda3) / np.sqrt(3)
            return np.vstack((x, y)).T

        # Initialize figure
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()

        # Plot text
        if self.maximize:
            ax.text(x=0.5, y=1.4 / np.sqrt(3) + 0.005, s="no-diff", ha="center", va="bottom", weight='bold')
            ax.text(x=0.35, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[1] + " +", ha="right", va="top", weight='bold')
            ax.text(x=0.75, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[0] + " +", ha="left", va="top", weight='bold')
        else:
            ax.text(x=0.5, y=1.4 / np.sqrt(3) + 0.005, s="no-diff", ha="center", va="bottom", weight='bold')
            ax.text(x=0.35, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[0] + " +", ha="right", va="top", weight='bold')
            ax.text(x=0.75, y=0.175 / np.sqrt(3) - 0.005, s=alg_names[1] + " +", ha="left", va="top", weight='bold')

        # Conversion between barycentric and Cartesian coordinates
        sample2d = np.zeros((data.shape[0], 2))
        for p in range(data.shape[0]):
            sample2d[p, :] = transform(data[p, :])

        # Plot projected points
        hb = ax.hexbin(sample2d[:, 0], sample2d[:, 1], mincnt=min_points_per_hexbin, cmap=plt.cm.plasma)

        # Add colorbar to the plot for better visualization
        cb = plt.colorbar(hb, ax=ax, orientation="vertical", fraction=0.05, pad=0.0, shrink=0.6)
        cb.set_label("Count")

        ax.plot([0.095, 0.505], [0.2 / np.sqrt(3), 1.4 / np.sqrt(3)], linewidth=3.0, color="white")
        ax.plot([0.505, 0.905], [1.4 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="white")
        ax.plot([0.09, 0.905], [0.2 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="white")
        ax.plot([0.5, 0.5], [0.2 / np.sqrt(3), 0.6 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.3, 0.5], [0.8 / np.sqrt(3), 0.6 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.5, 0.7], [0.6 / np.sqrt(3), 0.8 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.1, 0.5], [0.2 / np.sqrt(3), 1.4 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.5, 0.9], [1.4 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="orange")
        ax.plot([0.1, 0.9], [0.2 / np.sqrt(3), 0.2 / np.sqrt(3)], linewidth=3.0, color="orange")

    def _obtain_posterior_probabilities(self, alg1: str, alg2: str, sample_size: int) -> np.array:
        """Obtains the posterior probabilities of the Bayesian statistical test between two algorithms."""

        # Filter data to include only the specified algorithms
        data = self.data[self.data['Algorithm'].isin([alg1, alg2])]
        execution_min = data['ExecutionId'].min()
        execution_max = data['ExecutionId'].max() + 1

        # Initialize an empty list to store posterior probabilities
        posterior_probabilities = []
        for i in range(execution_min, execution_max):
            # Filter data for the current execution
            data_i = data[data['ExecutionId'] == i]
            data_i = data_i.pivot(index='Instance', columns='Algorithm', values='MetricValue')
            data_i = data_i[[alg1, alg2]]

            # If it's the first iteration, initialize the posterior probabilities list
            if self.bayesian_test == "sign":
                test_results = bayesian_sign_test(data_i.values, sample_size=sample_size)[1]
            else:
                test_results = bayesian_signed_rank_test(data_i.values, sample_size=sample_size)[1]
            
            if len(posterior_probabilities) == 0:
                posterior_probabilities = test_results
            else:
                # For subsequent iterations, stack the new posterior probabilities with the previous ones
                posterior_probabilities = np.vstack((posterior_probabilities, test_results))

        # Return the posterior probabilities as a NumPy array
        return np.array(posterior_probabilities)
    