from abc import abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen

class Gauge:
    
    def __init__(self) -> None:
        self._width = 300

    @abstractmethod
    def updateValues(val:dict)->None:
        """Updates the values displayed in the Gauge.
            Has to be implemented.

        Args:
            val (dict): the set of datas that the gauge partially uses

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("The method has to be implemented")
    
    def drawNoValue(self, ev, painter: QPainter):
        painter.resetTransform()
        painter.setPen(QPen(Qt.red,6,Qt.SolidLine))
        painter.drawLine(0, 0, self._width, self._width)
        painter.drawLine(self._width, 0, 0, self._width)
