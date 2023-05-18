from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QHBoxLayout,
        QMainWindow,
        QWidget,
        QAbstractItemView,
        QPushButton,
        QTableView,
        QVBoxLayout,
        QHeaderView,
        QDialog,
        QDialogButtonBox,
        QFormLayout,
        QLineEdit,
        QMessageBox,
        QComboBox,
        QDateEdit,
        QStyledItemDelegate
    )
from .model import FertilizationModel, AnalysisModel
from PyQt5.QtSql import QSqlQueryModel

class Window(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de fertilizaciones y análisis de suelo - Uriel Ferro")
        self.resize(1700, 900)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.fertilizationModel = FertilizationModel()
        self.analysisModel = AnalysisModel()

        self.setupUI()

    def setupUI(self):
        color_back_tables = "#F0F0F0"

        # Creo la tabla de fertilizaciones
        self.tableFer = QTableView()
        self.tableFer.setStyleSheet(f"background-color: {color_back_tables}")
        self.tableFer.setModel(self.fertilizationModel.model)
        self.tableFer.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableFer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.tableFer.verticalHeader().setVisible(False)
        self.tableFer.setItemDelegate(AlignmentDelegate()) 
        self.tableFer.setSortingEnabled(True)
        self.tableFer.setColumnHidden(0, True)
        style = "::section {""background-color: #ADD8E6}"
        self.tableFer.horizontalHeader().setStyleSheet(style)

        # Creo la tabla de análisis de suelo
        self.tableAn = QTableView()
        self.tableAn.setStyleSheet(f"background-color: {color_back_tables}")
        self.tableAn.setModel(self.analysisModel.model)
        self.tableAn.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableAn.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.tableAn.verticalHeader().setVisible(False)
        self.tableAn.setItemDelegate(AlignmentDelegate())  
        self.tableAn.setSortingEnabled(True)
        self.tableAn.setColumnHidden(0, True)
        style = "::section {""background-color: #ADD8E6}"
        self.tableAn.horizontalHeader().setStyleSheet(style)

        # Creo los botones
        color_button = "#ADD8E6"
        self.addButtonFertilizacion = QPushButton("Añadir fertilización")
        self.addButtonFertilizacion.setStyleSheet(f"background-color: {color_button}")
        self.addButtonFertilizacion.clicked.connect(self.openAddDialogFertilization)

        self.addButtonAnalisis = QPushButton("Añadir análisis")
        self.addButtonAnalisis.setStyleSheet(f"background-color: {color_button}")
        self.addButtonAnalisis.clicked.connect(self.openAddDialogAnalysis)

        self.deleteButtonFertilizacion = QPushButton("Eliminar fertilización")
        self.deleteButtonFertilizacion.setStyleSheet(f"background-color: {color_button}")
        self.deleteButtonFertilizacion.clicked.connect(self.deleteFertilization)

        self.deleteButtonAnalisis = QPushButton("Eliminar análisis")
        self.deleteButtonAnalisis.setStyleSheet(f"background-color: {color_button}")
        self.deleteButtonAnalisis.clicked.connect(self.deleteAnalysis)

        self.clearAllButtonFertilizacion = QPushButton("Eliminar todas las fertilizaciones")
        self.clearAllButtonFertilizacion.setStyleSheet(f"background-color: {color_button}")
        self.clearAllButtonFertilizacion.clicked.connect(self.clearFertilizations)

        self.clearAllButtonAnalisis = QPushButton("Eliminar todos los análisis")
        self.clearAllButtonAnalisis.setStyleSheet(f"background-color: {color_button}")
        self.clearAllButtonAnalisis.clicked.connect(self.clearAnalysis)

        self.filterButtonFertilizacion = QPushButton("Filtrar fertilizaciones")
        self.filterButtonFertilizacion.setStyleSheet(f"background-color: {color_button}")
        self.filterButtonFertilizacion.clicked.connect(self.openFilterDialogFertilization)

        self.filterButtonAnalisis = QPushButton("Filtrar análisis")
        self.filterButtonAnalisis.setStyleSheet(f"background-color: {color_button}")
        self.filterButtonAnalisis.clicked.connect(self.openFilterDialogAnalysis)

        # Diseño la disposición de la GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButtonAnalisis)
        layout.addWidget(self.addButtonFertilizacion)
        layout.addStretch()
        layout.addWidget(self.deleteButtonAnalisis)
        layout.addWidget(self.deleteButtonFertilizacion)
        layout.addStretch()
        layout.addWidget(self.filterButtonAnalisis)
        layout.addWidget(self.filterButtonFertilizacion)
        layout.addStretch()
        layout.addWidget(self.clearAllButtonAnalisis)
        layout.addWidget(self.clearAllButtonFertilizacion)
        self.layout.addWidget(self.tableAn)
        self.layout.addWidget(self.tableFer)
        self.layout.addLayout(layout)

    def openAddDialogFertilization(self):
        dialog = AddDialogFertilization(self)

        if dialog.exec() == QDialog.Accepted:
            self.fertilizationModel.addFertilization(dialog.data)
            self.tableFer.resizeColumnsToContents()

    def openAddDialogAnalysis(self):
        dialog = AddDialogAnalysis(self)

        if dialog.exec() == QDialog.Accepted:
            self.analysisModel.addAnalysis(dialog.data)
            self.tableAn.resizeColumnsToContents()

    def deleteFertilization(self):
        row = self.tableFer.currentIndex().row()

        if row < 0:
            return
        
        messageBox = QMessageBox.warning(
            self,
            "ADVERTENCIA!",
            "¿Seguro que quiere eliminar esta fertilización?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.fertilizationModel.deleteFertilization(row)

    def deleteAnalysis(self):
        row = self.tableAn.currentIndex().row()

        if row < 0:
            return
        
        messageBox = QMessageBox.warning(
            self,
            "ADVERTENCIA!",
            "¿Seguro que quiere eliminar este análisis?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.analysisModel.deleteAnalysis(row)

    def clearFertilizations(self):
        messageBox = QMessageBox.warning(
            self,
            "ADVERTENCIA!",
            "¿Seguro que quiere eliminar todas las fertilizaciones?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.fertilizationModel.clearFertilizations()

    def clearAnalysis(self):
        messageBox = QMessageBox.warning(
            self,
            "ADVERTENCIA!",
            "¿Seguro que quiere eliminar todos los análisis?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.analysisModel.clearAnalysis()

    def openFilterDialogFertilization(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Filtrar fertilizaciones")

        layout = QFormLayout()
        self.potreroFilterLineEditFertilizacion = QLineEdit()
        self.fertilizanteFilterLineEditFertilizacion = QLineEdit()
        layout.addRow("Potrero:", self.potreroFilterLineEditFertilizacion)
        layout.addRow("Fertilizante:", self.fertilizanteFilterLineEditFertilizacion)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        dialog.setLayout(layout)
        layout.addRow(buttonBox)

        if dialog.exec() == QDialog.Accepted:
            self.filterFertilizations()

    def openFilterDialogAnalysis(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Filtrar análisis")

        layout = QFormLayout()
        self.potreroFilterLineEditAnalysis = QLineEdit()
        layout.addRow("Potrero:", self.potreroFilterLineEditAnalysis)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        dialog.setLayout(layout)
        layout.addRow(buttonBox)

        if dialog.exec() == QDialog.Accepted:
            self.filterAnalysis()

    def filterFertilizations(self):
        potrero = self.potreroFilterLineEditFertilizacion.text()
        fertilizante = self.fertilizanteFilterLineEditFertilizacion.text()

        if potrero and not fertilizante:
            self.fertilizationModel.model.setFilter(f"Potrero = '{potrero}'")
        elif fertilizante and not potrero:
            self.fertilizationModel.model.setFilter(f"Fertilizante = '{fertilizante}'")
        elif potrero and fertilizante:
            self.fertilizationModel.model.setFilter(f"Potrero = '{potrero}' AND Fertilizante = '{fertilizante}'")
        else:
            self.fertilizationModel.model.setFilter(None)

    def filterAnalysis(self):
        potrero = self.potreroFilterLineEditAnalysis.text()

        if potrero:
            self.analysisModel.model.setFilter(f"Potrero = '{potrero}'")
        else:
            self.analysisModel.model.setFilter(None)

class AddDialogFertilization(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setWindowTitle("Añadir fertilización")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        # Campo para agregar la fecha
        self.dateEdit = QDateEdit()
        self.dateEdit.setDisplayFormat("dd-MM-yyyy")

        # Campo para agregar el fertilizante
        self.fertField = QLineEdit()
        self.fertField.setObjectName("Fertilizante")

        # Campo para agregar los kg por hectárea
        self.kgHectField = QLineEdit()
        self.kgHectField.setObjectName("kg por hecárea")

        # Campo para agregar el potrero
        self.potreroCombo = QComboBox()
        self.potreroCombo.setPlaceholderText("Select")
        model = QSqlQueryModel()
        model.setQuery("SELECT NumeroPotrero FROM POTREROS")
        self.potreroCombo.setModel(model)

        # Configuro los campos
        layout = QFormLayout()
        layout.addRow("Fecha:", self.dateEdit)
        layout.addRow("Fertilizante:", self.fertField)
        layout.addRow("kg por hectárea:", self.kgHectField)
        layout.addRow("Potrero:", self.potreroCombo)

        self.layout.addLayout(layout)

        # Añadir y conectar botones
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        fecha = self.dateEdit.date().toString("dd-MM-yyyy")
        fertilizante = self.fertField.text()
        kgPorHectarea = self.kgHectField.text()
        potrero = self.potreroCombo.currentText()

        # Validar los campos
        if not (fertilizante and kgPorHectarea and potrero):
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos.")
        else:
            self.data = (fecha, fertilizante, kgPorHectarea, potrero)
            super().accept()

class AddDialogAnalysis(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setWindowTitle("Añadir análisis")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        # Campo para agregar la fecha
        self.dateEdit = QDateEdit()
        self.dateEdit.setDisplayFormat("dd-MM-yyyy")

        # Campo para agregar el valor del fósforo
        self.fosField = QLineEdit()
        self.fosField.setObjectName("Fósforo")

        # Campo para agregar el valor del potasio
        self.potField = QLineEdit()
        self.potField.setObjectName("Potasio")

        # Campo para agregar el valor del PH
        self.phField = QLineEdit()
        self.phField.setObjectName("PH")

        # Campo para agregar el valor de la materia orgánica
        self.moField = QLineEdit()
        self.moField.setObjectName("Materia orgánica")

        # Campo para agregar el potrero
        self.potreroCombo = QComboBox()
        self.potreroCombo.setPlaceholderText("Select")
        model = QSqlQueryModel()
        model.setQuery("SELECT NumeroPotrero FROM POTREROS")
        self.potreroCombo.setModel(model)

        # Configuro los campos
        layout = QFormLayout()
        layout.addRow("Fecha:", self.dateEdit)
        layout.addRow("Fósforo:", self.fosField)
        layout.addRow("Potasio:", self.potField)
        layout.addRow("PH:", self.phField)
        layout.addRow("Materia orgánica:", self.moField)
        layout.addRow("Potrero", self.potreroCombo)

        self.layout.addLayout(layout)

        # Añadir y conectar botones
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        fecha = self.dateEdit.date().toString("dd-MM-yyyy")
        fosforo = self.fosField.text()
        potasio = self.potField.text()
        ph = self.phField.text()
        materia_organica = self.moField.text()
        potrero = self.potreroCombo.currentText()

        # Validar los campos
        if not (fosforo and potasio and ph and materia_organica and potrero):
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos.")
        else:
            self.data = (fecha, fosforo, potasio, ph, materia_organica, potrero)
            super().accept()

class AlignmentDelegate(QStyledItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter