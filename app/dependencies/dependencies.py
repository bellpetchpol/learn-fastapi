from typing import Annotated, Generic, TypeVar
from sqlalchemy.orm import Session
from fastapi import Depends, Query
from ..database import SessionLocal
from ..dtos.request_dtos import PageRequestDto, PageResponseDto


def get_db():
    db = SessionLocal()
    try:
        yield db
        # before this line execute before sending response
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def page_parameter(
    page: Annotated[int, Query(gt=0)] = 1,
    size: Annotated[int, Query(le=100)] = 25
) -> PageRequestDto:
    return PageRequestDto(
        page=page,
        size=size
    )


page_dependency = Annotated[PageRequestDto, Depends(page_parameter)]

