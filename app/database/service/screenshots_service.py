'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:27:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 14:33:28
FilePath: \aistore\app\database\service\screenshots_service.py
Description: service of screenshots
'''
from app.database.dao import ScreenshotsDao
from ..entity import Screenshots
from PyQt5.QtSql import QSqlDatabase
from typing import List

class ScreenshotsService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.screenshots_dao = ScreenshotsDao(db)

    def createTable(self) -> bool:
        return self.screenshots_dao.createTable()

    def listAll(self) -> List[Screenshots]:
        return self.screenshots_dao.listAll()
    
    def listBy(self, **condition) -> List[Screenshots]:
        return self.screenshots_dao.listBy(**condition)