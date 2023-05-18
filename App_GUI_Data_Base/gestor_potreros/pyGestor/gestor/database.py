from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def createConnection(databaseName):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Gestor de fertilizaciones y análisis de suelo",
            f"DB Error: {connection.lastError().text()}",
        )
        return False

    _crearTablaPotreros()
    _crearTablaFertilizacion()
    _crearTablaAnalisis()    
    _insertPredeterminedValuesIntoPotrerosTable()
    return True

def _crearTablaFertilizacion():
    createTableQuery = QSqlQuery()
    
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS FERTILIZACION (
            "id" INTEGER,
            "Fecha"	NUMERIC,
            "Fertilizante" TEXT,
            "kg por hectarea" INTEGER,
            "Potrero" INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("Potrero") REFERENCES "POTREROS"("NumeroPotrero")
        )
        """
    )

def _crearTablaAnalisis():
    createTableQuery = QSqlQuery()
    
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS ANALISIS (
            "id" INTEGER,
            "Fecha"	NUMERIC,
            "Valor de Fosforo (P)" REAL,
            "Valor de Potasio (K)" REAL,
            "PH" REAL,
            "Materia Organica (MO)"	REAL,
            "Potrero" INTEGER,
            FOREIGN KEY("Potrero") REFERENCES "POTREROS"("NumeroPotrero"),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    ) 

def _crearTablaPotreros():
    createTableQuery = QSqlQuery()
    
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS POTREROS (
            "NumeroPotrero"	INTEGER NOT NULL UNIQUE,
            "Hectareas"	INTEGER DEFAULT 0,
            PRIMARY KEY("NumeroPotrero")
        );
        """
    ) 

def _insertPredeterminedValuesIntoPotrerosTable():
     insertValuesQuery = QSqlQuery()

     return insertValuesQuery.exec(
         """
        INSERT INTO "POTREROS" ("NumeroPotrero", "Hectareas")
        VALUES
            (1, 10),
            (2, 15),
            (3, 12),
            (4, 8),
            (5, 20),
            (6, 17),
            (7, 9),
            (8, 11),
            (9, 14),
            (10, 16),
            (11, 21);
         """
     )

