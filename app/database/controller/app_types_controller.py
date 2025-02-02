from app.database.service.app_types_service import AppTypesService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class AppTypesController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.app_types_service = AppTypesService(db)

    def list_all(self):
        """ get all app types"""
        app_types = self.app_types_service.listAll()

        return app_types