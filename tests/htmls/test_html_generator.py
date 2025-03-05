from SAES.html.html_generator import notebook_no_fronts, notebook_fronts2D, notebook_fronts3D, notebook_frontsND, notebook_bayesian
import unittest, os

class TestHTMLs(unittest.TestCase):
    
    def setUp(self):
        self.swarmIntelligence = "tests/test_data/swarmIntelligence.csv"
        self.multiobjectiveMetrics = "tests/test_data/multiobjectiveMetrics.csv"
        self.metric = "HV"
        self.fronts = "tests/test_data/fronts"
        self.references = "tests/test_data/references"
        self.dimensions = 3
        self.pivot = "NSGAII"

    def test_notebook_no_fronts(self):
        notebook_no_fronts(self.swarmIntelligence, self.multiobjectiveMetrics, self.metric, "tests/htmls")
        self.assertTrue(os.path.exists("tests/htmls/no_fronts.html"))
        os.remove("tests/htmls/no_fronts.html")

    def test_notebook_fronts2D(self):
        notebook_fronts2D(self.swarmIntelligence, self.multiobjectiveMetrics, self.metric, self.fronts, self.references, "tests/htmls")
        self.assertTrue(os.path.exists("tests/htmls/fronts2D.html"))
        os.remove("tests/htmls/fronts2D.html")

    def test_notebook_fronts3D(self):
        notebook_fronts3D(self.swarmIntelligence, self.multiobjectiveMetrics, self.metric, self.fronts, self.references, "tests/htmls")
        self.assertTrue(os.path.exists("tests/htmls/fronts3D.html"))
        os.remove("tests/htmls/fronts3D.html")

    def test_notebook_frontsND(self):
        notebook_frontsND(self.swarmIntelligence, self.multiobjectiveMetrics, self.metric, self.fronts, self.references, self.dimensions, "tests/htmls")
        self.assertTrue(os.path.exists("tests/htmls/frontsND.html"))
        os.remove("tests/htmls/frontsND.html")

    def test_notebook_bayesian(self):
        notebook_bayesian(self.swarmIntelligence, self.multiobjectiveMetrics, self.metric, self.pivot, "tests/htmls")
        self.assertTrue(os.path.exists("tests/htmls/bayesian.html"))
        os.remove("tests/htmls/bayesian.html")
