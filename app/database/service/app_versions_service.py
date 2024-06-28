from app.database.dao.app_versions_dao import AppVersionsDao
from PyQt5.QtSql import QSqlDatabase

class AppVersionsService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_versions_dao = AppVersionsDao(db)

    def createTable(self) -> bool:
        return self.app_versions_dao.createTable()