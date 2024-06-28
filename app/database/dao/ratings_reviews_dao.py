from app.database.dao.dao_base import DaoBase

class LicensesDao(DaoBase):
    table = 'tbl_ratings_reviews'
    fields = ['id', 'user_id', 'app_id','rating','review', 'review_date']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                app_id INTEGER,
                rating INTEGER NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
                review TEXT,
                review_date TEXT,
                FOREIGN KEY (user_id) REFERENCES tbl_user(id),
                FOREIGN KEY (app_id) REFERENCES tbl_app_info(id)
            )
        """)
        return success