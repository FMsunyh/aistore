'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:19:41
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 15:11:35
FilePath: \aistore\app\database\entity\__init__.py
Description: 
'''
from app.database.entity.entity import Entity
from app.database.entity.user import User
from app.database.entity.app_info import AppInfo
from app.database.entity.app_types import AppTypes
from app.database.entity.app_versions import AppVersions
from app.database.entity.developers import Developers
from app.database.entity.licenses import Licenses
from app.database.entity.ratings_reviews import RatingsReviews
from app.database.entity.screenshots import Screenshots
from app.database.entity.user_app import UserApp


class EntityFactory:
    """ Entity factory """

    @staticmethod
    def create(table: str):
        """ create an entity instance

        Parameters
        ----------
        table: str
            database table name corresponding to entity

        Returns
        -------
        entity:
            entity instance
        """
        tables = {
            "tbl_user": User,
            "tbl_app_info": AppInfo,
            "tbl_app_types": AppTypes,
            "tbl_app_versions": AppVersions,
            "tbl_developers": Developers,
            "tbl_licenses": Licenses,
            "tbl_ratings_reviews": RatingsReviews,
            "tbl_screenshots": Screenshots,
            "tbl_user_app": UserApp,
        }
        if table not in tables:
            raise ValueError(f"Table name `{table}` is illegal")

        return tables[table]()
