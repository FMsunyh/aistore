from app.database.dao.dao_base import DaoBase

class ScreenshotsDao(DaoBase):
    table = 'tbl_screenshots'
    fields = ['id', 'software_id','image_url','description', 'upload_date']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                software_id INTEGER,
                image_url TEXT NOT NULL,
                description TEXT,
                upload_date TEXT,
                FOREIGN KEY (software_id) REFERENCES tbl_app_info(id)
            )
        """)
        return success