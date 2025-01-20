import unittest
from SAES.plots.boxplot import boxplots_all_metrics_instances
from pathlib import Path
import pandas as pd
import os
import shutil

def remove_files():
    """Clean up directories and files created during testing."""
    if os.path.exists("outputs"):
        shutil.rmtree("outputs")

class TestPlots(unittest.TestCase):
    def test_generate_boxplots_from_csv(self):
        remove_files()
        # Create a mock DataFrame with test data for algorithms, instances, and their metrics
        df = pd.DataFrame({
            'Algorithm': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'B'],
            'Instance': ['P1', 'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P2'],
            'MetricValue': [1, 0, 1, 1, 1, 1, 1, 1],
            'MetricName': ['Python', 'Python', 'Python', 'Python', 'Python', 'Python', 'Python', 'Python']
        })

        # Create a mock metrics DataFrame with metric properties (e.g., whether to maximize the metric)
        metrics = pd.DataFrame({
            'MetricName': ['Python'],
            'Maximize': [True]
        })
        
        # Call the function to generate boxplots
        boxplots_all_metrics_instances(df, metrics)

        # Check if the boxplots are generated
        number_of_plots = len(os.listdir(Path('outputs/boxplots/Python')))

        # Assert that the expected number of plots (one for each problem: P1 and P2) were created
        self.assertEqual(number_of_plots, 2)
        remove_files()
