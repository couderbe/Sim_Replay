import math
from gpxpy.gpx import GPXTrackPoint

from tools.geometry import DEG_2_RAD, Point3D

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
    return compute_attitude(previous_attitude,Position(0,0,0),Position(rel_pos[0],rel_pos[1],rel_pos[2]))

def compute_attitude(previous_attitude:Attitude,previous_point:Position,point:Position)->Attitude:
    heading = math.atan2(point.x-previous_point.x,point.y-previous_point.y)/DEG_2_RAD
    bank = (heading-previous_attitude.psi)*2
    pitch = (point.z-previous_point.z)*0.1
    return Attitude(bank,pitch,heading)

