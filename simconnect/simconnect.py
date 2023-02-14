import threading

from ctypes import *
from ctypes import _SimpleCData
from ctypes.wintypes import HANDLE, DWORD
from simconnect.structs import *
from simconnect.enums import *
from simconnect.consts import *

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

class Sim():

    def __init__(self, dll_path: str = "./SimConnect.dll") -> None:
        self._simconnect = WinDLL(dll_path)
        self._hSimConnect = HANDLE(None)
        self._opened: bool = False
        self._listened_parameters: list[Parameter] = []

    def update(self) -> None:
        if not (self._opened):
            print("Open communication before updating")
            return
        err = self._simconnect.SimConnect_CallDispatch(
            self._hSimConnect, self._get_disptach_proc(), None)

        if err != 0:
            print(f"Unable to CallDispatch ErrorCode{err}")
            return

    def add_listened_parameter(self, name: str, unit: str, ctype: _SimpleCData, refresh_rate: SIMCONNECT_PERIOD = SIMCONNECT_PERIOD.SIMCONNECT_PERIOD_SECOND) -> None:
        """
        All parameters must exist and be consistent with SimConnect APÏ reference
        """

        # Considering no parameter is ever removed from _listened_parameters
        define_id = len(self._listened_parameters)
        # Considering one request is made for each parameter
        request_id = define_id

        if not (self._opened):
            print("Open communication before adding listened parameter")
            return

        err = self._simconnect.SimConnect_AddToDataDefinition(self._hSimConnect, define_id,
                                                              name.encode("utf-8"), unit.encode("utf-8"), 4, c_float(0), DWORD(0xfffffffff))
        if err != 0:
            print(f"Unable to AddToDataDefinition ErrorCode{err}")
            return
        err = self._simconnect.SimConnect_RequestDataOnSimObject(self._hSimConnect, request_id, define_id, SIMCONNECT_OBJECT_ID_USER,
                                                                 refresh_rate.value, DWORD(0), DWORD(0), DWORD(0), DWORD(0))
        if err != 0:
            print(f"Unable to RequestDataOnSimObject ErrorCode{err}")
            return

        self._listened_parameters.append(
            Parameter(name, unit, ctype, refresh_rate, define_id, request_id))

    def open(self) -> int:
        err = self._simconnect.SimConnect_Open(
            byref(self._hSimConnect), b"Sim Replay", None, 0, 0, 0)
        if err != 0:
            print("Error connecting to the simulation")
            return err
        print("Connected to simulation")
        self._opened = True
        return 0

    def close(self) -> None:
        # TODO : test the method
        self._hSimConnect.SimConnect_Close(self._hSimConnect)
        self._opened = False

    def get_param_value(self, name: str):
        """
        Shorter call
        """
        return self.get_param_value_from_name(name)

    def get_param_value_from_name(self, name: str):
        return self._get_param_from_name(name).value()

    def _get_param_from_name(self, name: str):
        for param in self._listened_parameters:
            if param.name == name:
                return param.value()
        return None

    def _get_param_from_name(self, name: str) -> Parameter:
        for param in self._listened_parameters:
            if param.name == name:
                return param
        return None

    def set_param_value_from_name(self, name: str, value) -> None:
        if (param := self._get_param_from_name(name)) == None:
            print("Parameter must be listened before being settable")
            return None
        else:
            self._simconnect.SimConnect_SetDataOnSimObject(self._hSimConnect, param.define_id, SIMCONNECT_OBJECT_ID_USER, 0,0, sizeof(param.ctype), byref(param.ctype(value)))

    def _get_disptach_proc(self):
        """
        Instead of using my_disptach_proc in SimConnect_CallDispatch it is needed to create a function to allow accessing self in the callback.
        Performance cost of creating a function at every callback must be assessed.
        TO TEST: Create call _get_dispatch_proc only once. Store it in class variable and use this class variable in update.
        """
        @WINFUNCTYPE(None, POINTER(SIMCONNECT_RECV), DWORD, c_void_p)
        def my_dispatch_proc(pData: SIMCONNECT_RECV, cbData, pContext):
            # print(pData.contents.dwID)
            # print(cbData)
            # print(pContext)
            match pData.contents.dwID:
                case SIMCONNECT_RECV_ID.SIMCONNECT_RECV_ID_SIMOBJECT_DATA.value:
                    pObjData = cast(pData, POINTER(
                        SIMCONNECT_RECV_SIMOBJECT_DATA))
                    # print(f"RequetsID {pObjData.contents.dwRequestID}")
                    # How does ObjectID parameter work ?
                    # print(f"ObjectID {pObjData.contents.dwObjectID}")
                    # print(f"DefineID {pObjData.contents.dwDefineID}")
                    # Access parameter using DefinedID or RequestID is equivalent as they are always the same in the current implementation
                    param = self._listened_parameters[pObjData.contents.dwDefineID]
                    print(cast(pObjData.contents.dwData,
                          POINTER(param.ctype)).contents.value)
                    param.set_value(cast(pObjData.contents.dwData,
                                            POINTER(param.ctype)).contents.value)
                case SIMCONNECT_RECV_ID.SIMCONNECT_RECV_ID_QUIT.value:
                    print("Sim has just closed")
                    self._opened = False
            return 0

        return my_dispatch_proc