'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 11:04:10
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 15:52:52
FilePath: user_app.py
Description: entity of user-app
'''
from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class UserApp(Entity):
    id : int = 0
    user_id : int = 0
    software_id : int = 0 
    license_id: int = 0 
    install_date : str = None
    is_installed : bool = False

    def __str__(self):
        return f"{self.id} ({self.user_id}-{self.software_id})"