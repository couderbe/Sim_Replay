class Message:
    def __init__(self, _label: str, _message: str):
        self.title = _label
        self.message = _message


PLAY_WITHOUT_TIMESTAMP_ERROR = Message(
    "Cannot play whithout timestamp",
    "You cannot play a record whithout a proper timestamp in datatable",
)
PLAY_DURING_RECORD_ERROR = Message(
    "Cannot play while recording", "You cannot play a record while recording"
)
NOT_CONNECTED_SIM_ERROR = Message(
    "Not connected to the sim",
    "You must be connected to the sim before playing a record",
)

NOT_CONNECTED_SIM_ERROR = Message(
    "Not connected to the sim",
    "You must be connected to the sim before playing a record",
)

DATA_LOST_WARNING = Message(
    "Warning",
    "You are going to start recording. All the current data will be lost\n"
    "Do you want to continue ?",
)
