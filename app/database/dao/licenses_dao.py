from app.database.dao.dao_base import DaoBase

class LicensesDao(DaoBase):
    table = 'tbl_licenses'
    fields = ['id', 'app_id', 'license_key','release_date','expiry_date', 'license_type']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                app_id INTEGER,
                license_key TEXT,
                release_date TEXT,
                expiry_date TEXT,
                license_type TEXT,
                FOREIGN KEY (app_id) REFERENCES tbl_app_info(id)
            )
        """)
        return success