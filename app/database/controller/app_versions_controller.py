from app.database.service.app_versions_service import AppVersionsService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class AppVersionsController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.app_versions_service = AppVersionsService(db)
