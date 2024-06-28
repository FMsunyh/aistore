'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 11:34:22
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 11:44:14
FilePath: \aistore\app\database\entity\developer.py
Description: entity of developers
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class Developers(Entity):
    id : int = 0
    name : str = None
    contact_info : str = None
    type : str = None # [Individual, Company]
    website_url : str = None

    def __str__(self):
        return f"{self.id} ({self.name})"