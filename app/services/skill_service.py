from ..repositories.skill_repository import SkillRepository
from typing import Annotated
from fastapi import Depends, HTTPException
from ..dependencies import auth_user_dependency
from ..dtos.skill_dtos import AddSkillDto, GetSkillDto
from ..dtos.request_dtos import PageResponseDto
from ..models import Skills


class SkillService:
    def __init__(self,
                 repo: Annotated[SkillRepository, Depends()],
                 auth_user: auth_user_dependency
                 ):
        self.repo = repo
        self.auth_user = auth_user

    def read_all(self, page: int, size: int) -> PageResponseDto[GetSkillDto]:
        db_page_response = self.repo.read_all(
            page=page, size=size
        )
        page_response = PageResponseDto[GetSkillDto](
            **db_page_response.model_dump())
        return page_response

    def read_by_id_return_db_skill(self, skill_id: int) -> Skills:
        db_skill = self.repo.read_by_id(
            skill_id=skill_id)
        if db_skill is None:
            raise HTTPException(
                status_code=404, detail=f"Skill id: {skill_id} not found")
        return db_skill

    def read_by_id(self, skill_id: int) -> GetSkillDto:
        db_skill = self.read_by_id_return_db_skill(
            skill_id=skill_id)
        return GetSkillDto.model_validate(db_skill)

    def add(self, new_skill: AddSkillDto) -> GetSkillDto:
        db_skill = Skills(**new_skill.model_dump())
        db_skill = self.repo.add(new_skill=db_skill)
        skill = GetSkillDto.model_validate(db_skill)
        return skill

    def add_dummy(self) -> None:
        skills = [
            AddSkillDto(
                name="ลูกบอลไฟ",
                damage=30
            ),
            AddSkillDto(
                name="สายฟ้าฟาด",
                damage=35
            ),
            AddSkillDto(
                name="พายุน้ำแข็ง",
                damage=40
            )
        ]
        
        for skill in skills:
            self.add(skill)
         
