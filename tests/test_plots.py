import unittest
from algorithm_benchmark_toolkit.plots import generate_boxplots_from_csv
from pathlib import Path
import pandas as pd
import os

class TestUtils(unittest.TestCase):
    def test_generate_boxplots_from_csv(self):
        df = pd.DataFrame({
            'Algorithm': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'B'],
            'Problem': ['P1', 'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P2'],
            'MetricValue': [1, 0, 1, 1, 1, 1, 1, 1],
            'Metric': ['Python', 'Python', 'Python', 'Python', 'Python', 'Python', 'Python', 'Python']
        })
        metrics = pd.DataFrame({
            'Metric': ['Python'],
            'Maximize': [True]
        })
        
        generate_boxplots_from_csv(df, metrics)

        # Check if the boxplots are generated
        number_of_plots = len(os.listdir(Path('outputs/boxplots/Python')))
        self.assertEqual(number_of_plots, 2)
