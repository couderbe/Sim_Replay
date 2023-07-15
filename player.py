import threading
import time
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QStandardItemModel
from simconnect.source import Source

class PlayerProxy(QObject):
    # TODO Consider that time may not be in seconds
    # Signal Emited when time change. The current time is sent as float in seconds
    time_changed = Signal(float)
    record_changed = Signal(int)
    
class Player():

    def __init__(self, src: Source, record_table:QStandardItemModel, parameters_to_play: list[str], time_column_id: int = 0) -> None:
        super().__init__()
        self._src = src
        self._record_table = record_table
        self._parameters_to_play = parameters_to_play
        self._time_column_id = time_column_id

        self._pause_flag = False
        self._stop_flag = False

        self._proxy = PlayerProxy()
        self.time_changed = self._proxy.time_changed
        self.record_changed = self._proxy.record_changed
        self.current_record = 0

    def player_thread(self):
        headers = [self._record_table.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._record_table.columnCount())]
        while not self._stop_flag:
            while self._pause_flag:
                time.sleep(1)
            for column, header in enumerate(headers):
                if header in self._parameters_to_play:
                    self._src.set_param_value_from_name(
                        header, float(self._record_table.item(self.current_record, column).data(Qt.ItemDataRole.DisplayRole)))
                if column == self._time_column_id:
                    self._current_time = float(self._record_table.item(
                        self.current_record, column).data(Qt.ItemDataRole.DisplayRole))
                    if self.current_record<self._record_table.rowCount()-1:
                        self._next_time = float(self._record_table.item(
                            self.current_record + 1, column).data(Qt.ItemDataRole.DisplayRole))
                    else:
                        self.stop()

            # TODO Consider time may not be in seconds
            self.time_changed.emit(self._current_time)
            self.record_changed.emit(self.current_record+1)
            
            self.current_record+=1
            time.sleep(self._next_time - self._current_time)

    def pause(self):
        self._pause_flag = True
    
    def start(self):
        self._pause_flag = False
        self._stop_flag = False
        if self.current_record >= self._record_table.rowCount()-1:
            self.current_record = 0

        if not hasattr(self, '_thread') or not self._thread.is_alive():
            self._thread = threading.Thread(
                target=self.player_thread, daemon=True)
            self._thread.start()

    def stop(self):
        self._stop_flag = True

    def go_to(self, rec: int):
        self.current_record = rec
