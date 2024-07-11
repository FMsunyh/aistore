from app.database.dao.app_models_dao import AppModelsDao
from ..entity import AppModels
from PyQt5.QtSql import QSqlDatabase
from typing import List

class AppModelsService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.app_models_dao = AppModelsDao(db)

    def createTable(self) -> bool:
        return self.app_models_dao.createTable()
    
    def listAll(self) -> List[AppModels]:
        return self.app_models_dao.listAll()
    
    def listBy(self, **condition) -> List[AppModels]:
        return self.app_models_dao.listBy(**condition)