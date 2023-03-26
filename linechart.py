from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QStandardItemModel
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QSplineSeries


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

        self.win.setLayout(self.grid)
        self.setCentralWidget(self.win)