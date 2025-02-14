from SAES.utils.dataframe_processor import process_dataframe_metric
from SAES.logger import get_logger

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

logger = get_logger(__name__)

class Boxplot:
    def __init__(self, data: pd.DataFrame, metrics: pd.DataFrame, metric: str):
        self.data, _ = process_dataframe_metric(data, metrics, metric)
        self.metric = metric
        self.instances = self.data['Instance'].unique()

    def save_instance(self, instance: str, output_path: str):
        self._plot_instance(instance)
        os.makedirs(output_path, exist_ok=True)
        plt.savefig(f"{output_path}/boxplot_{self.metric}_{instance}.png")
        plt.close()
        logger.info(f"Boxplot {self.metric}_{instance} saved to {output_path}")
    
    def save_all_instances(self, output_path: str):
        self._plot_all_instances()
        os.makedirs(output_path, exist_ok=True)
        plt.savefig(f"{output_path}/boxplot_{self.metric}_all.png")
        plt.close()
        logger.info(f"Boxplot {self.metric}_all saved to {output_path}")

    def show_instance(self, instance: str):
        self._plot_instance(instance)
        plt.show()

    def show_all_instances(self):
        self._plot_all_instances()
        plt.show()

    def _plot_instance(self, instance: str):
        dataframe_instance = self.data[self.data["Instance"] == instance]

        plt.figure(figsize=(10, 6))  
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

    def _plot_all_instances(self) -> None:
        instances = self.data["Instance"].unique()
        n_cols = 3 
        n_rows = int(np.ceil(len(instances) / n_cols))  

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(30, 7.5 * n_rows))
        axes = axes.flatten()

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

if __name__ == "__main__":
    data = '/home/khaosdev/SAES/notebooks/swarmIntelligence.csv'
    metrics = '/home/khaosdev/SAES/notebooks/multiobjectiveMetrics.csv'
    metric = 'IGD+'
    boxplot = Boxplot(data, metrics, metric)
    import os

    boxplot.save_all_instances(os.getcwd())
        



