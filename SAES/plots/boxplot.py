from SAES.utils.dataframe_processor import process_dataframe_metric
from SAES.logger import get_logger

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class Boxplot:
    """
    Class to generate boxplots for the performance of different algorithms across multiple instances.

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
            Initializes the Boxplot object with the given data, metrics, and metric.
        
        save_instance(instance: str, output_path: str):
            Generates a boxplot for the specified instance and saves it to the specified output path.
        
        save_all_instances(output_path: str):
            Generates a boxplot for all instances and saves it to the specified output path.

        show_instance(instance: str):
            Generates a boxplot for the specified instance and displays it.
        
        show_all_instances():
            Generates a boxplot for all instances and displays it.
    """

    def __init__(self, data: pd.DataFrame, metrics: pd.DataFrame, metric: str) -> None:
        """
        Initializes the Boxplot object with the given data, metrics, and metric.

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
            >>> frtom SAES.plots.boxplot import Boxplot
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> boxplot = Boxplot(data, metrics, metric)
        """

        self.data, _ = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.instances = self.data['Instance'].unique()
        self.logger = get_logger(__name__)

    def save_instance(self, instance: str, output_path: str, file_name: str = None, width: int = 8) -> None:
        """
        Generates a boxplot for the specified instance and saves it to the specified output path.

        Args:
            instance (str):
                The name of the instance for which the boxplot is to be generated.
            
            output_path (str):
                The path where the boxplot image will be saved.

            file_name (str):
                The name of the file to be saved. If None, a default name will be used.

            width (int):
                The width of the boxplot image.
        
        returns:
            None
        
        Example:
            >>> frtom SAES.plots.boxplot import Boxplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> boxplot = Boxplot(data, metrics, metric)
            >>> boxplot.save_instance("ZDT1", os.getcwd())
        """

        self._plot_instance(instance, width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"boxplot_{self.metric}_{instance}.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"Boxplot {file_name} saved to {output_path}")
    
    def save_all_instances(self, output_path: str, file_name: str = None, width: int = 30) -> None:
        """
        Generates a boxplot for all instances and saves it to the specified output path.

        Args:
            output_path (str):
                The path where the boxplot image will be saved.

            file_name (str):
                The name of the file to be saved. If None, a default name will be used.

            width (int):
                The width of the boxplot image.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.boxplot import Boxplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> boxplot = Boxplot(data, metrics, metric)
            >>> boxplot.save_all_instances(os.getcwd())
        """

        self._plot_all_instances(width=width)
        os.makedirs(output_path, exist_ok=True)
        file_name = file_name if file_name else f"boxplot_{self.metric}_all.png"
        plt.savefig(f"{output_path}/{file_name}")
        plt.close()
        self.logger.info(f"Boxplot {file_name} saved to {output_path}")

    def show_instance(self, instance: str, width: int = 8) -> None:
        """
        Generates a boxplot for the specified instance and displays it.

        Args:
            instance (str):
                The name of the instance for which the boxplot is to be generated.
            
            width (int):   
                The width of the boxplot image.
        
        returns:
            None
        
        Example:
            >>> frtom SAES.plots.boxplot import Boxplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> boxplot = Boxplot(data, metrics, metric)
            >>> boxplot.show_instance("ZDT1")
        """
                
        self._plot_instance(instance, width=width)
        plt.show()

    def show_all_instances(self, width: int = 30) -> None:
        """
        Generates a boxplot for all instances and displays it.

        Args:
            width (int):
                The width of the boxplot image.

        Returns:
            None

        Example:
            >>> frtom SAES.plots.boxplot import Boxplot
            >>> import os
            >>> 
            >>> data = pd.read_csv("data.csv")
            >>> metrics = pd.read_csv("metrics.csv")
            >>> metric = "HV"
            >>> boxplot = Boxplot(data, metrics, metric)
            >>> boxplot.show_all_instances()
        """

        self._plot_all_instances(width=width)
        plt.show()

    def _plot_instance(self, instance: str, width: int) -> None:
        """Generates a boxplot for the specified instance."""

        dataframe_instance = self.data[self.data["Instance"] == instance]

        plt.figure(figsize=(width, width * (4.5 / 8)))  
        sns.boxplot(
            x='Algorithm', y='MetricValue', data=dataframe_instance, 
            boxprops=dict(facecolor=(0, 0, 1, 0.3), edgecolor="darkblue", linewidth=1.5),  
            whiskerprops=dict(color="darkblue", linewidth=1.5),  
            capprops=dict(color="darkblue", linewidth=1.5),  
            medianprops=dict(color="red", linewidth=1.5),  
            flierprops=dict(marker='o', color='red', markersize=5, alpha=0.8)  
        )

        plt.title(f'Comparison of Algorithms for {instance} for {self.metric}', fontsize=16, weight='bold', pad=20)
        plt.ylabel(f'{self.metric}', fontsize=12, weight='bold')
        plt.xticks(rotation=15, fontsize=10, weight='bold')
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
        instances = self.data["Instance"].unique()
        n_cols = 3 if len(instances) >= 3 else len(instances)
        n_rows = int(np.ceil(len(instances) / n_cols))  

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(width, width * (n_rows / 4)))

        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, instance in enumerate(instances):
            df_instance = self.data[self.data["Instance"] == instance]
            
            sns.boxplot(
                x='Algorithm', y='MetricValue', data=df_instance, ax=axes[i],
                boxprops=dict(facecolor=(0, 0, 1, 0.3), edgecolor="darkblue", linewidth=1.5),
                whiskerprops=dict(color="darkblue", linewidth=1.5),
                capprops=dict(color="darkblue", linewidth=1.5),
                medianprops=dict(color="red", linewidth=1.5),
                flierprops=dict(marker='o', color='red', markersize=5, alpha=0.8)
            )
            
            axes[i].set_title(f'Instance: {instance}', fontsize=12, weight='bold')
            axes[i].set_ylabel(f'{self.metric}', fontsize=10, weight='bold')
            axes[i].set_xticks(range(len(df_instance['Algorithm'].unique())))
            axes[i].set_xticklabels(df_instance['Algorithm'].unique(), rotation=15, fontsize=9, weight='bold')
            
            axes[i].grid(axis='y', linestyle='-', alpha=0.7)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['left'].set_visible(False)
            axes[i].spines['bottom'].set_visible(False)
            axes[i].tick_params(axis='x', bottom=False)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.35, hspace=0.45)
