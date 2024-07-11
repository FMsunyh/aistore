'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 16:27:54
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 16:32:47
FilePath: \aistore\app\database\dao\model_info_dao.py
Description: 
'''
from app.database.dao.dao_base import DaoBase

class ModelInfoDao(DaoBase):
    table = 'tbl_model_info'
    fields = ['id', 'name', 'type_id', 'author', 'download_url', 'file_name', 'description', 'size']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type_id INTEGER NOT NULL,
                author TEXT,
                download_url TEXT NOT NULL,
                file_name TEXT NOT NULL,
                description TEXT,
                size INTEGER,
                FOREIGN KEY (type_id) REFERENCES tbl_model_types(id)
            )
        """)
        return success