'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 15:57:14
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-11 17:24:51
FilePath: \aistore\app\database\entity\model_info.py
Description: 
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class ModelInfo(Entity):
    id : int = 0
    name : str = None
    type_id : int = 0
    author : str = None
    download_url : int = 0
    file_name : str = None
    description: str = None
    size : int = 0
    
    def __str__(self):
        return f"{self.id} ({self.name})"