import time
from PySide6.QtCore import Signal, QObject
from simconnect.simconnect import Sim


class Recorder(QObject):

    new_record = Signal(list)

    def __init__(self, sim: Sim, parameters_to_record: list[str], rate: float = 1) -> None:
        super().__init__()
        self._sim = sim
        self._rate = rate
        self._parameters_to_record = parameters_to_record
        self._stop_flag = False

    def task(self):
        while not (self._stop_flag):
            record = []
            for param in self._parameters_to_record:
                record.append(str(self._sim.get_param_value_from_name(param)))
            self.new_record.emit(record)
            time.sleep(self._rate)

    def stop(self):
        self._stop_flag = True
