from PySide6.QtCore import (
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
    QMimeData,
    Signal,
)
from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtCore import QAbstractListModel
from src.main.python.model.training_model import TrainingModel
from src.main.python.ui.record_window_ui import Ui_RecordWindow
from src.main.python.qt_user_roles import UserRoles
from src.main.python.ui.pattern_training_window_ui import Ui_PatternTrainingWindow
from src.main.python.airport_store import AirportStore
from src.main.python.tools.geometry import DEG_2_RAD, format_angle
from src.main.python.training.pattern_training_manager import PatternTrainingManager
from src.main.python.training.pattern_training_processor import Runway

STEP_2_M_DOWNSIDE_OFFSET = 50 / 1852
STEP_2_M_FINALE_OFFSET = 20 / 1852


class PatternTrainingWindow(QDialog):

    def __init__(self, _training_model: TrainingModel, parent=None) -> None:
        super().__init__(
            parent,
        )
        self.training_model = _training_model
        self.ui = Ui_PatternTrainingWindow()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.airportComboBox.addItems(AirportStore.get_airports().keys())

        self.training_manager = PatternTrainingManager()

        self.ui.qfuLabel.setText(
            get_runway_number(format_angle(self.training_manager.runway.qfu))
        )

        self.ui.airportComboBox.currentIndexChanged.connect(self.update_airport)

        self.ui.revertQFUPushButton.clicked.connect(self.update_qfu)
        self.ui.teleportPushButton.clicked.connect(self.do_teleport)

        self.ui.leftHandRadioButton.toggled.connect(self.update_left_hand)
        self.ui.rightHandradioButton.toggled.connect(self.update_left_hand)

        self.ui.crossDistanceHorizontalSlider.valueChanged.connect(
            self.update_cross_distance
        )
        self.ui.finaleDistanceVerticalSlider.valueChanged.connect(
            self.update_finale_distance
        )

    def update_airport(self):
        self.training_manager.pattern.runway = Runway(
            AirportStore.get_airports()[self.ui.airportComboBox.currentText()][
                "point0"
            ],
            AirportStore.get_airports()[self.ui.airportComboBox.currentText()][
                "point1"
            ],
        )
        self.ui.qfuLabel.setText(
            get_runway_number(
                format_angle(
                    self.training_manager.pattern.runway.qfu
                    + (0 if self.training_manager.isQfu else 180)
                )
            )
        )

    def update_qfu(self):
        self.training_manager.isQfu = not self.training_manager.isQfu
        self.ui.qfuLabel.setText(
            get_runway_number(
                format_angle(
                    self.training_manager.runway.qfu
                    + (0 if self.training_manager.isQfu else 180)
                )
            )
        )

    def update_cross_distance(self):
        self.training_manager.pattern.downwind_offset = (
            50 - self.ui.crossDistanceHorizontalSlider.value()
        ) * STEP_2_M_DOWNSIDE_OFFSET
        self.ui.crossDistanceLabel.setText(
            str(round(self.training_manager.pattern.downwind_offset,3))
        )

    def update_finale_distance(self):
        self.training_manager.pattern.final_offset = (
            50 - self.ui.finaleDistanceVerticalSlider.value()
        ) * STEP_2_M_FINALE_OFFSET
        self.ui.finaleDistanceLabel.setText(
            str(round(self.training_manager.pattern.final_offset,3))
        )

    def update_left_hand(self):
        self.training_manager.pattern.is_left_hand = (
            self.ui.leftHandRadioButton.isChecked()
        )

    def do_teleport(self):
        self.training_manager.do_teleport(self.training_model)


def get_runway_number(dir):
    if dir < 95:
        return "0" + str(round(dir / 10))
    else:
        return str(round(dir / 10))
