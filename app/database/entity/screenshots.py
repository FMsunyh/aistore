'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 11:17:40
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-02 14:16:29
FilePath: \aistore\app\database\entity\screenshots.py
Description: entity of screenshots
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class Screenshots(Entity):
    id : int = 0
    software_id : int = 0 
    image_url: str = None
    description : str = None
    upload_date : str = None

    def __str__(self):
        return f"{self.id} ({self.software_id})"