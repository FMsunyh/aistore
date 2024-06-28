from app.database.dao.dao_base import DaoBase

class developersDao(DaoBase):
    table = 'tbl_developers'
    fields = ['id', 'name', 'contact_info','type','website_url']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_info TEXT,
                type TEXT,
                website_url TEXT
            )
        """)
        return success