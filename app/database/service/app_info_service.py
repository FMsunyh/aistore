from app.database.dao.app_info_dao import AppInfoDao
from ..entity import AppInfo
from PyQt5.QtSql import QSqlDatabase
from typing import List

class AppInfoService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_info_dao = AppInfoDao(db)

    def createTable(self) -> bool:
        return self.app_info_dao.createTable()

    def listAll(self) -> List[AppInfo]:
        return self.app_info_dao.listAll()
