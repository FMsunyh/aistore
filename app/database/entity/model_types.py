'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 15:56:08
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-12 17:58:38
FilePath: \aistore\app\database\entity\model_types.py
Description: 
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class ModelTypes(Entity):
    id : int = 0
    name : str = None 

    def __str__(self):
        return f"{self.id} ({self.name})"