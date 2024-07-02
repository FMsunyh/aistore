'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 17:06:35
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 14:46:24
FilePath: \aistore\app\database\db_sqlite.py
Description: library
'''
# coding:utf-8
from pathlib import Path
from typing import List, Union

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtSql import QSqlDatabase

from .controller import *


class Library(QObject):
    """ Song library """
    loadFinished = pyqtSignal()

    def __init__(self, db: QSqlDatabase = None, parent=None):
        """
        Parameters
        ----------
        directories: List[str]
            audio directories

        db: QDataBase
            database to be used

        parent:
            parent instance
        """
        super().__init__(parent=parent)
        self.app_types = []
        self.app_infos = []
        self.developers = []
        self.app_versions = []
        self.user = []
        self.user_app = []
        self.screenshots = []
        self.licenses = []
        self.ratings_reviews = []

        self.app_types_controller = AppTypesController(db)
        self.app_info_controller = AppInfoController(db)
        self.developers_controller = DevelopersController(db)
        self.app_versions_controller = AppVersionsController(db)
        self.user_controller = UserController(db)
        self.user_app_controller = UserAppController(db)
        self.screenshots_controller = ScreenshotsController(db)
        self.licenses_controller = LicensesController(db)
        self.ratings_reviews_controller = RatingsReviewsController(db)

        self.load()

    def load(self):
        """ load data to library """
        self.app_types = self.app_types_controller.list_all()
        self.app_infos = self.app_info_controller.list_all()
        self.developers = self.developers_controller.list_all()
        
        self.loadFinished.emit()

    