import unittest
import pandas as pd
import os
import shutil
from SAES.utils.csv_processor import process_dataframe_basic, process_dataframe_extended
from SAES.utils.csv_processor import process_csv, process_csv_metrics

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
            'Instance': ['P1', 'P1', 'P2', 'P2', 'P3', 'P3'],
            'Algorithm': ['A1', 'A2', 'A1', 'A2', 'A1', 'A2'],
            'MetricValue': [0.8, 0.6, 0.75, 0.65, 0.85, 0.7],
            'MetricName': ['accuracy', 'accuracy', 'accuracy', 'accuracy', 'accuracy', 'accuracy']
        })

        self.metrics = pd.DataFrame({
            'MetricName': ['accuracy'],
            'Maximize': [True]
        })

        self.metric = "accuracy"

    def test_process_dataframe_basic(self):
        """Test the basic processing of Dataframe data."""

        remove_files()
        result, _ = process_dataframe_basic(self.df, self.metric)

        # Check if the output CSV file exists
        self.assertTrue(os.path.exists(f"CSVs/data_{self.metric}.csv"))

        # Validate the result DataFrame matches the input DataFrame
        pd.testing.assert_frame_equal(result, self.df)
        remove_files()

    def test_process_dataframe_extended(self):
        """Test extended Dataframe processing with extra metrics enabled."""
        remove_files()
        df_pivot, df_std_pivot, name, _ = process_dataframe_extended(self.df, self.metric)

        # Check if output CSV files exist
        self.assertTrue(os.path.exists(f"CSVs/data_{name}_{self.metric}.csv"))
        self.assertTrue(os.path.exists(f"CSVs/data_std_{name}_{self.metric}.csv"))

        # Validate the pivoted DataFrame for median or mean
        expected_pivot = self.df.groupby(['Instance', 'Algorithm'])['MetricValue'].median().reset_index()
        
        expected_pivot = expected_pivot.pivot(index='Instance', columns='Algorithm', values='MetricValue')
        expected_pivot.index.name = None  
        expected_pivot.columns.name = None
        pd.testing.assert_frame_equal(df_pivot, expected_pivot)

        # Validate the pivoted DataFrame for standard deviation
        expected_std = self.df.groupby(['Instance', 'Algorithm'])['MetricValue'].std().reset_index()
        expected_std = expected_std.pivot(index='Instance', columns='Algorithm', values='MetricValue')

        pd.testing.assert_frame_equal(df_std_pivot, expected_std)
        remove_files()

    def test_process_csv(self):
        """Test the basic processing of CSV data."""

        remove_files()

        # Test the function with the sample data
        result = process_csv(self.df, self.metrics)

        # Check that the output is a dictionary with the correct keys
        self.assertTrue(len(result) == 1)

        remove_files()

    def test_process_csv_metrics(self):
        """Test the processing of CSV data with specific metrics."""

        remove_files()

        # Test the function with the sample data
        result = process_csv_metrics(self.df, self.metrics, self.metric)
       
        # Check that the output is a tuple with the correct length
        self.assertTrue(result[1] == True)

        remove_files()
