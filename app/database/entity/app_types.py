from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class AppTypes(Entity):
    id : str = None
    name : str = None 

    def __str__(self):
        return f"{self.id} ({self.name})"
