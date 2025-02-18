from SAES.latex_generation.stats_table import MeanMedian
from SAES.utils.dataframe_processor import get_metrics
from SAES.logger import get_logger

import matplotlib.pyplot as plt
import pandas as pd
import os

class Front:
    def __init__(self, data: str | pd.DataFrame, metrics: str | pd.DataFrame, metric: str, fronts_path: str):
        mean_median = MeanMedian(data, metrics, metric)
        self.algorithms = mean_median.algorithms
        self.instances = mean_median.instances
        self.metric = metric

        self.fronts_path = fronts_path
        if not os.path.exists(self.fronts_path):
            raise FileNotFoundError(f"Fronts path {self.fronts_path} not found")
        
        self.logger = get_logger(__name__)

    def save(self, algorithm: str, instance: str, output_path: str, median: bool=True):
        median_best = 'MEDIAN' if median else 'BEST'
        front_path = f"{self.fronts_path}/{algorithm}/{instance}/{median_best}_{self.metric}_FUN.csv"
        file_name = f"front_{algorithm}_{instance}_{self.metric}_{median_best}.png"
        
        self._front(front_path, algorithm)

        os.makedirs(output_path, exist_ok=True)
        plt.savefig(f"{output_path}/{file_name}")
        self.logger.info(f"Front {file_name} saved to {output_path}")
        plt.close()

    def save_all_algorithms(self, instance: str, output_path: str, median: bool=True):
        median_best = 'MEDIAN' if median else 'BEST'
        fronts_paths = [f"{self.fronts_path}/{algorithm}/{instance}/{median_best}_{self.metric}_FUN.csv" for algorithm in self.algorithms]
        file_name = f"front_all_{instance}_{self.metric}_{median_best}.png"

        self._front_all_algorithms(fronts_paths)

        os.makedirs(output_path, exist_ok=True)
        plt.savefig(f"{output_path}/{file_name}")
        self.logger.info(f"Front {file_name} saved to {output_path}")
        plt.close()

    def show(self, algorithm: str, instance: str, median: bool=True):
        median_best = 'MEDIAN' if median else 'BEST'
        front_path = f"{self.fronts_path}/{algorithm}/{instance}/{median_best}_{self.metric}_FUN.csv"
        self._front(front_path, algorithm)
        plt.show()

    def show_all_algorithms(self, instance: str, median: bool=True):
        median_best = 'MEDIAN' if median else 'BEST'
        fronts_paths = [f"{self.fronts_path}/{algorithm}/{instance}/{median_best}_{self.metric}_FUN.csv" for algorithm in self.algorithms]
        self._front_all_algorithms(fronts_paths)
        plt.show()
        
    def _front(self, front_path: str, algorithm: str):
        if not os.path.exists(front_path):
            raise FileNotFoundError(f"Front {front_path} not found")
    
        # Read the front
        df = pd.read_csv(front_path, header=None)
        x = df[0]
        y = df[1]

        # Create the plot
        _, ax = plt.subplots()
        ax.scatter(x, y, alpha=0.7) 

        # Personalize the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='both', which='both', length=0)
        ax.set_title(algorithm, pad=20)  
        ax.grid(True, alpha=0.3)

    def _front_all_algorithms(self, front_paths: list):
        # Veriffy that the number of front_paths and algorithms are the same
        if len(front_paths) != len(self.algorithms):
            raise ValueError("Las listas de rutas y algoritmos deben tener la misma longitud.")
        
        # Number of plots
        num_plots = len(front_paths)
        rows = int(num_plots**0.5)
        cols = (num_plots + rows - 1) // rows  

        _, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*6))
        axes = axes.flatten()  

        for i, (front_path, algorithm) in enumerate(zip(front_paths, self.algorithms)):
            if not os.path.exists(front_path):
                raise FileNotFoundError(f"Front {front_path} not found")
            
            # Read the front
            df = pd.read_csv(front_path, header=None)
            x = df[0]
            y = df[1]
            
            # Create the plot
            ax = axes[i]
            ax.scatter(x, y, alpha=0.7)
            
            # Personalize the plot
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='both', which='both', length=0)
            ax.set_title(algorithm, pad=20)
            ax.grid(True, alpha=0.3)

        # Remove empty plots
        plt.tight_layout()

if __name__ == "__main__":
    fronts_path = "/home/khaosdev/SAES/data"
    algorithm = "MOEAD"
    instance = "KroABC100TSP"
    metric = "HV"
    front = Front("", "", metric, fronts_path)
    # front.save("MOEAD", "KroABC100TSP", os.getcwd(), median=True)
    front.save_all_algorithms("KroABC100TSP", os.getcwd(), median=True)
        