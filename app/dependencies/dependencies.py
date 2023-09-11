from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Path
from ..database import SessionLocal
from ..dtos.request_dtos import PageDto


def get_db():
    db = SessionLocal()
    try:
        yield db
        # before this line execute before sending response
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


async def page_parameters(
    page: Annotated[int, Path(ge=1)] = 1,
    size: Annotated[int, Path(le=100)] = 25
) -> PageDto:
    return PageDto(**{"page": page, "size": size})


page_dependency = Annotated[PageDto, Depends(page_parameters)]
