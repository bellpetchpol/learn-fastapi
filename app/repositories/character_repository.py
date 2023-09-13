from math import ceil
from ..dependencies.dependencies import db_dependency
from ..models import Characters
from ..dtos.character_dtos import UpdateCharacterDto
from ..dtos.request_dtos import PageResponseDto


class CharacterRepository:

    def __init__(self, db: db_dependency):
        self.db = db

    def read_all(self, page: int, size: int) -> PageResponseDto[Characters]:
        offset = size * (page - 1)
        query = self.db.query(Characters).order_by(Characters.id)
        total = query.count()
        pages = ceil(total / size)
        
        result = PageResponseDto[Characters](
            items=query.offset(offset).limit(size).all(),
            page=page,
            pages=pages,
            size=size,
            total=total
        )
        
        return result

    def read_by_id(self, character_id: int) -> Characters | None:
        return self.db.query(Characters).filter(Characters.id == character_id).first()

    def add(self, new_character: Characters) -> Characters:
        self.db.add(new_character)
        self.db.commit()
        return new_character

    def update(self, db_character: Characters, update_character: UpdateCharacterDto) -> Characters:
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
        self.db.commit()
        return db_character

    def delete(self, db_character: Characters) -> None:
        self.db.delete(db_character)
        self.db.commit()
