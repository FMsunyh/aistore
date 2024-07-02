'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 11:46:28
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 14:17:33
FilePath: \aistore\app\database\dao\ratings_reviews_dao.py
Description: 
'''
from app.database.dao.dao_base import DaoBase

class RatingsReviewsDao(DaoBase):
    table = 'tbl_ratings_reviews'
    fields = ['id', 'user_id', 'software_id','rating','review', 'review_date']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                software_id INTEGER,
                rating INTEGER NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
                review TEXT,
                review_date TEXT,
                FOREIGN KEY (user_id) REFERENCES tbl_user(id),
                FOREIGN KEY (software_id) REFERENCES tbl_app_info(id)
            )
        """)
        return success