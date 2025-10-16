from src.main.python.importer.specific_parsers import SpecificParser
import unittest


class SpecificParserTest(unittest.TestCase):

    def test_SDVFR_parser(self):
        data = """Vitesse : 6 kmh
Altitude : 459 ft
Latitude : 43.585122
Longitude : 1.502755
Cap : 163°"""

        parser = SpecificParser(data)
        parsed_data = parser.parse_data(data)

        self.assertEqual(6, parsed_data.get("GPS GROUND SPEED"))
        self.assertEqual(163, parsed_data.get("GPS GROUND TRUE HEADING"))

    def test_SDVFR_parser_incorrect_data(self):
        data = """Vitesse incompatible : XX kmh
Altitude : 459 ft
Latitude : 43.585122
Longitude : 1.502755"""

        parser = SpecificParser(data)
        parsed_data = parser.parse_data(data)

        self.assertEqual(None, parsed_data.get("GPS GROUND SPEED"))
        self.assertEqual(None, parsed_data.get("GPS GROUND TRUE HEADING"))