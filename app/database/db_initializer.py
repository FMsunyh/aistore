'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:20:39
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 16:35:34
FilePath: \aistore\app\database\db_initializer.py
Description: initializer database
'''
# coding:utf-8
from pathlib import Path
from app.common.logger import logger
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import qApp

from app.database.service import (UserService,AppInfoService,AppTypesService,AppVersionsService,
                                  DevelopersService,LicensesService,ScreenshotsService,
                                  UserAppService,RatingsReviewsService, ModelTypesService,ModelInfoService,AppModelsService)

from  app.common.config import cfg

class DBInitializer:
    """ Database initializer """

    CONNECTION_NAME = "main"
    CACHE_FILE = str(Path(cfg.get(cfg.cacheFolder)) / "cache.db")

    @classmethod
    def init(cls):
        """ Initialize database """
        db = QSqlDatabase.addDatabase('QSQLITE', cls.CONNECTION_NAME)
        db.setDatabaseName(cls.CACHE_FILE)
        if not db.open():
            logger.error("Database connection failed")
            raise Exception("Failed to open database")
            # qApp.exit()

        UserService(db).createTable()
        AppInfoService(db).createTable()
        AppTypesService(db).createTable()
        AppVersionsService(db).createTable()
        DevelopersService(db).createTable()
        LicensesService(db).createTable()
        ScreenshotsService(db).createTable()
        UserAppService(db).createTable()
        RatingsReviewsService(db).createTable()
        ModelTypesService(db).createTable()
        ModelInfoService(db).createTable()
        AppModelsService(db).createTable()