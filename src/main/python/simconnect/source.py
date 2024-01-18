
from abc import abstractmethod
from ctypes import _SimpleCData
from src.main.python.datas.datas_manager import FlightDataset

from src.main.python.simconnect.enums import SIMCONNECT_PERIOD

class Source:

    @abstractmethod
    def get_param_value_from_name(self, param: str):
        """Getter of a data with a specific name.
            Has to be implemented.

        Args:
            param (str): the name of the desired data

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("The method has to be implemented")
    
    @abstractmethod
    def set_param_value_from_name(self, name: str, value: float) -> None:
        """Setter of a data with a specific name.
           Has to be implemented.

        Args:
            name (str): the name of the data to be changed
            value (float): the value to be set

        Raises:
            NotImplementedError
        """        
        raise NotImplementedError("The method has to be implemented")
    
    def add_listened_parameter(self, name: str, unit: str, ctype: _SimpleCData, refresh_rate: SIMCONNECT_PERIOD, *args) -> None:
        """Add a new listened parameter."""
        raise NotImplementedError("The method has to be implemented")
    
    @abstractmethod
    def add_dataset(self, flight_dataset:FlightDataset):
        """Listen all parameters contained in a given dataset.

        Args:
            flight_dataset (FlightDataset): the dataset that contains parameters to be listened
        """
        raise NotImplementedError("The method has to be implemented")

    def is_param_listened(param_name):
        """Check if a parameter is listened."""
        raise NotImplementedError("The method has to be implemented")
