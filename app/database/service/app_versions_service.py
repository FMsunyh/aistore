from app.database.dao.app_versions_dao import AppVersionsDao
from ..entity import AppVersions
from PyQt5.QtSql import QSqlDatabase
from typing import List

class AppVersionsService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_versions_dao = AppVersionsDao(db)

    def createTable(self) -> bool:
        return self.app_versions_dao.createTable()
    
    def listAll(self) -> List[AppVersions]:
        return self.app_versions_dao.listAll()
    
    def listBy(self, **condition) -> List[AppVersions]:
        return self.app_versions_dao.listBy(**condition)