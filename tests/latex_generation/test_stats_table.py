import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from SAES.utils.dataframe_processor import process_dataframe_metric, check_normality
from SAES.statistical_tests.non_parametrical import friedman, wilcoxon
from SAES.logger import get_logger
from SAES.latex_generation.stats_table import MeanMedian, Friedman, WilcoxonPivot, Wilcoxon  # Replace 'your_module' with the actual module name

class TestTableClasses(unittest.TestCase):
    
    def setUp(self):
        self.data_no_diff = pd.DataFrame({
            'Instance': ['I1', 'I1', 'I2', 'I2', 'I1', 'I1', 'I2', 'I2', 'I1', 'I1', 'I2', 'I2'],
            'Algorithm': ['A1', 'A1', 'A1', 'A1', 'A2', 'A2', 'A2', 'A2', 'A3', 'A3', 'A3', 'A3'],
            'ExecutionId': [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            'MetricValue': [0.1, 0.2, 0.15, 0.25, 75.2, 75.4, 7.1, 7, 12, 13, 14, 15],
            'MetricName': ['Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy']
        })

        self.data_diff = pd.DataFrame({
            'Instance': ['I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1', 'I1'],
            'Algorithm': ['A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2', 'A2'],
            'ExecutionId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            'MetricValue': [0.1, 0.2, 0.15, 0.25, 0.1, 0.2, 0.15, 0.25, 0.1, 0.2, 0.15, 0.25, 0.1, 0.2, 0.15, 3, 6, 4, 5, 7, 3, 6, 4, 5, 7, 3, 6, 4, 5, 7],
            'MetricName': ['Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy', 'Accuracy']
        })

        self.metrics = pd.DataFrame({
            'MetricName': ['Accuracy'],
            'Maximize': [True]
        })

        self.metric = 'Accuracy'
   
    def test_mean_median(self):
        median = MeanMedian(self.data_no_diff, self.metrics, self.metric)
        median.compute_table()
        self.assertFalse(median.normality)
        self.assertAlmostEqual(median.table.loc["I1", "A1"], 0.15, places=2)
        self.assertAlmostEqual(median.table.loc["I1", "A2"], 75.3, places=2)
        self.assertAlmostEqual(median.table.loc["I2", "A1"], 0.2, places=2)
        self.assertAlmostEqual(median.table.loc["I2", "A2"], 7.05, places=2)

    def test_friedman_difference(self):
        friedman = Friedman(self.data_diff, self.metrics, self.metric)
        friedman.compute_table()
        self.assertAlmostEqual(friedman.table.loc["I1", "A1"], 0.15, places=2)
        self.assertAlmostEqual(friedman.table.loc["I1", "A2"], 5.0, places=2)
        self.assertEqual(friedman.table.loc["I1", "Friedman"], "+")

    def test_friedman_no_difference(self):
        friedman = Friedman(self.data_no_diff, self.metrics, self.metric)
        friedman.compute_table()
        self.assertEqual(friedman.table.loc["I1", "Friedman"], "=")
        self.assertEqual(friedman.table.loc["I2", "Friedman"], "=")

    def test_wilcoxon_pivot_difference(self):
        wilcoxon_pivot = WilcoxonPivot(self.data_diff, self.metrics, self.metric)
        wilcoxon_pivot.compute_table()
        self.assertAlmostEqual(wilcoxon_pivot.table.loc["I1", "A1"][0], 0.15, places=2)
        self.assertEqual(wilcoxon_pivot.table.loc["I1", "A1"][1], "+")
        self.assertAlmostEqual(wilcoxon_pivot.table.loc["I1", "A2"][0], 5.0, places=2)
        self.assertEqual(wilcoxon_pivot.table.loc["I1", "A2"][1], "")
    
    def test_wilcoxon_pivot_no_difference(self):
        wilcoxon_pivot = WilcoxonPivot(self.data_no_diff, self.metrics, self.metric)
        wilcoxon_pivot.compute_table()
        self.assertEqual(wilcoxon_pivot.table.loc["I1", "A3"], (12.5, ""))
        self.assertEqual(wilcoxon_pivot.table.loc["I2", "A3"], (14.5, ""))
        self.assertAlmostEqual(wilcoxon_pivot.table.loc["I1", "A1"][0], 0.15, places=2)
        self.assertEqual(wilcoxon_pivot.table.loc["I1", "A1"][1], "=")
    
    def test_wilcoxon_difference(self):
        wilcoxon = Wilcoxon(self.data_diff, self.metrics, self.metric)
        wilcoxon.compute_table()
        self.assertEqual(wilcoxon.table.loc["A1", "A2"], "-")

    def test_wilcoxon_no_difference(self):
        wilcoxon = Wilcoxon(self.data_no_diff, self.metrics, self.metric)
        wilcoxon.compute_table()
        self.assertEqual(wilcoxon.table.loc["A1", "A2"], "==")
        self.assertEqual(wilcoxon.table.loc["A1", "A3"], "==")
        self.assertEqual(wilcoxon.table.loc["A2", "A3"], "==")
        self.assertEqual(wilcoxon.table.loc["A2", "A2"], "")

if __name__ == '__main__':
    unittest.main()
