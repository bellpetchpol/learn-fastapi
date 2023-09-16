from typing import Annotated
from fastapi import Depends, FastAPI, Path, Query, status
from fastapi_pagination import Page, add_pagination
from . import models
from .database import engine

from .dependencies.service_dependencies import character_service_dependency, user_service_dependency
from .dtos.character_dtos import AddCharacterDto, GetCharacterDto, UpdateCharacterDto
from .dependencies.dependencies import page_dependency
from .dtos.request_dtos import PageResponseDto
from fastapi.security import OAuth2PasswordBearer
from .dtos.user_dtos import RegisterUserDto, GetUserDto


Page = Page.with_custom_options(# type: ignore[misc]
    size=Query(default=25, ge=1, le=100),
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

add_pagination(app)

models.Base.metadata.create_all(bind=engine)

@app.get("/token/")
async def read_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/characters/")
async def read_all_character(
    character_service: character_service_dependency,
    page: page_dependency
) -> PageResponseDto[GetCharacterDto]:
    return character_service.read_all(page=page.page, size=page.size)


@app.get("/{character_id}", status_code=200)
async def read_character_by_id(
    character_id: Annotated[int, Path(gt=0)],
    character_service: character_service_dependency
) -> GetCharacterDto:
    return character_service.read_by_id(character_id=character_id)


@app.post("/", status_code=status.HTTP_201_CREATED)
async def add_character(
    new_character: AddCharacterDto,
    character_service: character_service_dependency
) -> GetCharacterDto:
    result = character_service.add(new_character=new_character)
    return result


@app.put("/{character_id}/update")
async def update_character(
    character_id: Annotated[int, Path(gt=0)],
    update_character: UpdateCharacterDto,
    character_service: character_service_dependency
) -> GetCharacterDto:
    result = character_service.update(
        character_id=character_id, update_character=update_character
    )
    return result

@app.delete("/{character_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    character_id: Annotated[int, Path(gt=0)],
    character_service: character_service_dependency
) -> None:
    character_service.delete(character_id=character_id)
    
@app.post("/users/register", status_code=201)
async def register_user(
    new_user: RegisterUserDto,
    user_service: user_service_dependency
) -> GetUserDto:
    user = user_service.register(new_user=new_user)
    return user
