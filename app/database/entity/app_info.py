'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 18:29:11
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 18:08:36
FilePath: \aistore\app\database\entity\app_info.py
Description: entity of app
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class AppInfo(Entity):
    id : int = 0
    icon : str = None
    name : str = None
    title : str = None
    type_id : int = 0 # app_types id
    developer_id : int = 0 # developers id
    brief_introduction: str = None 
    description: str = None 
    release_date : str = None
    
    def __str__(self):
        return f"{self.name} ({self.brief_introduction})"
