from SAES.latex_generation.stats_table import MeanMedian, Friedman, WilcoxonPivot, Wilcoxon, Anova, TTest, TTestPivot, FriedmanPValues
import pandas.testing as pdt
import unittest, os
import pandas as pd

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

        self.swarmIntelligence = "tests/test_data/swarmIntelligence.csv"
        self.multiobjectiveMetrics = "tests/test_data/multiobjectiveMetrics.csv"
   
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
        self.assertEqual(friedman.table.loc["I1", "Friedman"], "+")
        self.assertEqual(friedman.table.loc["I2", "Friedman"], "+")

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

    def test_mean_median_table(self):
        mean_median = MeanMedian(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        mean_median.compute_table()

        # Check if the table is correct
        self.assertAlmostEqual(mean_median.table.loc["ZDT6", "AutoMOPSOZ"], 0.401480, places=2)
        pdt.assert_frame_equal(mean_median.table, mean_median.mean_median)

        mean_median.create_latex_table()
        latex_doc = mean_median.latex_doc
        mean_median.save("tests/latex_generation", file_name="MeanMedian_HV.tex")
        
        with open("tests/latex_generation/MeanMedian_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/MeanMedian_HV.tex")
        
        mean_median.show()
        self.assertTrue(True)

    def test_mean_friedman_table(self):
        friedman = Friedman(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        friedman.compute_table()

        # Check if the table is correct
        self.assertAlmostEqual(friedman.table.loc["ZDT6", "AutoMOPSOZ"], 0.401480, places=2)
        self.assertEqual(friedman.table.loc["ZDT6", "Friedman"], "+")
        
        friedman.create_latex_table()
        latex_doc = friedman.latex_doc
        friedman.save("tests/latex_generation", file_name="Friedman_HV.tex")
        
        with open("tests/latex_generation/Friedman_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/Friedman_HV.tex")

        friedman.show()
        self.assertTrue(True)

    def test_mean_wilcoxon_pivot_table(self):
        wilcoxon_pivot = WilcoxonPivot(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        wilcoxon_pivot.compute_table()

        # Check if the table is correct
        self.assertAlmostEqual(wilcoxon_pivot.table.loc["ZDT6", "AutoMOPSOZ"][0], 0.401480, places=2)
        self.assertEqual(wilcoxon_pivot.table.loc["ZDT6", "AutoMOPSOZ"][1], "")
        self.assertEqual(wilcoxon_pivot.table.loc["ZDT6", "NSGAII"][1], "+")

        wilcoxon_pivot.create_latex_table()
        latex_doc = wilcoxon_pivot.latex_doc
        wilcoxon_pivot.save("tests/latex_generation", file_name="WilcoxonPivot_HV.tex")

        with open("tests/latex_generation/WilcoxonPivot_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/WilcoxonPivot_HV.tex")

        wilcoxon_pivot.show()
        self.assertTrue(True)

    def test_mean_wilcoxon_table(self):
        wilcoxon = Wilcoxon(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        wilcoxon.compute_table()

        # Check if the table is correct
        self.assertEqual(wilcoxon.table.loc["NSGAII", "AutoMOPSOZ"], "---+--+==+--")
        
        wilcoxon.create_latex_table()
        latex_doc = wilcoxon.latex_doc
        wilcoxon.save("tests/latex_generation", file_name="Wilcoxon_HV.tex")
        
        with open("tests/latex_generation/Wilcoxon_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/Wilcoxon_HV.tex")

        wilcoxon.show()
        self.assertTrue(True)

    def test_anova_difference(self):
        anova = Anova(self.data_diff, self.metrics, self.metric)
        anova.compute_table()
        self.assertAlmostEqual(anova.table.loc["I1", "A1"], 0.169, places=2)
        self.assertAlmostEqual(anova.table.loc["I1", "A2"], 5.0, places=2)
        self.assertEqual(anova.table.loc["I1", "Anova"], "=")

    def test_anova_no_difference(self):
        anova = Anova(self.data_no_diff, self.metrics, self.metric)
        anova.compute_table()
        self.assertEqual(anova.table.loc["I1", "Anova"], "=")
        self.assertEqual(anova.table.loc["I2", "Anova"], "=")

    def test_ttest_pivot_difference(self):
        ttest_pivot = TTestPivot(self.data_diff, self.metrics, self.metric)
        ttest_pivot.compute_table()
        self.assertAlmostEqual(ttest_pivot.table.loc["I1", "A1"][0], 0.169, places=2)
        self.assertEqual(ttest_pivot.table.loc["I1", "A1"][1], "+")
        self.assertAlmostEqual(ttest_pivot.table.loc["I1", "A2"][0], 5.0, places=2)
        self.assertEqual(ttest_pivot.table.loc["I1", "A2"][1], "")
    
    def test_ttest_pivot_no_difference(self):
        ttest_pivot = TTestPivot(self.data_no_diff, self.metrics, self.metric)
        ttest_pivot.compute_table()
        self.assertEqual(ttest_pivot.table.loc["I1", "A3"], (12.5, ""))
        self.assertEqual(ttest_pivot.table.loc["I2", "A3"], (14.5, ""))
        self.assertAlmostEqual(ttest_pivot.table.loc["I1", "A1"][0], 0.15, places=2)
        self.assertEqual(ttest_pivot.table.loc["I1", "A1"][1], "+")
    
    def test_ttest_difference(self):
        ttest = TTest(self.data_diff, self.metrics, self.metric)
        ttest.compute_table()
        self.assertEqual(ttest.table.loc["A1", "A2"], "-")

    def test_ttest_no_difference(self):
        ttest = TTest(self.data_no_diff, self.metrics, self.metric)
        ttest.compute_table()
        self.assertEqual(ttest.table.loc["A1", "A2"], "--")
        self.assertEqual(ttest.table.loc["A1", "A3"], "--")
        self.assertEqual(ttest.table.loc["A2", "A3"], "+-")
        self.assertEqual(ttest.table.loc["A2", "A2"], "")

    def test_mean_anova_table(self):
        anova = Anova(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        anova.compute_table()

        # Check if the table is correct
        self.assertAlmostEqual(anova.table.loc["ZDT6", "AutoMOPSOZ"], 0.401480, places=2)
        self.assertEqual(anova.table.loc["ZDT6", "Anova"], "=")
        
        anova.create_latex_table()
        latex_doc = anova.latex_doc
        anova.save("tests/latex_generation", file_name="Anova_HV.tex")
        
        with open("tests/latex_generation/Anova_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/Anova_HV.tex")

        anova.show()
        self.assertTrue(True)

    def test_mean_ttest_pivot_table(self):
        ttest_pivot = TTestPivot(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        ttest_pivot.compute_table()

        # Check if the table is correct
        self.assertAlmostEqual(ttest_pivot.table.loc["ZDT6", "AutoMOPSOZ"][0], 0.401480, places=2)
        self.assertEqual(ttest_pivot.table.loc["ZDT6", "AutoMOPSOZ"][1], "")
        self.assertEqual(ttest_pivot.table.loc["ZDT6", "NSGAII"][1], "+")

        ttest_pivot.create_latex_table()
        latex_doc = ttest_pivot.latex_doc
        ttest_pivot.save("tests/latex_generation", file_name="TtestPivot_HV.tex")

        with open("tests/latex_generation/TtestPivot_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/TtestPivot_HV.tex")

        ttest_pivot.show()
        self.assertTrue(True)

    def test_mean_ttest_table(self):
        ttest = TTest(self.swarmIntelligence, self.multiobjectiveMetrics, "HV")
        ttest.compute_table()

        # Check if the table is correct
        self.assertEqual(ttest.table.loc["NSGAII", "AutoMOPSOZ"], "---+-++==+--")
        
        ttest.create_latex_table()
        latex_doc = ttest.latex_doc
        ttest.save("tests/latex_generation", file_name="Ttest_HV.tex")
        
        with open("tests/latex_generation/Ttest_HV.tex", "r") as file:
            contenido = file.read()

        # Check if the latex table is correct
        self.assertEqual(latex_doc, contenido)
        os.remove("tests/latex_generation/Ttest_HV.tex")

        ttest.show()
        self.assertTrue(True)




        

        
