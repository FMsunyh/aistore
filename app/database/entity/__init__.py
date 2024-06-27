'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:19:41
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-27 17:33:04
FilePath: \aistore\app\database\entity\__init__.py
Description: 
'''
from .entity import Entity
from .user import User
from .app_info import AppInfo


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
            "tbl_user": AppInfo,
        }
        if table not in tables:
            raise ValueError(f"Table name `{table}` is illegal")

        return tables[table]()
