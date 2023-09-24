from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush

from src.main.python.ui.gauges.gauge import Gauge


class StickIndicator(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.x_axis = 0.0
        self.y_axis = 0.0
        self._width = 300
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("stick indicator")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        if self.y_axis != None and self.x_axis != None:
            self.drawStickPosition(event, qp)
        else:
            self.drawNoValue(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self._width, self._width)
        painter.translate(self._width / 2, self._width / 2)
        painter.drawLine(-10, 0, 10, 0)
        painter.drawLine(0, -10, 0, 10)

    def drawStickPosition(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red))
        painter.drawEllipse(
            QPointF(
                self.x_axis * self._width / 2 / 50, self.y_axis * self._width / 2 / 50
            ),
            20.0,
            20.0,
        )

    def updateValues(self, values: dict):
        self.x_axis = values.get("Aileron Position")
        self.y_axis = values.get("Elevator Position")
        self.repaint()
