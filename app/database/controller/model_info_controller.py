from app.database.service import ModelInfoService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class ModelInfoController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.service = ModelInfoService(db)

    def list_all(self):
        """ get all app types"""
        model_infos = self.service.listAll()

        return model_infos

    
    # def listBy(self, **condition) -> List[AppInfo]:
    #     return self.app_info_dao.listBy(**condition)