from app.database.dao import LicensesDao
from ..entity import Licenses
from PyQt5.QtSql import QSqlDatabase
from typing import List

class LicensesService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.licenses_dao = LicensesDao(db)

    def createTable(self) -> bool:
        return self.licenses_dao.createTable()
    
    def listAll(self) -> List[Licenses]:
        return self.licenses_dao.listAll()