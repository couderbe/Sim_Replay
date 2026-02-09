from enum import Enum
from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.interpoler import Interpoler
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt


class InterpolationType(Enum):
    LINEAR = 0
    CUBIC = 0


class FunctionalInterpoler(Interpoler):

    def __init__(self, type: InterpolationType, model: QStandardItemModel):
        super().__init__()
        self._type = type
        self._model = model
        self.index = 0
        self.start_time = 0.0
        self.end_time = 0.0
        self.update_bounds(0)

    def compute_interpolation(
        self, index: int, current_time: float
    ) -> dict:
        if index != self.index:
            self.update_bounds(index)
        match self._type:
            case InterpolationType.LINEAR:
                current_value = {}
                for column, header in enumerate(
                    [
                        self._model.headerData(
                            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
                        )
                        for i in range(self._model.columnCount())
                    ]
                ):

                    # Linear interpolation
                    previous_value = float(
                        self._model.item(self.index, column).data(
                            Qt.ItemDataRole.DisplayRole
                        )
                    )
                    next_value = float(
                        self._model.item(self.index + 1, column).data(
                            Qt.ItemDataRole.DisplayRole
                        )
                    )
                    current_value[header] = previous_value + (
                        (next_value - previous_value) / (self.end_time - self.start_time)
                    ) * (current_time - self.start_time)
                return current_value
            case _:
                raise NotImplementedError("more complex inteprolators will be implemented")

    def update_bounds(self, index: int):
        if (
            self._model.headerData(
                0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            == FlightDatasManager.timestamp
        ):
            self.start_time = float(
                self._model.item(index, 0).data(Qt.ItemDataRole.DisplayRole)
            )
            self.end_time = float(
                self._model.item(index + 1, 0).data(Qt.ItemDataRole.DisplayRole)
            )
            self.index = index
        else:
            raise NotImplementedError("cannot do interpolation without timestamp")
