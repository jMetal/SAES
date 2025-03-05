from SAES.multiobjective.pareto_front import Front2D, Front3D, FrontND
from PIL import Image
import unittest, os

class TestParetoFront(unittest.TestCase):
    
    def setUp(self):
        fronts = "tests/test_data/fronts"
        references = "tests/test_data/references"
        metric = "HV"
        self.front2d = Front2D(fronts, references, metric)
        self.front3d = Front3D(fronts, references, metric)
        self.frontnd = FrontND(fronts, references, metric, 3)

    def test_save2d(self):
        self.front2d.save("DTLZ1", f"{os.getcwd()}/tests/multiobjective", file_name="front2d.png")
        image_path = f"{os.getcwd()}/tests/multiobjective/front2d.png"
        self.assertTrue(os.path.exists(image_path))

        # Open the image and check its size
        with Image.open(image_path) as img:
            width, height = img.size
            self.assertEqual((width, height), (1800, 1200))

        os.remove(image_path)

    def test_show2d(self):
        self.front2d.show("DTLZ1")
        self.assertTrue(True)

    def test_save3d(self):
        self.front3d.save("DTLZ1", f"{os.getcwd()}/tests/multiobjective", file_name="front3d.png")
        image_path = f"{os.getcwd()}/tests/multiobjective/front3d.png"
        self.assertTrue(os.path.exists(image_path))

        # Open the image and check its size
        with Image.open(image_path) as img:
            width, height = img.size
            self.assertEqual((width, height), (1800, 1200))

        os.remove(image_path)

    def test_show3d(self):
        self.front3d.show("DTLZ1")
        self.assertTrue(True)

    def test_save_nd(self):
        self.frontnd.save("DTLZ1", f"{os.getcwd()}/tests/multiobjective", file_name="frontnd.png")
        image_path = f"{os.getcwd()}/tests/multiobjective/frontnd.png"
        self.assertTrue(os.path.exists(image_path))

        # Open the image and check its size
        with Image.open(image_path) as img:
            width, height = img.size
            self.assertEqual((width, height), (1800, 1200))

        os.remove(image_path)

    def test_shownd(self):
        self.frontnd.show("DTLZ1")
        self.assertTrue(True)
