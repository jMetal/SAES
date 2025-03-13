from SAES.logger import get_logger

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import os

# Wikipedia reference: https://en.wikipedia.org/wiki/Parallel_coordinates

class Front(ABC):
    """
    Abstract class to generate Pareto fronts for different algorithms and instances.

    Attributes:
        fronts_path (str):
            The path to the folder containing the Pareto fronts.

        references_path (str):
            The path to the folder containing the reference fronts.

        metric (str):
            The metric used to generate the fronts.

        algorithms (list):
            A list of algorithms present in the fronts path.

        instances (list):
            A list of instances present in the fronts path.

        logger (Logger):
            A logger object to record and display log messages.

    Methods:
        __init__(fronts_path: str, references_path: str, metric: str):
            Initializes the Front object with the given fronts path, references path, and metric.

        save(instance: str, output_path: str, median: bool=True):
            Generates a Pareto front for the specified instance and saves it to the specified output path.

        show(instance: str, median: bool=True):
            Generates a Pareto front for the specified instance and displays it.
    """

    def __init__(self, fronts_path: str, references_path: str, metric: str, dimensions: int) -> None:
        """
        Initializes the Front object with the given fronts path, references path, and metric.

        Args:
            fronts_path (str):
                The path to the folder containing the Pareto fronts.
            
            references_path (str):
                The path to the folder containing the reference fronts.

            metric (str):
                The metric used to generate the fronts.

            dimensions (int):
                The number of dimensions of the Pareto front

        Returns:
            None

        Example:
            >>> from SAES.multiobjective.pareto_front import Front2D
            >>>
            >>> fronts_path = "path/to/fronts"
            >>> references_path = "path/to/references"
            >>> metric = "HV"
            >>> front = Front2D(fronts_path, references_path, metric)
        """

        if not os.path.exists(fronts_path) or not os.path.isdir(fronts_path):
            raise FileNotFoundError(f"Fronts path {fronts_path} or references path {references_path} not found")
        
        self.fronts_path = fronts_path
        self.references_path = references_path
        self.metric = metric
        self.dimensions = dimensions
    
        self.algorithms = sorted([
            algorithm for algorithm in os.listdir(fronts_path) 
            if os.path.isdir(f"{fronts_path}/{algorithm}") and 
               f"{fronts_path}/{algorithm}" != references_path    
        ])

        self.instances = sorted([
            instance for instance in os.listdir(f"{fronts_path}/{self.algorithms[0]}") 
            if os.path.isdir(f"{fronts_path}/{self.algorithms[0]}/{instance}")
        ])

        self.logger = get_logger(__name__)

    def save(self, instance: str, output_path: str, file_name: str = None, median: bool = True) -> None:
        """
        Generates a Pareto front for the specified instance and saves it to the specified output path.

        Args:
            instance (str):
                The name of the instance for which the Pareto front is to be generated.
            
            output_path (str):
                The path where the Pareto front image will be saved.
            
            median (bool):
                A boolean indicating whether to generate the median front or the best front. Default is True.

        Returns:
            None

        Example:
            >>> from SAES.multiobjective.pareto_front import Front2D
            >>>
            >>> fronts_path = "path/to/fronts"
            >>> references_path = "path/to/references"
            >>> metric = "HV"
            >>> front = Front2D(fronts_path, references_path, metric)
            >>> front.save("ZDT1", "path/to/output")
        """

        median_best = 'MEDIAN' if median else 'BEST'
        fronts_paths = [f"{self.fronts_path}/{algorithm}/{instance}/{median_best}_{self.metric}_FUN.csv" for algorithm in self.algorithms]
        file_name = file_name if file_name else f"front_all_{instance}_{self.metric}_{median_best}.png"

        self._front(fronts_paths, instance)

        os.makedirs(output_path, exist_ok=True)
        plt.savefig(f"{output_path}/{file_name}")
        self.logger.info(f"Front {file_name} saved to {output_path}")
        plt.close()

    def show(self, instance: str, median: bool=True) -> None:
        """
        Generates a Pareto front for the specified instance and displays it.

        Args:
            instance (str):
                The name of the instance for which the Pareto front is to be generated.
            
            median (bool):
                A boolean indicating whether to generate the median front or the best front. Default is True.

        Returns:
            None

        Example:
            >>> from SAES.multiobjective.pareto_front import Front2D
            >>>
            >>> fronts_path = "path/to/fronts"
            >>> references_path = "path/to/references"
            >>> metric = "HV"
            >>> front = Front2D(fronts_path, references_path, metric)
            >>> front.show("ZDT1")
        """

        median_best = 'MEDIAN' if median else 'BEST'
        fronts_paths = [f"{self.fronts_path}/{algorithm}/{instance}/{median_best}_{self.metric}_FUN.csv" for algorithm in self.algorithms]
        self._front(fronts_paths, instance)
        plt.show()

    @abstractmethod
    def _front(self, front_paths: list, instance: str) -> None:
        """Abstract method to generate a Pareto front for the specified instance."""
        pass

class Front2D(Front):
    """Class to generate 2D Pareto fronts for different algorithms and instances."""
    def __init__(self, fronts_path: str, references_path: str, metric: str) -> None:
        """Initializes the Front2D object with the given fronts path, references path, and metric."""
        super().__init__(fronts_path, references_path, metric, 2)

    def _front(self, front_paths: list, instance: str) -> None:
        """Generates a 2D Pareto front for the specified instance."""

        # Veriffy that the number of front_paths and algorithms are the same
        if len(front_paths) != len(self.algorithms):
            raise ValueError("The paths and algorithms lists must have the same length.")
                
        # Number of plots
        num_plots = len(front_paths) + 1
        rows = int(num_plots**0.5)
        cols = (num_plots + rows - 1) // rows  

        _, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*6))
        axes = axes.flatten()  

        for i, (front_path, algorithm) in enumerate(zip([f"{self.references_path}/{instance}.{self.dimensions}D.csv"] + front_paths, ["Reference"] + self.algorithms)):
            if not os.path.exists(front_path):
                raise FileNotFoundError(f"Front {front_path} not found")
            
            # Read the front
            df = pd.read_csv(front_path, header=None)
            x, y = df[0], df[1]
            
            # Create the plot
            ax = axes[i]
            ax.scatter(x, y, alpha=0.7, color='red' if algorithm == "Reference" else 'blue')
            
            # Personalize the plot
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='both', which='both', length=0)
            ax.set_title(algorithm, pad=20)
            ax.grid(True, alpha=0.3)

        # Remove empty plots
        plt.tight_layout()

class Front3D(Front):
    """Class to generate 3D Pareto fronts for different algorithms and instances."""
    def __init__(self, fronts_path: str, references_path: str, metric: str) -> None:
        """Initializes the Front3D object with the given fronts path, references path, and metric."""
        super().__init__(fronts_path, references_path, metric, 3)

    def _front(self, front_paths: list, instance: str) -> None:
        """Generates a 3D Pareto front for the specified instance."""

        # Veriffy that the number of front_paths and algorithms are the same
        if len(front_paths) != len(self.algorithms):
            raise ValueError("The paths and algorithms lists must have the same length.")
    
        # Número de gráficos
        num_plots = len(front_paths) + 1
        rows = int(num_plots ** 0.5)
        cols = (num_plots + rows - 1) // rows  
        
        fig = plt.figure(figsize=(cols * 6, rows * 6))
        
        for i, (front_path, algorithm) in enumerate(zip([f"{self.references_path}/{instance}.{self.dimensions}D.csv"] + front_paths, ["Reference"] + self.algorithms)):
            if not os.path.exists(front_path):
                raise FileNotFoundError(f"Front {front_path} not found")
            
            # Read the front
            df = pd.read_csv(front_path, header=None)
            x, y, z = df[0], df[1], df[2]
            
            # Create the plot
            ax = fig.add_subplot(rows, cols, i + 1, projection='3d')
            ax.scatter(x, y, z, alpha=0.7, color='red' if algorithm == "Reference" else 'blue')
            
            # Personalize the plot
            ax.set_title(algorithm, pad=20)
            ax.grid(True, alpha=0.3)
            
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            ax.view_init(elev=20, azim=45)
        
        # Remove empty plots
        plt.tight_layout()

class FrontND(Front):
    """Class to generate ND Pareto fronts for different algorithms and instances."""
    def __init__(self, fronts_path: str, references_path: str, metric: str, dimensions: int) -> None:
        """Initializes the FrontND object with the given fronts path, references path, metric, and dimensions."""
        super().__init__(fronts_path, references_path, metric, dimensions)

    def _front(self, front_paths: list, instance: str) -> None:
        """Generates an ND Pareto front for the specified instance."""

        # Veriffy that the number of front_paths and algorithms are the same
        if len(front_paths) != len(self.algorithms):
            raise ValueError("The paths and algorithms lists must have the same length.")
    
        # Number of plots
        num_plots = len(front_paths) + 1
        rows = int(num_plots ** 0.5)
        cols = (num_plots + rows - 1) // rows  
        
        _, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 6))
        axes = axes.flatten()
        
        for i, (front_path, algorithm) in enumerate(zip([f"{self.references_path}/{instance}.{self.dimensions}D.csv"] + front_paths, ["Reference"] + self.algorithms)):
            if not os.path.exists(front_path):
                raise FileNotFoundError(f"Front {front_path} not found")
            
            # Read the front
            df = pd.read_csv(front_path, header=None, names=[f"f{j}" for j in range(self.dimensions)])
            df["Name"] = "Value"

            # Create the plot
            pd.plotting.parallel_coordinates(df, 'Name', color = ('red') if algorithm == "Reference" else ('blue'), ax=axes[i])
            axes[i].set_title(algorithm)
            axes[i].get_legend().remove()

        # Remove empty plots
        plt.tight_layout()
