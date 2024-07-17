'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-17 16:28:00
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-17 17:05:16
FilePath: \aistore\app\database\entity\model_folder.py
Description: 
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class ModelFolder(Entity):
    id : int = 0
    software_id : int = 0
    model_type_id : int = 0
    folder : str = None
    description: str = None

    def __str__(self):
        return f"{self.id} ({self.description})"