from pydantic import BaseModel


class PageDto(BaseModel):
    skip: int = 0
    limit: int = 25