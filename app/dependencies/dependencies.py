from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
        # before this line execute before sending response
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
