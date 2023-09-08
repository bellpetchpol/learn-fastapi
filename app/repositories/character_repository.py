from ..dependencies import db_dependency
from ..models import Characters

class CharacterRepository:
    
    def __init__(self, db: db_dependency):
        self.db = db
        
    def read_all(self) -> list[Characters]:
        return self.db.query(Characters).all()
    
    def add(self, new_character: Characters) -> Characters:
        self.db.add(new_character)
        self.db.commit()
        return new_character
    
    # def add(self, new_character: Characters) -> Characters:
    #     self.db.add(new_character)