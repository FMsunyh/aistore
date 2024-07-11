'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 15:56:08
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:20:58
FilePath: \aistore\app\database\entity\model_types.py
Description: 
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class ModelTypes(Entity):
    id : str = None
    name : str = None 

    def __str__(self):
        return f"{self.id} ({self.name})"