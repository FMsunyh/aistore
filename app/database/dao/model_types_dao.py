from app.database.dao.dao_base import DaoBase

class ModelTypesDao(DaoBase):
    table = 'tbl_model_types'
    fields = ['id', 'name']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        return success