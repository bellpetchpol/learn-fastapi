from typing import Annotated
from fastapi import Depends
from ..services.character_service import CharacterService
from ..services.auth_service import AuthService

character_service_dependency = Annotated[CharacterService, Depends(
    CharacterService)]

auth_service_dependency = Annotated[AuthService, Depends(AuthService)]
