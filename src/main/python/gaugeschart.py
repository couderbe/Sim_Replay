from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from src.main.python.model.model import Model, ModelStatus
from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.ui.gauges.attitude_indicator import AttitudeIndicator
from src.main.python.ui.gauges.gauge import Gauge


class GaugesChart(QMainWindow):
    """Class that displays a set of charts that simulates cockpit gauges"""

    def __init__(self, _model: Model, parent=None):
        super().__init__(parent)
        self._model = _model
        self.win = QWidget()

        self.grid = QGridLayout()

        self.gauges:list[Gauge] = [AttitudeIndicator()]

        for g in self.gauges:
            self.grid.addWidget(g)

        self.win.setLayout(self.grid)
        self.setCentralWidget(self.win)
        self.connect_player()

    def connect_player(self):
        if self._model.status != ModelStatus.OFFLINE:
            self._model._player.record_changed.connect(self.updateGauges)

    def updateGauges(self, row: int):
        res = {}
        if FlightDatasManager.has_positioning and row < self._model._mainTableModel.rowCount():
            for column, header in enumerate(
                [
                    self._model._mainTableModel.headerData(
                        i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
                    )
                    for i in range(self._model._mainTableModel.columnCount())
                ]
            ):
                res[header] = float(
                    self._model._mainTableModel.item(row, column).data(
                        Qt.ItemDataRole.DisplayRole
                    )
                )
            for g in self.gauges:
                g.updateValues(res)
