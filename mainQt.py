import sys
import csv
import time
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QModelIndex, QThread
from main_window import Ui_MainWindow
from player import Player
from record_table import ListenableRecordTable
from recorder import Recorder
from simconnect.simconnect import Sim
from simconnect.mock import Mock, Mock_Value
from ctypes import c_double

from simconnect.source import Source

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._sim = Sim()
        self._recording = False
        self._playing = False

        self._mock = Mock()

        self._time_column_id = None
        
        self.ui.actionOpen.setShortcut('Ctrl+O')
        self.ui.actionOpen.triggered.connect(self.open_dialog)

        self.ui.actionConnect_to_sim.triggered.connect(self.connect)
        self.ui.actionConnect_to_mock.triggered.connect(self.connect_mock)


        self.ui.actionSave.setShortcut('Ctrl+S')
        self.ui.actionSave.triggered.connect(self.save_dialog)

        self.ui.actionStart_Recording.setShortcut('Ctrl+R')
        self.ui.actionStart_Recording.triggered.connect(self.record)

        self.ui.playPausePushButton.clicked.connect(self.play_pause)

        self._mainTableModel = QStandardItemModel(self)
        self.ui.mainTableView.setModel(self._mainTableModel)
        self.ui.mainTableView.clicked.connect(self.on_item_clicked)

        self._record_table = ListenableRecordTable([])

    def play_pause(self) -> None:
        if self._playing:
            self._player.stop()
            self._playing = False
            self.ui.playPausePushButton.setText("Play")
        else:
            if self._sim.is_opened():
                if not (self._recording):
                    # TODO Allow user to choose which parameters to record
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
                        self._sim,self._record_table, parameters_to_play)
                    self._player.time_changed.connect(self.set_time)
                    self._player.start()
                    self._playing = True
                    self.ui.playPausePushButton.setText("Stop")
                else:
                    _ = QMessageBox.critical(
                        self, "Cannot play while recording", "You cannot play a record while recording")
            else:
                _ = QMessageBox.critical(
                    self, "Not connected to the sim", "You must be connected to the sim before playing a record")

    def record(self) -> None:
        if self._recording:
            self._recorder.stop()
          #  self._recorder_thread.exit(0)
          #  self._recorder_thread.wait()
            self._recording = False
            self.ui.actionStart_Recording.setText("Start Recording")
        else:
            if self._sim.is_opened():   
                self.start_src_record(self._sim)

            elif self._mock.is_opened():
                self.start_src_record(self._mock)
            else:
                _ = QMessageBox.critical(
                    self, "Not connected to the sim/mock", "You must be connected to the sim or the mock before recording")

    def start_src_record(self,src:Source):
        # TODO Allow user to choose which parameters to record
        # TODO Check that all parameters are listened by the sim

        # Reset Model
       
        if self._mainTableModel.rowCount() > 0:
            ret = QMessageBox.warning(self, "Warning",
                                    "You are going to start recording. All the current data will be lost\n"
                                    "Do you want to continue ?",
                                    QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                return

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

        self._record_table.set_record_header(parameters_to_record)

        # Create a Recorder object that runs in another thread
        self._recorder = Recorder(
                    src, self._record_table,parameters_to_record, 1)

        self._record_table._proxy.resized.connect(self.add_record)
        self._recorder.start() 
        self._recording = True
        self.ui.actionStart_Recording.setText("Stop Recording")

    
    def add_record(self, record: list[str]):
        self._mainTableModel.appendRow([QStandardItem(elt) for elt in record])

    def connect(self) -> None:
        if not (self._sim.is_opened()):
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
                self.ui.actionConnect_to_sim.setText("Disconnect from sim")
                self.ui.actionConnect_to_mock.setDisabled(True)

        else:
            self.ui.actionConnect_to_sim.setText("Connect to sim")
            self.ui.actionConnect_to_mock.setEnabled(True)
            self._sim.close()

    def connect_mock(self) -> None:
        if not (self._mock.is_opened()):
            if self._mock.open() == 0:
                self._mock.add_listened_parameter(Mock_Value("ZULU TIME","s",1,1,1000000,False))
                self._mock.add_listened_parameter(Mock_Value("Plane Latitude","°",40,40,60))
                self._mock.add_listened_parameter(Mock_Value("Plane Longitude","°",0,0,10))
                self._mock.add_listened_parameter(Mock_Value("Plane Altitude","ft",1000,1000,2000))
                self._mock.add_listened_parameter(Mock_Value("Plane Bank Degrees","°",-60,-60,60))
                self._mock.add_listened_parameter(Mock_Value("Plane Pitch Degrees","°",-20,-20,20))
                self._mock.add_listened_parameter(Mock_Value("Plane Heading Degrees True","°",10,10,355))
                # deamon = True forces the thread to close when the parent is closed
                self._mock.start()
                self.ui.actionConnect_to_mock.setText("Disconnect from mock")
                self.ui.actionConnect_to_sim.setDisabled(True)
        else:
            self.ui.actionConnect_to_mock.setText("Connect to mock (Dev)")
            self.ui.actionConnect_to_sim.setEnabled(True)
            self._mock.stop()

    def save_dialog(self) -> None:
        fileName, _ = QFileDialog.getSaveFileName(
            self, 'Save record', '', 'Csv files (*.csv);;All files (*.*)')
        if fileName:
            with open(fileName, 'w') as csvfile:
                headers = [self._mainTableModel.headerData(
                    i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._mainTableModel.columnCount())]
                writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=";",
                                        lineterminator="\n")
                writer.writeheader()
                # Optimization ?
                for row in range(self._mainTableModel.rowCount()):
                    row_data = {}
                    for column in range(self._mainTableModel.columnCount()):
                        row_data[headers[column]] = self._mainTableModel.data(
                            self._mainTableModel.index(row, column))
                    writer.writerow(row_data)

    def on_item_clicked(self, index: QModelIndex):
        if self._time_column_id != None:
            self.set_time(index.siblingAtColumn(self._time_column_id).data())

    def set_time(self, time: str | int | float):
        self.ui.timeLabel.setText(str(time))

    def open_dialog(self) -> None:
        """
        Manage file opening
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Csv files (*.csv);;All files (*.*)')
        if fileName:
            self._mainTableModel.clear()
            # TODO : sync View with RecordTable
            with open(fileName, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=";",
                                    lineterminator="\n")
                headers = reader.__next__()
                self._record_table.header=headers
                for row in reader:
                    items = [QStandardItem(field) for field in row]
                    self._mainTableModel.appendRow(items)
                    self._record_table.addRow([float(field) for field in row])
                for i, header in enumerate(headers):
                    self._mainTableModel.setHeaderData(
                        i, Qt.Orientation.Horizontal, header)
                    
                    if header == "ZULU TIME":
                        self._time_column_id = i
            # Set time label initial value
            self.ui.timeLabel.setText(
                self._mainTableModel.item(0, self._time_column_id).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
