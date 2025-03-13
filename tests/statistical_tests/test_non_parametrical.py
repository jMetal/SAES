from SAES.statistical_tests.non_parametrical import friedman, wilcoxon, NemenyiCD, friedman_aligned_rank, quade
import pandas as pd
import unittest

class TestStatisticalTests(unittest.TestCase):
    
    def setUp(self):
        
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
        
        result = friedman(self.friedman_data, maximize=True)
        self.assertIn("Results", result.columns)
        self.assertGreater(result.loc["Friedman-stat", "Results"], 0)
        self.assertGreaterEqual(result.loc["p-value", "Results"], 0)
        self.assertLessEqual(result.loc["p-value", "Results"], 1)

    def test_friedman_test_raises(self):
        
        with self.assertRaises(ValueError):
            friedman(pd.DataFrame(), maximize=True)  # No data

    def test_wilcoxon_test_equal(self):
       
        result = wilcoxon(self.wilcoxon_data_equal, maximize=True)
        self.assertEqual(result, "=")

    def test_wilcoxon_test_different(self):
        
        result = wilcoxon(self.wilcoxon_data_different, maximize=True)
        self.assertIn(result, ["+", "-"])  # It will be depend of the medians

    def test_wilcoxon_test_raises(self):
       
        with self.assertRaises(KeyError):
            wilcoxon(pd.DataFrame({"InvalidA": [1, 2], "InvalidB": [2, 3]}), maximize=True)  # Invalid columns

    def test_NemenyiCD(self):
        result = NemenyiCD(0.05, 5, 2)
        self.assertAlmostEqual(result, 41.4507836, 2)
        
    def test_friedman_align_test(self):
        
        result = friedman_aligned_rank(self.friedman_data, maximize=True)
        self.assertIn("Results", result.columns)
        self.assertGreater(result.loc["Aligned Rank stat", "Results"], 0)
        self.assertGreaterEqual(result.loc["p-value", "Results"], 0)
        self.assertLessEqual(result.loc["p-value", "Results"], 1)

    def test_friedman_align_test_raises(self):
        
        with self.assertRaises(ValueError):
            friedman_aligned_rank(pd.DataFrame(), maximize=True)  # No data

    def test_quade_test(self):
        
        result = quade(self.friedman_data, maximize=True)
        self.assertIn("Results", result.columns)
        self.assertGreater(result.loc["Quade Test stat", "Results"], 0)
        self.assertGreaterEqual(result.loc["p-value", "Results"], 0)
        self.assertLessEqual(result.loc["p-value", "Results"], 1)

    def test_quade_test_raises(self):
        
        with self.assertRaises(ValueError):
            quade(pd.DataFrame(), maximize=True)  # No data