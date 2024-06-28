from app.database.entity import Entity
from dataclasses import dataclass
@dataclass
class User(Entity):
    id : int = 0
    name : str = None
    email : str = None
    password : str = None

    def __str__(self):
        return f"{self.id} ({self.name} - {self.email})"
