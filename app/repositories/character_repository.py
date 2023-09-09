from ..dependencies import db_dependency
from ..models import Characters
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import select
from ..dtos.character_dtos import UpdateCharacterDto


class CharacterRepository:

    def __init__(self, db: db_dependency):
        self.db = db

    def read_all(self) -> Page[Characters]:
        return paginate(self.db, select(Characters).order_by(Characters.id))

    def read_by_id(self, character_id: int) -> Characters | None:
        return self.db.query(Characters).filter(Characters.id == character_id).first()

    def add(self, new_character: Characters) -> Characters:
        self.db.add(new_character)
        self.db.commit()
        return new_character

    def update(self, character_id: int, update_character: UpdateCharacterDto) -> Characters:
        db_character = self.db.query(Characters).filter(
            Characters.id == character_id).first()
        if update_character.name is not None:
            db_character.name = update_character.name

        if update_character.hit_points is not None:
            db_character.hit_points = update_character.hit_points

        if update_character.role is not None:
            db_character.role = update_character.role

        if update_character.attack is not None:
            db_character.attack = update_character.attack

        if update_character.defence is not None:
            db_character.defence = update_character.defence

        if update_character.magic is not None:
            db_character.magic = update_character.magic

        self.db.add(db_character)
        self.db.flush()
        return db_character

    def delete(self, db_character: Characters) -> None:
        self.db.delete(db_character)
        self.db.commit()
