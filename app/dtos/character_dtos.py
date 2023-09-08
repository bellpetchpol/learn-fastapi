from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class CharacterRoleEnum(str, Enum):
    Knight = "Knight"
    Cleric = "Cleric"
    Mage = "Mage"


class AddCharacterDto(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    role: CharacterRoleEnum
    hit_points: int = Field(gt=0, lt=101)
    attack: int = Field(ge=5, le=20)
    defence: int = Field(ge=5, le=20)
    magic: int = Field(ge=5, le=20)


class GetCharacterDto(AddCharacterDto):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(gt=0)
