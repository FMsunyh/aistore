'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 18:19:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 18:22:29
FilePath: \aistore\app\database\service\app_info_service.py
Description: 
'''
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

    def findBy(self, **condition) -> AppInfo:
        return self.app_info_dao.selectBy(**condition)

    def listBy(self, **condition) -> List[AppInfo]:
        return self.app_info_dao.listBy(**condition)