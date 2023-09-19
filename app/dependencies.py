from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Query, status
from .database import SessionLocal
from .dtos.request_dtos import PageRequestDto
from jose import JWTError, jwt
from .dtos.auth_dtos import CurrentUserDto

from .env import SECRET_KEY, SECURITY_ALGORITHM


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUserDto:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        current_user = CurrentUserDto(username=username,user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    return current_user

auth_user_dependency = Annotated[CurrentUserDto, Depends(get_current_user)]

