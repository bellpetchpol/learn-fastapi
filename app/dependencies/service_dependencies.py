from typing import Annotated
from fastapi import Depends
from ..services.character_service import CharacterService
from ..services.auth_service import AuthService
from ..services.user_service import UserService

character_service_dependency = Annotated[CharacterService, Depends(
    CharacterService)]

auth_service_dependency = Annotated[AuthService, Depends(AuthService)]

user_service_dependency = Annotated[UserService, Depends(UserService)]
