import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt, QModelIndex
from src.main.python.gaugeschart import GaugesChart
from src.main.python.messages import *
from src.main.python.model.model import Model, ModelStatus
from src.main.python.linechart import LineChart
from src.main.python.record_window import RecordWindow
from src.main.python.ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._mainTableModel = QStandardItemModel(self)
        self._model = Model(self._mainTableModel)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen.setShortcut("Ctrl+O")
        self.ui.actionOpen.triggered.connect(self.open_dialog)

        self.ui.actionConnect_to_sim.triggered.connect(self.on_connect)
        self.ui.actionConnect_to_mock.triggered.connect(self.on_connect_mock)

        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave.triggered.connect(self.save_dialog)

        self.ui.actionStart_Recording.setShortcut("Ctrl+R")
        self.ui.actionStart_Recording.triggered.connect(self.record)

        self.ui.actionImport.setShortcut("Ctrl+I")
        self.ui.actionImport.triggered.connect(self.import_dialog)

        self.ui.actionView_Charts.triggered.connect(self.open_charts_window)

        self.ui.playPausePushButton.clicked.connect(self.play_pause)

        self.ui.mainTableView.setModel(self._model._mainTableModel)
        self.ui.mainTableView.clicked.connect(self.on_item_clicked)

        self.ui.horizontalSlider.setDisabled(True)
        self.reset_ui_record_number()

        self.ui.horizontalSlider.sliderPressed.connect(self.on_slider_pressed)
        self.ui.horizontalSlider.sliderMoved.connect(self.on_slider_moved)
        self.ui.horizontalSlider.sliderReleased.connect(self.on_slider_released)

        self._slider_dragging = False

    def on_slider_pressed(self):
        if self._model.has_timestamp():
            self._slider_dragging = True
            self._model.pause_playing()
        else:
            _ = QMessageBox.critical(
                self,
                PLAY_WITHOUT_TIMESTAMP_ERROR.title,
                PLAY_WITHOUT_TIMESTAMP_ERROR.message,
            )

    def on_slider_moved(self, val):
        self._model.move_to_player_record(val)
        self.ui.timeLabel.setText(
            str(val) + "/" + str(self._model._mainTableModel.rowCount())
        )

    def on_slider_released(self):
        self._slider_dragging = False
        if self._model.status == ModelStatus.PLAYING:
            self._model.start_playing()

    def play_pause(self) -> None:
        match self._model.status:
            case ModelStatus.PLAYING:
                self.stop_playing()
            case ModelStatus.RECORDING:
                _ = QMessageBox.critical(
                    self,
                    PLAY_DURING_RECORD_ERROR.title,
                    PLAY_DURING_RECORD_ERROR.message,
                )
            case ModelStatus.CONNECTED:
                if self._model.has_timestamp():
                    self.open_charts_gauges()
                    self._model.start_playing()
                    self.ui.playPausePushButton.setText("Stop")
                else:
                    _ = QMessageBox.critical(
                        self,
                        PLAY_WITHOUT_TIMESTAMP_ERROR.title,
                        PLAY_WITHOUT_TIMESTAMP_ERROR.message,
                    )
            case _:
                _ = QMessageBox.critical(
                    self, NOT_CONNECTED_SIM_ERROR.title, NOT_CONNECTED_SIM_ERROR.message
                )

    def record(self) -> None:
        match self._model.status:
            case ModelStatus.RECORDING:
                self._model.stop_record()
                self.ui.actionStart_Recording.setText("Start Recording")
                self.ui.horizontalSlider.setDisabled(False)
                self.ui.horizontalSlider.setMinimum(1)
                self.ui.horizontalSlider.setMaximum(
                    self._model._mainTableModel.rowCount()
                )
                self.change_ui_record_number(1)

            case ModelStatus.OFFLINE:
                _ = QMessageBox.critical(
                    self, NOT_CONNECTED_SIM_ERROR.title, NOT_CONNECTED_SIM_ERROR.message
                )
            case _:
                self.stop_playing()
                self.start_src_record()
                self.reset_ui_record_number()
                self.ui.horizontalSlider.setDisabled(True)

    def start_src_record(self):
        # TODO Allow user to choose which parameters to record
        # TODO Check that all parameters are listened by the sim

        # Reset Model

        if self._model._mainTableModel.rowCount() > 0:
            ret = QMessageBox.warning(
                self,
                DATA_LOST_WARNING.title,
                DATA_LOST_WARNING.message,
                QMessageBox.Yes | QMessageBox.No,
            )
            if ret == QMessageBox.No:
                return

        parameters_to_record = []

        self._record_window = RecordWindow(parent=self, f=Qt.WindowType.Dialog)
        self._record_window.accepted.connect(
            lambda data: parameters_to_record.extend([item["name"] for item in data])
        )
        self._record_window.exec()

        self._model.start_record(parameters_to_record)
        self.ui.actionStart_Recording.setText("Stop Recording")

    def on_connect(self) -> None:
        self.stop_playing()
        match self._model.status:
            case ModelStatus.OFFLINE:
                self._model.connect()
                if self._model.status == ModelStatus.CONNECTED:
                    self._model._player.record_changed.connect(
                        self.change_ui_record_number
                    )

                    self.ui.actionConnect_to_sim.setText("Disconnect from sim")
                    self.ui.actionConnect_to_mock.setDisabled(True)
                    self.ui.horizontalSlider.setDisabled(False)

            case _:
                self._model.disconnect()
                self.change_ui_record_number(1)
                self.ui.actionConnect_to_sim.setText("Connect to sim")
                self.ui.actionConnect_to_mock.setEnabled(True)
                self.ui.horizontalSlider.setDisabled(True)

    def on_connect_mock(self) -> None:
        self.stop_playing()
        match self._model.status:
            case ModelStatus.OFFLINE:
                self._model.connect_mock()
                self._model._player.record_changed.connect(self.change_ui_record_number)

                self.ui.actionConnect_to_mock.setText("Disconnect from mock")
                self.ui.horizontalSlider.setDisabled(False)
                self.ui.actionConnect_to_sim.setDisabled(True)
            case _:
                self._model.disconnect_mock()
                self.change_ui_record_number(1)
                self.ui.actionConnect_to_mock.setText("Connect to mock (Dev)")
                self.ui.actionConnect_to_sim.setEnabled(True)
                self.ui.horizontalSlider.setDisabled(True)

    def save_dialog(self) -> None:
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save record", "", "Csv files (*.csv);;All files (*.*)"
        )
        if fileName:
            self._model.save_file(fileName)

    def change_player_record(self, index: int):
        if self._model.status != ModelStatus.OFFLINE:
            self._model.move_to_player_record(index)
            self.change_ui_record_number(index + 1)

    def on_item_clicked(self, index: QModelIndex):
        if self._model.has_timestamp():
            self.change_player_record(index.row())
        else:
            _ = QMessageBox.critical(
                self,
                PLAY_WITHOUT_TIMESTAMP_ERROR.title,
                PLAY_WITHOUT_TIMESTAMP_ERROR.message,
            )

    def change_ui_record_number(self, rec: int):
        self.ui.timeLabel.setText(
            str(rec) + "/" + str(self._model._mainTableModel.rowCount())
        )
        if not self._slider_dragging:
            self.ui.horizontalSlider.setValue(rec)

    def reset_ui_record_number(self):
        self.ui.timeLabel.setText("X/X")
        self.ui.horizontalSlider.setValue(0)

    def open_dialog(self) -> None:
        """
        Manage file opening
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Csv files (*.csv);;All files (*.*)"
        )
        if fileName:
            self.stop_playing()
            self._model.load_file(fileName)
            # Set time label initial value
            self.ui.horizontalSlider.setMinimum(1)
            self.ui.horizontalSlider.setMaximum(self._model._mainTableModel.rowCount())
            self.change_ui_record_number(1)

    def import_dialog(self) -> None:
        """
        Manage file import
        """
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Import file", "", "gps files (*.gpx);;All files (*.*)"
        )
        if fileName:
            self.stop_playing()
            self._model.import_file(fileName)
            # Set time label initial value
            self.ui.horizontalSlider.setMinimum(1)
            self.ui.horizontalSlider.setMaximum(self._model._mainTableModel.rowCount())
            self.change_ui_record_number(1)

    def stop_playing(self):
        self._model.stop_playing()
        if self._model.status != ModelStatus.PLAYING:
            self.ui.playPausePushButton.setText("Play")

    def open_charts_window(self):
        """method that opens the Window that contains charts"""
        window2 = LineChart(self._mainTableModel, self)
        window2.show()
        window2.setGeometry(30, 30, 1720, 920)
    
    def open_charts_gauges(self):
        """method that opens the Window that contains gauges"""
        window_gauges = GaugesChart(self._model,self)
        window_gauges.show()
        window_gauges.setGeometry(30, 30, 1720, 920)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
