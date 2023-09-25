import calendar
import math
import threading
import time

from ctypes import _SimpleCData
from src.main.python.flight_model.flight_model import FlightModel
from src.main.python.simconnect.listener import Listener
from src.main.python.ui.gauges.command import Emitter
from src.main.python.datas.datas_manager import FlightDataset
from src.main.python.simconnect.source import Source
from src.main.python.simconnect.structs import *
from src.main.python.simconnect.enums import *
from src.main.python.simconnect.consts import *

from PySide6.QtCore import Signal, QObject, Qt


class Mock_Value():
    def __init__(self, name: str, unit: str, val: float, min_val: float, max_val: float,is_loop=True) -> None:
        self.name = name
        self.unit = unit
        self.val = val
        self.min_val = min_val
        self.max_val = max_val
        self._is_loop = is_loop
        self._lock = threading.Lock()


    def value(self):
        return self.val

    def set_value(self, value):
        with self._lock:
            self.val = value

    def get_is_looped(self):
        return self._is_loop

    def __repr__(self) -> str:
        return str(self.__dict__)

class MockProxy(QObject):
    # Signal Emited when record changes. The current record is sent as integer
    mock_changed = Signal(dict)

class Mock(Source, Emitter, Listener):

    def __init__(self) -> None:
        self._opened: bool = False
        self._listened_parameters: list[Mock_Value] = []
        self._proxy = MockProxy()
        self.flight_model = FlightModel()
        self.command = {  "Aileron Position": 0,
                          "Elevator Position":  0,
                          "Rudder Position":0,
                          "General Eng Throttle Lever Position:1": 0
                        } 
        self.state = None

    def update(self) -> int:
        if not (self._opened):
            print("Mock is closed, killing thread")
            return -1
        for v in self._listened_parameters:
            if v.get_is_looped():
                new_v = v.value()+5/100*math.fabs(v.max_val-v.min_val)
                if new_v>v.max_val:
                    v.set_value(v.min_val)
                else:
                    v.set_value(new_v)
            else:
                v.set_value(v.value()+0.1)
        if self.command != None:
            self.flight_model.compute(self.command.get("Aileron Position"),
                                  self.command.get("Elevator Position"),
                                  self.command.get("General Eng Throttle Lever Position:1"))
        
            self.state = {
                "ZULU TIME": calendar.timegm(time.gmtime()),
                "Plane Latitude": 0.0,
                "Plane Longitude": 0.0,
                "Plane Altitude": self.flight_model.pos.z,
                "Plane Bank Degrees": self.flight_model.attitude.phi,
                "Plane Pitch Degrees":self.flight_model.attitude.theta,
                "Plane Heading Degrees True":self.flight_model.attitude.psi,

                "Aileron Position": self.command.get("Aileron Position"),
                "Elevator Position":  self.command.get("Elevator Position"),
                "Rudder Position": self.command.get("Rudder Position"),
                "General Eng Throttle Lever Position:1": self.command.get("General Eng Throttle Lever Position:1")
            }

            self._proxy.mock_changed.emit(self.state)
        #self._proxy.mock_changed.emit(self._listened_parameters)
        return 0
    
    def add_dataset(self, flight_dataset:FlightDataset):
        self.add_listened_parameter(
            "ZULU TIME", "s", None, None, 1, 1, 1000000, False)
        self.add_listened_parameter(
            "Plane Latitude", "°", None, None, 40, 40, 60)
        self.add_listened_parameter(
            "Plane Longitude", "°", None, None, 0, 0, 10)
        self.add_listened_parameter(
            "Plane Altitude", "ft", None, None, 1000, 1000, 2000)
        self.add_listened_parameter(
            "Plane Bank Degrees", "°", None, None, -60, -60, 60)
        self.add_listened_parameter(
            "Plane Pitch Degrees", "°", None, None, -20, -20, 20)
        self.add_listened_parameter(
            "Plane Heading Degrees True", "°", None, None, 10, 10, 355)

    def add_listened_parameter(self, name: str, unit: str, ctype: _SimpleCData, refresh_rate: SIMCONNECT_PERIOD = SIMCONNECT_PERIOD.SIMCONNECT_PERIOD_SECOND, *args) -> None:
        """
        All parameters must exist and be consistent with SimConnect API reference
        """
        # Considering no parameter is ever removed from _listened_parameters
        if len(args) < 3:
            args = (20, 0, 1000)
        self._listened_parameters.append(Mock_Value(name, unit, *args))

    def open(self) -> int:
        print("Mock activated")
        self._opened = True
        return 0

    def is_opened(self) -> bool:
        return self._opened
    
    def close(self) -> None:
        self._opened = False
        self._thread.join()

    def get_all_params(self):
        return self._listened_parameters.copy()
        
    def get_param_value(self, name: str):
        """
        Shorter call
        """
        return self.get_param_value_from_name(name)

    def get_param_value_from_name(self, name: str):
        return self.state.get(name)

    def _get_param_from_name(self, name: str):
        return next((x for x in self._listened_parameters if (x.name==name)), None)
    
    def set_param_value_from_name(self, name: str, value: float) -> None:
        if(name == "ZULU TIME"):
            print("\rmock has sent value : "+name +" with : "+ str(value))
        return

    def start(self):
        self._thread = threading.Thread(
        target=self._mocking_thread, daemon=True)
        self._thread.start()
    
    def stop(self):
        self.close()
   
    def _mocking_thread(self):
        mock_opened = 0
        while mock_opened>=0:
            mock_opened = self.update()
            time.sleep(0.1)

    def is_param_listened(self, name:str):
        return name in [param.name for param in self._listened_parameters]

    def connect(self, listener:Listener):
        self._proxy.mock_changed.connect(listener.apply)
    
    def apply(self, params:dict):
        self.command.update(params)