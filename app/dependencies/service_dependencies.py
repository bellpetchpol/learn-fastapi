from typing import Annotated
from fastapi import Depends
from ..services.character_service import CharacterService

character_service_dependency = Annotated[CharacterService, Depends(
    CharacterService)]
