from app.database.dao.user_app_dao import UserAppDao
from PyQt5.QtSql import QSqlDatabase

class UserAppService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.user_app_dao = UserAppDao(db)

    def createTable(self) -> bool:
        return self.user_app_dao.createTable()