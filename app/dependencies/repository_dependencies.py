from typing import Annotated
from fastapi import Depends
from ..repositories.character_repository import CharacterRepository
from ..repositories.user_repository import UserRepository

character_repository_dependency = Annotated[CharacterRepository, Depends(
    CharacterRepository)]

user_repository = Annotated[UserRepository, Depends(UserRepository)]
