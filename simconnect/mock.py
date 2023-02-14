import threading

class Mock_Value():
    def __init__(self, name: str, unit: str, val: float, min_val: float, max_val: float) -> None:
        self.name = name
        self.unit = unit
        self.val = val
        self.min_val = min_val
        self.max_val = max_val
        self._lock = threading.Lock()

    def value(self):
        return self.val

    def set_value(self, value):
        with self._lock:
            self.val = value

    def __repr__(self) -> str:
        return str(self.__dict__)


class Mock():

    def __init__(self) -> None:
        self._opened: bool = False
        self._listened_parameters: list[Mock_Value] = []

    def update(self) -> None:
        if not (self._opened):
            print("(Mock) Open communication before updating")
            return
        for v in self._listened_parameters:
            v.set_value(v.value()+5)
            if v.value()>v.max_val:
                v.set_value(v.min_val)
        

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

    def close(self) -> None:
        # TO IMPLEMENT
        self._opened = False

    def get_param_value(self, name: str):
        """
        Shorter call
        """
        return self.get_param_value_from_name(name)

    def get_param_value_from_name(self, name: str):
        return self._get_param_from_name(name).value()

    def _get_param_from_name(self, name: str):
        return next((x for x in self._listened_parameters if (x.name==name)), None)
