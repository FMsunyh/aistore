# coding:utf-8
from typing import Dict, List

from PyQt5.QtSql import QSqlDatabase

from app.database.service import ModelFolderService
from app.database.utils import UUIDUtils

class ModelFolderController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.service = ModelFolderService(db)

    def list_all(self):
        data = self.service.listAll()

        return data
    
    def get_model_folders_by_app_id(self, software_id: int):
        return self.service.listBy(software_id=software_id)