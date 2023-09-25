from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from ..services.auth_service import AuthService
from ..dtos.user_dtos import RegisterUserDto, GetUserDto
from fastapi.security import OAuth2PasswordRequestForm
import logging

logger = logging.getLogger(__name__)  # the __name__ resolve to "app.services"
# This will load the app logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

auth_service_dependnecy = Annotated[AuthService, Depends()]


@router.post("/register", status_code=201)
async def register_user(
    new_user: RegisterUserDto,
    auth_service: auth_service_dependnecy
) -> GetUserDto:
    try:
        user = auth_service.register(new_user=new_user)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: auth_service_dependnecy):
    try:
        result = auth_service.login_for_access_token(
            username=form_data.username, password=form_data.password)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")
