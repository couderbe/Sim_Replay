import math
import threading

from simconnect.source import Source

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


class Mock(Source):

    def __init__(self) -> None:
        self._opened: bool = False
        self._listened_parameters: list[Mock_Value] = []

    def update(self) -> int:
        if not (self._opened):
            print("Mock is closed, killing thread")
            return -1
        for v in self._listened_parameters:
            if v.get_is_looped():
                v.set_value(v.value()+5/100*math.fabs(v.max_val-v.min_val))
                if v.value()>v.max_val:
                    v.set_value(v.min_val)
            else:
                v.set_value(v.value()+0.1)
        return 0

    def add_listened_parameter(self, mock_value:Mock_Value) -> None:
        """
        All parameters must exist and be consistent with SimConnect APÏ reference
        """

        # Considering no parameter is ever removed from _listened_parameters
        self._listened_parameters.append(mock_value)

    def open(self) -> int:
        print("Mock activated")
        self._opened = True
        return 0

    def is_opened(self) -> bool:
        return self._opened
    
    def close(self) -> None:
        # TO IMPLEMENT
        self._opened = False

    def get_all_param_values(self):
        return self._listened_parameters.copy()
        
    def get_param_value(self, name: str):
        """
        Shorter call
        """
        return self.get_param_value_from_name(name)

    def get_param_value_from_name(self, name: str):
        return self._get_param_from_name(name).value()

    def _get_param_from_name(self, name: str):
        return next((x for x in self._listened_parameters if (x.name==name)), None)
