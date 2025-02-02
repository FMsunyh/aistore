'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 18:19:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 18:25:24
FilePath: \aistore\app\database\controller\app_info_controller.py
Description: controller of app info
'''
from app.database.entity.app_info import AppInfo
from app.database.service.app_info_service import AppInfoService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class AppInfoController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.app_info_service = AppInfoService(db)

    def list_all(self):
        """ get all app types"""
        app_infos = self.app_info_service.listAll()

        return app_infos

    def get_app_infos_by_type_id(self, type_id: str):
        return self.app_info_service.listBy(type_id=type_id)
    
    # def listBy(self, **condition) -> List[AppInfo]:
    #     return self.app_info_dao.listBy(**condition)