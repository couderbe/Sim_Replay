from PySide6.QtCore import QRect, Qt, QPointF, QRectF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath, QMouseEvent

from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.utils import between



class ThrottleIndicator(QWidget, Gauge):
    def __init__(self, _on_change=lambda x: None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.z_axis = 0.0
        self._width = 300
        self.on_change = _on_change
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("throttle indicator")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        if self.z_axis != None:
            self.drawThrottlePosition(event, qp)
        else:
            self.drawNoValue(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.gray, 4, Qt.SolidLine))
        painter.translate(self._width / 2, 0)
        painter.drawLine(-15, 0, -15, self._width)
        painter.drawLine(15, 0, 15, self._width)
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        for i in range(11):
            painter.drawLine(-15, self._width*i/10, -10, self._width*i/10)
        
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        for i in range(11):
            painter.drawLine(10, self._width*i/10, 15, self._width*i/10)

    def drawThrottlePosition(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black))
        path:QPainterPath = QPainterPath()
        path.addRoundedRect(QRectF(-25,-10+((100-self.z_axis)/100*self._width),50,20),8,8)
        painter.drawPath(path)

    def updateValues(self, values: dict):
        self.z_axis = values.get("General Eng Throttle Lever Position:1")
        self.repaint()

    def mousePressEvent(self, event:QMouseEvent):
        self.is_dragging = True
        res = {"General Eng Throttle Lever Position:1":between(1-event.y() / self._width,0,1 ) * 100 }
        self.on_change(res)
    
    def mouseMoveEvent(self, event:QMouseEvent):
        if self.is_dragging:
            res = {"General Eng Throttle Lever Position:1":between(1-event.y() / self._width,0, 1) * 100 }
            self.on_change(res)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.is_dragging:
            self.is_dragging = False
