from simconnect.simconnect import Sim
from ctypes import c_double
import time
import threading

def sim_connect_thread(sim):
    while True:
        sim.update()
        time.sleep(0.1)
        print(sim.get_param_value("Plane Altitude"))


if __name__ == "__main__":
    sim = Sim()
    sim.open()
    sim.add_listened_parameter("Plane Latitude","degrees latitude", c_double)
    sim.add_listened_parameter("Plane Longitude","degrees latitude", c_double)
    sim.add_listened_parameter("Plane Altitude","feet", c_double)
    # deamon = True forces the thread to close when the parent is closed
    sim_thread = threading.Thread(target=sim_connect_thread, args=(sim,), daemon=True)
    sim_thread.start()
    while True:
        time.sleep(5)
        print("Setting new altitude")
        print(sim.set_param_value_from_name("Plane Altitude", 5000))