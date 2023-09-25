from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated


class AddWeaponDto(BaseModel):
    name: Annotated[str, Field(max_length=50)]
    damage: Annotated[int, Field(gt=0)]


class GetWeaponDto(AddWeaponDto):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(gt=0)]
