from app.database.dao.dao_base import DaoBase

class UserDao(DaoBase):
    table = 'tbl_user'
    fields = ['user_id', 'name', 'email']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                user_id CHAR(32) PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        """)
        return success
