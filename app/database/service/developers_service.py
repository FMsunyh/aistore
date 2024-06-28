'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:27:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 14:30:12
FilePath: \aistore\app\database\service\developers_service.py
Description: service of developers
'''
from app.database.dao.developers_dao import DevelopersDao
from PyQt5.QtSql import QSqlDatabase

class DevelopersService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.developers_dao = DevelopersDao(db)

    def createTable(self) -> bool:
        return self.developers_dao.createTable()