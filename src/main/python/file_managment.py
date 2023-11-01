import csv
import io
import json
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt


def save_sr(fileName: str, model: QStandardItemModel) -> None:
    csv_output = io.StringIO()
    headers = [model.headerData(
        i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(model.columnCount())]
    writer = csv.DictWriter(csv_output, fieldnames=headers, delimiter=";",
                            lineterminator="\n")
    writer.writeheader()
    for row in range(model.rowCount()):
        row_data = {}
        for column in range(model.columnCount()):
            row_data[headers[column]] = model.data(
                model.index(row, column))
        writer.writerow(row_data)
    
    with open(fileName, 'w') as file:
        file.write(json.dumps({"data": csv_output.getvalue()}))

def open_sr(fileName: str):
    pass
