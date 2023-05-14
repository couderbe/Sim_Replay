from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QStandardItemModel
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QLineSeries,QXYSeries,QScatterSeries

from tools.geometry import Point


class LineChart(QMainWindow):
    def __init__(self,table:QStandardItemModel,parent=None):
        super().__init__(parent)

        self.win = QWidget()

        self.grid = QGridLayout()

        headers = [table.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(table.columnCount())]

        for column in range(table.columnCount()):
            series = QSplineSeries()
            for row in range(table.rowCount()):
               series.append(row,float(table.item(row, column).data(Qt.ItemDataRole.DisplayRole)))

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setTitle(headers[column])

            _chart_view = QChartView(chart)
            _chart_view.setRenderHint(QPainter.Antialiasing)

            self.grid.addWidget(_chart_view,column%3,column//3)
        
        self.grid.addWidget(self.create_XY_line_chart(table,headers.index("Plane Longitude"),headers.index("Plane Latitude")))
        self.win.setLayout(self.grid)
        self.setCentralWidget(self.win)
    
    def create_XY_line_chart(self,table:QStandardItemModel,indX,indY):
        series = QLineSeries()
      #  series.setMarkerSize(5.0)

        pt0 = Point(float(table.item(0, indY).data(Qt.ItemDataRole.DisplayRole)),float(table.item(0, indX).data(Qt.ItemDataRole.DisplayRole)))
        for row in range(1,table.rowCount()):
            pt = Point(float(table.item(row, indY).data(Qt.ItemDataRole.DisplayRole)),float(table.item(row, indX).data(Qt.ItemDataRole.DisplayRole))).spherical_to_carthesian(pt0)
            series.append(pt[0],pt[1])

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle(table.headerData(
            indX, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) +'-'+table.headerData(
            indY, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) )
        chart.setPlotArea(QRectF(width=200,height=200))
        _chart_view = QChartView(chart)
        _chart_view.setRenderHint(QPainter.Antialiasing)
        return _chart_view
