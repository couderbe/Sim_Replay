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
        """Custom ListModel for the record window

        Args:
            data (list[dict]): Initial data to be stored in the model. Each dict in the list shall have name and description keys defined.
            parent (QObject | None, optional): Parent Object. Defaults to ....
        """
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = ...) -> int:
        """Return the number of rows in the model

        Args:
            parent (QModelIndex | QPersistentModelIndex, optional): parent. Defaults to ....

        Returns:
            int: row count
        """
        return len(self._data)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.DisplayRole) -> Any:
        """Returns the model data at given index for a given row

        Args:
            index (QModelIndex | QPersistentModelIndex): index
            role (int, optional): Qtrole. Defaults to Qt.DisplayRole.

        Returns:
            Any: data
        """
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
        """Return itemflag for the given index. An item of the listview can be dragged but it is not possible to drop an item on it whereas the listView itself can be dropped on but not dragged

        Args:
            index (QModelIndex | QPersistentModelIndex): index

        Returns:
            Qt.ItemFlag: flags
        """
        if index.isValid():  # i.e item of the listView
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled
        else:  # i.e listView itself
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDropEnabled

    def removeRows(self, row: int, count: int, parent: QModelIndex | QPersistentModelIndex = ...) -> bool:
        """Remove count of rows from row

        Args:
            row (int): row to start deletion from
            count (int): number of rows to delete
            parent (QModelIndex | QPersistentModelIndex, optional): parent. Defaults to ....

        Returns:
            bool: True if the operation is succesful. False otherwise
        """
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(row, row + count):
            self._data.pop(i)
        self.endRemoveRows()
        return True

    def insertRows(self, row: int, count: int, parent: QModelIndex | QPersistentModelIndex = ...) -> bool:
        """Insert count of rows from row

        Args:
            row (int): row to start insertion from
            count (int): number of rows to add
            parent (QModelIndex | QPersistentModelIndex, optional): parent. Defaults to ....

        Returns:
            bool: True if the operation is succesful. False otherwise
        """
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(row, row + count):
            self._data.insert(i, {})
        self.endInsertRows()
        return True

    def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = ...) -> bool:
        """Set raw data at given index.

        Args:
            index (QModelIndex | QPersistentModelIndex): index
            value (Any): value to save
            role (int, optional): role Defaults to ....

        Returns:
            bool: True if the operation is succesful. False otherwise
        """
        if index.isValid():
            match role:
                case UserRoles.RAW.value:
                    self._data[index.row()] = value
                    return True
        return False

    def supportedDragActions(self) -> Qt.DropAction:
        """Set drag to move action

        Returns:
            Qt.DropAction: 
        """
        return Qt.DropAction.MoveAction

    def supportedDropActions(self) -> Qt.DropAction:
        """Set drop to move action

        Returns:
            Qt.DropAction: 
        """
        return Qt.DropAction.MoveAction

    def mimeTypes(self) -> List[str]:
        """json is the only supported mimetype from drag and drop actions.

        Returns:
            List[str]: 
        """
        return ["application/json"]

    def mimeData(self, indexes: Sequence[QModelIndex]) -> QMimeData:
        """Encode the raw data of the indexes into json

        Args:
            indexes (Sequence[QModelIndex]): indexes to encode

        Returns:
            QMimeData: encoded indexes' data
        """
        mimeData = QMimeData()
        mimeData.setData("application/json", json.dumps(
            [index.data(int(UserRoles.RAW.value)) for index in indexes]).encode())
        return mimeData

    def dropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: QModelIndex | QPersistentModelIndex) -> bool:
        """Decode dropped elements and add them to the model. New rows are created at the drop position. If the list is empty the dropped position is manually set to 0.

        Args:
            data (QMimeData): dropped data
            action (Qt.DropAction): action
            row (int): row position of the drop action
            column (int): column position of the drop action. Unused in this model type.
            parent (QModelIndex | QPersistentModelIndex): parent

        Returns:
            bool: True if the operation is succesful. False otherwise
        """
        # If list is empty dropped row value is -1
        if row == -1:
            row = 0
        items = json.loads(data.data("application/json").data().decode())
        self.insertRows(row, len(items), parent)
        for i, item in enumerate(items):
            self.setData(self.index(i + row), item, UserRoles.RAW.value)
        return True
