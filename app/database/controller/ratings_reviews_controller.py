from app.database.service.ratings_reviews_service import RatingsReviewsService
from typing import Dict, List
from PyQt5.QtSql import QSqlDatabase
from app.database.utils import UUIDUtils

class RatingsReviewsController:

    def __init__(self, db: QSqlDatabase = None) -> None:
        self.ratings_reviews_service = RatingsReviewsService(db)

    def list_all(self):
        ratings_reviews = self.ratings_reviews_service.listAll()

        return ratings_reviews