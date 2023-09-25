from fastapi import APIRouter, Depends, Path, status
from typing import Annotated
from ..services.skill_service import SkillService
from ..dependencies import page_dependency
from ..dtos.request_dtos import PageResponseDto
from ..dtos.skill_dtos import GetSkillDto, AddSkillDto

router = APIRouter(
    prefix="/skills",
    tags=["skills"]
)

skill_service = Annotated[SkillService, Depends()]

@router.get("/")
async def read_all_skill(
    skill_service: skill_service,
    page: page_dependency
) -> PageResponseDto[GetSkillDto]:
    return skill_service.read_all(page=page.page, size=page.size)

@router.get("/{skill_id}", status_code=200)
async def read_skill_by_id(
    skill_id: Annotated[int, Path(gt=0)],
    skill_service: skill_service
) -> GetSkillDto:
    return skill_service.read_by_id(skill_id=skill_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_skill(
    new_skill: AddSkillDto,
    skill_service: skill_service
) -> GetSkillDto:
    result = skill_service.add(new_skill=new_skill)
    return result