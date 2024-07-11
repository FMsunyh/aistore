from app.database.service import ModelTypesService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class ModelTypesController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.service = ModelTypesService(db)

    def list_all(self):
        """ get all app types"""
        types = self.service.listAll()

        return types