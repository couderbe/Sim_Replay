from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from src.main.python.model.gauges_model import GaugesModel
from src.main.python.ui.gauges.attitude_indicator import AttitudeIndicator
from src.main.python.ui.gauges.compass import Compass
from src.main.python.ui.gauges.gauge import Gauge


class GaugesChart(QMainWindow):
    """Class that displays a set of charts that simulates cockpit gauges"""

    def __init__(self, _gauge_model: GaugesModel, parent=None):
        super().__init__(parent)
        self._gauge_model = _gauge_model
        self.win = QWidget()

        self.grid = QGridLayout()

        self.gauges:list[Gauge] = [AttitudeIndicator(),Compass()]

        for g in self.gauges:
            self.grid.addWidget(g)

        self.win.setLayout(self.grid)
        self.setCentralWidget(self.win)
        self.connect_player()

    def connect_player(self):
        self._gauge_model.connect_player(self.updateGauges)

    def refresh_all_gauges(self,res):
        if res!=None:
            for g in self.gauges:
                g.updateValues(res)

    def updateGauges(self, row: int):
        res:dict = self._gauge_model.get_values_in_row(row)
        self.refresh_all_gauges(res)
