
import sys
sys.path.insert(0, r'D:/aistore')

from app.database.controller.user_controller import UserController
from app.database.controller.app_info_controller import AppInfoController
from app.database.dao.user_dao import UserDao
from app.database.dao.app_info_dao import AppInfoDao
from app.database.service.user_service import UserService
from app.database.service.app_info_service import AppInfoService
from app.database.entity.user import User
from app.database.db_initializer import DBInitializer
from PyQt5.QtSql import QSqlDatabase

if __name__ == '__main__':

    DBInitializer.init()