from typing import Annotated
from fastapi import Depends
from ..repositories.character_repository import CharacterRepository
from ..repositories.user_repository import UserRepository
from ..repositories.auth_repository import AuthRepository

character_repository_dependency = Annotated[CharacterRepository, Depends(
    CharacterRepository)]

user_repository = Annotated[UserRepository, Depends(UserRepository)]

auth_repository = Annotated[AuthRepository, Depends(AuthRepository)]
