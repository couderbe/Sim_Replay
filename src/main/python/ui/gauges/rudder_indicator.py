from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QMouseEvent

from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.utils import between



class RudderIndicator(QWidget, Gauge):
    def __init__(self, _on_change=lambda x: None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.z_axis = 0.0
        self._width = 300
        self.on_change = _on_change
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("rudder indicator")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        if self.z_axis != None:
            self.drawRudderPosition(event, qp)
        else:
            self.drawNoValue(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.gray, 4, Qt.SolidLine))
        painter.translate(0, self._width / 2)
        painter.drawLine(0, 0, self._width, 0)
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        for i in range(11):
            painter.drawLine(self._width*i/10, -5, self._width*i/10, 5)
        painter.drawLine(self._width / 2, -10, self._width / 2, 10)

    def drawRudderPosition(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red))
        painter.translate(self._width / 2, 0)
        painter.drawPolygon(
            [
                QPointF(self.z_axis * self._width / 2 / 50, -2),
                QPointF(self.z_axis * self._width / 2 / 50 - 15, -22),
                QPointF(self.z_axis * self._width / 2 / 50 + 15, -22),
            ]
        )

    def updateValues(self, values: dict):
        self.z_axis = values.get("Rudder Position")
        self.repaint()

    def mousePressEvent(self, event:QMouseEvent):
        self.is_dragging = True
        res = {"Rudder Position":between(event.x() / self._width - 0.5,-0.5,0.5 ) * 100 }
        self.on_change(res)
    
    def mouseMoveEvent(self, event:QMouseEvent):
        if self.is_dragging:
            res = {"Rudder Position":between(event.x() / self._width - 0.5,-0.5,0.5 ) * 100 }
            self.on_change(res)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.is_dragging:
            res = {"Rudder Position":0 }
            self.on_change(res)
            self.is_dragging = False

