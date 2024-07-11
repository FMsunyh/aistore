'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 17:15:17
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:27:48
FilePath: \aistore\app\database\service\models_service.py
Description:
'''

from app.database.dao.model_info_dao import ModelInfoDao
from ..entity import ModelInfo
from PyQt5.QtSql import QSqlDatabase
from typing import List

class ModelInfoService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.model_info_dao = ModelInfoDao(db)

    def createTable(self) -> bool:
        return self.model_info_dao.createTable()

    def listAll(self) -> List[ModelInfo]:
        return self.model_info_dao.listAll()

    def findBy(self, **condition) -> ModelInfo:
        return self.model_info_dao.selectBy(**condition)

    def listBy(self, **condition) -> List[ModelInfo]:
        return self.model_info_dao.listBy(**condition)