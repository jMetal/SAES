import unittest
from SAES.utils.statistical_checks import check_normality
import pandas as pd

class TestUtils(unittest.TestCase):
    def test_normality(self):
        # Create a sample DataFrame with normal data
        data = {
            "Algorithm": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
            "Instance": ["P1", "P1", "P1", "P1", "P1", "P1", "P1", "P1", "P1", "P1"],
            "MetricValue": [0.09010988,  0.79997335,  0.45336877,  0.77117614,  1.33044881, -0.08708802, -0.70524954,  0.91971554, -0.96683618, -0.12781421]
        }
        df = pd.DataFrame(data)
        
        # Test the normality check function
        self.assertTrue(check_normality(df))
        
        # Add non-normal data to the DataFrame
        df.loc[6] = ["A", "P1", 1]
        df.loc[7] = ["A", "P2", 2]
        df.loc[8] = ["B", "P1", 3]
        df.loc[9] = ["B", "P2", 4]
        df.loc[10] = ["C", "P1", 5]
        df.loc[11] = ["C", "P2", 6]

        # Test the normality check function with non-normal data
        self.assertFalse(check_normality(df))

        # Test the normality check function with identical values
        df.loc[6] = ["A", "P1", 1]
        df.loc[7] = ["A", "P2", 1]
        df.loc[8] = ["B", "P1", 1]
        df.loc[9] = ["B", "P2", 1]
        df.loc[10] = ["C", "P1", 1]
        df.loc[11] = ["C", "P2", 1]

        # Test the normality check function with identical values
        self.assertFalse(check_normality(df))
