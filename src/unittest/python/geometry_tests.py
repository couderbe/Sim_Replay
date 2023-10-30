from src.main.python.tools.geometry import Point
import unittest


class PointTest(unittest.TestCase):
    def test_carthesian_computation(self):
        pt0 = Point(0.0,0.0)
        pt1 = Point(0.0,10.0)
        self.assertEqual(pt1.spherical_to_carthesian(pt0),(0,600))