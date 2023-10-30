from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from src.main.python.simconnect.listener import Listener
from src.main.python.model.inputs_model import InputsModel
from src.main.python.ui.gauges.attitude_indicator import AttitudeIndicator
from src.main.python.ui.gauges.compass import Compass
from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.ui.gauges.sliding_graph import SlidingGraph
from src.main.python.ui.gauges.gps_trajectory import GpsTrajectory
from src.main.python.ui.gauges.needle_gauge import NeedleGauge
from src.main.python.ui.gauges.stick_indicator import StickIndicator
from src.main.python.ui.gauges.rudder_indicator import RudderIndicator
from src.main.python.ui.gauges.throttle_indicator import ThrottleIndicator

from PySide6.QtCore import Signal, QObject

from src.main.python.ui.gauges.command import Emitter


class InputsProxy(QObject):
    # Signal Emited when record changes. The current record is sent as a dictionary
    inputs_changed = Signal(dict)


class InputsChart(QMainWindow, Emitter, Listener):
    """Class that displays a set of charts that simulates cockpit inputs"""

    def __init__(self, _inputs_model: InputsModel, parent=None):
        super().__init__(parent)
        self.inputs_model = _inputs_model
        self.win = QWidget()

        self.grid = QGridLayout()

        self.proxy = InputsProxy()

        self.gauges: list[Gauge] = [
            AttitudeIndicator(),
            Compass(),
            SlidingGraph("Plane Altitude"),
           # SlidingGraph("Speed"),
           # GpsTrajectory(),
            NeedleGauge(),
            StickIndicator(self.on_value_update),
            RudderIndicator(self.on_value_update),
            ThrottleIndicator(self.on_value_update)
        ]

        for column,g in enumerate(self.gauges):
            self.grid.addWidget(g,column % 2, column//2)

        self.win.setLayout(self.grid)
        self.setCentralWidget(self.win)
        self.connect_mock()

    def connect_mock(self):
        self.inputs_model.connect_view(self)
        self.inputs_model.connect_input(self)

    def on_value_update(self,params:set):
        self.proxy.inputs_changed.emit(params)

    def refresh_all_gauges(self, res: dict | None):
        if res != None:
            for g in self.gauges:
                g.updateValues(res)

    def updateGauges(self, res:dict):
        self.refresh_all_gauges(res)
    
    def connect(self, listener:Listener):
        self.proxy.inputs_changed.connect(listener.apply)

    def apply(self, params:dict):
        self.updateGauges(params)
