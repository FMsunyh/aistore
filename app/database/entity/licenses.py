'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 10:56:53
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 11:02:41
FilePath: \aistore\app\database\entity\licenses.py
Description: entity of licenses
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class Licenses(Entity):
    id : int = 0
    app_id : int = 0
    license_key : str = None
    release_date : str = None
    expiry_date : str = None
    license_type : str = None

    def __str__(self):
        return f"{self.id} ({self.license_key})"
