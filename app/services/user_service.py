from ..dependencies.repository_dependencies import user_repository
from ..dtos.user_dtos import RegisterUserDto, GetUserDto
from ..models import Users
from ..dependencies.service_dependencies import auth_service_dependency


class UserService:

    def __init__(self, repo: user_repository, auth: auth_service_dependency):
        self.repo = repo
        self.auth = auth

    def register(self, new_user: RegisterUserDto) -> GetUserDto:
        db_user = self.repo.add(new_user=Users(**new_user.model_dump()))
        db_user.hashed_password = self.auth.create_password_hash(new_user.password)
        user = GetUserDto.model_validate(db_user)
        return user
