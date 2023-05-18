from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class FertilizationModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        tableModel = QSqlTableModel()
        tableModel.setTable("FERTILIZACION")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("id", "Fecha", "Fertilizante", "kg por hectárea", "Potrero")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel
    
    def addFertilization(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        
        self.model.submitAll()
        self.model.select()

    def deleteFertilization(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearFertilizations(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
    
class AnalysisModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        tableModel = QSqlTableModel()
        tableModel.setTable("ANALISIS")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("id", "Fecha", "Fósforo", "Potasio", "PH", "Materia Org.", "Potrero")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel
    
    def addAnalysis(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        
        self.model.submitAll()
        self.model.select()

    def deleteAnalysis(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
    
    def clearAnalysis(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

    