from fastapi import Depends
from ..models import Characters
from ..repositories.character_repository import CharacterRepository
from typing import Annotated
from ..dtos.character_dtos import AddCharacterDto, GetCharacterDto


class CharacterService:
    def __init__(self, repo: Annotated[CharacterRepository, Depends(CharacterRepository)]):
        self.repo = repo

    def read_all(self) -> list[Characters]:
        return self.repo.read_all()

    def add(self, new_character: AddCharacterDto) -> GetCharacterDto:
        db_character = self.repo.add(new_character=Characters(**new_character.model_dump()))
        character = GetCharacterDto.model_validate(db_character)
        return character
