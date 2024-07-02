from app.database.service.user_app_service import UserAppService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class UserAppController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.user_app_service = UserAppService(db)

    def list_all(self):
        user_app = self.user_app_service.listAll()

        return user_app