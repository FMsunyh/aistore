'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 16:12:14
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 16:24:59
FilePath: \aistore\app\database\entity\app_models.py
Description: 
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class AppModels(Entity):
    id : int = 0
    software_id : int = 0
    model_id : int = 0

    def __str__(self):
        return f"{self.id} ({self.software_id})"