from app.database.dao.licenses_dao import LicensesDao
from PyQt5.QtSql import QSqlDatabase

class LicensesService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.licenses_dao = LicensesDao(db)

    def createTable(self) -> bool:
        return self.licenses_dao.createTable()