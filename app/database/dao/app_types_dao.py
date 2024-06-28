from app.database.dao.dao_base import DaoBase

class AppTypesDao(DaoBase):
    table = 'tbl_app_types'
    fields = ['id', 'name']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        return success