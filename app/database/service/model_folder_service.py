'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-17 16:47:39
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-17 17:41:27
FilePath: \aistore\app\database\service\model_folder_service.py
Description: 
'''
from app.database.dao import ModelFolderDao
from ..entity import ModelFolder
from PyQt5.QtSql import QSqlDatabase
from typing import List

class ModelFolderService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.dao = ModelFolderDao(db)

    def createTable(self) -> bool:
        return self.dao.createTable()
    
    def listAll(self) -> List[ModelFolder]:
        return self.dao.listAll()

    def listBy(self, **condition) -> List[ModelFolder]:
        return self.dao.listBy(**condition)