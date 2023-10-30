from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from src.main.python.model.gauges_model import GaugesModel
from src.main.python.ui.gauges.attitude_indicator import AttitudeIndicator
from src.main.python.ui.gauges.compass import Compass
from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.ui.gauges.sliding_graph import SlidingGraph
from src.main.python.ui.gauges.gps_trajectory import GpsTrajectory
from src.main.python.ui.gauges.needle_gauge import NeedleGauge
from src.main.python.ui.gauges.stick_indicator import StickIndicator
from src.main.python.ui.gauges.rudder_indicator import RudderIndicator
from src.main.python.ui.gauges.throttle_indicator import ThrottleIndicator


class GaugesChart(QMainWindow):
    """Class that displays a set of charts that simulates cockpit gauges"""

    def __init__(self, _gauge_model: GaugesModel, parent=None):
        super().__init__(parent)
        self._gauge_model = _gauge_model
        self.win = QWidget()

        self.grid = QGridLayout()

        self.gauges: list[Gauge] = [
            AttitudeIndicator(),
            Compass(),
            SlidingGraph("Plane Altitude"),
           # SlidingGraph("Speed"),
            GpsTrajectory(),
            NeedleGauge(),
            StickIndicator(),
            RudderIndicator(),
            ThrottleIndicator()
        ]

        for column,g in enumerate(self.gauges):
            self.grid.addWidget(g,column % 2, column//2)

        self.win.setLayout(self.grid)
        self.setCentralWidget(self.win)
        self.connect_player()

    def connect_player(self):
        self._gauge_model.connect_player(self.updateGauges)

    def refresh_all_gauges(self, res: dict | None):
        if res != None:
            for g in self.gauges:
                g.updateValues(res)

    def updateGauges(self, row: int):
        res: dict = self._gauge_model.get_values_in_row(row)
        self.refresh_all_gauges(res)
