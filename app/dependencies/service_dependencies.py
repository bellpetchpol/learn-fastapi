from typing import Annotated
from fastapi import Depends
from ..services.character_service import CharacterService
from ..services.user_service import UserService

character_service_dependency = Annotated[CharacterService, Depends(
    CharacterService)]


user_service_dependency = Annotated[UserService, Depends(UserService)]
