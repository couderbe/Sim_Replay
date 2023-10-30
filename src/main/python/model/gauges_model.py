
from PySide6.QtCore import Qt

from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.model.model import Model, ModelStatus

class GaugesModel:

    def __init__(self,_model:Model) -> None:
        self.model = _model


    def connect_player(self, func):
        if self.model.status != ModelStatus.OFFLINE:
            self.model._player.record_changed.connect(func)

    def get_values_in_row(self,row:int)-> dict|None:
        if FlightDatasManager.has_positioning and row < self.model._mainTableModel.rowCount():
            res = {}
            for column, header in enumerate(
                [
                    self.model._mainTableModel.headerData(
                        i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
                    )
                    for i in range(self.model._mainTableModel.columnCount())
                ]
            ):
                res[header] = float(
                    self.model._mainTableModel.item(row, column).data(
                        Qt.ItemDataRole.DisplayRole
                    )
                )
            return res
        else :
            return None
