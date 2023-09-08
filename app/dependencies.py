from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import SessionLocal
from .dtos.request_dtos import PageDto


def get_db():
    db = SessionLocal()
    try:
        yield db
        # before this line execute before sending response
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


async def page_parameters(skip: int = 0, limit: int = 25) -> PageDto:
    return PageDto(**{"skip": skip, "limit": limit})

page_dependency = Annotated[PageDto, Depends(page_parameters)]