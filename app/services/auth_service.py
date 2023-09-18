from datetime import timedelta
from ..dependencies.repository_dependencies import user_repository, auth_repository
from ..dtos.user_dtos import RegisterUserDto, GetUserDto
from ..dtos.auth_dtos import GetTokenDto
from ..models import Users
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)  # the __name__ resolve to "app.services"
# This will load the app logger

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:

    def __init__(self, user_repo: user_repository, auth: auth_repository):
        self.user_repo = user_repo
        self.auth = auth

    def register(self, new_user: RegisterUserDto) -> GetUserDto:
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
        if db_user is None:
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
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.auth.create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        response = GetTokenDto(
            access_token=access_token,
            token_type="bearer"
        )
        return response
