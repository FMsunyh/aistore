'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:19:41
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 14:59:39
FilePath: user_service.py
Description: service of user
'''

# coding:utf-8
from app.database.dao import UserDao
from ..entity import User
from PyQt5.QtSql import QSqlDatabase
from typing import List

class UserService:

    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.user_dao = UserDao(db)

    def createTable(self) -> bool:
        return self.user_dao.createTable()

    def listAll(self) -> List[User]:
        return self.user_dao.listAll()  
