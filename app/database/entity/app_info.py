'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 18:29:11
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 10:49:23
FilePath: \aistore\app\database\entity\app_info.py
Description: entity of app
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class AppInfo(Entity):
    id : str = None
    icon : str = None
    name : str = None 
    content: str = None 

    def __str__(self):
        return f"{self.name} ({self.content})"
