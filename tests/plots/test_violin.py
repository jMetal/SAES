from SAES.plots.violin import Violin
from PIL import Image
import unittest, os

class TestViolin(unittest.TestCase):
    
    def setUp(self):
        swarmIntelligence = "tests/test_data/swarmIntelligence.csv"
        multiobjectiveMetrics = "tests/test_data/multiobjectiveMetrics.csv"
        metric = "HV"
        self.violin = Violin(swarmIntelligence, multiobjectiveMetrics, metric)

    def test_save_instance(self):
        self.violin.save_instance("ZDT1", f"{os.getcwd()}/tests/plots", width=10)
        image_path = f"{os.getcwd()}/tests/plots/violin_HV_ZDT1.png"
        self.assertTrue(os.path.exists(image_path))

        # Open the image and check its size
        with Image.open(image_path) as img:
            width, height = img.size
            self.assertEqual((width, height), (1000, 562))

        os.remove(image_path)

    def test_save_all_instances(self):
        self.violin.save_all_instances(f"{os.getcwd()}/tests/plots", file_name="violin_name.png", width=20)
        image_path = f"{os.getcwd()}/tests/plots/violin_name.png"
        self.assertTrue(os.path.exists(image_path))

        # Open the image and check its size
        with Image.open(image_path) as img:
            width, height = img.size
            self.assertEqual((width, height), (2000, 2000))

        os.remove(image_path)

    def test_show_instance(self):
        self.violin.show_instance("ZDT1", width=10)
        self.assertTrue(True)

    def test_show_all_instances(self):
        self.violin.show_all_instances(width=20)
        self.assertTrue(True)
