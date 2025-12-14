import threading
import time
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QStandardItemModel
from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.simconnect.source import Source


class PlayerProxy(QObject):
    # Signal Emited when record changes. The current record is sent as integer
    record_changed = Signal(int)


class Player():

    def __init__(self, src: Source, record_table: QStandardItemModel) -> None:
        super().__init__()
        self._src = src
        self._record_table = record_table

        self._pause_flag = False
        self._stop_flag = False

        self._proxy = PlayerProxy()
        self.record_changed = self._proxy.record_changed
        self.current_record = 0

        self._interpolated = True

    def player_thread(self):
        self.headers = [self._record_table.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._record_table.columnCount())]
        while not self._stop_flag:
            while self._pause_flag:
                time.sleep(1)
                
            self.move_to_current_record()            
            
            if not self._interpolated:
                time.sleep(self._next_time - self._current_time)
            else:
                current_time_interpol = self._current_time
                while(self._next_time - self._current_time > 0) and not self._stop_flag:
                    computer_timeref = time.time_ns()
                    time.sleep(0.001) # Freqency must be caped ortherwise Simconnect seems unable to manage
                    self.interpolated_move(current_time_interpol, self._current_time, self._next_time)
                    self._current_time = self._current_time + (time.time_ns() - computer_timeref)*10**-9



    def move_to_current_record(self):
        for column, header in enumerate([self._record_table.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._record_table.columnCount())]):
            self._src.set_param_value_from_name(
                header, float(self._record_table.item(self.current_record, column).data(Qt.ItemDataRole.DisplayRole)))
            if header == FlightDatasManager.timestamp:
                self._current_time = float(self._record_table.item(
                    self.current_record, column).data(Qt.ItemDataRole.DisplayRole))
                if self.current_record < self._record_table.rowCount()-1:
                    self._next_time = float(self._record_table.item(
                        self.current_record + 1, column).data(Qt.ItemDataRole.DisplayRole))
                else:
                    self.stop()
        self.current_record += 1

        self.record_changed.emit(self.current_record)

    def interpolated_move(self, previous_time, current_time, next_time):
        for column, header in enumerate([self._record_table.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._record_table.columnCount())]):

            # Linear interpolation
            previous_value = float(self._record_table.item(self.current_record, column).data(Qt.ItemDataRole.DisplayRole))
            next_value = float(self._record_table.item(self.current_record + 1, column).data(Qt.ItemDataRole.DisplayRole))
            current_value = previous_value + ((next_value - previous_value)/(next_time - previous_time))*(current_time - previous_time)
            self._src.set_param_value_from_name(header, float(current_value))

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
        self.move_to_current_record()
    
    def reset(self):
        self.current_record = 0
