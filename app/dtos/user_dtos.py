from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated


class AddUserDto(BaseModel):
    username: Annotated[str, Field(max_length=25)]
    full_name: str | None = None


class RegisterUserDto(AddUserDto):
    password: str


class GetUserDto(AddUserDto):
    model_config = ConfigDict(from_attributes=True)
    disabled: bool
    create_by: str
    create_date: datetime
    update_by: str | None = None
    update_date: datetime
