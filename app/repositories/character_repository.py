from ..dependencies import db_dependency
from ..models import Characters


class CharacterRepository:

    def __init__(self, db: db_dependency):
        self.db = db

    def read_all(self, skip: int, limit: int) -> list[Characters]:
        return self.db.query(Characters).offset(skip).limit(limit).all()

    def read_by_id(self, character_id: int) -> Characters | None:
        return self.db.query(Characters).filter(Characters.id == character_id).first()

    def add(self, new_character: Characters) -> Characters:
        self.db.add(new_character)
        self.db.commit()
        return new_character

    # def add(self, new_character: Characters) -> Characters:
    #     self.db.add(new_character)
