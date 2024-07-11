'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:27:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:21:40
FilePath: \aistore\app\database\service\app_types_service.py
Description: service of app types
'''
from app.database.dao import AppTypesDao
from ..entity import AppTypes
from PyQt5.QtSql import QSqlDatabase
from typing import List

class AppTypesService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_types_dao = AppTypesDao(db)

    def createTable(self) -> bool:
        return self.app_types_dao.createTable()
    
    def listAll(self) -> List[AppTypes]:
        return self.app_types_dao.listAll()