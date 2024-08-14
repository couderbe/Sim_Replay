from ctypes import c_double
from src.main.python.datas.datas_manager import FlightDatasManager
import unittest

from training.pattern_training_processor import Pattern, PatternStep, Runway, compute_init_direction, compute_init_position
from src.main.python.tools.geometry import Point3D
from airport_store import AIRPORT_SETTINGS


class PatternTrainingTest(unittest.TestCase):
    def test_compute_init_position(self):

        runway = Runway(Point3D(0.0, 45.0,400.0),Point3D(0.01,45.0,400.0))
        #runway = Runway(AIRPORT_SETTINGS["point0"],AIRPORT_SETTINGS["point1"])

        pattern = Pattern(runway,True, 0.6,0.6,700)

        res = compute_init_position(pattern, PatternStep.BASE, True)

        self.assertEqual(
            res.lat,
            45.01,
        )
        self.assertEqual(
            res.lon,
            -0.014142135623730949,
        )
        self.assertEqual(
            res.altitude,
            1100,
        )

    def test_compute_init_direction(self):
        runway = Runway(Point3D(0.0, 45.0,400.0),Point3D(0.01,45.0,400.0))

        pattern = Pattern(runway,True, 0.6,0.6,700)

        res = compute_init_direction(pattern, PatternStep.BASE, True)

        self.assertEqual(
            res,
            180,
        )

    
    def test_compute_init_direction_graulhet(self):
        runway = Runway(AIRPORT_SETTINGS["point0"],AIRPORT_SETTINGS["point1"])

        pattern = Pattern(runway,True, 0.6,0.6,700)

        res = compute_init_direction(pattern, PatternStep.BASE, True)

        self.assertEqual(
            res,
            186.020274259487,
        )

