'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 10:48:43
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 11:48:40
FilePath: \aistore\app\database\entity\app_types.py
Description: entity of app types
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class AppTypes(Entity):
    id : int = 0
    name : str = None 

    def __str__(self):
        return f"{self.id} ({self.name})"
