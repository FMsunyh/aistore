# coding:utf-8
from app.database.dao.user_dao import UserDao
from app.database.entity.user import User
from PyQt5.QtSql import QSqlDatabase

class UserService:

    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.user_dao = UserDao(db)

    def createTable(self) -> bool:
        return self.user_dao.createTable()
    
    def add_user(self, name, email):
        user = User(name=name, email=email)
        self.user_dao.add_user(user)

    def update_user(self, user_id, name, email):
        user = User(user_id, name, email)
        self.user_dao.update_user(user)

    def delete_user(self, user_id):
        self.user_dao.delete_user(user_id)

    def get_user_by_id(self, user_id):
        return self.user_dao.get_user_by_id(user_id)

    def get_all_users(self):
        return self.user_dao.get_all_users()
