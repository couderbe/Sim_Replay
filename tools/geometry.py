
import math

DEG_2_RAD = math.pi/180

class Point:
    """Class that defines a geographic point with a latitude and a longitude in degrees"""

    def __init__(self, lon: float, lat: float):
        self.lon = lon
        self.lat = lat

    def spherical_to_carthesian(self, other):
        """Returns a tuple containing a relative displacement with carthesian X Y coordinates between two points 

        Args:
            other (Point): the point used as origin

        Returns:
            Tuple: 2 floats as XY relative position
        """
        return (math.cos((other.lat+self.lat)*DEG_2_RAD/2)*(self.lon-other.lon)*60, (self.lat-other.lat)*60)
    

class Point3D(Point):
    
    def __init__(self, lon: float, lat: float,altitude: float):
        super().__init__(lon, lat)
        self.altitude = altitude
    
    def spherical_to_carthesian(self, other):
        return (super().spherical_to_carthesian(other)+(self.altitude-other.altitude,))


def bound(x,m,M):
    return min(max(x,m),M)