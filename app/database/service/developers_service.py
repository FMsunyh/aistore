'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:27:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:21:30
FilePath: \aistore\app\database\service\developers_service.py
Description: service of developers
'''
from app.database.dao import DevelopersDao
from ..entity import Developers
from PyQt5.QtSql import QSqlDatabase
from typing import List

class DevelopersService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.developers_dao = DevelopersDao(db)

    def createTable(self) -> bool:
        return self.developers_dao.createTable()
    
    def listAll(self) -> List[Developers]:
        return self.developers_dao.listAll()