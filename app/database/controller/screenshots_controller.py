'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:46:12
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 15:00:41
FilePath: \aistore\app\database\controller\screenshots_controller.py
Description: 
'''
from app.database.service.screenshots_service import ScreenshotsService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class ScreenshotsController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.screenshots_service = ScreenshotsService(db)

    def list_all(self):
        screenshots = self.screenshots_service.listAll()

        return screenshots