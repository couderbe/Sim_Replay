from src.main.python.model.training_model import TrainingModel
from src.main.python.airport_store import AirportStore
from src.main.python.training.pattern_training_processor import Pattern, PatternStep, Runway, compute_init_direction, compute_init_position


class PatternTrainingManager:
    def __init__(self) -> None:
        self.runway = Runway(
            list(AirportStore.get_airports().values())[0]["point0"],
            list(AirportStore.get_airports().values())[0]["point1"]
        )
        self.pattern = Pattern(self.runway,True,0.0,0.0,500.0)
        self.isQfu = True
        self.patternStep = PatternStep.FINAL


    def do_teleport(self, training_model:TrainingModel):
        pos = compute_init_position(self.pattern, self.patternStep, self.isQfu)
        dir = compute_init_direction(self.pattern, self.patternStep, self.isQfu)

        training_model.tp_to_pos(pos,dir,50)
