'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-17 16:48:08
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-17 16:56:22
FilePath: \aistore\app\database\dao\model_folder_dao.py
Description: 
'''
from app.database.dao.dao_base import DaoBase

class ModelFolderDao(DaoBase):
    table = 'tbl_model_folder'
    fields = ['id', 'software_id', 'model_type_id', 'folder', 'description']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                software_id INTEGER NOT NULL,
                model_type_id INTEGER NOT NULL,
                folder TEXT NOT NULL,
                description TEXT,
                FOREIGN  KEY (software_id) REFERENCES tbl_app_info(id),
                FOREIGN  KEY (model_type_id) REFERENCES tbl_model_types(id)
            )
        """)
        return success