from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen

from src.main.python.ui.gauges.gauge import Gauge


class NeedleGauge(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.value = None
        self.max_val = 250
        self._width = 300
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("needle_gauge")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        if (self.value!=None):
            self.drawNeedle(event, qp)
        else:
            self.drawNoValue(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.gray, 4, Qt.SolidLine))
        painter.drawArc(0, 0, self._width, self._width, 260 * 16, -325 * 16)
        painter.translate(self._width / 2, self._width / 2)

    def drawNeedle(self, ev, painter: QPainter):
        painter.drawText(QPointF(0.0, 20), str(round(self.value)))
        #painter.rotate(10 * 340 / self.max_val)
        for i in range(0, round(self.max_val / 10) - 1):
            painter.rotate(10 * 340 / self.max_val)
            painter.drawLine(0, self._width / 2 - 10, 0, self._width / 2)
            if i % 2 != 0:
                painter.rotate(3.5 if self.value>=100 else 3)
                painter.drawText(
                    QPointF(0.0, self._width / 2 - 18),
                    str((i+1) * 10),
                )
                painter.rotate(-3.5 if self.value>=100 else -3)
        painter.rotate(-((round(self.max_val / 10)-1) * 10) * 340 / self.max_val)
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        
        painter.rotate(self.value * 340 / self.max_val)
        painter.drawLine(0, 0, 0, self._width / 2 * 4 / 5)
    
    def updateValues(self, values: dict):
        self.value = values.get("Speed")
        if self.value != None:
            self.max_val += (
                self.value - self.max_val * 0.5
            ) * 0.008
        self.repaint()
