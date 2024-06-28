'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 17:06:35
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 17:12:12
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

        watch: bool
            whether to monitor audio directories

        parent:
            parent instance
        """
        super().__init__(parent=parent)
        self.app_types = []
        self.app_info = []
        self.developers = []

        self.app_types_controller = AppTypesController(db)
        self.app_info_controller = AppInfoController(db)
        self.developers_controller = DevelopersController(db)

        self.load()

    def load(self):
        """ load data to library """
        self.app_types = self.app_types_controller.list_all()
        self.app_info = self.app_info_controller.list_all()
        self.developers = self.developers_controller.list_all()
        
        self.loadFinished.emit()

    