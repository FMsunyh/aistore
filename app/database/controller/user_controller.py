# coding:utf-8
from typing import Dict, List

from PyQt5.QtSql import QSqlDatabase

from app.database.service import UserService
from app.database.utils import UUIDUtils

class UserController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.user_service = UserService(db)

    def list_all(self):
        users = self.user_service.listAll()

        return users