import csv
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt, QModelIndex

def save_datas(fileName,mainTableModel:QStandardItemModel):
    with open(fileName, 'w') as csvfile:
        headers = [mainTableModel.headerData(
            i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(mainTableModel.columnCount())]
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=";",
                                lineterminator="\n")
        writer.writeheader()
        # Optimization ?
        for row in range(mainTableModel.rowCount()):
            row_data = {}
            for column in range(mainTableModel.columnCount()):
                row_data[headers[column]] = mainTableModel.data(
                    mainTableModel.index(row, column))
            writer.writerow(row_data)