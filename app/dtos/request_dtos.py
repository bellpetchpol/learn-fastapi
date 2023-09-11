from pydantic import BaseModel


class PageDto(BaseModel):
    page: int = 0
    size: int = 25