from SAES.plots.cdplot import CDplot
from PIL import Image
import unittest, os

class TestCDplot(unittest.TestCase):
    
    def setUp(self):
        swarmIntelligence = "tests/test_data/swarmIntelligence.csv"
        multiobjectiveMetrics = "tests/test_data/multiobjectiveMetrics.csv"
        metric = "HV"
        self.cdplot = CDplot(swarmIntelligence, multiobjectiveMetrics, metric)

    def test_save(self):
        self.cdplot.save(f"{os.getcwd()}/tests/plots", file_name="cdplot.png", width=10)
        image_path = f"{os.getcwd()}/tests/plots/cdplot.png"
        self.assertTrue(os.path.exists(image_path))

        # Open the image and check its size. save() crops with bbox_inches="tight" (so long
        # algorithm names are not cut off at the figure edge), so the pixel size now depends on
        # the rendered label text for this test's fixture data, not just the `width` argument.
        with Image.open(image_path) as img:
            width, height = img.size
            self.assertEqual((width, height), (1019, 498))

        os.remove(image_path)

    def test_show(self):
        self.cdplot.show(width=10)
        self.assertTrue(True)
