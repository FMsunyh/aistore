from app.database.service.developers_service import DevelopersService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class DevelopersController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.developers_service = DevelopersService(db)

    def list_all(self):
        """ get all app types"""
        developers = self.developers_service.listAll()

        return developers