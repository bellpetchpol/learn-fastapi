from typing import Annotated
from fastapi import Depends, FastAPI
from . import models
from .database import engine

from .services.CharacterService import CharacterService
from .dtos.character_dtos import AddCharacterDto, GetCharacterDto

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_all_character(character_service: Annotated[CharacterService, Depends(CharacterService)]):
    return character_service.read_all()

@app.post("/")
async def add_character(new_character: AddCharacterDto, character_service: Annotated[CharacterService, Depends(CharacterService)]) -> GetCharacterDto:
    result = character_service.add(new_character=new_character)
    return result
