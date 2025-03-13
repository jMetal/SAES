from SAES.statistical_tests.parametrical import anova, t_test
import pandas as pd
import unittest

class TestStatisticalTests(unittest.TestCase):
    
    def setUp(self):
        
        self.anova_data = pd.DataFrame({
            "Algorithm A": [0.9, 0.85, 0.95, 0.8, 0.92],
            "Algorithm B": [0.8, 0.75, 0.85, 0.85, 0.87],
        })

        self.ttes_data_equal = pd.DataFrame({
            "Algorithm A": [0.5, 0.6, 0.7],
            "Algorithm B": [0.5, 0.6, 0.7]
        })

        self.ttest_data_different = pd.DataFrame({
            "Algorithm A": [0.9, 0.85, 0.95, 0.9, 0.85, 0.95],
            "Algorithm B": [0.1, 0.2, 0.3, 0.1, 0.2, 0.3]
        })

    def test_anova_test(self):
        
        result = anova(self.anova_data)
        self.assertIn("Results", result.columns)
        self.assertGreater(result.loc["Anova-stat", "Results"], 0)
        self.assertGreaterEqual(result.loc["p-value", "Results"], 0)
        self.assertLessEqual(result.loc["p-value", "Results"], 1)

    def test_anova_test_raises(self):
        
        with self.assertRaises(ValueError):
            anova(pd.DataFrame())  # No data

    def test_t_test_equal(self):
       
        result = t_test(self.ttes_data_equal, maximize=True)
        self.assertEqual(result, "=")

    def test_t_test_different(self):
        
        result = t_test(self.ttest_data_different, maximize=True)
        self.assertIn(result, ["+", "-"])  # It will be depend of the medians

    def test_t_test_raises(self):
       
        with self.assertRaises(KeyError):
            t_test(pd.DataFrame({"InvalidA": [1, 2], "InvalidB": [2, 3]}), maximize=True)  # Invalid columns
