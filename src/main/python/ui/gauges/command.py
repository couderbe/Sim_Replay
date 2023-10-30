from abc import abstractmethod

from src.main.python.simconnect.listener import Listener

class Emitter:
    
    def __init__(self) -> None:
        self._width = 300

    @abstractmethod
    def connect(listener:Listener)->None:
        """Connects the Emitter to a listener that will be trigered when a value is get.
            Has to be implemented.

        Args:
            listener : the listener that has to be called

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("The method has to be implemented")