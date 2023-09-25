from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QMouseEvent
from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.utils import between


class StickIndicator(QWidget, Gauge):
    def __init__(self, _on_change=lambda x: None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.x_axis = 0.0
        self.y_axis = 0.0
        self._width = 300
        self.on_change = _on_change
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

    def mousePressEvent(self, event:QMouseEvent):
        self.is_dragging = True
        res = {"Aileron Position":between(event.x() / self._width -0.5,-0.5,0.5) * 100,
                "Elevator Position":between(event.y() / self._width-0.5,-0.5,0.5) * 100
            }
        self.on_change(res)
    
    def mouseMoveEvent(self, event:QMouseEvent):
        if self.is_dragging:
            res = {"Aileron Position":between(event.x() / self._width -0.5,-0.5,0.5) * 100,
                    "Elevator Position":between( event.y() / self._width-0.5,-0.5,0.5) * 100
                }
            self.on_change(res)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.is_dragging:
            res = {"Aileron Position":0 * 100,
                    "Elevator Position":0 * 100
                }
            self.on_change(res)
            self.is_dragging = False
