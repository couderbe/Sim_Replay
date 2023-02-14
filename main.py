from simconnect.simconnect import Sim
from simconnect.mock import Mock,Mock_Value
from ctypes import c_double
import time
import threading

def sim_connect_thread(sim):
    while True:
        sim.update()
        time.sleep(0.1)
        print("Plane Altitude : {}".format(sim.get_param_value("Plane Altitude")))

def mocking_thread(mock):
    while True:
        mock.update()
        time.sleep(0.1)
        print("Mocked Plane Altitude : {}\r".format(mock.get_param_value("Mocked Plane Altitude")),end="")

if __name__ == "__main__":
    sim = Sim()
    if sim.open()==0:
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
    else:
        mock = Mock()
        mock.add_listened_parameter(Mock_Value("Mocked Plane Altitude","ft",1000,1000,2000))
        mock.open()
        mock_thread = threading.Thread(target=mocking_thread, args=(mock,), daemon=True)
        mock_thread.start()
        while True:
           time.sleep(5)