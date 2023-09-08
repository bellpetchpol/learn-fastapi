from enum import Enum
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class CharacterRoleEnum(str, Enum):
    Knight = "Knight"
    Cleric = "Cleric"
    Mage = "Mage"


class AddCharacterDto(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    role: CharacterRoleEnum
    hit_points: Annotated[int, Field(gt=0, lt=101)]
    attack: Annotated[int, Field(ge=5, le=20)]
    defence: Annotated[int, Field(ge=5, le=20)]
    magic: Annotated[int, Field(ge=5, le=20)]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Bell",
                    "role": "Mage",
                    "hit_points": 100,
                    "attack": 15,
                    "defence": 10,
                    "magic": 5
                }
            ]
        }
    }


class GetCharacterDto(AddCharacterDto):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(gt=0)]
