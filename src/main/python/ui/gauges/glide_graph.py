import math
from PySide6.QtCore import QRect, Qt, QPointF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen

from src.main.python.flight_model.flight_model import NM_2_M
from src.main.python.tools.queue import Queue
from src.main.python.ui.gauges.gauge import Gauge
from src.main.python.tools.geometry import DEG_2_RAD, FEET_2_M, NM_2_FEET, Point3D
from src.main.python.airport_store import AIRPORT_SETTINGS

finesse = 10.0


class CrossGlideGraph(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.max_altitude = 1500
        self.max_xtrack = 1.1

        self.xtrack = 0
        self.altitude = 0
        self._width = 300
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("Cross Glide indicator")
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
        painter.drawLine(2, 0, 2, self._width - 2)
        painter.drawLine(0, self._width - 2, self._width, self._width - 2)
        painter.setPen(QPen(Qt.gray, 0.5, Qt.SolidLine))

        painter.drawLine(
            0,
            self._width,
            self._width,
            self._width
            * (1 - self.max_xtrack * NM_2_FEET / finesse / self.max_altitude),
        )

        painter.setPen(QPen(Qt.gray, 0.5, Qt.SolidLine))

        painter.drawLine(
            0,
            self._width,
            self._width,
            self._width
            * (1 - self.max_xtrack * NM_2_FEET / finesse / self.max_altitude * 2),
        )

        painter.setPen(QPen(Qt.lightGray, 0.5, Qt.DashLine))

        for d in [10, 15, 20, 25]:
            painter.drawLine(
                0,
                self._width,
                self._width,
                self._width
                * (
                    1
                    - self.max_xtrack
                    * NM_2_FEET
                    * math.tan(d * DEG_2_RAD)
                    / self.max_altitude
                ),
            )
        painter.drawText(
            QPointF(8, 10), str(math.floor(self.max_altitude * FEET_2_M * 10) / 10)
        )
        painter.drawText(
            QPointF(self._width - 8, self._width - 10),
            str(math.floor(self.max_xtrack * 1852 * 10) / 10),
        )

    def drawCurve(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.blue, 4, Qt.SolidLine))
        pos = QPointF(
            self.xtrack * self._width / self.max_xtrack,
            (self.max_altitude - self.altitude) * self._width / self.max_altitude,
        )
        painter.drawEllipse(
            QPointF(
                self.xtrack * self._width / self.max_xtrack,
                (self.max_altitude - self.altitude) * self._width / self.max_altitude,
            ),
            5,
            5,
        )
        painter.drawText(
            pos + QPointF(0, -10),
            str(math.floor(self.xtrack * NM_2_M * 10) / 10)
            + ","
            + str(math.floor(self.altitude * FEET_2_M * 10) / 10),
        )

    def updateValuesOld(self, values: dict):
        plane_point = Point3D(
            values.get("Plane Longitude"),
            values.get("Plane Latitude"),
            values.get("Plane Altitude"),
        )

        self.altitude = plane_point.altitude - AIRPORT_SETTINGS["point0"].altitude

        dist = plane_point.spherical_to_carthesian(AIRPORT_SETTINGS["point0"])
        self.xtrack = math.hypot(dist[0], dist[1])

        self.repaint()

    def updateValues(self, values: dict):
        plane_point = Point3D(
            values.get("Plane Longitude"),
            values.get("Plane Latitude"),
            values.get("Plane Altitude"),
        )

        self.altitude = (
            plane_point.altitude
            - (
                AIRPORT_SETTINGS["point0"].altitude
                + AIRPORT_SETTINGS["point1"].altitude
            )
            / 2
        )

        distP0 = plane_point.spherical_to_carthesian(AIRPORT_SETTINGS["point0"])
        distP1 = plane_point.spherical_to_carthesian(AIRPORT_SETTINGS["point1"])

        if(math.hypot(distP0[0],distP0[1])<math.hypot(distP1[0],distP1[1])):
            dist = distP0
            conf = AIRPORT_SETTINGS["point0"]
        else:
            dist = distP1
            conf = AIRPORT_SETTINGS["point1"]

        self.xtrack = math.fabs(
            math.sin(
                plane_point.relevement(conf)
                - AIRPORT_SETTINGS["point1"].relevement(AIRPORT_SETTINGS["point0"]) # TODO: replace by const
            )
            * math.hypot(dist[0], dist[1])
        )
        self.repaint()


class FinalGlideGraph(QWidget, Gauge):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.max_altitude = 1500
        self.max_xtrack = 0.7

        self.xtrack = 0
        self.altitude = 0
        self._width = 300
        self.setGeometry(QRect(0, 0, self._width, self._width))
        self.setWindowTitle("Final Glide indicator")
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
        painter.drawLine(2, 0, 2, self._width - 2)
        painter.drawLine(0, self._width - 2, self._width, self._width - 2)
        painter.setPen(QPen(Qt.gray, 0.5, Qt.SolidLine))

        painter.drawLine(
            0,
            self._width,
            self._width,
            self._width
            * (1 - self.max_xtrack * NM_2_FEET / finesse / self.max_altitude),
        )

        painter.setPen(QPen(Qt.gray, 0.5, Qt.SolidLine))

        painter.drawLine(
            0,
            self._width,
            self._width,
            self._width
            * (1 - self.max_xtrack * NM_2_FEET / finesse / self.max_altitude * 2),
        )

        painter.setPen(QPen(Qt.lightGray, 0.5, Qt.DashLine))

        for d in [2, 4, 6, 8]:
            painter.drawLine(
                0,
                self._width,
                self._width,
                self._width
                * (
                    1
                    - self.max_xtrack
                    * NM_2_FEET
                    * math.tan(d * DEG_2_RAD)
                    / self.max_altitude
                ),
            )

        painter.drawText(
            QPointF(8, 10), str(math.floor(self.max_altitude * FEET_2_M * 10) / 10)
        )
        painter.drawText(
            QPointF(self._width - 8, self._width - 10),
            str(math.floor(self.max_xtrack * 1852 * 10) / 10),
        )

    def drawCurve(self, ev, painter: QPainter):
        painter.setPen(QPen(Qt.blue, 4, Qt.SolidLine))

        pos = QPointF(
            self.xtrack * self._width / self.max_xtrack,
            (self.max_altitude - self.altitude) * self._width / self.max_altitude,
        )
        painter.drawEllipse(
            pos,
            10,
            3,
        )
        painter.drawText(
            pos + QPointF(0,-10),
            str(math.floor(self.xtrack * NM_2_M * 10) / 10)
            + ","
            + str(math.floor(self.altitude * FEET_2_M * 10) / 10),
        )

    def updateValues(self, values: dict):
        plane_point = Point3D(
            values.get("Plane Longitude"),
            values.get("Plane Latitude"),
            values.get("Plane Altitude"),
        )

        self.altitude = (
            plane_point.altitude
            - (
                AIRPORT_SETTINGS["point0"].altitude
                + AIRPORT_SETTINGS["point1"].altitude
            )
            / 2
        )
        distP0 = plane_point.spherical_to_carthesian(AIRPORT_SETTINGS["point0"])
        distP1 = plane_point.spherical_to_carthesian(AIRPORT_SETTINGS["point1"])

        if(math.hypot(distP0[0],distP0[1])<math.hypot(distP1[0],distP1[1])):
            dist = distP0
            conf = AIRPORT_SETTINGS["point0"]
        else:
            dist = distP1
            conf = AIRPORT_SETTINGS["point1"]

        self.xtrack = math.fabs(
            math.cos(
                plane_point.relevement(conf)
                - AIRPORT_SETTINGS["point1"].relevement(AIRPORT_SETTINGS["point0"]) # TODO: replace by const
            )
            * math.hypot(dist[0], dist[1])
        )
        self.repaint()
