
import signal
from PySide6.QtCore import QObject

from src.main.python.player import Player


class GaugesModelProxy(QObject):
    # Signal Emited when record changes. The current record is sent as integer
    record_changed = signal(int)

class GaugesModel:

    def __init__(self,_mainTable) -> None:
        self.mainTable = _mainTable


    def connect_player(self, _player:Player):
        _player.record_changed.connect()
