from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.simconnect.listener import Listener

from src.main.python.model.model import Model, ModelStatus
from src.main.python.ui.gauges.command import Emitter
from src.main.python.tools.geometry import Point3D


class TrainingModel:

    def __init__(self, _model: Model) -> None:
        self.model = _model

    def connect_view(self, listener: Listener):
        if False and self.model.status != ModelStatus.OFFLINE:
            self.model._sim.connect(listener)  # TODO : manage mock case

    def tp_to_pos(self, pos: Point3D, heading: float, speed: float):
        if self.model.status != ModelStatus.OFFLINE:
            if not FlightDatasManager.has_positioning:
                FlightDatasManager.set_dataset_as_state()
            FlightDatasManager.add_data("Airspeed Indicated", "Knots")
            self.model.get_active_source().add_dataset(
                FlightDatasManager.current_dataset
            )
            self.model.get_active_source().set_param_value_from_name(
                "Plane Latitude", pos.lat
            )
            self.model.get_active_source().set_param_value_from_name(
                "Plane Longitude", pos.lon
            )
            self.model.get_active_source().set_param_value_from_name(
                "Plane Altitude", pos.altitude
            )
            self.model.get_active_source().set_param_value_from_name(
                "Plane Heading Degrees True", heading
            )
            self.model.get_active_source().set_param_value_from_name(
                "Airspeed Indicated", speed
            )
