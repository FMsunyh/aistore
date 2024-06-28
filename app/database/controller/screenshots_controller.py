from app.database.service.screenshots_service import ScreenshotsService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class ScreenshotsController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.screenshots_service = ScreenshotsService(db)
