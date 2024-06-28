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
    
    # def add_app_info(self, app_id, icon, name, content):
    #     app_info = AppInfo()
    #     app_info.id= app_id
    #     app_info.icon= icon
    #     app_info.name= name
    #     app_info.content= content
    #     self.app_info_dao.add_app_info(app_info)

    # def update_app_info(self, app_id, icon, name, content):
    #     app_info = AppInfo(app_id, icon, name, content)
    #     self.app_info_dao.update_app_info(app_info)

    # def delete_app_info(self, app_id):
    #     self.app_info_dao.delete_app_info(app_id)

    # def get_app_info_by_id(self, app_id):
    #     return self.app_info_dao.get_app_info_by_id(app_id)

    # def get_all_app_info(self):
    #     return self.app_info_dao.get_all_app_info()
