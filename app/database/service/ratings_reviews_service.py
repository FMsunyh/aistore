'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 14:27:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:23:00
FilePath: \aistore\app\database\service\ratings_reviews_service.py
Description: service of ratings and reviews
'''
from app.database.dao import RatingsReviewsDao
from ..entity import RatingsReviews
from PyQt5.QtSql import QSqlDatabase
from typing import List

class RatingsReviewsService:
    
    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.ratings_reviews_dao = RatingsReviewsDao(db)

    def createTable(self) -> bool:
        return self.ratings_reviews_dao.createTable()
    
    def listAll(self) -> List[RatingsReviews]:
        return self.ratings_reviews_dao.listAll()