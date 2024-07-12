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

    # def find_model_infos_by_ids(self, ids: list):
    #     return self.service.findBy(ids=ids)

    def get_model_infos_by_type_id(self, type_id: int):
        return self.service.listBy(type_id=type_id)

    def get_model_infos_by_ids(self, ids: list):
        return self.service.listByIds(ids=ids) 
    
    def get_fields(self):
        return self.service.get_fields() 