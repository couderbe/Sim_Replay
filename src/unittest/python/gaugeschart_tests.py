import sys
import unittest
import threading
import time
import math

from mockito import mock

from PySide6.QtWidgets import QApplication

from src.main.python.gaugeschart import GaugesChart


class GaugesChartTest(unittest.TestCase):
    @unittest.skip('Graphical tests, not automatic')
    def test_open_gauges_chart(self):
        _gaugesmodel = mock()
        app = QApplication(sys.argv)
        window = GaugesChart(_gaugesmodel)
        window.show()
        window.setGeometry(30, 30, 1720, 960)
        val = [0]
        proceed = True

        def update_gauges():
            while proceed:
                window.refresh_all_gauges(
                    {
                        "Plane Bank Degrees": -90 + val[0],
                        "Plane Pitch Degrees": -50 + val[0] * 100 / 180,
                        "Plane Heading Degrees True": 0 + val[0] * 2,
                        "Plane Altitude": 10 + val[0] * val[0],
                        "Speed": 150 * math.cos((math.pi / 90) * val[0]) + 110,
                        "Plane Longitude": 10 + math.sin((math.pi / 90) * val[0]) * 1.5,
                        "Plane Latitude": 45
                        + math.cos((math.pi / 90) * val[0])
                        * (1 + 0.1*math.cos((math.pi / 10) * val[0])),
                    }
                )
                val[0] = val[0] + 1 if val[0] < 180 else 0
                time.sleep(0.03)

        t = threading.Thread(target=update_gauges)
        t.start()

        self.assertEquals(app.exec_(), 0)
        proceed = False
