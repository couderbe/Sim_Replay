
import math

DEG_2_RAD = math.pi/180

class Point:
    def __init__(self, lat:float, lon:float):
        self.lat = lat
        self.lon = lon

    def spherical_to_carthesian(self,other):
        return (math.cos((other.lat+self.lat)*DEG_2_RAD/2)*(other.lon-self.lon)*60,(other.lat-self.lat)*60)