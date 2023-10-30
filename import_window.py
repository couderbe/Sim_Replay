from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox
from ui.import_window_ui import Ui_ImportWindow
from qt_user_roles import UserRoles
import os
import csv


class ImportWindow(QDialog):

    def __init__(self, parent: QWidget | None = ..., f: Qt.WindowType = ...) -> None:
        super().__init__(parent, f)
        self.ui = Ui_ImportWindow()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self._file_path = ""
        self._delimiter = ","
        self._openning_function = None

        self._tableModel = QStandardItemModel(self)

        self.ui.tableView.setModel(self._tableModel)
        self.ui.filePushButton.clicked.connect(self.choose_file)
        self.ui.fileLineEdit.editingFinished.connect(self.file_path_edited)
        self.ui.CSVRadioButton.toggled.connect(self.csv_toggled)
        self.ui.commaRadioButton.toggled.connect(self.comma_toggled)
        self.ui.tabulationRadioButton.toggled.connect(self.tabulation_toggled)
        self.ui.semiclonRadioButton.toggled.connect(self.semicolon_toggled)
        self.ui.spaceRadioButton.toggled.connect(self.space_toggled)


    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Import file', '', 'gps files (*.gpx);;csv files (*.csv);;All files (*.*)')
        if file_path:
            self.ui.fileLineEdit.setText(file_path)
            self.open_file(file_path)

    def file_path_edited(self):
        file_path = self.ui.fileLineEdit.text()
        if os.path.isfile(file_path):
            self.open_file(file_path)
        else:
            self.ui.fileLineEdit.setText(self._file_path)
            _ = QMessageBox.critical(
                        self, "Invalid File", "Selected file does not exist")

    def open_file(self, file_path):
            self._file_path = file_path
            match file_path.split(".")[-1]:
                case "gpx":
                    pass
                case "csv":
                    self._openning_function = self.open_csv
                    if not(self.ui.CSVRadioButton.isChecked()):
                        self.ui.CSVRadioButton.setChecked(True)
                    else:
                        self.open_csv()

    def csv_toggled(self):
        if self.ui.CSVRadioButton.isChecked():
            self.ui.GPXRadioButton.setChecked(False)
            self.open_csv()

    def gpx_toggled(self):
        if self.ui.GPXRadioButton.isChecked():
            self.ui.CSVRadioButton.setChecked(False)
            
    def comma_toggled(self):
        if self.ui.commaRadioButton.isChecked():
            self.ui.semiclonRadioButton.setChecked(False)
            self.ui.spaceRadioButton.setChecked(False)
            self.ui.tabulationRadioButton.setChecked(False)
            self._delimiter = ","
            self._openning_function()

    def semicolon_toggled(self):
        if self.ui.semiclonRadioButton.isChecked():
            self.ui.commaRadioButton.setChecked(False)
            self.ui.spaceRadioButton.setChecked(False)
            self.ui.tabulationRadioButton.setChecked(False)
            self._delimiter = ";"
            self._openning_function()

    def space_toggled(self):
        if self.ui.spaceRadioButton.isChecked():
            self.ui.semiclonRadioButton.setChecked(False)
            self.ui.commaRadioButton.setChecked(False)
            self.ui.tabulationRadioButton.setChecked(False)
            self._delimiter = " "
            self._openning_function()

    def tabulation_toggled(self):
        if self.ui.tabulationRadioButton.isChecked():
            self.ui.semiclonRadioButton.setChecked(False)
            self.ui.spaceRadioButton.setChecked(False)
            self.ui.commaRadioButton.setChecked(False)
            self._delimiter = "\t"
            self._openning_function()

    def open_csv(self):
        print("open csv")
        self._tableModel.clear()
        with open(self._file_path, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=self._delimiter, 
                                    lineterminator="\n")
                line_read = 0
                for row in reader:
                    items = [QStandardItem(field) for field in row]
                    self._tableModel.appendRow(items)
                    line_read += 1
                    if line_read >= 10:
                        break