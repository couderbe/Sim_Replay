from PySide6.QtCore import QRect, Qt, QPoint
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen

from src.main.python.ui.gauges.gauge import Gauge

class Compass(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.heading = 0
        self._width = 300
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("compass")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        if (self.heading!=None):
            self.drawCompass(event, qp)
        else:
            self.drawNoValue(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.translate(self._width / 2, self._width / 2)
        painter.drawLine(-self._width / 6, 0, self._width / 6, 0)
        painter.drawLine(0,-self._width / 4, 0, self._width / 4)

    def drawCompass(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        painter.rotate(-self.heading)

        painter.drawText(QPoint(-4,-self._width/2+45),"N")
        painter.rotate(90)
        painter.drawText(QPoint(-4,-self._width/2+45),"E")
        painter.rotate(90)
        painter.drawText(QPoint(-4,-self._width/2+45),"S")
        painter.rotate(90)
        painter.drawText(QPoint(-4,-self._width/2+45),"W")
        painter.rotate(90)
        
        for i in range(0, 72):
            painter.drawLine(
                0,
                -self._width/2,
                0,
                -self._width/2+(30 if i%2==0 else 15)
            )
            painter.rotate(5)

    def updateValues(self,values:dict):
        self.heading = values.get('Plane Heading Degrees True')
        self.repaint()