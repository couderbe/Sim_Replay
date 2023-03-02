import time
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QStandardItemModel
from simconnect.simconnect import Sim


class Player(QObject):

    # TODO Consider that time may not be in seconds
    # Signal Emited when time change. The current time is sent as float in seconds
    time_changed = Signal(float)

    def __init__(self, sim: Sim, model: QStandardItemModel, parameters_to_play: list[str], time_column_id: int = 0) -> None:
        super().__init__()
        self._sim = sim
        self._model = model
        self._parameters_to_play = parameters_to_play
        self._time_column_id = time_column_id

        self._pause_flag = False
        self._stop_flag = False

    def task(self):
        headers = [self._model.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._model.columnCount())]
        for row in range(self._model.rowCount()):
            while self._pause_flag:
                time.sleep(1)
            if self._stop_flag:
                break
            for column, header in enumerate(headers):
                if header in self._parameters_to_play:
                    self._sim.set_param_value_from_name(
                        header, float(self._model.item(row, column).data(Qt.ItemDataRole.DisplayRole)))
                if column == self._time_column_id:
                    self._current_time = float(self._model.item(
                        row, column).data(Qt.ItemDataRole.DisplayRole))
                    self._next_time = float(self._model.item(
                        row + 1, column).data(Qt.ItemDataRole.DisplayRole))

            # TODO Consider time may not be in seconds
            self.time_changed.emit(self._current_time)
            time.sleep(self._next_time - self._current_time)

    def pause(self):
        self._pause_flag = True

    def stop(self):
        self._stop_flag = True
