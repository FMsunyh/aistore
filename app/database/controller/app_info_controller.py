from app.database.service.app_info_service import AppInfoService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class AppInfoController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.app_info_service = AppInfoService(db)

    def add_app_info(self, icon, name, content):
        self.app_info_service.add_app_info(icon, name, content)

    def update_app_info(self, app_id, icon, name, content):
        self.app_info_service.update_app_info(app_id, icon, name, content)

    def delete_app_info(self, app_id):
        self.app_info_service.delete_app_info(app_id)

    def get_app_info_by_id(self, app_id):
        return self.app_info_service.get_app_info_by_id(app_id)

    def get_all_app_info(self):
        return self.app_info_service.get_all_app_info()
