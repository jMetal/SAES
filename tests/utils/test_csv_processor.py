import unittest
import pandas as pd
import os
import shutil
from SAES.utils.csv_processor import process_csv_basic, process_csv_extended

def remove_files():
    """Clean up directories and files created during testing."""
    if os.path.exists("CSVs"):
        shutil.rmtree("CSVs")
    if os.path.exists("outputs"):
        shutil.rmtree("outputs")

class TestProcessCSV(unittest.TestCase):
    def setUp(self):
        """Setup common variables and temporary DataFrame for testing."""
        self.df = pd.DataFrame({
            'Problem': ['P1', 'P1', 'P2', 'P2', 'P3', 'P3'],
            'Algorithm': ['A1', 'A2', 'A1', 'A2', 'A1', 'A2'],
            'MetricValue': [0.8, 0.6, 0.75, 0.65, 0.85, 0.7]
        })
        self.metric = "accuracy"

    def test_process_csv_basic(self):
        """Test the basic processing of CSV data."""

        remove_files()
        result = process_csv_basic(self.df, self.metric)

        # Check if the output CSV file exists
        self.assertTrue(os.path.exists(f"CSVs/data_{self.metric}.csv"))

        # Validate the result DataFrame matches the input DataFrame
        pd.testing.assert_frame_equal(result, self.df)
        remove_files()

    def test_process_csv_extended_with_extra(self):
        """Test extended CSV processing with extra metrics enabled."""
        remove_files()
        df_pivot, df_std_pivot, name = process_csv_extended(self.df, self.metric, extra=True)

        # Check if output CSV files exist
        self.assertTrue(os.path.exists(f"CSVs/data_{name}_{self.metric}.csv"))
        self.assertTrue(os.path.exists(f"CSVs/data_std_{name}_{self.metric}.csv"))

        # Validate the pivoted DataFrame for median or mean
        expected_pivot = self.df.groupby(['Problem', 'Algorithm'])['MetricValue'].median().reset_index()
        expected_pivot = expected_pivot.pivot(index='Problem', columns='Algorithm', values='MetricValue')
        pd.testing.assert_frame_equal(df_pivot, expected_pivot)

        # Validate the pivoted DataFrame for standard deviation
        expected_std = self.df.groupby(['Problem', 'Algorithm'])['MetricValue'].std().reset_index()
        expected_std = expected_std.pivot(index='Problem', columns='Algorithm', values='MetricValue')
        pd.testing.assert_frame_equal(df_std_pivot, expected_std)
        remove_files()

    def test_process_csv_extended_without_extra(self):
        """Test extended CSV processing without extra metrics."""
        remove_files()
        df_pivot, df_std_pivot, name = process_csv_extended(self.df, self.metric, extra=False)

        # Check if output CSV file exists
        self.assertTrue(os.path.exists(f"CSVs/data_{name}_{self.metric}.csv"))
        self.assertIsNone(df_std_pivot)  # Standard deviation DataFrame should be None

        # Validate the pivoted DataFrame for median or mean
        expected_pivot = self.df.groupby(['Problem', 'Algorithm'])['MetricValue'].median().reset_index()
        expected_pivot = expected_pivot.pivot(index='Problem', columns='Algorithm', values='MetricValue')
        pd.testing.assert_frame_equal(df_pivot, expected_pivot)
        remove_files()

