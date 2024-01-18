from ctypes import c_double
from src.main.python.datas.datas_manager import FlightDatasManager
import unittest


class FlightDatasManagerTest(unittest.TestCase):
    def test_add_data(self):
        FlightDatasManager.add_data("TEST_DATA", "rad")
        self.assertEqual(
            FlightDatasManager.current_dataset.set,
            {
                "ZULU TIME": {"unit": "seconds", "type": c_double},
                "Plane Latitude": {"unit": "degrees", "type": c_double},
                "Plane Longitude": {"unit": "degrees", "type": c_double},
                "Plane Altitude": {"unit": "feet", "type": c_double},
                "Plane Bank Degrees": {"unit": "degrees", "type": c_double},
                "Plane Pitch Degrees": {"unit": "degrees", "type": c_double},
                "Plane Heading Degrees True": {"unit": "degrees", "type": c_double},
                "TEST_DATA": {"unit": "rad", "type": c_double},
            },
        )
        self.assertTrue(FlightDatasManager.has_positioning)

    def test_clean_dataset(self):
        FlightDatasManager.clean_dataset()
        self.assertEqual(
            FlightDatasManager.current_dataset.set,
            {},
        )
        self.assertFalse(FlightDatasManager.has_positioning)
