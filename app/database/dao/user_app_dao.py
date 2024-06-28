from app.database.dao.dao_base import DaoBase

class UserAppDao(DaoBase):
    table = 'tbl_user_app'
    fields = ['id', 'user_id', 'app_id','license_id','install_date', 'is_installed']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                app_id INTEGER,
                license_id INTEGER,
                install_date TEXT,
                is_installed INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES tbl_user(id),
                FOREIGN KEY (app_id) REFERENCES tbl_app_info(id),
                FOREIGN KEY (license_id) REFERENCES tbl_licenses(id)
            )
        """)
        return success