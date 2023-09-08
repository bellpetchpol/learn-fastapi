from typing import Annotated
from fastapi import Depends, FastAPI, Path, status
from . import models
from .database import engine

from .services.CharacterService import CharacterService
from .dtos.character_dtos import AddCharacterDto, GetCharacterDto

from .dependencies import page_dependency

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_all_character(
    page_dtos: page_dependency,
    character_service: Annotated[CharacterService, Depends(CharacterService)]
) -> list[GetCharacterDto]:
    return character_service.read_all(page_dtos)


@app.get("/{character_id}", status_code=200)
async def read_character_by_id(
    character_id: Annotated[int, Path(gt=0)],
    character_service: Annotated[CharacterService, Depends(CharacterService)]
) -> GetCharacterDto:
    return character_service.read_by_id(character_id=character_id)


@app.post("/", status_code=status.HTTP_201_CREATED)
async def add_character(
    new_character: AddCharacterDto,
    character_service: Annotated[CharacterService, Depends(CharacterService)]
) -> GetCharacterDto:
    result = character_service.add(new_character=new_character)
    return result
