import sys
import csv
import time
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QModelIndex, QThread
from main_window import Ui_MainWindow
from recorder import Recorder
from simconnect.simconnect import Sim
from ctypes import c_double

from simconnect.simconnect import Sim


def sim_connect_thread(sim):
    while True:
        sim.update()
        time.sleep(0.1)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._sim = Sim()
        self._recording = False

        self.ui.actionOpen.setShortcut('Ctrl+O')
        self.ui.actionOpen.triggered.connect(self.open_dialog)

        self.ui.actionConnect_to_sim.triggered.connect(self.connect)

        self.ui.actionSave.setShortcut('Ctrl+S')
        self.ui.actionSave.triggered.connect(self.save_dialog)

        self.ui.actionStart_Recording.setShortcut('Ctrl+R')
        self.ui.actionStart_Recording.triggered.connect(self.record)

        self._mainTableModel = QStandardItemModel(self)
        self.ui.mainTableView.setModel(self._mainTableModel)
        self.ui.mainTableView.clicked.connect(self.on_item_clicked)

    def record(self) -> None:
        if self._recording:
            self._recorder.stop()
            self._recorder_thread.exit(0)
            self._recorder_thread.wait()
            self._recording = False
            self.ui.actionStart_Recording.setText("Start Recording")
        else:
            if self._sim.is_opened():
                # TODO Allow user to choose which parameters to record
                # TODO Check that all parameters are listened by the sim
                parameters_to_record = [
                    "ZULU TIME", "Plane Longitude", "Plane Latitude", "Plane Altitude"]

                # Random row is added to allow header to be set
                self._mainTableModel.appendRow(
                    [QStandardItem("a") for _ in range(len(parameters_to_record))])
                for i, header in enumerate(parameters_to_record):
                    self._mainTableModel.setHeaderData(
                        i, Qt.Orientation.Horizontal, header)
                self._mainTableModel.removeRow(0)

                # Create a Recorder object that runs in another thread
                self._recorder_thread = QThread()
                self._recorder = Recorder(
                    self._sim, parameters_to_record, 0.01)
                self._recorder.moveToThread(self._recorder_thread)
                self._recorder_thread.started.connect(self._recorder.task)
                self._recorder.new_record.connect(self.add_record)
                self._recorder_thread.start()
                self._recording = True
                self.ui.actionStart_Recording.setText("Stop Recording")
            else:
                _ = QMessageBox.critical(
                    self, "Not connected to the sim", "You must be connected to the sim before recording")

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

                # deamon = True forces the thread to close when the parent is closed
                sim_thread = threading.Thread(
                    target=sim_connect_thread, args=(self._sim,), daemon=True)
                sim_thread.start()
                self.ui.actionConnect_to_sim.setText("Disconnect from sim")
        else:
            self.ui.actionConnect_to_sim.setText("Connect to sim")
            self._sim.close()

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
        self.ui.timeLabel.setText(
            str(index.siblingAtColumn(self._time_column_id).data()))

    def open_dialog(self) -> None:
        """
        Manage file opening
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Csv files (*.csv);;All files (*.*)')
        if fileName:
            self._mainTableModel.clear()
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
                    if header == "time":
                        self._time_column_id = i
            # Set time label initial value
            self.ui.timeLabel.setText(
                self._mainTableModel.item(0, self._time_column_id).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
