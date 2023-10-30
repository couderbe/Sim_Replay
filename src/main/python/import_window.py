import csv
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QWidget

from src.main.python.tools.gpx_interpolate import gpx_read
from src.main.python.importer import *
from src.main.python.ui.import_window_ui import Ui_ImportWindow
from src.main.python.model.model import Model


class ImportWindow(QDialog):

    PREVIEW_ITEM_COUNT = 10

    def __init__(self, target_table_model: Model, parent: QWidget | None = ..., f: Qt.WindowType = ...) -> None:
        super().__init__(parent, f)
        self.ui = Ui_ImportWindow()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.fileFormatGroup.setEnabled(False)
        self.ui.configurationGroup.setEnabled(False)
        self.ui.parametersDefinitionGroup.setEnabled(False)
        self.ui.dataEnhancementGroup.setEnabled(False)

        self._target_table_model = target_table_model._mainTableModel
        self._file_path = ""
        self._delimiter = ","
        self._openning_function = lambda: None

        self._tableModel = QStandardItemModel(self)
        self._parameters_fieldname_choices = QStandardItemModel(self)

        self.ui.tableView.setModel(self._tableModel)
        self.ui.timeComboBox.setModel(self._parameters_fieldname_choices)
        self.ui.longitudeComboBox.setModel(self._parameters_fieldname_choices)
        self.ui.latitudeComboBox.setModel(self._parameters_fieldname_choices)
        self.ui.altitudeComboBox.setModel(self._parameters_fieldname_choices)
        self.ui.headingComboBox.setModel(self._parameters_fieldname_choices)
        self.ui.bankComboBox.setModel(self._parameters_fieldname_choices)
        self.ui.pitchComboBox.setModel(self._parameters_fieldname_choices)

        self.ui.filePushButton.clicked.connect(self.choose_file)
        self.ui.fileLineEdit.editingFinished.connect(self.file_path_edited)
        self.ui.CSVRadioButton.toggled.connect(self.csv_toggled)
        self.ui.GPXRadioButton.toggled.connect(self.gpx_toggled)
        self.ui.commaRadioButton.toggled.connect(self.comma_toggled)
        self.ui.tabulationRadioButton.toggled.connect(self.tabulation_toggled)
        self.ui.semiclonRadioButton.toggled.connect(self.semicolon_toggled)
        self.ui.spaceRadioButton.toggled.connect(self.space_toggled)
        self.ui.ligneIgnoreSpinBox.valueChanged.connect(
            self.ligne_ignore_changed)
        self.ui.importButton.clicked.connect(self.finish_import)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.columnFirstLineCheckBox.stateChanged.connect(
            lambda x: self._openning_function())

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Import file', '', 'gps files (*.gpx);;csv files (*.csv);;All files (*.*)')
        if file_path:
            self.ui.fileLineEdit.setText(file_path)
            self.ui.fileFormatGroup.setEnabled(True)
            self.open_file(file_path)

    def file_path_edited(self):
        file_path = self.ui.fileLineEdit.text()
        if os.path.isfile(file_path):
            self.open_file(file_path)
            self.ui.fileFormatGroup.setEnabled(True)
        else:
            self.ui.fileLineEdit.setText(self._file_path)
            _ = QMessageBox.critical(
                self, "Invalid File", "Selected file does not exist")

    def open_file(self, file_path: str):
        self._file_path = file_path
        match file_path.split(".")[-1]:
            case "gpx":
                self._openning_function = self.update_preview_gpx
                if not (self.ui.GPXRadioButton.isChecked()):
                    self.ui.GPXRadioButton.setChecked(True)
                else:
                    self.update_preview_gpx()
            case "csv":
                self._openning_function = self.update_preview_csv
                if not (self.ui.CSVRadioButton.isChecked()):
                    self.ui.CSVRadioButton.setChecked(True)
                else:
                    self.update_preview_csv()

    def csv_toggled(self):
        if self.ui.CSVRadioButton.isChecked():
            self.ui.GPXRadioButton.setChecked(False)
            self._openning_function = self.update_preview_csv
            self.update_preview_csv()
            self.ui.configurationGroup.setEnabled(True)
            self.ui.parametersDefinitionGroup.setEnabled(True)
            self.ui.dataEnhancementGroup.setEnabled(True)

    def gpx_toggled(self):
        if self.ui.GPXRadioButton.isChecked():
            self.ui.CSVRadioButton.setChecked(False)
            self._openning_function = self.update_preview_gpx
            self.update_preview_gpx()
            self.ui.configurationGroup.setEnabled(False)
            self.ui.parametersDefinitionGroup.setEnabled(False)
            self.ui.dataEnhancementGroup.setEnabled(True)

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

    def ligne_ignore_changed(self):
        self._openning_function()

    def update_preview_csv(self):
        self.csv_to_model(self._tableModel, self.PREVIEW_ITEM_COUNT)
        self.update_parameters_fieldname_choices()

    def update_preview_gpx(self):
        self._tableModel.clear()
        if self.ui.interpolationCheckBox.isChecked():
            #TODO : To be implemented
            pass
        else:
            gpx_datas = gpx_read(self._file_path)
        import_gpx_file(self._tableModel, self._file_path, limit=self.PREVIEW_ITEM_COUNT)

    def update_parameters_fieldname_choices(self):
        self._parameters_fieldname_choices.clear()
        headers = [self._tableModel.horizontalHeaderItem(
            i) for i in range(self._tableModel.columnCount())]
        self._parameters_fieldname_choices.appendColumn(headers)

    def csv_to_model(self, model: QStandardItemModel, nbr_line: int = -1):
        model.clear()
        with open(self._file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=self._delimiter,
                                lineterminator="\n")

            line_read = 1

            headers = reader.__next__()
            if not (self.ui.columnFirstLineCheckBox.isChecked()):
                model.appendRow([QStandardItem(field) for field in headers])
                headers = [f"field_{i}" for i in range(len(headers))]
            else:
                line_read = 0

            for i in range(self.ui.ligneIgnoreSpinBox.value()):
                reader.__next__()
            for row in reader:
                items = [QStandardItem(field) for field in row]
                model.appendRow(items)
                if nbr_line > 0:
                    line_read += 1
                    if line_read >= nbr_line:
                        break

            for i, header in enumerate(headers):
                self._tableModel.setHeaderData(
                    i, Qt.Orientation.Horizontal, header)

    def finish_import(self):
        # Checks of compatibility of the main parameters shall be performed before any import
        if self.ui.CSVRadioButton.isChecked():
            self.csv_to_model(self._target_table_model)
            self._target_table_model.setHorizontalHeaderItem(
                self.ui.timeComboBox.currentIndex(), QStandardItem("ZULU TIME"))
            self._target_table_model.setHorizontalHeaderItem(
                self.ui.longitudeComboBox.currentIndex(), QStandardItem("Plane Longitude"))
            self._target_table_model.setHorizontalHeaderItem(
                self.ui.latitudeComboBox.currentIndex(), QStandardItem("Plane Latitude"))
            self._target_table_model.setHorizontalHeaderItem(
                self.ui.altitudeComboBox.currentIndex(), QStandardItem("Plane Altitude"))
        elif self.ui.GPXRadioButton.isChecked():
            import_gpx_file_module(self._target_table_model, self._file_path)
        self.close()
