from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen

from src.main.python.tools.queue import Queue
from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.tools.geometry import Point


class GpsTrajectory(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.length = 3000
        self.queueX = Queue(self.length)
        self.queueY = Queue(self.length)
        self._width = 300

        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("sliding graph")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        self.drawTraj(event, qp)
        qp.end()

    def drawBackground(self, ev, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))
        painter.drawRect(1, 1, self._width - 1, self._width - 1)

    def drawTraj(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.magenta, 1, Qt.SolidLine))
        if self.queueX.get_size() > 0:
            res = max(self.queueX.M - self.queueX.m, self.queueY.M - self.queueY.m, 0.5)
            painter.drawText(
                QPointF(6.0, 12.0), str(round(max(self.queueY.M, 0.5),1))
            )
            painter.drawText(
                QPointF(6.0, self._width - 10),
                str(round(self.queueY.m ,1)),
            )
            points = [
                    QPointF(
                        (x - self.queueX.m) / res * self._width,
                        (1 - (self.queueY.get_values()[i] - self.queueY.m) / res)
                        * self._width,
                    )
                    for (i, x) in enumerate(self.queueX.get_values())
                ]
            painter.drawPolyline(
                points
            )

            if len(points)>0:
                painter.drawEllipse(points[-1],4.0,4.0)

    def updateValues(self, values: dict):
        if values.get("Plane Longitude") and values.get("Plane Latitude"):
            if self.queueX.get_size() <= 1:
                self.pt0: Point = Point(values["Plane Longitude"], values["Plane Latitude"])
                pt = (0.0,0.0)
            else:
                pt = Point(
                    values["Plane Longitude"], values["Plane Latitude"]
                ).spherical_to_carthesian(self.pt0)

            self.queueX.add(pt[0])
            self.queueY.add(pt[1])
            self.repaint()
