from app.database.service import AppModelsService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class AppModelsController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.service = AppModelsService(db)

    def list_all(self):
        app_models = self.service.listAll()

        return app_models
    
    def get_models_by_app_id(self, software_id: int):
        return self.service.listBy(software_id=software_id)
    

    # def get_model_types_by_app_id(self, software_id: str):
    #     pass
        