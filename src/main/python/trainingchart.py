from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QVBoxLayout, QPushButton
from src.main.python.model.training_model import TrainingModel
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
from src.main.python.ui.gauges.glide_graph import CrossGlideGraph, FinalGlideGraph
from src.main.python.training.pattern_training_processor import Pattern, PatternStep, Runway, compute_init_direction, compute_init_position
from src.main.python.tools.geometry import Point3D
from src.main.python.airport_store import AIRPORT_SETTINGS

class TrainingProxy(QObject):
    # Signal Emited when record changes. The current record is sent as a dictionary
    inputs_changed = Signal(dict)


class TrainingChart(QMainWindow, Emitter, Listener):
    """Class that displays a set of charts that can be used for training"""

    def __init__(self, _training_model: TrainingModel, parent=None):
        super().__init__(parent)
        self.training_model = _training_model
        self.mainWin = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWin.setLayout(self.mainLayout)

        self.win = QWidget()

        self.grid = QGridLayout()

        self.proxy = TrainingProxy()

        self.gauges: list[Gauge] = [
           CrossGlideGraph(),
           FinalGlideGraph()
        ]

        for column,g in enumerate(self.gauges):
            self.grid.addWidget(g,column % 2, column//2)

        self.win.setLayout(self.grid)

        self.mainLayout.addWidget(self.win)

        self.button = QPushButton("TP for training")

        self.mainLayout.addWidget(self.button)

        self.button.clicked.connect(self.on_request_tp_clicked)

        self.setCentralWidget(self.mainWin)
        self.connect_mock()

    def connect_mock(self):
        self.training_model.connect_view(self)

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

    def on_request_tp_clicked(self):
        runway = Runway(AIRPORT_SETTINGS["point0"],AIRPORT_SETTINGS["point1"])

        pattern = Pattern(runway,True, -0.1,0.1,2500)

        pos = compute_init_position(pattern, PatternStep.BASE, True)
        dir = compute_init_direction(pattern, PatternStep.BASE, True)

        self.training_model.tp_to_pos(pos,dir,50)


        
