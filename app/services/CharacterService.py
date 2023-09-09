from fastapi import Depends, HTTPException
from fastapi_pagination import Page

from ..models import Characters
from ..repositories.character_repository import CharacterRepository
from typing import Annotated
from ..dtos.character_dtos import AddCharacterDto, GetCharacterDto, UpdateCharacterDto


class CharacterService:
    def __init__(self, repo: Annotated[CharacterRepository, Depends(CharacterRepository)]):
        self.repo = repo

    def read_all(self) -> Page[GetCharacterDto]:
        # paginated_db_characters = self.repo.read_all()
        # characters = list[GetCharacterDto]()
        # for db_character in paginated_db_characters.items:
        #     characters.append(GetCharacterDto.model_validate(db_character))

        # paginated_characters = Page[GetCharacterDto](
        #     page =
        # )
        # paginated_characters.page = paginated_db_characters.page
        # paginated_characters.pages = paginated_db_characters.pages
        # paginated_characters.size = paginated_db_characters.size
        # paginated_characters.total = paginated_db_characters.total
        # paginated_db_characters.items = characters
        return self.repo.read_all()

    def read_by_id(self, character_id: int) -> GetCharacterDto:
        db_character = self.repo.read_by_id(character_id=character_id)
        if db_character is None:
            raise HTTPException(
                status_code=404, detail=f"Character id: {character_id} not found")
        return GetCharacterDto.model_validate(db_character)

    def add(self, new_character: AddCharacterDto) -> GetCharacterDto:
        db_character = self.repo.add(
            new_character=Characters(**new_character.model_dump()))
        character = GetCharacterDto.model_validate(db_character)
        return character

    def update(self, character_id: int, update_character: UpdateCharacterDto) -> GetCharacterDto:
        db_character = self.repo.update(
            character_id=character_id, update_character=update_character
        )
        result = GetCharacterDto.model_validate(db_character)
        return result
    
    def delete(self, character_id: int) -> None:
        db_character = self.repo.read_by_id(character_id=character_id)
        if db_character is None:
            raise HTTPException(
                status_code=404, detail=f"Character id: {character_id} not found")
        self.repo.delete(db_character=db_character)
        
