

import csv
from ctypes import c_double
from src.main.python.importer import import_gpx_file_module
from src.main.python.outputs import save_datas
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
    def __init__(self,mainTableModel:QStandardItemModel):
        self._sim = Sim()
        self.status = ModelStatus.OFFLINE
        self._recording = False
        self._playing = False

        self._mock = Mock()

        self._time_column_id = None  
        self._mainTableModel = mainTableModel
    
    def load_file(self,fileName):
        self._mainTableModel.clear()
            # TODO : sync View with RecordTable
        with open(fileName, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=";",
                                lineterminator="\n")
            headers = reader.__next__()
            for row in reader:
                items = [QStandardItem(field) for field in row]
                self._mainTableModel.appendRow(items)
            for i, header in enumerate(headers):
                self._mainTableModel.setHeaderData(
                    i, Qt.Orientation.Horizontal, header)

                if header == "ZULU TIME":
                    self._time_column_id = i

    def save_file(self, fileName):
        save_datas(fileName, self._mainTableModel)

    def import_file(self, fileName):
        self._mainTableModel.clear()
        import_gpx_file_module(self._mainTableModel, fileName)
        self._time_column_id = 0

    def start_playing(self):
        self._player.start()
        self._playing = True
        self.status = ModelStatus.PLAYING

    def pause_playing(self):
        self._player.pause()


    def stop_playing(self):
        if self.status==ModelStatus.PLAYING:
            self._player.stop()
            self._playing = False
            self.status = ModelStatus.CONNECTED

    def connect(self):
        if self._sim.open() == 0:
            self._sim.add_listened_parameter(
                "Plane Longitude", "degrees latitude", c_double)
            self._sim.add_listened_parameter(
                "Plane Altitude", "feet", c_double)
            self._sim.add_listened_parameter(
                "Plane Latitude", "degrees latitude", c_double)
            self._sim.add_listened_parameter(
                "ZULU TIME", "seconds", c_double)
            self._sim.add_listened_parameter(
                "Plane Bank Degrees", "degrees", c_double)
            self._sim.add_listened_parameter(
                "Plane Pitch Degrees", "degrees", c_double)
            self._sim.add_listened_parameter(
                "Plane Heading Degrees True", "degrees", c_double)
            # deamon = True forces the thread to close when the parent is closed
            self._sim.start()

            # TODO Check that all parameters are registered by the sim
            parameters_to_play = [
                "ZULU TIME",
                "Plane Longitude",
                "Plane Latitude",
                "Plane Altitude",
                "Plane Bank Degrees",
                "Plane Pitch Degrees",
                "Plane Heading Degrees True"]

            # Create a Player object that runs in another thread
            self._player = Player(
                self._sim, self._mainTableModel, parameters_to_play)
            self.status = ModelStatus.CONNECTED
    
    def disconnect(self):
        self._sim.close()
        self.status = ModelStatus.OFFLINE


    def connect_mock(self):
        if self._mock.open() == 0:
            self._mock.add_listened_parameter(
                "ZULU TIME", "s", None, None, 1, 1, 1000000, False)
            self._mock.add_listened_parameter(
                "Plane Latitude", "°", None, None, 40, 40, 60)
            self._mock.add_listened_parameter(
                "Plane Longitude", "°", None, None, 0, 0, 10)
            self._mock.add_listened_parameter(
                "Plane Altitude", "ft", None, None, 1000, 1000, 2000)
            self._mock.add_listened_parameter(
                "Plane Bank Degrees", "°", None, None, -60, -60, 60)
            self._mock.add_listened_parameter(
                "Plane Pitch Degrees", "°", None, None, -20, -20, 20)
            self._mock.add_listened_parameter(
                "Plane Heading Degrees True", "°", None, None, 10, 10, 355)
            self._mock.start()

            # TODO Check that all parameters are registered by the sim
            parameters_to_play = [
                "ZULU TIME",
                "Plane Longitude",
                "Plane Latitude",
                "Plane Altitude",
                "Plane Bank Degrees",
                "Plane Pitch Degrees",
                "Plane Heading Degrees True"]

            # Create a Player object that runs in another thread
            self._player = Player(
                self._mock, self._mainTableModel, parameters_to_play)
            self.status = ModelStatus.CONNECTED

    def disconnect_mock(self):
        self._mock.stop()
        self.status = ModelStatus.OFFLINE


    def start_record(self):

        parameters_to_record = [
            "ZULU TIME",
            "Plane Longitude",
            "Plane Latitude",
            "Plane Altitude",
            "Plane Bank Degrees",
            "Plane Pitch Degrees",
            "Plane Heading Degrees True"]
        
        # TODO : sync refresh with record table
        self._mainTableModel.clear()

        # Random row is added to allow header to be set
        self._mainTableModel.appendRow(
            [QStandardItem("a") for _ in range(len(parameters_to_record))])
        for i, header in enumerate(parameters_to_record):
            self._mainTableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)
        self._mainTableModel.removeRow(0)

        # Create a Recorder object that runs in another thread
        self._recorder = Recorder(
            self._sim if self._sim.is_opened() else self._mock, self._mainTableModel, parameters_to_record, 0.1)

        self.status = ModelStatus.RECORDING
        self._recorder.start()
        self._recording = True

    def stop_record(self):
        self._recorder.stop()
        self._recording = False
        self._time_column_id = 0
        self.status = ModelStatus.CONNECTED

    def move_to_player_record(self,index: int):
        self._player.go_to(index)
