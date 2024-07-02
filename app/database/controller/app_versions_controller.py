'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:46:12
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 14:56:10
FilePath: \aistore\app\database\controller\app_versions_controller.py
Description: 
'''
from app.database.service.app_versions_service import AppVersionsService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class AppVersionsController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.app_versions_service = AppVersionsService(db)

    def list_all(self):
        app_versions = self.app_versions_service.listAll()

        return app_versions