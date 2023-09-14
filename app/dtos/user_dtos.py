from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated


class AddUserDto(BaseModel):
    username: Annotated[str, Field(max_length=25)]
    full_name: str | None


class RegisterUserDto(AddUserDto):
    password: str


class GetUserDto(AddUserDto):
    disabled: bool
    create_by: str
    create_date: datetime
    update_by: str
    update_date: datetime
