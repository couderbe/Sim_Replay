from abc import ABC, abstractmethod


class Gauge(ABC):
    
    @abstractmethod
    def updateValues(val:dict)->None:
        pass