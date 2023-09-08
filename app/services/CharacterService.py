from fastapi import Depends, HTTPException

from ..models import Characters
from ..repositories.character_repository import CharacterRepository
from typing import Annotated
from ..dtos.character_dtos import AddCharacterDto, GetCharacterDto
from ..dtos.request_dtos import PageDto


class CharacterService:
    def __init__(self, repo: Annotated[CharacterRepository, Depends(CharacterRepository)]):
        self.repo = repo

    def read_all(self, page_dto: PageDto) -> list[GetCharacterDto]:
        db_characters = self.repo.read_all(page_dto.skip, page_dto.limit)
        characters = list[GetCharacterDto]()
        for db_character in db_characters:
            characters.append(GetCharacterDto.model_validate(db_character))
        return characters
    
    def read_by_id(self, character_id: int) -> GetCharacterDto:
        db_character = self.repo.read_by_id(character_id=character_id)
        if db_character is None:
            raise HTTPException(status_code=404, detail=f"Character id: {character_id} not found")
        return GetCharacterDto.model_validate(db_character)

    def add(self, new_character: AddCharacterDto) -> GetCharacterDto:
        db_character = self.repo.add(new_character=Characters(**new_character.model_dump()))
        character = GetCharacterDto.model_validate(db_character)
        return character
