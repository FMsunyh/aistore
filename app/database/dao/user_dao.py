'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:19:41
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 14:20:44
FilePath: user_dao.py
Description: DAO of user
'''
from app.database.dao.dao_base import DaoBase

class UserDao(DaoBase):
    table = 'tbl_user'
    fields = ['id', 'name', 'email', 'password']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        return success
