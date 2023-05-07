from ctypes import c_double
import threading
import time
import utils

from simconnect.source import Source
from PySide6.QtGui import QStandardItemModel,QStandardItem

class Recorder():

    def __init__(self, src: Source,record_table:QStandardItemModel, parameters_to_record: list[str], rate: float = 1) -> None:
        super().__init__()
        self._src = src
        self._rate = rate
        self._record_table = record_table
        self._parameters_to_record = parameters_to_record
        self._stop_flag = False

        for param_name in self._parameters_to_record:
            if not(self._src.is_param_listened(param_name)):
                self._src.add_listened_parameter(param_name, utils.get_var_unit(param_name), c_double)

    def start(self):
        self._thread = threading.Thread(
            target=self.recorder_thread, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_flag = True
        
    def recorder_thread(self):
        while not (self._stop_flag):
            record = []
            for param in self._parameters_to_record:
                record.append(QStandardItem(str(self._src.get_param_value_from_name(param))))
            self._record_table.appendRow(record)
            time.sleep(self._rate)

