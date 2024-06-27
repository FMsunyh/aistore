from .entity import Entity
from dataclasses import dataclass
@dataclass
class AppInfo(Entity):
    id : str = None
    icon : str = None
    name : str = None 
    content: str = None 

    def __str__(self):
        return f"{self.name} ({self.content})"
