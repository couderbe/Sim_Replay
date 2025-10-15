from mockito import mock, verify
from src.main.python.importer.importer import import_gpx_file_module, retrieve_SDVFR_heading, retrieve_SDVFR_speed
import unittest


class ImportTest(unittest.TestCase):
    def test_import_invalid_name(self):
        _mainTableModel = mock()

        with self.assertRaises(FileNotFoundError):
            import_gpx_file_module(_mainTableModel, "ZZZ.gpx")

    def test_SDVFR_parser(self):
        data = """Vitesse : 6 kmh
Altitude : 459 ft
Latitude : 43.585122
Longitude : 1.502755
Cap : 163°"""
        self.assertEqual(6, retrieve_SDVFR_speed(data))
        self.assertEqual(163, retrieve_SDVFR_heading(data))

    def test_SDVFR_parser_incorrect_data(self):
        data = """Vitesse incompatible : XX kmh
Altitude : 459 ft
Latitude : 43.585122
Longitude : 1.502755"""
        self.assertEqual(None, retrieve_SDVFR_speed(data))
        self.assertEqual(None, retrieve_SDVFR_heading(data))