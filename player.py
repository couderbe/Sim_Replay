import threading
import time
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QStandardItemModel
from record_table import RecordTable
from simconnect.simconnect import Sim

class PlayerProxy(QObject):
    # TODO Consider that time may not be in seconds
    # Signal Emited when time change. The current time is sent as float in seconds
    time_changed = Signal(float)
    
class Player():

    def __init__(self, sim: Sim, record_table:RecordTable, parameters_to_play: list[str], time_column_id: int = 0) -> None:
        super().__init__()
        self._sim = sim
        self._record_table = record_table
        self._parameters_to_play = parameters_to_play
        self._time_column_id = time_column_id

        self._pause_flag = False
        self._stop_flag = False

        self._proxy = PlayerProxy()
        self.time_changed = self._proxy.time_changed

    def player_thread(self):
        headers = self._record_table.header
        for row in range(self._record_table.rowCount()):
            while self._pause_flag:
                time.sleep(1)
            if self._stop_flag:
                break
            for column, header in enumerate(headers):
                if header in self._parameters_to_play:
                    self._sim.set_param_value_from_name(
                        header, float(self._record_table.item(row, column)))
                if column == self._time_column_id:
                    self._current_time = float(self._record_table.item(
                        row, column))
                    if row<self._record_table.rowCount()-1:
                        self._next_time = float(self._record_table.item(
                            row + 1, column))

            # TODO Consider time may not be in seconds
            self.time_changed.emit(self._current_time)
            time.sleep(self._next_time - self._current_time)

    def pause(self):
        self._pause_flag = True
    
    def start(self):
        self._thread = threading.Thread(
            target=self.player_thread, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_flag = True
