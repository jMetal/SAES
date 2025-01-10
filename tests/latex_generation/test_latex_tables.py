import unittest
import pandas as pd
from io import StringIO
import os
import shutil
from SAES.latex_generation.latex_skeleton import create_tables_latex

def remove_files():
    """Clean up directories and files created during testing."""
    if os.path.exists("CSVs"):
        shutil.rmtree("CSVs")

class TestCreateTablesLatexMetrics(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data_csv = StringIO("""
Algorithm,Instance,MetricName,ExecutionId,MetricValue
mistralai/mistral-large,Subasi2016,Java,0,1.0
mistralai/mistral-large,Subasi2016,Python,1,2.5
mistralai/mistral-large,Subasi2016,Java,2,1.5
mistralai/mistral-large,Subasi2016,Python,3,2.8
mistralai/mistral-small,Subasi2016,Java,0,1.0
mistralai/mistral-small,Subasi2016,Python,1,2.5
mistralai/mistral-small,Subasi2016,Java,2,1.5
mistralai/mistral-small,Subasi2016,Python,3,2.8
"""
        )
        
        self.metrics_csv = StringIO("""
MetricName,Maximize
Python,True
Java,True
"""     )

        # Convert sample CSVs into DataFrames
        self.data_df = pd.read_csv(self.data_csv)
        self.metrics_df = pd.read_csv(self.metrics_csv)

    def test_create_tables_latex_metrics(self):
        """Test the create_tables_latex_metrics function."""
        remove_files()
        # Test the function with the sample data
        create_tables_latex(self.data_df, self.metrics_df)

        # Check if the output files exist
        self.assertTrue(os.path.exists(f"outputs/tables/Python/base_table_tex"))
        self.assertTrue(os.path.exists(f"outputs/tables/Java/base_table_tex"))
        remove_files()
