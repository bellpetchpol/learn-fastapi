from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

class AddSkillDto(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    damage: Annotated[int, Field(gt=0)]
    
class GetSkillDto(AddSkillDto):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(gt=0)]
