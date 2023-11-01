import csv
import io
import json
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


def save_sr(fileName: str, model: QStandardItemModel) -> None:
    """Save model in to fileName in .sr format

    Args:
        fileName (str): Name of the save file
        model (QStandardItemModel): model to be saved
    """
    csv_output = io.StringIO()
    headers = [model.headerData(
        i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) for i in range(model.columnCount())]
    writer = csv.DictWriter(csv_output, fieldnames=headers, delimiter=";")
    writer.writeheader()
    for row in range(model.rowCount()):
        row_data = {}
        for column in range(model.columnCount()):
            row_data[headers[column]] = model.data(
                model.index(row, column))
        writer.writerow(row_data)
    
    with open(fileName, 'w') as file:
        file.write(json.dumps({"data": csv_output.getvalue()}))

def open_sr(fileName: str, model: QStandardItemModel) -> None:
    """Open .sr file and save data into the model

    Args:
        fileName (str): .sr file to open
        model (QStandardItemModel): model to be populated
    """
    with open(fileName, "r") as file:
        file_content = json.loads(file.read())
        reader = csv.reader(io.StringIO(file_content["data"]), delimiter=";")
        headers = reader.__next__()

        for row in reader:
            items = [QStandardItem(field) for field in row]
            model.appendRow(items)

        for i, header in enumerate(headers):
            model.setHeaderData(
                i, Qt.Orientation.Horizontal, header)