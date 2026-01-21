import logging
import os
import threading

from ctypes import *
from ctypes import _SimpleCData
from ctypes.wintypes import HANDLE, DWORD
from typing import Any
import time
from src.main.python.datas.datas_manager import FlightDataset
from src.main.python.simconnect.source import Source
from src.main.python.simconnect.structs import *
from src.main.python.simconnect.enums import *
from src.main.python.simconnect.consts import *

logger = logging.getLogger(__name__)

class Parameter():
    def __init__(self, name: str, unit: str, ctype: _SimpleCData, refresh_rate: SIMCONNECT_PERIOD, define_id: int, request_id: int) -> None:
        self.name = name
        self.unit = unit
        self.ctype = ctype
        self.refresh_rate = refresh_rate
        self.define_id = define_id
        self.request_id = request_id
        self._last_value = None
        self._lock = threading.Lock()

    def value(self):
        return self._last_value

    def set_value(self, value):
        with self._lock:
            self._last_value = value

    def __repr__(self) -> str:
        return str(self.__dict__)

class Sim(Source):

    def __init__(self, dll_path: str = "./SimConnect.dll") -> None:
        """
        Constructor for Sim object
        
        :param self:
        :param dll_path: Path for Simconnect dll file (default "SimConnect.dll" in executable folder)
        :type dll_path: str
        """
        super().__init__()
        if os.path.exists(dll_path):
            self._simconnect = WinDLL(dll_path)
        else:
            self._simconnect = None
            logger.warning("The SimConnect.dll file is missing, connection to Flight Simulator won't be possible")
        self._hSimConnect = HANDLE(None) 
        self._opened: bool = False
        self._listened_parameters: list[Parameter] = []
        self._dispatch_proc = self._get_disptach_proc()

    def _update(self) -> int:
        """
        Updates the values of the listened parameters using Dispatch Proc. This function should be called internally by a dedicated Thread created with start function. 
        
        :param self
        :return: Error code
        :rtype: int
        """
        if not (self._opened):
            logger.info("User should open communication before update function can be called")
            return -1
        err = self._simconnect.SimConnect_CallDispatch(
            self._hSimConnect, self._dispatch_proc, c_void_p(0))

        if err != 0:
            logger.error(f"Unable to CallDispatch ErrorCode {err:#x}")
            return 1
        return 0
    
    def add_dataset(self, flight_dataset:FlightDataset) -> None:
        """
        Adds all parameters from the dataset with default `refresh_rate` to the listened parameters.  
        
        :param self:
        :param flight_dataset: Dataset to be added
        :type flight_dataset: FlightDataset
        """
        for param in flight_dataset.set.items():
            self.add_listened_parameter(
                param[0], param[1]["unit"], param[1]["type"])

    def add_listened_parameter(self, name: str, unit: str, ctype: _SimpleCData, refresh_rate: SIMCONNECT_PERIOD = SIMCONNECT_PERIOD.SIMCONNECT_PERIOD_SIM_FRAME) -> None:
        """
        Creates a parameter based on inputed definition. This parameter is automatically added to the listened parameters list and inputed to the sim server for data update at :param:`refresh_rate`.
        This parameter definition shall exist and be consistent with SimConnect API reference. 

        :param self:
        :param name: Name of the parameter
        :type name: str
        :param unit: Unit of the parameter
        :type unit: str
        :param ctype: C type of the parameter
        :type ctype: _SimpleCData
        :param refresh_rate: How often should the server send an updated value of the parameters, defaults to `SIMCONNECT_PERIOD_SIM_FRAME`
        :type refresh_rate: SIMCONNECT_PERIOD
        
        """

        # Considering no parameter is ever removed from _listened_parameters
        define_id = len(self._listened_parameters)
        # Considering one request is made for each parameter
        request_id = define_id

        if not (self._opened):
            logger.info("Open communication before adding listened parameter")
            return

        err = self._simconnect.SimConnect_AddToDataDefinition(self._hSimConnect, define_id,
                                                              name.encode("utf-8"), unit.encode("utf-8"), 4, c_float(0), DWORD(0xfffffffff))
        if err != 0:
            logger.error(f"Unable to AddToDataDefinition ErrorCode{err}")
            return
        err = self._simconnect.SimConnect_RequestDataOnSimObject(self._hSimConnect, request_id, define_id, SIMCONNECT_OBJECT_ID_USER,
                                                                 refresh_rate.value, DWORD(0), DWORD(0), DWORD(0), DWORD(0))
        if err != 0:
            logger.error(f"Unable to RequestDataOnSimObject ErrorCode{err}")
            return

        self._listened_parameters.append(
            Parameter(name, unit, ctype, refresh_rate, define_id, request_id))
        logger.info(f"Parameter {name} is now listened by simconnect")

    def open(self) -> int:
        """
        Open communication with the simulation. This function shall be called before any communication with the simulation is attempted. 
        
        :param self:
        :return: Success or error code
        :rtype: int
        """
        if self._simconnect==None:
            logger.error("Simconnect dll was not initilized. Most likely the file was not found.")
            return 1
        err = self._simconnect.SimConnect_Open(
            byref(self._hSimConnect), b"Sim Replay", None, 0, 0, 0)
        if err != 0:
            logger.error(f"Unexpected error while openning the communication with the simulation. Error code:{err}")
            return err
        logger.info("Connected to the simulation")
        self._opened = True
        return 0

    def close(self) -> None:
        """
        Close communication with the simulation. 
        
        :param self:
        """
        # TODO : test the method
        self._simconnect.SimConnect_Close(self._hSimConnect)
        self._opened = False

    def get_all_params(self) -> list[Parameter]:
        """
        Returns the list of listened `Parameter` by the simulation.
        
        :param self:
        :return: List of listened parameters
        :rtype: list[Parameter]
        """
        return self._listened_parameters.copy()
    
    def is_opened(self) -> bool:
        """
        Returns `True` if the communication with the sim is opened
        
        :param self:
        :return: `True` if the communication with the sim is opened. `False` otherwise.
        :rtype: bool
        """
        return self._opened

    def get_param_value(self, name: str) -> Any:
        """
        Shorter call for :func:`get_param_value_from_name`.
        
        :param self:
        :param name: Parameter `name`
        :type name: str
        :return: Parameter value
        :rtype: Any
        """
        
        return self.get_param_value_from_name(name)

    def get_param_value_from_name(self, name: str) -> Any:
        """
        Returns the value of the parameter.
        
        :param self:
        :param name: Parameter `name`
        :type name: str
        :return: Parameter value
        :rtype: Any
        """
        return self._get_param_from_name(name).value()
    
    def is_param_listened(self, name:str) -> bool:
        """
        Returns whether the parameter is listened.
        
        :param self:
        :param name: Parameter `name`
        :type name: str
        :return: `True` if the parameter is listened. `False` otherwise.
        :rtype: bool
        """
        return name in [param.name for param in self._listened_parameters]

    def _get_param_from_name(self, name: str):
        """
        Gets `Parameter` object from name from tht listened parameters list. Returns `None` if no matching parameter is found.
        
        :param self:
        :param name: Parameter name
        :type name: str
        :return: Found parameter. `None` if no matching parameter is found. 
        :rtype: Parameter
        """
        for param in self._listened_parameters:
            if param.name == name:
                return param
        return None

    def set_param_value_from_name(self, name: str, value: Any) -> None:
        """
        Set parameter value if name found in listened parameter list. `value` type must be consistent with target parameter.
        
        :param self:
        :param name: Name of the parameter
        :type name: str
        :param value: Value to be set on the parameter. Type must be consistent with target parameter.
        :type value: Any
        """
        if (param := self._get_param_from_name(name)) == None:
            logger.info("Parameter must be listened before being settable")
            return None
        else:
            self._simconnect.SimConnect_SetDataOnSimObject(self._hSimConnect, param.define_id, SIMCONNECT_OBJECT_ID_USER, 0,0, sizeof(param.ctype), byref(param.ctype(value)))

    def _get_disptach_proc(self):
        """
        Instead of using my_disptach_proc in SimConnect_CallDispatch it is needed to create a function to allow accessing self in the callback.
        """
        @WINFUNCTYPE(None, POINTER(SIMCONNECT_RECV), c_ulong, c_void_p)
        def my_dispatch_proc(pData: SIMCONNECT_RECV, cbData, pContext):
            match pData.contents.dwID:
                case SIMCONNECT_RECV_ID.SIMCONNECT_RECV_ID_SIMOBJECT_DATA.value:
                    pObjData = cast(pData, POINTER(
                        SIMCONNECT_RECV_SIMOBJECT_DATA))
                    # Access parameter using DefinedID or RequestID is equivalent as they are always the same in the current implementation
                    param = self._listened_parameters[pObjData.contents.dwDefineID]
                    param.set_value(cast(pObjData.contents.dwData,
                                            POINTER(param.ctype)).contents.value)
                case SIMCONNECT_RECV_ID.SIMCONNECT_RECV_ID_QUIT.value:
                    logger.info("Sim has just closed")
                    self._opened = False
            return 0

        return my_dispatch_proc
    
    def start(self):
        """
        Starts a new thread which calls the :func:`update` function every 0.01s until :func:`stop` function is called. 
        
        :param self
        """
        self._thread = threading.Thread(
        target=self._sim_connect_thread, daemon=True)
        self._thread.start()
    
    def stop(self):
        """
        Stops simulation update thread.
        
        :param self:
        """
        self.close()
        self._thread.join()

    def _sim_connect_thread(self):
        sim_opened = 0
        while sim_opened>=0:
            sim_opened = self._update()
            time.sleep(0.01)