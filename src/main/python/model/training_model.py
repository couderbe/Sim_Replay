from src.main.python.simconnect.listener import Listener

from src.main.python.model.model import Model, ModelStatus
from src.main.python.ui.gauges.command import Emitter

class TrainingModel:

    def __init__(self,_model:Model) -> None:
        self.model = _model


    def connect_view(self, listener:Listener):
        if self.model.status != ModelStatus.OFFLINE:
            self.model._sim.connect(listener)