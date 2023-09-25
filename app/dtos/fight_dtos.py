from pydantic import BaseModel

class GetResultDto(BaseModel):
    attacker: str
    message: str
    defender: str