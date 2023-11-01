import csv
from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.importer import import_gpx_file_module
from src.main.python.file_managment import save_sr, open_sr
from src.main.python.player import Player
from src.main.python.recorder import Recorder
from src.main.python.simconnect.mock import Mock
from src.main.python.simconnect.simconnect import Sim
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from enum import Enum

class ModelStatus(Enum):
    OFFLINE = 0
    CONNECTED = 1
    RECORDING = 2
    PLAYING = 3


class Model:
    def __init__(self, mainTableModel: QStandardItemModel):
        self._sim = Sim()
        self.status = ModelStatus.OFFLINE

        self._mock = Mock()

        self._mainTableModel = mainTableModel

    def save_file(self, fileName):
        save_sr(fileName, self._mainTableModel)

    def open_file(self, fileName):
        self._mainTableModel.clear()
        open_sr(fileName, self._mainTableModel)
        FlightDatasManager.set_dataset_as_state()
        if self.status != ModelStatus.OFFLINE:
            self._player.reset()

    def start_playing(self):
        self._player.start()
        self._playing = True
        self.status = ModelStatus.PLAYING

    def pause_playing(self):
        self._player.pause()

    def stop_playing(self):
        if self.status == ModelStatus.PLAYING:
            self._player.stop()
            self._playing = False
            self.status = ModelStatus.CONNECTED

    def connect(self):
        if self._sim.open() == 0:
            self._sim.start()
            # Create a Player object that runs in another thread
            self._player = Player(self._sim, self._mainTableModel)
            self.status = ModelStatus.CONNECTED

    def disconnect(self):
        self._sim.close()
        self.status = ModelStatus.OFFLINE

    def connect_mock(self):
        if self._mock.open() == 0:
            self._mock.add_dataset(FlightDatasManager.current_dataset)
            self._mock.start()

            # Create a Player object that runs in another thread
            self._player = Player(self._mock, self._mainTableModel)
            self.status = ModelStatus.CONNECTED

    def disconnect_mock(self):
        self._mock.stop()
        self.status = ModelStatus.OFFLINE

    def start_record(self, _recorded_parameters:list):
        for param in _recorded_parameters:
            FlightDatasManager.add_data(param, None)
        parameters_to_record = FlightDatasManager.get_current_keys()

        # TODO : sync refresh with record table
        self._mainTableModel.clear()

        # Random row is added to allow header to be set
        self._mainTableModel.appendRow(
            [QStandardItem("a") for _ in range(len(parameters_to_record))]
        )
        for i, header in enumerate(parameters_to_record):
            self._mainTableModel.setHeaderData(i, Qt.Orientation.Horizontal, header)
        self._mainTableModel.removeRow(0)

        # Create a Recorder object that runs in another thread
        self._recorder = Recorder(
            self._sim if self._sim.is_opened() else self._mock,
            self._mainTableModel,
            parameters_to_record,
            0.1,
        )

        if self.status != ModelStatus.OFFLINE:
            self._player.reset()

        self.status = ModelStatus.RECORDING
        self._recorder.start()

    def stop_record(self):
        self._recorder.stop()
        self.status = ModelStatus.CONNECTED

    def move_to_player_record(self, index: int):
        self._player.go_to(index)

    def has_timestamp(self) -> bool:
        return FlightDatasManager.timestamp != None
