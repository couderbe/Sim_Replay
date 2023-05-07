import json
from typing import Any, Union
from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QAbstractListModel
from ui.record_window_ui import Ui_RecordWindow
from qt_user_roles import UserRoles


class RecordWindow(QWidget):

    VARS_FILE_PATH = "data\\vars.json"

    def __init__(self):
        super(RecordWindow, self).__init__()
        self.ui = Ui_RecordWindow()
        self.ui.setupUi(self)

        self.load_avalaible_vars()

        self._availableListModel = RecorderListModel(self.vars, self)
        self._recordedListModel = RecorderListModel([], self)
        self.ui.avalaibleListView.setModel(self._availableListModel)
        self.ui.recordedListView.setModel(self._recordedListModel)

        self.ui.addButton.clicked.connect(self.add_recorded_value)
        self.ui.removeButton.clicked.connect(self.remove_recorded_value)

    def load_avalaible_vars(self) -> None:
        """Loads available variables for recording from vars json file 
        """
        with open(self.VARS_FILE_PATH, "r") as f:
            self.vars = json.loads(f.read())

    def add_recorded_value(self) -> bool:
        for index in self.ui.avalaibleListView.selectedIndexes():
            if self._recordedListModel.insertRow(0):
                if self._recordedListModel.setData(self._recordedListModel.index(0), self._availableListModel.data(index, UserRoles.RAW), UserRoles.RAW):
                    return self._availableListModel.removeRow(index.row())
        return False

    def remove_recorded_value(self) -> bool:
        for index in self.ui.recordedListView.selectedIndexes():
            if self._availableListModel.insertRow(0):
                if self._availableListModel.setData(self._availableListModel.index(0), self._recordedListModel.data(index, UserRoles.RAW), UserRoles.RAW):
                    return self._recordedListModel.removeRow(index.row())
        return False


class RecorderListModel(QAbstractListModel):
    def __init__(self, data: list[dict], parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = ...) -> int:
        return len(self._data)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.DisplayRole) -> str:
        if index.isValid():
            match role:
                case Qt.DisplayRole:
                    return str(self._data[index.row()]['name'])
                case Qt.ToolTipRole:
                    return str(self._data[index.row()]['description'])
                case UserRoles.RAW:
                    return self._data[index.row()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        return super().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: QModelIndex | QPersistentModelIndex = ...) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(row, row + count):
            self._data.pop(i)
        self.endRemoveRows()
        return True

    def insertRows(self, row: int, count: int, parent: QModelIndex | QPersistentModelIndex = ...) -> bool:
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(row, row + count):
            self._data.insert(i, {})
        self.endInsertRows()
        return True

    def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = ...) -> bool:
        if index.isValid():
            match role:
                case UserRoles.RAW:
                    self._data[index.row()] = value
                    return True
        return False
