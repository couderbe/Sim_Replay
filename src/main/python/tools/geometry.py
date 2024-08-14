import math

DEG_2_RAD = math.pi / 180

NM_2_FEET = 1852 / 0.3048
FEET_2_M = 0.3048


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
        return (
            math.cos((other.lat + self.lat) * DEG_2_RAD / 2)
            * (self.lon - other.lon)
            * 60,
            (self.lat - other.lat) * 60,
        )

    def relevement(self, other):
        provi = self.spherical_to_carthesian(other)
        return math.atan2(provi[0], provi[1])

    def absolute_dist(self, other):
        provi = self.spherical_to_carthesian(other)
        return math.hypot(provi[0], provi[1])

    def add_distance(self, dist, track):
        self.lon += (
            dist / 60 * math.sin(track * DEG_2_RAD) / math.cos(self.lat * DEG_2_RAD)
        )
        self.lat += dist / 60 * math.cos(track * DEG_2_RAD)


class Point3D(Point):

    def __init__(self, lon: float, lat: float, altitude: float):
        super().__init__(lon, lat)
        self.altitude = altitude

    def spherical_to_carthesian(self, other):
        return super().spherical_to_carthesian(other) + (
            self.altitude - other.altitude,
        )

    def absolute_dist(self, other):
        return math.hypot(
            super().absolute_dist(other), (self.altitude - other.altitude) / NM_2_FEET
        )


def bound(x, m, M):
    return min(max(x, m), M)


def format_angle(angle):
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle
