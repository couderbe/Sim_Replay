import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, QModelIndex
from main_window import Ui_MainWindow
import csv
from simconnect.simconnect import Sim
from simconnect.mock import Mock, Mock_Value
from ctypes import c_double
import time
import threading

from simconnect.simconnect import Sim


def sim_connect_thread(sim):
    while True:
        sim.update()
        time.sleep(0.1)
        print("Plane Altitude : {}".format(
            sim.get_param_value("Plane Altitude")))


def mocking_thread(mock):
    while True:
        mock.update()
        time.sleep(0.1)
        print("Mocked Plane Altitude : {}\r".format(
            mock.get_param_value("Mocked Plane Altitude")), end="")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._sim = Sim()

        self.ui.actionOpen.setShortcut('Ctrl+O')
        self.ui.actionOpen.triggered.connect(self.open_dialog)

        self.ui.actionConnect_to_sim.triggered.connect(self.connect)

        self.ui.actionSave.setShortcut('Crtl+S')
        self.ui.actionSave.triggered.connect(self.save_dialog)

        self._mainTableModel = QStandardItemModel(self)
        self.ui.mainTableView.setModel(self._mainTableModel)
        self.ui.mainTableView.clicked.connect(self.on_item_clicked)

    def connect(self) -> None:
        if not (self._sim.is_opened()):
            if self._sim.open() == 0:
                self._sim.add_listened_parameter(
                    "Plane Longitude", "degrees latitude", c_double)
                self._sim.add_listened_parameter(
                    "Plane Altitude", "feet", c_double)
                self._sim.add_listened_parameter(
                    "Plane Latitude", "degrees latitude", c_double)
                # deamon = True forces the thread to close when the parent is closed
                sim_thread = threading.Thread(
                    target=sim_connect_thread, args=(self._sim,), daemon=True)
                sim_thread.start()
                self.ui.actionConnect_to_sim.setText("Disconnect from sim")
        else:
            self.ui.actionConnect_to_sim.setText("Connect to sim")
            self._sim.close()

    def save_dialog(self) -> None:
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save record', '', 'Csv files (*.csv);;All files (*.*)')
        if fileName:
            with open(fileName, 'w') as csvfile:
                headers = [self._mainTableModel.headerData(i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(self._mainTableModel.columnCount())]
                writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=";",
                                    lineterminator="\n")
                writer.writeheader()
                # Optimization ?
                for row in range(self._mainTableModel.rowCount()):
                    row_data = {}
                    for column in range(self._mainTableModel.columnCount()):
                        row_data[headers[column]] = self._mainTableModel.data(self._mainTableModel.index(row, column))
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
