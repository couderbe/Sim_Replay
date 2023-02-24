from simconnect.simconnect import Sim
from simconnect.mock import Mock,Mock_Value
from ctypes import c_double
import time
import threading

def sim_connect_thread(sim:Sim):
    sim_opened = 0
    while sim_opened >= 0 :
        sim_opened = sim.update()
        time.sleep(0.1)
        print("------------------------------")
        for param_value in sim.get_all_param_values():
            print("Sim {} : {} {}\n".format(param_value.name, param_value.value(),param_value.unit),end="")
        print("------------------------------")
    return

def mocking_thread(mock:Mock):
    while True:
        mock.update()
        time.sleep(0.2)
        print("------------------------------")
        for param_value in mock.get_all_param_values():
            print("Mocked {} : {} {}\n".format(param_value.name, param_value.val,param_value.unit),end="")
        print("------------------------------")

if __name__ == "__main__":
    sim = Sim()
    if sim.open()==0:
        sim.add_listened_parameter("Plane Latitude","degrees latitude", c_double)
        sim.add_listened_parameter("Plane Longitude","degrees latitude", c_double)
        sim.add_listened_parameter("Plane Altitude","feet", c_double)
        sim.add_listened_parameter("Plane Bank Degrees","degrees",c_double)
        sim.add_listened_parameter("Plane Pitch Degrees","degrees",c_double)
        sim.add_listened_parameter("Plane Heading Degrees True","degrees",c_double)
        
        # deamon = True forces the thread to close when the parent is closed
        sim_thread = threading.Thread(target=sim_connect_thread, args=(sim,), daemon=True)
        sim_thread.start()
        while True:
            time.sleep(5)
            print("Setting new altitude")
            print(sim.set_param_value_from_name("Plane Altitude", 5000))
    else:
        mock = Mock()
        mock.add_listened_parameter(Mock_Value("Plane Latitude","°",40,40,60))
        mock.add_listened_parameter(Mock_Value("Plane Longitude","°",0,0,10))
        mock.add_listened_parameter(Mock_Value("Plane Altitude","ft",1000,1000,2000))
        mock.add_listened_parameter(Mock_Value("Plane Bank Degrees","°",-60,-60,60))
        mock.add_listened_parameter(Mock_Value("Plane Pitch Degrees","°",-20,-20,20))
        mock.add_listened_parameter(Mock_Value("Plane Heading Degrees True","°",10,10,355))
        mock.open()
        mock_thread = threading.Thread(target=mocking_thread, args=(mock,), daemon=True)
        mock_thread.start()
        while True:
           time.sleep(5)