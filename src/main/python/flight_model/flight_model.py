import math
from gpxpy.gpx import GPXTrackPoint

from src.main.python.tools.geometry import DEG_2_RAD, Point3D, bound

G = 9.81
NM_2_M = 1852

ROLL_RATE = 10

class Position:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z


class Attitude:
    
    def __init__(self,phi,theta,psi):
        self.phi = phi
        self.theta = theta
        self.psi = psi


def compute_attitude_from_gpx(previous_attitude:Attitude,previous_point:GPXTrackPoint,point:GPXTrackPoint):
    pt1 = Point3D(point.longitude,point.latitude,point.elevation)
    pt0 = Point3D(previous_point.longitude,previous_point.latitude,previous_point.elevation)
    rel_pos = pt1.spherical_to_carthesian(pt0)
    delta_t = point.time-previous_point.time
    return compute_attitude(previous_attitude,Position(0,0,0),Position(rel_pos[0],rel_pos[1],rel_pos[2]),delta_t)

def compute_attitude(previous_attitude:Attitude,previous_point:Position,point:Position,delta_t)->Attitude:
    heading = math.atan2(point.x-previous_point.x,point.y-previous_point.y)/DEG_2_RAD
    _d_y = math.sin((heading-previous_attitude.psi)*DEG_2_RAD)*math.hypot(point.x-previous_point.x,point.y-previous_point.y)*NM_2_M
    bank = bound(-math.atan2(2 * _d_y, G * math.pow(delta_t,2))/DEG_2_RAD,previous_attitude.phi-ROLL_RATE*delta_t,previous_attitude.phi+ROLL_RATE*delta_t)
    pitch = -(point.z-previous_point.z)*2.5
    return Attitude(bank,pitch,heading)

