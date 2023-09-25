from typing import Annotated

from fastapi import Depends
from ..repositories.character_repository import CharacterRepository
from ..dependencies import auth_user_dependency
from ..dtos.fight_dtos import GetResultDto


class FightService:
    def __init__(self,
                 character_repo: Annotated[CharacterRepository, Depends()],
                 auth_user: auth_user_dependency,
                 ):
        self.character_repo = character_repo
        self.auth_user =  auth_user
        
    # def start(self) -> GetResultDto:
    #     result = GetResultDto()
    #     characters = self.character_repo.read_all(1, 100, self.auth_user.user_id)
        