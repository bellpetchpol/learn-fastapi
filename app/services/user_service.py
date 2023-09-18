from ..dependencies.repository_dependencies import user_repository, auth_repository
from ..dtos.user_dtos import RegisterUserDto, GetUserDto
from ..models import Users
import logging

logger = logging.getLogger(__name__)  # the __name__ resolve to "app.services"
                                      # This will load the app logger



class UserService:

    def __init__(self, repo: user_repository, auth: auth_repository):
        self.repo = repo
        self.auth = auth

    def register(self, new_user: RegisterUserDto) -> GetUserDto:
        user_dict = new_user.model_dump()
        user_dict.pop("password")
        db_user = Users(**user_dict)
        db_user.create_by = "register"
        db_user.hashed_password = self.auth.create_password_hash(new_user.password)
        db_user = self.repo.add(new_user=db_user)
        user = GetUserDto.model_validate(db_user)
        return user
