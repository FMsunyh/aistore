'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:27:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:27:37
FilePath: \aistore\app\database\service\app_types_service.py
Description: service of app types
'''
from app.database.dao import ModelTypesDao
from ..entity import ModelTypes
from PyQt5.QtSql import QSqlDatabase
from typing import List

class ModelTypesService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.model_types_dao = ModelTypesDao(db)

    def createTable(self) -> bool:
        return self.model_types_dao.createTable()
    
    def listAll(self) -> List[ModelTypes]:
        return self.model_types_dao.listAll()