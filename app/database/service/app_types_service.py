from app.database.dao.app_types_dao import AppTypesDao
from PyQt5.QtSql import QSqlDatabase

class AppTypesService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_types_dao = AppTypesDao(db)

    def createTable(self) -> bool:
        return self.app_types_dao.createTable()