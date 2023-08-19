from mockito import mock, verify
from src.main.python.importer import import_gpx_file_module
import unittest


class ImportTest(unittest.TestCase):
    def test_import_invalid_name(self):
        _mainTableModel = mock()

        with self.assertRaises(FileNotFoundError):
            import_gpx_file_module(_mainTableModel, "ZZZ.gpx")