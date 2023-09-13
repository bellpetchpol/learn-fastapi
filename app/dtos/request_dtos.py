from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict
T = TypeVar("T")
C = TypeVar("C")


class PageRequestDto(BaseModel):
    page: int
    size: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BasePageResponseDto(PageRequestDto):
    pages: int = 1
    total: int


class PageResponseDto(BasePageResponseDto, Generic[T]):
    items: list[T]


# pydantic.errors.PydanticSchemaGenerationError: Unable to generate pydantic-core schema for <class 'app.models.Characters'>. Set `arbitrary_types_allowed=True` in the model_config to ignore this error or implement `__get_pydantic_core_schema__` on your type to fully support it.
