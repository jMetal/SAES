from SAES.utils.dataframe_processor import process_dataframe_metric
from SAES.logger import get_logger

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class Violin:
    """
    Class to generate violin plots for the performance results of different algorithms across multiple instances.

    Attributes:
        data (pd.DataFrame):
            A pandas DataFrame containing the performance results of different algorithms across multiple instances.
        
        metric (str):
            The metric to be used for comparison.

        algorithms (np.ndarray):
            An array containing the names of the algorithms.

        instances (np.ndarray):
            An array containing the names of the instances.

        logger (Logger):
            A logger object to record and display log messages.

    Methods:
        __init__(data: pd.DataFrame, metrics: pd.DataFrame, metric: str):
            Initializes the violin object with the given data, metrics, and metric.
        
        save_instance(instance: str, output_path: str):
            Generates a violin for the specified instance and saves it to the specified output path.
        
        save_all_instances(output_path: str):
            Generates a violin for all instances and saves it to the specified output path.

        show_instance(instance: str):
            Generates a violin for the specified instance and displays it.
        
        show_all_instances():
            Generates a violin for all instances and displays it.
    """

    def __init__(self, data: pd.DataFrame, metrics: pd.DataFrame, metric: str) -> None:
        """
        Initializes the Violin object with the given data, metrics, and metric.

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
            >>> from SAES.plots.violin import Violin
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> violin = Violin(data, metrics, metric)
        """

        self.data, _ = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.algorithms = self.data['Algorithm'].unique()
        self.instances = self.data['Instance'].unique()
        self.logger = get_logger(__name__)

    def save_instance(self, instance: str, output_path: str, file_name: str = None, width: int = 8) -> None:
        """
        Generates a violin for the specified instance and saves it to the specified output path.

        Args:
            instance (str):
                The name of the instance for which the violin is to be generated.
            
            output_path (str):
                The path where the violin image will be saved.

            file_name (str):
                The name of the file to be saved. If None, a default name will be used.

            width (int):
                The width of the violin image.
        
        returns:
            None
        
        Example:
            >>> from SAES.plots.violin import Violin
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> violin = Violin(data, metrics, metric)
            >>> violin.save_instance("ZDT1", os.getcwd())
        """

        self._plot_instance(instance, width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"violin_{self.metric}_{instance}.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"Violin {file_name} saved to {output_path}")
    
    def save_all_instances(self, output_path: str, file_name: str = None, width: int = 30) -> None:
        """
        Generates a violin for all instances and saves it to the specified output path.

        Args:
            output_path (str):
                The path where the violin image will be saved.

            file_name (str):
                The name of the file to be saved. If None, a default name will be used.

            width (int):
                The width of the violin image.

        Returns:
            None

        Example:
            >>> from SAES.plots.violin import Violin
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> violin = Violin(data, metrics, metric)
            >>> violin.save_all_instances(os.getcwd())
        """

        self._plot_all_instances(width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"violin_{self.metric}_all.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"Violin {file_name} saved to {output_path}")

    def show_instance(self, instance: str, width: int = 8) -> None:
        """
        Generates a violin for the specified instance and displays it.

        Args:
            instance (str):
                The name of the instance for which the violin is to be generated.
            
            width (int):   
                The width of the violin image.
        
        returns:
            None
        
        Example:
            >>> from SAES.plots.violin import Violin
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> violin = Violin(data, metrics, metric)
            >>> violin.show_instance("ZDT1")
        """
                
        self._plot_instance(instance, width=width)
        plt.show()

    def show_all_instances(self, width: int = 30) -> None:
        """
        Generates a violin for all instances and displays it.

        Args:
            width (int):
                The width of the violin image.

        Returns:
            None

        Example:
            >>> from SAES.plots.violin import Violin
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> violin = Violin(data, metrics, metric)
            >>> violin.show_all_instances()
        """

        self._plot_all_instances(width=width)
        plt.show()

    def _plot_instance(self, instance: str, width: int) -> None:
        """Generates a violin for the specified instance."""

        dataframe_instance = self.data[self.data["Instance"] == instance]
        metric_values_by_algorithm = dataframe_instance.groupby("Algorithm")["MetricValue"].apply(list).loc[self.algorithms].tolist()
        plt.figure(figsize=(width, width * (4.5 / 8))) 
        sns.violinplot(data=metric_values_by_algorithm, palette=["#5B92E5"] * len(self.algorithms))
    
        sns.despine()
        plt.xticks(ticks=range(len(self.algorithms)), labels=self.algorithms, fontsize=12, weight="bold", rotation=30)
        plt.title(f'Comparison of Algorithms for {instance} for {self.metric}', fontsize=16, weight='bold', pad=20)
        plt.ylabel(f'{self.metric}', fontsize=12, weight='bold')
        plt.yticks(fontsize=10, weight='bold')
        plt.grid(axis='y', linestyle='-', alpha=0.7)

        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)

        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
        plt.gca().set_xlabel('')
        plt.tight_layout()

    def _plot_all_instances(self, width: int) -> None:
        """Generates a violin for all instances."""
        
        instances = self.data["Instance"].unique()
        n_cols = 3 if len(instances) >= 3 else len(instances)
        n_rows = int(np.ceil(len(instances) / n_cols))  

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(width, width * (n_rows / 4)))

        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, instance in enumerate(instances):
            dataframe_instance = self.data[self.data["Instance"] == instance]
            metric_values_by_algorithm = dataframe_instance.groupby("Algorithm")["MetricValue"].apply(list).loc[self.algorithms].tolist()

            # Plot violin for each instance
            sns.violinplot(data=metric_values_by_algorithm, palette=["#5B92E5"] * len(self.algorithms), ax=axes[i])

            axes[i].set_title(f'Instance: {instance}', fontsize=12, weight='bold')
            axes[i].set_ylabel(f'{self.metric}', fontsize=10, weight='bold')
            axes[i].set_xticks(range(len(dataframe_instance['Algorithm'].unique())))
            axes[i].set_xticklabels(dataframe_instance['Algorithm'].unique(), rotation=15, fontsize=9, weight='bold')

            axes[i].grid(axis='y', linestyle='-', alpha=0.7)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['left'].set_visible(False)
            axes[i].spines['bottom'].set_visible(False)
            axes[i].tick_params(axis='x', bottom=False)

        # Remove extra axes if any
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.35, hspace=0.45)
