# coding:utf-8
from typing import Dict, List

from PyQt5.QtSql import QSqlDatabase

from app.database.service import UserService
from app.database.utils import UUIDUtils

class UserController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.user_service = UserService(db)

    # def add_user(self, name, email):
    #     self.user_service.add_user(name, email)

    # def update_user(self, user_id, name, email):
    #     self.user_service.update_user(user_id, name, email)

    # def delete_user(self, user_id):
    #     self.user_service.delete_user(user_id)

    # def get_user_by_id(self, user_id):
    #     return self.user_service.get_user_by_id(user_id)

    # def get_all_users(self):
    #     return self.user_service.get_all_users()
