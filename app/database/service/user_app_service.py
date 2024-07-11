from app.database.dao import UserAppDao
from ..entity import UserApp
from PyQt5.QtSql import QSqlDatabase
from typing import List

class UserAppService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.user_app_dao = UserAppDao(db)

    def createTable(self) -> bool:
        return self.user_app_dao.createTable()
    
    def listAll(self) -> List[UserApp]:
        return self.user_app_dao.listAll()