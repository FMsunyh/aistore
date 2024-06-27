# service/app_info_service.py
from app.database.dao.app_info_dao import AppInfoDao
from app.database.entity.app_info import AppInfo
from PyQt5.QtSql import QSqlDatabase

class AppInfoService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_info_dao = AppInfoDao(db)

    def createTable(self) -> bool:
        return self.app_info_dao.createTable()

    def add_app_info(self, icon, name, content):
        app_info = AppInfo(icon=icon, name=name, content=content)
        self.app_info_dao.add_app_info(app_info)

    def update_app_info(self, app_id, icon, name, content):
        app_info = AppInfo(app_id, icon, name, content)
        self.app_info_dao.update_app_info(app_info)

    def delete_app_info(self, app_id):
        self.app_info_dao.delete_app_info(app_id)

    def get_app_info_by_id(self, app_id):
        return self.app_info_dao.get_app_info_by_id(app_id)

    def get_all_app_info(self):
        return self.app_info_dao.get_all_app_info()
