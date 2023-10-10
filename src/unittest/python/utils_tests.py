from src.main.python.utils import get_var_unit, between
import unittest


class UtilsTest(unittest.TestCase):

    def test_get_var_unit(self):
        var = get_var_unit("ZULU TIME")
        self.assertEqual(var,"Seconds")

    def test_between(self):
        btw = between(5,6.0,2000)
        self.assertEqual(btw,6.0)