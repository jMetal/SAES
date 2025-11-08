from SAES.utils.dataframe_processor import process_dataframe_metric
from SAES.logger import get_logger

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class HistoPlot:
    """
    Class to generate histoplots for the performance of different algorithms across multiple instances.

    Attributes:
        data (pd.DataFrame):
            A pandas DataFrame containing the performance results of different algorithms across multiple instances.
        
        metric (str):
            The metric to be used for comparison.

        instances (np.ndarray):
            An array containing the names of the instances.

        logger (Logger):
            A logger object to record and display log messages.

    Methods:
        __init__(data: pd.DataFrame, metrics: pd.DataFrame, metric: str):
            Initializes the histoplot object with the given data, metrics, and metric.
        
        save_instance(instance: str, output_path: str):
            Generates a histoplot for the specified instance and saves it to the specified output path.
        
        save_all_instances(output_path: str):
            Generates a histoplot for all instances and saves it to the specified output path.

        show_instance(instance: str):
            Generates a histoplot for the specified instance and displays it.
        
        show_all_instances():
            Generates a histoplot for all instances and displays it.
    """

    def __init__(self, data: pd.DataFrame, metrics: pd.DataFrame, metric: str) -> None:
        """
        Initializes the histoplot object with the given data, metrics, and metric.

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
            >>> from SAES.plots.histoplot import HistoPlot
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> histoplot = Histoplot(data, metrics, metric)
        """

        self.data, _ = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.algorithms = self.data['Algorithm'].unique()
        self.instances = self.data['Instance'].unique()
        self.logger = get_logger(__name__)

    def save_instance(self, instance: str, output_path: str, file_name: str = None, width: int = 8) -> None:
        """
        Generates a histoplot for the specified instance and saves it to the specified output path.

        Args:
            instance (str):
                The name of the instance for which the histoplot is to be generated.
            
            output_path (str):
                The path where the histoplot image will be saved.

            file_name (str):
                The name of the file to be saved. If None, a default name will be used.

            width (int):
                The width of the histoplot image.
        
        returns:
            None
        
        Example:
            >>> from SAES.plots.histoplot import HistoPlot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> histoplot = Histoplot(data, metrics, metric)
            >>> histoplot.save_instance("ZDT1", os.getcwd())
        """

        self._plot_instance(instance, width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"histoplot_{self.metric}_{instance}.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"Histoplot {file_name} saved to {output_path}")
    
    def save_all_instances(self, output_path: str, file_name: str = None, width: int = 30) -> None:
        """
        Generates a histoplot for all instances and saves it to the specified output path.

        Args:
            output_path (str):
                The path where the histoplot image will be saved.

            file_name (str):
                The name of the file to be saved. If None, a default name will be used.

            width (int):
                The width of the histoplot image.

        Returns:
            None

        Example:
            >>> from SAES.plots.histoplot import HistoPlot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> histoplot = Histoplot(data, metrics, metric)
            >>> histoplot.save_all_instances(os.getcwd())
        """

        self._plot_all_instances(width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"histoplot_{self.metric}_all.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"Histoplot {file_name} saved to {output_path}")

    def show_instance(self, instance: str, width: int = 8) -> None:
        """
        Generates a histoplot for the specified instance and displays it.

        Args:
            instance (str):
                The name of the instance for which the histoplot is to be generated.
            
            width (int):   
                The width of the histoplot image.
        
        returns:
            None
        
        Example:
            >>> from SAES.plots.histoplot import HistoPlot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> histoplot = Histoplot(data, metrics, metric)
            >>> histoplot.show_instance("ZDT1")
        """
                
        self._plot_instance(instance, width=width)
        plt.show()

    def show_all_instances(self, width: int = 30) -> None:
        """
        Generates a histoplot for all instances and displays it.

        Args:
            width (int):
                The width of the histoplot image.

        Returns:
            None

        Example:
            >>> from SAES.plots.histoplot import HistoPlot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> histoplot = Histoplot(data, metrics, metric)
            >>> histoplot.show_all_instances()
        """

        self._plot_all_instances(width=width)
        plt.show()

    def _plot_instance(self, instance: str, width: int) -> None:
        """Generates a histoplot for the specified instance."""
      
        dataframe_instance = self.data[self.data["Instance"] == instance].copy()
        dataframe_instance.drop(columns=['index', 'Instance', 'ExecutionId'], inplace=True)
        
        plt.figure(figsize=(width, width * (4.5 / 8)))  

        for algorithm in self.algorithms:
            dataframe_algorithm = dataframe_instance[dataframe_instance['Algorithm'] == algorithm]

            if dataframe_algorithm['MetricValue'].eq(0).all():
                dataframe_algorithm.loc[:, 'MetricValue'] += np.random.uniform(0.00001, 0.00002, size=len(dataframe_algorithm))
            
            sns.histplot(dataframe_algorithm['MetricValue'], kde=True, label=algorithm, element='bars')
            
        plt.legend()
        plt.title("Histograms with KDE")
        plt.title(f'Comparison of Algorithms for {instance} for {self.metric}', fontsize=16, weight='bold', pad=20)
        plt.xlabel(f'{self.metric}', fontsize=12, weight='bold')
        plt.ylabel('Frequency', fontsize=12, weight='bold')
        plt.xticks(rotation=15, fontsize=10, weight='bold')
        plt.yticks(fontsize=10, weight='bold')
        plt.grid(axis='y', linestyle='-', alpha=0.7)

        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)

        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
        plt.tight_layout()

    def _plot_all_instances(self, width: int) -> None:
        """Generates a histoplot for all instances."""

        instances = self.data["Instance"].unique()
        n_cols = 3 if len(instances) >= 3 else len(instances)
        n_rows = int(np.ceil(len(instances) / n_cols))  

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(width, width * (n_rows / 4)))

        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, instance in enumerate(instances):
            dataframe_instance = self.data[self.data["Instance"] == instance].copy()
            dataframe_instance.drop(columns=['index', 'Instance', 'ExecutionId'], inplace=True)
            
            for algorithm in self.algorithms:
                dataframe_algorithm = dataframe_instance[dataframe_instance['Algorithm'] == algorithm].copy()
                
                if (dataframe_algorithm['MetricValue'] == dataframe_algorithm['MetricValue'].iloc[0]).all():
                    dataframe_algorithm.loc[:, 'MetricValue'] += np.random.uniform(0.00001, 0.00002, size=len(dataframe_algorithm))
                
                sns.histplot(dataframe_algorithm['MetricValue'], kde=True, label=algorithm, element='bars', ax=axes[i])
            
            axes[i].legend()
            axes[i].set_title(f'Instance: {instance}', fontsize=12, weight='bold')
            axes[i].set_ylabel('Frequency', fontsize=10, weight='bold')
            axes[i].set_xlabel(f'{self.metric}', fontsize=10, weight='bold')            
            axes[i].grid(axis='y', linestyle='-', alpha=0.7)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['left'].set_visible(False)
            axes[i].spines['bottom'].set_visible(False)
            axes[i].tick_params(axis='x', bottom=False)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.35, hspace=0.45)