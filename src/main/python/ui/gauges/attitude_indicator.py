from PySide6.QtCore import QRect, Qt, QPoint
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen

from src.main.python.ui.gauges.gauge import Gauge

class AttitudeIndicator(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.bank = 0
        self.pitch = 0
        self._width = 300
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("attitude indicator")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        self.drawBird(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setBrush(QColor(172, 86, 17, 255))
        painter.drawRect(0, 0, self._width, self._width)
        painter.setBrush(QColor(55, 128, 241, 255))
        painter.drawRect(0, 0, self._width, self._width / 2 * (self.pitch + 50) / 50)

    def drawBird(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.white, 0.3, Qt.SolidLine))

        for i in range(1, 10):
            painter.drawLine(
                self._width *1/4,
                i / 10 * self._width,
                self._width *3/4,
                i / 10 * self._width,
            )

        painter.translate(self._width / 2, self._width / 2)
        painter.drawLine(-self._width / 2, 0, self._width / 2, 0)
        painter.rotate(self.bank)
        painter.setPen(QPen(Qt.black, 9, Qt.SolidLine))
        painter.drawEllipse(QPoint(0,0),8,8)
        painter.drawLine(0,0,0,-50)
        painter.drawLine(-self._width / 2*0.9, 0, self._width / 2*0.9, 0)

    def updateValues(self,values:dict):
        self.bank = -values['Plane Bank Degrees']
        self.pitch = -values['Plane Pitch Degrees']
        self.repaint()