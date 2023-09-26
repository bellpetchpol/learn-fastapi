from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..services.fight_service import FightService
from ..dtos.fight_dtos import GetResultDto
import logging

logger = logging.getLogger(__name__)  # the __name__ resolve to "app.services"
# This will load the app logger

router = APIRouter(
    prefix="/fights",
    tags=["fights"]
)

fight_service = Annotated[FightService, Depends()]


@router.get("/")
async def start(
    fight_service: fight_service
) -> list[GetResultDto]:
    try:
        return fight_service.start()
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=500, detail="Internal server error")
