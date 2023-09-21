from typing import Annotated
from fastapi import Depends, HTTPException

from ..models import Characters
from ..dtos.character_dtos import AddCharacterDto, GetCharacterDto, UpdateCharacterDto
from ..dtos.request_dtos import PageResponseDto
from ..repositories.character_repository import CharacterRepository
from ..dependencies import auth_user_dependency


class CharacterService:
    def __init__(self,
                 repo: Annotated[CharacterRepository, Depends()],
                 auth_user: auth_user_dependency
                 ):
        self.repo = repo
        self.auth_user = auth_user

    def read_all(self, page: int, size: int) -> PageResponseDto[GetCharacterDto]:
        db_page_response = self.repo.read_all(
            page=page, size=size, user_id=self.auth_user.user_id)
        # characters = [GetCharacterDto.model_validate(
        #     db_character) for db_character in db_page_response.items]
        # page_response = PageResponseDto[GetCharacterDto](
        #     items=characters,
        #     page=db_page_response.page,
        #     size=db_page_response.size,
        #     pages=db_page_response.pages,
        #     total=db_page_response.total
        # )
        page_response = PageResponseDto[GetCharacterDto](
            **db_page_response.model_dump())
        return page_response

    def read_by_id(self, character_id: int) -> GetCharacterDto:
        db_character = self.repo.read_by_id(
            character_id=character_id, user_id=self.auth_user.user_id)
        if db_character is None:
            raise HTTPException(
                status_code=404, detail=f"Character id: {character_id} not found")
        return GetCharacterDto.model_validate(db_character)

    def add(self, new_character: AddCharacterDto) -> GetCharacterDto:
        db_character = Characters(**new_character.model_dump())
        db_character.user_id = self.auth_user.user_id
        db_character = self.repo.add(new_character=db_character)
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
