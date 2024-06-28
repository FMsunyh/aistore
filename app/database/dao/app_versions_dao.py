from app.database.dao.dao_base import DaoBase

class AppVersionsDao(DaoBase):
    table = 'tbl_app_versions'
    fields = ['id', 'app_id', 'version_number','release_date', 'change_log']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                app_id INTEGER,
                version_number TEXT NOT NULL,
                release_date TEXT,
                change_log TEXT,
                FOREIGN KEY (app_id) REFERENCES tbl_app_info(id)
            )
        """)
        return success