from typing import Annotated
from fastapi import Depends
from ..repositories.character_repository import CharacterRepository

character_repository_dependency = Annotated[CharacterRepository, Depends(
    CharacterRepository)]
