'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:46:12
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 14:53:11
FilePath: \aistore\app\database\controller\licenses_controller.py
Description: contorller of licenses
'''
from app.database.service.licenses_service import LicensesService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class LicensesController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.licenses_service = LicensesService(db)

    def list_all(self):
        licenses = self.licenses_service.listAll()

        return licenses