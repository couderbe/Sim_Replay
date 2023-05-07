import json
from typing import Any, List, Sequence
from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex, Qt, QMimeData, Signal
from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtCore import QAbstractListModel
from ui.record_window_ui import Ui_RecordWindow
from qt_user_roles import UserRoles


class RecordWindow(QDialog):

    VARS_FILE_PATH = "data\\vars.json"

    accepted = Signal(list)

    def __init__(self, parent: QWidget | None = ..., f: Qt.WindowType = ...) -> None:
        super().__init__(parent, f)
        self.ui = Ui_RecordWindow()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.load_avalaible_vars()

        self._availableListModel = RecorderListModel(self.vars, self)
        self._recordedListModel = RecorderListModel([], self)
        self.ui.avalaibleListView.setModel(self._availableListModel)
        self.ui.recordedListView.setModel(self._recordedListModel)

        self.ui.addButton.clicked.connect(self.add_recorded_value)
        self.ui.removeButton.clicked.connect(self.remove_recorded_value)
        self.ui.avalaibleListView.doubleClicked.connect(
            self.add_recorded_value)
        self.ui.recordedListView.doubleClicked.connect(
            self.remove_recorded_value)

    def accept(self) -> None:
        self.setResult(QDialog.Accepted)
        self.hide()
        self.accepted.emit(self._recordedListModel._data)

    def load_avalaible_vars(self) -> None:
        """Loads available variables for recording from vars json file 
        """
        with open(self.VARS_FILE_PATH, "r") as f:
            self.vars = json.loads(f.read())

    def add_recorded_value(self) -> None:
        """Moves the selected variables in availableListView to recordedListView
        """
        selected_indexes = [QPersistentModelIndex(
            index) for index in self.ui.avalaibleListView.selectedIndexes()]
        for index in selected_indexes:
            if self._recordedListModel.insertRow(0):
                if self._recordedListModel.setData(self._recordedListModel.index(0), self._availableListModel.data(index, UserRoles.RAW.value), UserRoles.RAW.value):
                    self._availableListModel.removeRow(index.row())

    def remove_recorded_value(self) -> None:
        """Moves the selected variables in recordedListView to availableListView
        """
        selected_indexes = [QPersistentModelIndex(
            index) for index in self.ui.recordedListView.selectedIndexes()]
        for index in selected_indexes:
            if self._availableListModel.insertRow(0):
                if self._availableListModel.setData(self._availableListModel.index(0), self._recordedListModel.data(index, UserRoles.RAW.value), UserRoles.RAW.value):
                    self._recordedListModel.removeRow(index.row())


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
                case UserRoles.RAW.value:
                    return self._data[index.row()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if index.isValid(): # i.e item of the listView
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled
        else: # i.e listView itself
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDropEnabled

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
                case UserRoles.RAW.value:
                    self._data[index.row()] = value
                    return True
        return False

    def supportedDragActions(self) -> Qt.DropAction:
        return Qt.DropAction.MoveAction

    def supportedDropActions(self) -> Qt.DropAction:
        return Qt.DropAction.MoveAction

    def mimeTypes(self) -> List[str]:
        return ["application/json"]

    def mimeData(self, indexes: Sequence[QModelIndex]) -> QMimeData:
        mimeData = QMimeData()
        mimeData.setData("application/json", json.dumps(
            [index.data(int(UserRoles.RAW.value)) for index in indexes]).encode())
        return mimeData

    def dropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: QModelIndex | QPersistentModelIndex) -> bool:
        # If list is empty dropped row value is -1
        if row == -1:
            row = 0
        items = json.loads(data.data("application/json").data().decode())
        self.insertRows(row, len(items), parent)
        for i, item in enumerate(items):
            self.setData(self.index(i + row), item, UserRoles.RAW.value)
        return True
