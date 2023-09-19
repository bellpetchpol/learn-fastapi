from pydantic import BaseModel

class GetTokenDto(BaseModel):
    access_token: str
    token_type: str
    
class CurrentUserDto(BaseModel):
    user_id: int
    username: str