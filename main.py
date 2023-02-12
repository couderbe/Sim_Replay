from simconnect.simconnect import Sim
from ctypes import c_double
import time

if __name__ == "__main__":
    sim = Sim()
    sim.open()
    sim.add_listened_parameter("Plane Latitude","degrees latitude", c_double)
    sim.add_listened_parameter("Plane Longitude","degrees latitude", c_double)
    sim.add_listened_parameter("Plane Altitude","feet", c_double)
    while True:
        sim.update()
        time.sleep(0.1)
        print(sim.get_param("Plane Altitude"))