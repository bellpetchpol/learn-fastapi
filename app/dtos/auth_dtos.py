from pydantic import BaseModel

class GetTokenDto(BaseModel):
    access_token: str
    token_type: str