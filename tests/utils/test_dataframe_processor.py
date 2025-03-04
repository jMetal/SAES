from SAES.utils.dataframe_processor import process_dataframe_metric, check_normality, get_metrics
import pandas as pd
import unittest

class TestBoxplot(unittest.TestCase):
    
    def setUp(self):
        self.swarmIntelligence = pd.read_csv("tests/test_data/swarmIntelligence.csv")
        self.multiobjectiveMetrics = pd.read_csv("tests/test_data/multiobjectiveMetrics.csv")
        self.metric = "HV"

    def test_process_dataframe_metric(self):
        processed = process_dataframe_metric(self.swarmIntelligence, self.multiobjectiveMetrics, self.metric)
        self.assertAlmostEqual(processed[0].loc[3, "MetricValue"], 0.643772, 2)
        self.assertTrue(processed[1])

    def test_check_normality(self):
        self.assertFalse(check_normality(self.swarmIntelligence))

    def test_get_metrics(self):
        metrics = list(get_metrics(self.swarmIntelligence))
        metrics_og = list(self.multiobjectiveMetrics["MetricName"].unique())
        self.assertEqual(metrics, metrics_og) 
