'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 11:10:43
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 11:17:05
FilePath: \aistore\app\database\entity\ratings_reviews.py
Description: entity of ratings and reviews
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class RatingsReviews(Entity):
    id : int = 0
    user_id : int = 0
    app_id : int = 0 
    rating: int = 0 
    review : str = None
    review_date : str = None

    def __str__(self):
        return f"{self.id} ({self.user_id}-{self.app_id})"