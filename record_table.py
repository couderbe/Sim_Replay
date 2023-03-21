from PySide6.QtCore import Signal, QObject

class RecordTable:

    def __init__(self,_header) -> None:
        self.header = _header
        self.records = []

    def addRow(self,row:list):
        if len(row)==len(self.header):
            self.records.append(row)
    
    def cleanRows(self):
        self.records.clear()
    
    def rowCount(self):
        return len(self.records)
    
    def item(self,row,column):
        return self.records[row][column]

class RecordTableProxy(QObject):
    resized = Signal(list)

class ListenableRecordTable(RecordTable):
    def __init__(self,_header):
        super().__init__(_header)
        self._proxy = RecordTableProxy()
        self.resized = self._proxy.resized
    
    def set_record_header(self,_header):
        self.cleanRows()
        self.header = _header

    def addRow(self, row:list):
        super().addRow(row)
        self.resized.emit(row)

    def cleanRows(self):
        super().cleanRows()
        self.resized.emit([])