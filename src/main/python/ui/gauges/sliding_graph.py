from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen

from src.main.python.tools.queue import Queue
from src.main.python.ui.gauges.gauge import Gauge


class SlidingGraph(QWidget, Gauge):
    def __init__(self, _val_attr: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.val_attr = _val_attr

        self.length = 500
        self.queue = Queue(self.length)
        self._width = 300

        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("sliding graph")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        self.drawCurve(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.drawLine(2, 0, 2, self._width-2)
        painter.drawLine(0, self._width - 2, self._width, self._width - 2)

    def drawCurve(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        if self.queue.get_size() > 0:
            res = max(self.queue.M - self.queue.m, 1000)
            painter.drawText(
                QPointF(6.0, 10.0), str(round(max(self.queue.M, 1000) / 10) * 10)
            )
            painter.drawText(
                QPointF(6.0, self._width - 10),
                str(round(self.queue.m / 10) * 10),
            )
            points = []
            for i, v in enumerate(self.queue.get_values()):
                if v != None:
                    points.append(
                        QPointF(
                            i * self._width / self.length,
                            (1 - (v - self.queue.m) / res) * self._width,
                        )
                    )
            painter.drawPolyline(points)

    def updateValues(self, values: dict):
        if self.val_attr in values:
            self.queue.add(values.get(self.val_attr))
            self.repaint()
