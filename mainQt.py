import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, QModelIndex
from main_window import Ui_MainWindow
import csv

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.ui.actionOpen.setShortcut('Ctrl+O')
        self.ui.actionOpen.triggered.connect(self.openDialog)
        self._mainTableModel = QStandardItemModel(self)
        self.ui.mainTableView.setModel(self._mainTableModel)
        self.ui.mainTableView.clicked.connect(self.on_item_clicked)

    def on_item_clicked(self, index: QModelIndex):
        self.ui.timeLabel.setText(str(index.siblingAtColumn(self._time_column_id).data()))
        

    def openDialog(self) -> None:
        """
        Manage file opening
        """
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Csv files (*.csv);;All files (*.*)')
        if fileName:
            self._mainTableModel.clear()
            with open(fileName, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=";", lineterminator="\n")
                headers = reader.__next__()
                for row in reader:
                    items = [QStandardItem(field) for field in row]
                    self._mainTableModel.appendRow(items)
                for i,header in enumerate(headers):
                    self._mainTableModel.setHeaderData(i,Qt.Orientation.Horizontal,header)
                    if header == "time":
                        self._time_column_id = i
            # Set time label initial value
            self.ui.timeLabel.setText(self._mainTableModel.item(0,self._time_column_id).text())
                

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
