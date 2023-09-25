from datetime import timedelta
from typing import Annotated
from ..repositories.user_repository import UserRepository
from ..repositories.auth_repository import AuthRepository
from ..dtos.user_dtos import RegisterUserDto, GetUserDto
from ..dtos.auth_dtos import GetTokenDto
from ..models import Users
from fastapi import Depends, HTTPException, status
import logging
from ..env import ACCESS_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger(__name__)  # the __name__ resolve to "app.services"
# This will load the app logger


class AuthService:

    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends()],
                 auth: Annotated[AuthRepository, Depends()]
                 ):
        self.user_repo = user_repo
        self.auth = auth

    def register(self, new_user: RegisterUserDto) -> GetUserDto:
        db_user = self.user_repo.read_by_username(username=new_user.username)
        if db_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "001",
                    "message": f"The username {new_user.username} already exist."
                }
            )
        user_dict = new_user.model_dump()
        user_dict.pop("password")
        db_user = Users(**user_dict)
        db_user.create_by = "register"
        db_user.hashed_password = self.auth.create_password_hash(
            new_user.password)
        db_user = self.user_repo.add(new_user=db_user)
        user = GetUserDto.model_validate(db_user)
        return user

    def authenticate_user(self, username: str, password: str) -> Users:
        db_user = self.user_repo.read_by_username(username=username)
        if db_user is None or db_user.disabled:
            raise HTTPException(
                status_code=401, detail=f"Not Authenticated")
        if not self.auth.verify_password(
            plain_password=password,
            hashed_password=db_user.hashed_password
        ):
            raise HTTPException(
                status_code=401, detail=f"Not Authenticated")
        return db_user

    def login_for_access_token(
        self,
        username: str,
        password: str
    ) -> GetTokenDto:
        db_user = self.authenticate_user(username=username, password=password)
        access_token_expires = timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = self.auth.create_access_token(
            data={
                "sub": db_user.username,
                "user_id": str(db_user.id)
            }, expires_delta=access_token_expires
        )
        response = GetTokenDto(
            access_token=access_token,
            token_type="bearer"
        )
        return response
