'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:46:12
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-03 15:59:51
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
    
    def get_app_versions_by_app_id(self, software_id: str):
        return self.app_versions_service.listBy(software_id=software_id)
    
    def get_last_app_version_by_app_id(self, software_id: str):
        app_versions = self.get_app_versions_by_app_id(software_id=software_id)

        last_app_version = max(app_versions, key=lambda x: x.id)
        return last_app_version