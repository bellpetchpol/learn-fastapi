from fastapi import HTTPException
from fastapi_pagination import Page

from ..models import Characters
from ..repositories.character_repository import CharacterRepository
from ..dtos.character_dtos import AddCharacterDto, GetCharacterDto, UpdateCharacterDto
from ..dependencies.repository_dependencies import character_repository_dependency

class CharacterService:
    def __init__(self, repo: character_repository_dependency):
        self.repo = repo

    def read_all(self) -> Page[GetCharacterDto]:
        paginated_db_character = self.repo.read_all()
        characters = [GetCharacterDto.model_validate(
            db_character) for db_character in paginated_db_character.items]
        paginated_characters = Page[GetCharacterDto](
            items=characters,
            page=paginated_db_character.page,
            pages=paginated_db_character.pages,
            total=paginated_db_character.total,
            size= paginated_db_character.size
        )
        return paginated_characters

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
        db_character = self.repo.read_by_id(character_id=character_id)
        if db_character is None:
            raise HTTPException(
                status_code=404, detail=f"Character id: {character_id} not found")
        updated_db_character = self.repo.update(
            db_character=db_character, update_character=update_character
        )
        result = GetCharacterDto.model_validate(updated_db_character)
        return result

    def delete(self, character_id: int) -> None:
        db_character = self.repo.read_by_id(character_id=character_id)
        if db_character is None:
            raise HTTPException(
                status_code=404, detail=f"Character id: {character_id} not found")
        self.repo.delete(db_character=db_character)
