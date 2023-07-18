
import math

DEG_2_RAD = math.pi/180

class Point:
    """Class that defines a geographic point with a latitude and a longitude in degrees"""

    def __init__(self, lon: float, lat: float):
        self.lon = lon
        self.lat = lat

    def spherical_to_carthesian(self, other):
        """method that returns the position in the cartesian referential of an other Point relative to the inital Point in nm"""
        return (math.cos((other.lat+self.lat)*DEG_2_RAD/2)*(self.lon-other.lon)*60, (self.lat-other.lat)*60)
