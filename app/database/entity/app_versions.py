'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 10:52:34
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 14:06:41
FilePath: \aistore\app\database\entity\app_versions.py
Description: entity of app versions
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class AppVersions(Entity):
    id : int = 0
    app_id : int = 0
    version_number : str = None
    release_date : str = None
    change_log : str = None

    def __str__(self):
        return f"{self.id} ({self.app_id})"
