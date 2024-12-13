import unittest
import pandas as pd
from SAES.statistical_tests.non_parametrical import friedman_test, wilcoxon_test

class TestStatisticalTests(unittest.TestCase):
    
    def setUp(self):
        """Configure test data for the tests."""
        self.friedman_data = pd.DataFrame({
            "Algorithm A": [0.9, 0.85, 0.95, 0.8, 0.92],
            "Algorithm B": [0.8, 0.75, 0.85, 0.85, 0.87],
        })

        self.wilcoxon_data_equal = pd.DataFrame({
            "Algorithm A": [0.5, 0.6, 0.7],
            "Algorithm B": [0.5, 0.6, 0.7]
        })

        self.wilcoxon_data_different = pd.DataFrame({
            "Algorithm A": [0.9, 0.85, 0.95, 0.9, 0.85, 0.95],
            "Algorithm B": [0.1, 0.2, 0.3, 0.1, 0.2, 0.3]
        })

    def test_friedman_test(self):
        """Test the friedman_test function."""
        result = friedman_test(self.friedman_data, descending=True)
        self.assertIn("Results", result.columns)
        self.assertGreater(result.loc["Friedman-statistic", "Results"], 0)
        self.assertGreaterEqual(result.loc["p-value", "Results"], 0)
        self.assertLessEqual(result.loc["p-value", "Results"], 1)

    def test_friedman_test_raises(self):
        """Test that friedman_test raises exceptions with invalid inputs."""
        with self.assertRaises(ValueError):
            friedman_test(pd.DataFrame(), descending=True)  # No data

    def test_wilcoxon_test_equal(self):
        """Test the wilcoxon_test function with equal data."""
        result = wilcoxon_test(self.wilcoxon_data_equal)
        self.assertEqual(result, "=")

    def test_wilcoxon_test_different(self):
        """Test the wilcoxon_test function with different data."""
        result = wilcoxon_test(self.wilcoxon_data_different)
        self.assertIn(result, ["+", "-"])  # It will be depend of the medians

    def test_wilcoxon_test_raises(self):
        """Test that wilcoxon_test raises exceptions with invalid inputs."""
        with self.assertRaises(KeyError):
            wilcoxon_test(pd.DataFrame({"InvalidA": [1, 2], "InvalidB": [2, 3]}))  # Invalid columns
