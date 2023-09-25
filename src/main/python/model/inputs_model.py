from PySide6.QtCore import Qt
from src.main.python.simconnect.listener import Listener

from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.model.model import Model, ModelStatus
from src.main.python.ui.gauges.command import Emitter

class InputsModel:

    def __init__(self,_model:Model) -> None:
        self.model = _model


    def connect_view(self, listener:Listener):
        if self.model.status != ModelStatus.OFFLINE:
            self.model._mock.connect(listener)
    
    def connect_input(self, emitter:Emitter):
        emitter.connect(self.model._mock)
